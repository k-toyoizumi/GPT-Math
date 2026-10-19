import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1] / "scripts" / "lean_inventory_gate.py"
spec = importlib.util.spec_from_file_location("lean_inventory_gate", MODULE)
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        (self.root / "lakefile.toml").write_text('[[lean_lib]]\nname = "A"\n')
        (self.root / "A.lean").write_text("theorem a : True := trivial\n")
        subprocess.run(["git", "-C", str(self.root), "add", "lakefile.toml", "A.lean"], check=True)

    def test_registered_file(self):
        self.assertEqual(gate.inventory(self.root), (["A.lean"], ["A"]))

    def test_new_unregistered_file_is_still_in_inventory(self):
        (self.root / "B.lean").write_text("theorem b : True := trivial\n")
        subprocess.run(["git", "-C", str(self.root), "add", "B.lean"], check=True)
        self.assertEqual(gate.inventory(self.root)[0], ["A.lean", "B.lean"])

    def test_nested_unregistered_proof_is_included(self):
        (self.root / "proofs").mkdir()
        (self.root / "proofs" / "B.lean").write_text("theorem b : True := trivial\n")
        subprocess.run(["git", "-C", str(self.root), "add", "proofs/B.lean"], check=True)
        self.assertEqual(gate.inventory(self.root)[0], ["A.lean", "proofs/B.lean"])

    def test_deleted_tracked_source_fails(self):
        (self.root / "A.lean").unlink()
        with self.assertRaisesRegex(ValueError, "missing or unsafe"):
            gate.inventory(self.root)

    def test_missing_target_fails(self):
        (self.root / "lakefile.toml").write_text('[[lean_lib]]\nname = "Missing"\n')
        with self.assertRaisesRegex(ValueError, "no tracked Lean source"):
            gate.inventory(self.root)

    def test_no_tracked_proofs_fails(self):
        subprocess.run(["git", "-C", str(self.root), "rm", "-q", "--cached", "A.lean"], check=True)
        with self.assertRaisesRegex(ValueError, "No tracked Lean"):
            gate.inventory(self.root)

    def test_untracked_file_is_not_counted(self):
        (self.root / "B.lean").write_text("theorem b : True := trivial\n")
        self.assertEqual(gate.inventory(self.root)[0], ["A.lean"])

    def test_duplicate_targets_fail(self):
        (self.root / "lakefile.toml").write_text('[[lean_lib]]\nname = "A"\n[[lean_lib]]\nname = "A"\n')
        with self.assertRaisesRegex(ValueError, "duplicate"):
            gate.inventory(self.root)


if __name__ == "__main__":
    unittest.main()
