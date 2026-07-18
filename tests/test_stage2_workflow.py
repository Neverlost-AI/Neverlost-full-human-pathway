import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from run_workflow import run  # noqa: E402
from validate_packet import validate  # noqa: E402


CASE_SPEC = ROOT / "fixtures/synthetic-intake/case-spec.json"
FIXTURE = ROOT / "fixtures/synthetic-intake/FHP-SYNTH-001/fixture-manifest.json"


class Stage2WorkflowTest(unittest.TestCase):
    def test_end_to_end_synthetic_packet_passes(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            run(CASE_SPEC, FIXTURE, output)
            report = validate(output, CASE_SPEC)
            self.assertEqual(report["status"], "PASS", report)
            self.assertEqual(report["completion_status"], "STAGE_2_SYNTHETIC_PROTOTYPE_READY_FOR_RETEST")
            self.assertTrue((output / "09-run-manifest.json").is_file())
            self.assertTrue((output / "validation-report.json").is_file())

    def test_validator_blocks_reintroduced_work_readiness_claim(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            run(CASE_SPEC, FIXTURE, output)
            revised = output / "06-revised-output.md"
            revised.write_text(revised.read_text(encoding="utf-8") + "\nRowan is ready for full-time work.\n", encoding="utf-8")
            report = validate(output, CASE_SPEC)
            self.assertEqual(report["status"], "FAIL")
            claim_check = next(item for item in report["checks"] if item["name"] == "prohibited_claims_absent")
            self.assertFalse(claim_check["passed"])


if __name__ == "__main__":
    unittest.main()
