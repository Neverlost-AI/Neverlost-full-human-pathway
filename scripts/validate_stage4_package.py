#!/usr/bin/env python3
"""Validate the Stage 4 demonstration and evidence package."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from neverlost_core import load_json, write_json


ROOT = Path(__file__).resolve().parents[1]
DEMO = ROOT / "demo"
MANIFEST = DEMO / "stage4-package-manifest.json"
EVIDENCE = DEMO / "stage4-demo-evidence.json"
STAGE3_SCORE = ROOT / "examples/generated-review-packet/FHP-SYNTH-002/stage3-final-scorecard.json"
STAGE3_VALIDATION = ROOT / "examples/generated-review-packet/FHP-SYNTH-002/validation-report.json"
DEFAULT_OUTPUT = DEMO / "stage4-package-validation.json"


def validate() -> dict[str, Any]:
    manifest = load_json(MANIFEST)
    evidence = load_json(EVIDENCE)
    stage3_score = load_json(STAGE3_SCORE)
    stage3_validation = load_json(STAGE3_VALIDATION)
    checks: list[dict[str, Any]] = []

    def add(name: str, passed: bool, detail: str) -> None:
        checks.append({"name": name, "passed": passed, "detail": detail})

    missing_files = [relative for relative in manifest["files"] if not (DEMO / relative).is_file() and relative != DEFAULT_OUTPUT.name]
    add("manifest_files_present", not missing_files, f"missing={missing_files}")
    add("manifest_synthetic_only", manifest["synthetic_only"] is True, f"synthetic_only={manifest['synthetic_only']}")
    add("manifest_status", manifest["status"] == "STAGE_4_DEMONSTRATION_PACKAGE_READY_FOR_HUMAN_REVIEW", manifest["status"])
    add("demo_status", evidence["status"] == "PASS" and evidence["completion_status"] == manifest["status"], evidence["completion_status"])
    add("review_only_final_status", evidence["final_status"] == manifest["final_artifact_status"] == "READY_FOR_USER_REVIEW", evidence["final_status"])

    metric_map = {
        "defects_detected_and_corrected": "deliberate_defects_detected_and_corrected",
        "defects_possible": "deliberate_defects_possible",
        "classification_matches": "classification_matches",
        "classification_possible": "classification_possible",
        "critical_false_positives": "critical_false_positives",
        "packet_checks_passed": "packet_checks_passed",
        "packet_checks_possible": "packet_checks_possible",
        "qualitative_gates_passed": "qualitative_gates_passed",
        "qualitative_gates_possible": "qualitative_gates_possible",
        "regression_tests_passed": "regression_tests_passed",
        "regression_tests_run": "regression_tests_run",
        "governed_patch_cycles": "governed_patch_cycles",
    }
    metric_mismatches = {
        manifest_name: {"manifest": manifest["authoritative_metrics"][manifest_name], "demo": evidence["metrics"][evidence_name]}
        for manifest_name, evidence_name in metric_map.items()
        if manifest["authoritative_metrics"][manifest_name] != evidence["metrics"][evidence_name]
    }
    add("manifest_metrics_match_demo", not metric_mismatches, f"mismatches={metric_mismatches}")

    add("stage3_defect_score", stage3_score["defect_score"] == {"detected_and_corrected": 10, "possible": 10}, json.dumps(stage3_score["defect_score"], sort_keys=True))
    add("stage3_classification_score", stage3_score["classification_score"] == {"matches": 10, "possible": 10}, json.dumps(stage3_score["classification_score"], sort_keys=True))
    add("stage3_false_positives", stage3_score["critical_false_positives"] == [], f"count={len(stage3_score['critical_false_positives'])}")
    add("stage3_packet_validation", stage3_validation["status"] == "PASS" and all(item["passed"] for item in stage3_validation["checks"]), f"checks={len(stage3_validation['checks'])}")
    add("demo_evidence_checks", all(item["passed"] for item in evidence["evidence_checks"]), f"checks={len(evidence['evidence_checks'])}")

    before_after = (DEMO / "02_BEFORE_AFTER.md").read_text(encoding="utf-8")
    add("unsafe_draft_labeled", "deliberately unsafe" in before_after.lower() and "not an approved conclusion" in before_after.lower(), "synthetic unsafe input is explicitly bounded")
    add("human_patch_visible", "human-review patch" in before_after.lower() and "capacity" in before_after.lower(), "human inspection remains visible")

    architecture = (DEMO / "04_TECHNICAL_ARCHITECTURE.md").read_text(encoding="utf-8")
    add("architecture_limit_visible", "bounded rule-based prototype" in architecture.lower() and "not general-purpose" in architecture.lower(), "prototype limitation is explicit")

    vr_note = (DEMO / "06_VR_SAFE_DEMONSTRATION_NOTE.md").read_text(encoding="utf-8")
    add("vr_boundary_visible", "does not prove" in vr_note.lower() and "counselor agreement or endorsement" in vr_note.lower(), "VR framing stays non-authoritative")

    markdown_text = "\n".join(path.read_text(encoding="utf-8") for path in sorted(DEMO.glob("*.md")))
    real_tokens = ["Jeff Summerhays", "Dr. Murray", "Molina", "Jenny"]
    real_hits = [token for token in real_tokens if token.lower() in markdown_text.lower()]
    add("real_identifiers_absent", not real_hits, f"hits={real_hits}")

    prohibited_positive_patterns = {
        "counselor_endorsement_claim": r"(?i)\b(?:the )?counselor (?:endorses|approved|agrees that)\b",
        "operational_approval_claim": r"(?i)\bis operationally approved\b",
        "real_client_readiness_claim": r"(?i)\bis ready for real-client use\b",
    }
    pattern_hits = [name for name, pattern in prohibited_positive_patterns.items() if re.search(pattern, markdown_text)]
    add("prohibited_package_claims_absent", not pattern_hits, f"hits={pattern_hits}")

    passed = all(item["passed"] for item in checks)
    return {
        "stage": 4,
        "status": "PASS" if passed else "FAIL",
        "completion_status": "STAGE_4_DEMONSTRATION_PACKAGE_READY_FOR_HUMAN_REVIEW" if passed else "STAGE_4_DEMONSTRATION_PACKAGE_BLOCKED",
        "checks": checks,
    }


def main() -> int:
    report = validate()
    write_json(DEFAULT_OUTPUT, report)
    passed_count = sum(item["passed"] for item in report["checks"])
    print(f"{report['completion_status']}: {passed_count}/{len(report['checks'])} package checks")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
