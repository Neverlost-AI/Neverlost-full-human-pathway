import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from run_stage4_demo import demonstrate  # noqa: E402


class Stage4DemoTest(unittest.TestCase):
    def test_clean_demo_reproduces_governed_metrics(self):
        result = demonstrate(include_tests=False)
        self.assertEqual(result["status"], "PASS", result)
        self.assertEqual(result["completion_status"], "STAGE_4_DEMONSTRATION_PACKAGE_READY_FOR_HUMAN_REVIEW")
        self.assertEqual(result["metrics"]["deliberate_defects_detected_and_corrected"], 10)
        self.assertEqual(result["metrics"]["classification_matches"], 10)
        self.assertEqual(result["metrics"]["critical_false_positives"], 0)
        self.assertEqual(result["metrics"]["packet_checks_passed"], 24)
        self.assertEqual(result["final_status"], "READY_FOR_USER_REVIEW")


if __name__ == "__main__":
    unittest.main()
