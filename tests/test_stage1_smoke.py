import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("stage1_smoke", ROOT / "scripts/smoke_test.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


class Stage1SmokeTest(unittest.TestCase):
    def test_stage1_structure_passes(self):
        result = MODULE.run()
        self.assertEqual(result["status"], "PASS", result)
        self.assertEqual(result["completion_status"], "STAGE_1_FOUNDATION_READY_FOR_PROTOTYPE_BUILD")


if __name__ == "__main__":
    unittest.main()
