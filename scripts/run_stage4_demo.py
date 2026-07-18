#!/usr/bin/env python3
"""Run the reproducible Stage 4 Neverlost synthetic demonstration."""

from __future__ import annotations

import argparse
import io
import tempfile
import unittest
from pathlib import Path
from typing import Any

from neverlost_core import load_json, write_json
from run_workflow import run
from score_stage3_retest import score
from validate_packet import validate


ROOT = Path(__file__).resolve().parents[1]
CASE_SPEC = ROOT / "fixtures/synthetic-intake/FHP-SYNTH-002/case-spec.json"
FIXTURE = ROOT / "fixtures/synthetic-intake/FHP-SYNTH-002/fixture-manifest.json"
DEFAULT_OUTPUT = ROOT / "demo/stage4-demo-evidence.json"


def run_regressions() -> dict[str, Any]:
    suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"), pattern="test_*.py")
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=0).run(suite)
    return {
        "run": result.testsRun,
        "passed": result.testsRun - len(result.failures) - len(result.errors),
        "failures": len(result.failures),
        "errors": len(result.errors),
        "successful": result.wasSuccessful(),
    }


def demonstrate(include_tests: bool = True) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="neverlost-stage4-") as temporary:
        packet_dir = Path(temporary) / "FHP-SYNTH-002"
        run(CASE_SPEC, FIXTURE, packet_dir)
        validation = validate(packet_dir, CASE_SPEC, patch_cycle_count=1)
        scorecard = score(packet_dir, CASE_SPEC)
        capacity = load_json(packet_dir / "03-capacity-record.json")
        pathway = load_json(packet_dir / "04-pathway-plan.json")
        findings = load_json(packet_dir / "05-findings.json")
        checkpoint = load_json(packet_dir / "08-checkpoint.json")
        revised = (packet_dir / "06-revised-output.md").read_text(encoding="utf-8")

    checks_passed = sum(item["passed"] for item in validation["checks"])
    qualitative_passed = sum(item["passed"] for item in scorecard["qualitative_gates"])
    regressions = run_regressions() if include_tests else {"run": 0, "passed": 0, "failures": 0, "errors": 0, "successful": True}
    real_tokens = ["Jeff Summerhays", "Dr. Murray", "Molina", "Jenny"]
    real_identifier_hits = [token for token in real_tokens if token.lower() in revised.lower()]

    evidence_checks = [
        {"name": "packet_validation", "passed": validation["status"] == "PASS"},
        {"name": "defect_score", "passed": scorecard["defect_score"] == {"detected_and_corrected": 10, "possible": 10}},
        {"name": "classification_score", "passed": scorecard["classification_score"] == {"matches": 10, "possible": 10}},
        {"name": "critical_false_positives", "passed": scorecard["critical_false_positives"] == []},
        {"name": "capacity_source_separation", "passed": capacity["source_ids"] == ["S1"] and "3 separate client-observed" in capacity["output_achieved"]},
        {"name": "pathway_structure", "passed": len(pathway["lanes"]) == 6 and len(pathway["bridges"]) == 5},
        {"name": "findings_disposition", "passed": findings["counts"] == {"revision_required": 8, "revision_recommended": 2, "acceptable_as_written": 2}},
        {"name": "review_only_status", "passed": checkpoint["status"] == "READY_FOR_USER_REVIEW"},
        {"name": "privacy_boundary", "passed": not real_identifier_hits},
        {"name": "regression_tests", "passed": regressions["successful"]},
    ]
    passed = all(item["passed"] for item in evidence_checks)
    return {
        "stage": 4,
        "case_id": "FHP-SYNTH-002",
        "status": "PASS" if passed else "FAIL",
        "completion_status": "STAGE_4_DEMONSTRATION_PACKAGE_READY_FOR_HUMAN_REVIEW" if passed else "STAGE_4_DEMONSTRATION_PACKAGE_BLOCKED",
        "metrics": {
            "deliberate_defects_detected_and_corrected": scorecard["defect_score"]["detected_and_corrected"],
            "deliberate_defects_possible": scorecard["defect_score"]["possible"],
            "classification_matches": scorecard["classification_score"]["matches"],
            "classification_possible": scorecard["classification_score"]["possible"],
            "critical_false_positives": len(scorecard["critical_false_positives"]),
            "packet_checks_passed": checks_passed,
            "packet_checks_possible": len(validation["checks"]),
            "qualitative_gates_passed": qualitative_passed,
            "qualitative_gates_possible": len(scorecard["qualitative_gates"]),
            "pathway_lanes": len(pathway["lanes"]),
            "authority_bridges": len(pathway["bridges"]),
            "regression_tests_passed": regressions["passed"],
            "regression_tests_run": regressions["run"],
            "governed_patch_cycles": scorecard["patch_cycle_count"],
        },
        "human_review_evidence": {
            "baseline_packet_commit": "13af4f9",
            "baseline_score_commit": "d0f6b8e",
            "manual_finding": "S3-MANUAL-001 capacity observation conflation and counting",
            "patch_result": "Client observations separated from the distinct occupational-therapy simulation; quantity parsing corrected.",
        },
        "capacity_evidence": {
            "primary_source_ids": capacity["source_ids"],
            "output_achieved": capacity["output_achieved"],
            "repeatability": capacity["repeatability"],
            "delayed_recovery": capacity["recovery_cost"]["delayed"],
        },
        "evidence_checks": evidence_checks,
        "real_identifier_hits": real_identifier_hits,
        "final_status": checkpoint["status"],
        "boundary": "Synthetic demonstration only; no real-world approval, endorsement, professional conclusion, or operational authorization.",
    }


def print_summary(result: dict[str, Any]) -> None:
    metrics = result["metrics"]
    lines = [
        "NEVERLOST STAGE 4 — REPRODUCIBLE SYNTHETIC DEMO",
        f"Status: {result['completion_status']}",
        f"Defects handled: {metrics['deliberate_defects_detected_and_corrected']}/{metrics['deliberate_defects_possible']}",
        f"Classifications correct: {metrics['classification_matches']}/{metrics['classification_possible']}",
        f"Critical false positives: {metrics['critical_false_positives']}",
        f"Packet checks: {metrics['packet_checks_passed']}/{metrics['packet_checks_possible']}",
        f"Qualitative gates: {metrics['qualitative_gates_passed']}/{metrics['qualitative_gates_possible']}",
        f"Regression tests: {metrics['regression_tests_passed']}/{metrics['regression_tests_run']}",
        f"Final artifact status: {result['final_status']}",
        f"Boundary: {result['boundary']}",
    ]
    print("\n".join(lines))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, help="Optional path for machine-readable demo evidence")
    parser.add_argument("--skip-tests", action="store_true", help="Skip repository regression tests for a faster display-only run")
    args = parser.parse_args()
    result = demonstrate(include_tests=not args.skip_tests)
    if args.output:
        write_json(args.output.resolve(), result)
    print_summary(result)
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
