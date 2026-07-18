import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from neverlost_core import load_json  # noqa: E402
from run_workflow import run  # noqa: E402
from score_stage3_retest import score  # noqa: E402
from validate_packet import validate  # noqa: E402


CASE_SPEC = ROOT / "fixtures/synthetic-intake/FHP-SYNTH-002/case-spec.json"
FIXTURE = ROOT / "fixtures/synthetic-intake/FHP-SYNTH-002/fixture-manifest.json"


class Stage3Retest(unittest.TestCase):
    def test_distinct_case_passes_frozen_score_and_capacity_fidelity(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            run(CASE_SPEC, FIXTURE, output)
            validation = validate(output, CASE_SPEC, patch_cycle_count=1)
            self.assertEqual(validation["status"], "PASS", validation)

            capacity = load_json(output / "03-capacity-record.json")
            self.assertEqual(capacity["source_ids"], ["S1"])
            self.assertEqual(capacity["observation_window"]["duration_minutes"], 40)
            self.assertIn("3 separate client-observed", capacity["output_achieved"])

            scorecard = score(output, CASE_SPEC)
            self.assertEqual(scorecard["status"], "PASS", scorecard)
            self.assertEqual(scorecard["defect_score"], {"detected_and_corrected": 10, "possible": 10})
            self.assertEqual(scorecard["critical_false_positives"], [])

    def test_validator_blocks_reintroduced_stage3_authority_claims(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            run(CASE_SPEC, FIXTURE, output)
            revised = output / "06-revised-output.md"
            revised.write_text(
                revised.read_text(encoding="utf-8")
                + "\nAPPROVED: Maya's benefits will continue unchanged.\n",
                encoding="utf-8",
            )
            validation = validate(output, CASE_SPEC)
            self.assertEqual(validation["status"], "FAIL")
            claim_check = next(item for item in validation["checks"] if item["name"] == "prohibited_claims_absent")
            self.assertFalse(claim_check["passed"])


if __name__ == "__main__":
    unittest.main()
