import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from dependency_lock_gate import check
from proof_policy import classify
spec = importlib.util.spec_from_file_location('cert', ROOT/'experiments/verify_certificate.py')
cert = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cert)

class VerificationTests(unittest.TestCase):
    def test_actual_dependency_lock(self):
        self.assertEqual(check(ROOT), ('leanprover/lean4:v4.24.0', 9))
    def test_trust_rejection(self):
        for axiom in ('sorryAx', 'evil', 'Lean.unapproved'):
            with self.assertRaises(ValueError): classify([axiom])
        self.assertEqual(classify(['Lean.ofReduceBool']), 'native-assisted')
    def test_divisor_boundaries(self):
        for n in (1, 2, 4, 9, 12, 97):
            self.assertEqual(cert.divisors_from_factors(cert.factor(n)), cert.divisors_from_sqrt(n))
        self.assertEqual(cert.check(0), [])
        self.assertEqual(len(cert.check(1)), 1)
        with self.assertRaises(AssertionError): cert.denominators(8, 1, 320)
    def test_two_process_handoff_and_duplicate_suppression(self):
        with tempfile.TemporaryDirectory() as td:
            cmd = [sys.executable, str(ROOT/'scripts/handoff.py'), '--state', td+'/state.json',
                   '--task','T11', '--source','fixed-input', '--result','fixed-output',
                   '--status','success', '--next','wait for explicit research instruction']
            first = json.loads(subprocess.check_output(cmd, text=True))
            second = json.loads(subprocess.check_output(cmd, text=True))
            self.assertFalse(first['duplicate'])
            self.assertTrue(second['duplicate'])
            self.assertEqual(second['attempts'], 2)
            self.assertEqual(second['progress_count'], 1)
            self.assertEqual(first['next_action'], second['next_action'])

class EvidenceTests(unittest.TestCase):
    def test_missing_and_stale_evidence_rejected(self):
        from evidence_gate import validate
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            with self.assertRaises(FileNotFoundError): validate(root,'sha','run','1')
            (root/'run.json').write_text(json.dumps(dict(source_sha='old',run_id='run',attempt='1')))
            with self.assertRaisesRegex(ValueError,'stale_evidence'): validate(root,'sha','run','1')
    def test_changed_manifest_revision_rejected(self):
        import shutil
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            for path in ('lean-toolchain','lakefile.toml','lake-manifest.json','dependency-lock.sha256'):
                shutil.copy(ROOT/path,root/path)
            data=json.loads((root/'lake-manifest.json').read_text())
            data['packages'][0]['rev']='0'*40
            (root/'lake-manifest.json').write_text(json.dumps(data))
            with self.assertRaisesRegex(ValueError,'manifest differs'): check(root)
    def test_artifact_corruption_rejected(self):
        from evidence_gate import validate
        import hashlib
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            (root/'run.json').write_text(json.dumps(dict(source_sha='sha',run_id='run',attempt='1',status='failed')))
            (root/'test.log').write_text('original')
            (root/'SHA256SUMS').write_text(''.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n' for p in root.iterdir()))
            self.assertEqual(validate(root,'sha','run','1'),'failed')
            (root/'test.log').write_text('corrupted')
            with self.assertRaisesRegex(ValueError,'artifact_failed'): validate(root,'sha','run','1')
