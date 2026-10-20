"""Isolated negative controls executed inside the real Actions verification job."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import shutil
from proof_policy import classify

root = Path.cwd()
results = []
def reject(name, cmd, cwd=root):
    p = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    results.append({'fault': name, 'exit_code': p.returncode, 'output': p.stdout + p.stderr})
    if p.returncode == 0: raise AssertionError('fault escaped: ' + name)

with tempfile.TemporaryDirectory() as td:
    tmp = Path(td)
    for path in ('lean-toolchain', 'lakefile.toml', 'lake-manifest.json', 'dependency-lock.sha256'):
        shutil.copy(root/path, tmp/path)
    for fault in ('missing', 'sha', 'version'):
        shutil.copy(root/'lake-manifest.json', tmp/'lake-manifest.json')
        shutil.copy(root/'lean-toolchain', tmp/'lean-toolchain')
        if fault == 'missing': (tmp/'lake-manifest.json').unlink()
        if fault == 'sha':
            data = json.loads((tmp/'lake-manifest.json').read_text())
            data['packages'][0]['rev'] = '0'*40
            (tmp/'lake-manifest.json').write_text(json.dumps(data))
        if fault == 'version': (tmp/'lean-toolchain').write_text('leanprover/lean4:v4.23.0')
        reject('dependency-' + fault, [sys.executable, str(root/'scripts/dependency_lock_gate.py')], tmp)
    broken = tmp/'Broken.lean'
    broken.write_text('import Mathlib\ntheorem broken : False := by decide\n')
    reject('invalid-lean', ['lake', 'env', 'lean', str(broken)])
    broken.write_text('import Mathlib\ntheorem hole : False := by sorry\n#print axioms hole\n')
    p = subprocess.run(['lake', 'env', 'lean', str(broken)], capture_output=True, text=True, check=True)
    assert 'sorryAx' in p.stdout
    try: classify(['sorryAx'])
    except ValueError: pass
    else: raise AssertionError('sorry accepted')
    results.append({'fault':'sorry', 'detected_axiom':'sorryAx', 'output':p.stdout})
    broken.write_text('import Mathlib\naxiom evil : False\ntheorem bad : False := evil\n#print axioms bad\n')
    p = subprocess.run(['lake', 'env', 'lean', str(broken)], capture_output=True, text=True, check=True)
    assert 'evil' in p.stdout
    try: classify(['evil'])
    except ValueError: pass
    else: raise AssertionError('custom axiom accepted')
    results.append({'fault':'custom-axiom','detected_axiom':'evil','output':p.stdout})
    reject('pipefail', ['bash','-o','pipefail','-c','false | tee /dev/null'])
    source = (root/'experiments/verify_certificate.py').read_text().replace('len(rows7) == 35','len(rows7) == 36')
    damaged = tmp/'damaged.py'
    damaged.write_text(source)
    reject('python-expected-result', [sys.executable, str(damaged)])
Path('evidence/faults.json').write_text(json.dumps(results, indent=2)+'\n')
print('Isolated fault controls passed:', len(results))
