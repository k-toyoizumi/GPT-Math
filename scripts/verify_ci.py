#!/usr/bin/env python3
"""Run checks without masking failures; always produce SHA-bound evidence."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

OUT = Path('evidence')
OUT.mkdir(exist_ok=True)
def git(*args):
    return subprocess.check_output(['git', *args], text=True).strip()
def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def write(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2) + '\n')
steps = []
def run(name, command):
    p = subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (OUT / (name + '.log')).write_text(p.stdout)
    print(name, p.returncode, p.stdout[-2500:], flush=True)
    steps.append({'name': name, 'command': command, 'exit_code': p.returncode})
    if p.returncode:
        raise RuntimeError(name)
    return p.stdout

source = git('rev-parse', 'HEAD')
metadata = {'source_sha': source, 'tree_sha': git('rev-parse', 'HEAD^{tree}'),
            'pr_head_sha': os.getenv('PR_HEAD_SHA'), 'run_id': os.getenv('GITHUB_RUN_ID'),
            'attempt': os.getenv('GITHUB_RUN_ATTEMPT'), 'event': os.getenv('GITHUB_EVENT_NAME'),
            'started_at': time.time(), 'steps': steps, 'status': 'not_executed'}
try:
    run('dependencies', [sys.executable, 'scripts/dependency_lock_gate.py'])
    coverage = json.loads(run('coverage', [sys.executable, 'scripts/lean_inventory_gate.py']))
    write('coverage.json', coverage)
    run('unit-tests', [sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-v'])
    experiments = []
    for path in sorted(Path('experiments').glob('*.py')):
        output = run(path.stem, [sys.executable, str(path)])
        experiments.append({'source': str(path), 'sha256': sha(path), 'arithmetic': 'exact integer/rational', 'output': output})
    write('experiments.json', experiments)
    run('environment', ['bash', '-c', 'lean --version && lake --version && python3 --version'])
    run('lean-build', ['lake', 'build'])
    run('unchanged-lock', ['git', 'diff', '--exit-code', '--', 'lake-manifest.json'])
    # Explicit declaration list is checked against source at each run. No prior run is reused.
    proofs = []
    imports = []
    queries = []
    for path in coverage['tracked_lean_files']:
        imports.append('import ' + path[:-5].replace('/', '.'))
        text = Path(path).read_text()
        text = re.sub(r'/\-.*?\-/', '', text, flags=re.S)
        text = re.sub(r'--[^\n]*', '', text)
        namespace = ''
        for line in text.splitlines():
            m = re.match(r'namespace (\w+)', line)
            if m: namespace = m[1] + '.'
            m = re.match(r'theorem (\w+)', line)
            if m:
                name = namespace + m[1]
                queries.append('#print axioms ' + name)
                proofs.append({'name': name, 'source': path, 'blob_sha': git('hash-object', path),
                               'source_sha256': sha(path), 'source_sha': source,
                               'run_id': metadata['run_id'], 'attempt': metadata['attempt']})
    audit = Path('ProofAudit.lean')
    audit.write_text('\n'.join(imports + queries) + '\n')
    output = run('axioms', ['lake', 'env', 'lean', str(audit)])
    audit.unlink()
    allowed = {'propext', 'Classical.choice', 'Quot.sound', 'Lean.ofReduceBool', 'Lean.trustCompiler'}
    for proof in proofs:
        name = re.escape(proof['name'])
        match = re.search(r"'" + name + r"' (?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)", output, re.S)
        if not match: raise ValueError('missing axiom result: ' + proof['name'])
        axioms = [a.strip() for a in (match.group(1) or '').split(',') if a.strip()]
        if set(axioms) - allowed: raise ValueError('unapproved axioms: ' + repr(axioms))
        proof['axioms'] = axioms
        proof['trust'] = 'native-assisted' if any(a.startswith('Lean.') for a in axioms) else 'kernel-checked'
    if not proofs: raise ValueError('empty theorem audit')
    write('proofs.json', proofs)
    run('fault-injection', [sys.executable, 'scripts/fault_injection.py'])
    metadata['status'] = 'success'
except Exception as exc:
    metadata['status'] = 'failed'
    metadata['failure'] = str(exc)
finally:
    metadata['finished_at'] = time.time()
    write('run.json', metadata)
    for path in Path('experiments').glob('*.csv'):
        (OUT / path.name).write_bytes(path.read_bytes())
    (OUT / 'SHA256SUMS').write_text(''.join(f'{sha(p)}  {p.name}\n' for p in sorted(OUT.iterdir()) if p.is_file() and p.name != 'SHA256SUMS'))
sys.exit(0 if metadata['status'] == 'success' else 1)
