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
from proof_policy import classify

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
            'started_at': time.time(), 'steps': steps, 'status': 'not_executed',
            'dependencies': json.loads(Path('lake-manifest.json').read_text())}
try:
    run('dependencies', [sys.executable, 'scripts/dependency_lock_gate.py'])
    coverage = json.loads(run('coverage', [sys.executable, 'scripts/lean_inventory_gate.py']))
    coverage['registry'] = json.loads(Path('lean-sources.json').read_text())
    coverage['verification_command'] = ['lake', 'build']
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
    # Enumerate compiled environment declarations by defining module, not source regex.
    registry = json.loads(Path('lean-sources.json').read_text())
    modules = {p[:-5].replace('/', '.'): p for p, entry in registry.items() if entry['status'] == 'adopted'}
    imports = ['import ' + name for name in modules]
    audit = Path('ProofAudit.lean')
    audit.write_text('\n'.join(imports) + '''
open Lean in
run_cmd do
  let env ← getEnv
  let modules : List String := MODULES
  for (name, info) in env.constants.toList do
    let some idx := env.getModuleIdxFor? name | continue
    let modName := env.header.moduleNames[idx.toNat]!
    if modules.contains modName.toString then
      match info with
      | .thmInfo _ =>
        let axioms ← Lean.collectAxioms name
        let row := Json.mkObj [
          ("name", toJson name.toString),
          ("module", toJson modName.toString),
          ("statement", toJson (reprStr info.type)),
          ("axioms", toJson (axioms.map Name.toString))]
        logInfo m!"AUDIT_JSON {row.compress}"
      | _ => pure ()
'''.replace('MODULES', '[' + ', '.join(json.dumps(m) for m in modules) + ']'))
    output = run('axioms', ['lake', 'env', 'lean', str(audit)])
    audit.unlink()
    proofs = []
    for line in output.splitlines():
        if 'AUDIT_JSON ' not in line: continue
        proof = json.loads(line.split('AUDIT_JSON ', 1)[1])
        path = modules[proof.pop('module')]
        proof.update(source=path, blob_sha=git('hash-object', path), source_sha256=sha(path),
                     source_sha=source, run_id=metadata['run_id'], attempt=metadata['attempt'],
                     statement_hash=hashlib.sha256(proof['statement'].encode()).hexdigest(),
                     trust=classify(proof['axioms']))
        proofs.append(proof)
    if not proofs or set(p['source'] for p in proofs) != set(modules.values()):
        raise ValueError('missing compiled theorem audit for adopted module')
    proofs.sort(key=lambda p: p['name'])
    write('proofs.json', proofs)
    run('fault-injection', [sys.executable, 'scripts/fault_injection.py'])
    from handoff import record
    result_hash = hashlib.sha256((OUT/'proofs.json').read_bytes() + (OUT/'experiments.json').read_bytes()).hexdigest()
    for _ in range(2):
        record(OUT/'handoff.json', 'T11', source, result_hash, 'success', 'stop; await explicit research authorization')
    metadata['status'] = 'success'
except Exception as exc:
    metadata['status'] = 'failed'
    metadata['failure'] = str(exc)
    last = steps[-1]['name'] if steps else ''
    metadata['failure_category'] = ('dependency_failed' if last in ('dependencies','unchanged-lock') else
        'inventory_failed' if last == 'coverage' else 'lean_failed' if last in ('lean-build','axioms') else
        'python_failed' if last in ('unit-tests','fixed_first_denominator','first_denominator_offset','verify_certificate') else 'artifact_failed')
finally:
    metadata['finished_at'] = time.time()
    write('run.json', metadata)
    for path in Path('experiments').glob('*.csv'):
        (OUT / path.name).write_bytes(path.read_bytes())
    (OUT / 'SHA256SUMS').write_text(''.join(f'{sha(p)}  {p.name}\n' for p in sorted(OUT.iterdir()) if p.is_file() and p.name != 'SHA256SUMS'))
sys.exit(0 if metadata['status'] == 'success' else 1)
