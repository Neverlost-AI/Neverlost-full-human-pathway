#!/usr/bin/env python3
"""Score the locked FHP-SYNTH-002 packet against the frozen Stage 3 rubric."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

from neverlost_core import load_json, write_json


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PACKET = ROOT / "examples/stage3-baseline/FHP-SYNTH-002"
DEFAULT_CASE_SPEC = ROOT / "fixtures/synthetic-intake/FHP-SYNTH-002/case-spec.json"
DEFAULT_OUTPUT = DEFAULT_PACKET / "stage3-baseline-scorecard.json"

EXPECTED_CLASSIFICATION = {
    "client_goal_promoted_to_verified_capacity": "REVISION_RECOMMENDED",
    "episodic_activity_promoted_to_sustainable_schedule": "REVISION_REQUIRED",
    "provider_guidance_overstated_as_medical_clearance": "REVISION_REQUIRED",
    "single_ot_trial_overstated_as_prescription_and_proof": "REVISION_RECOMMENDED",
    "vr_possibility_overstated_as_service_and_funding_approval": "REVISION_REQUIRED",
    "generic_benefits_information_overstated_as_continuity_guarantee": "REVISION_REQUIRED",
    "stale_pre_interruption_plan_used_as_current_readiness_evidence": "REVISION_REQUIRED",
    "recovery_variability_and_untested_consecutive_days_omitted": "REVISION_REQUIRED",
    "source_authorities_blended_without_attribution": "REVISION_REQUIRED",
    "review_only_draft_incorrectly_marked_approved": "REVISION_REQUIRED",
}

UNSAFE_PATTERNS = {
    "client_goal_promoted_to_verified_capacity": [r"(?i)\bis (?:a )?sustainable 20-hour"],
    "episodic_activity_promoted_to_sustainable_schedule": [r"(?i)\bsustainable 20-hour remote administrative schedule\b"],
    "provider_guidance_overstated_as_medical_clearance": [r"(?i)\b(?:is|was|has been) medically cleared\b"],
    "single_ot_trial_overstated_as_prescription_and_proof": [r"(?i)\boccupational therapy proved\b", r"(?i)\bsplit keyboard and vertical mouse are required\b"],
    "vr_possibility_overstated_as_service_and_funding_approval": [r"(?i)\bvocational rehabilitation will purchase\b", r"(?i)\bpay for training\b"],
    "generic_benefits_information_overstated_as_continuity_guarantee": [r"(?i)\bbenefits will continue unchanged\b"],
    "stale_pre_interruption_plan_used_as_current_readiness_evidence": [r"(?i)\bprior full-time plan confirms\b", r"(?i)\bis employment ready\b"],
    "source_authorities_blended_without_attribution": [],
    "review_only_draft_incorrectly_marked_approved": [r"(?mi)^APPROVED\s*:"],
}


def score(packet_dir: Path, case_spec_path: Path) -> dict[str, Any]:
    case_spec = load_json(case_spec_path)
    findings_doc = load_json(packet_dir / "05-findings.json")
    classifications = load_json(packet_dir / "02-source-classification.json")
    capacity = load_json(packet_dir / "03-capacity-record.json")
    pathway = load_json(packet_dir / "04-pathway-plan.json")
    checkpoint = load_json(packet_dir / "08-checkpoint.json")
    validation = load_json(packet_dir / "validation-report.json")
    revised = (packet_dir / "06-revised-output.md").read_text(encoding="utf-8")
    finding_map = {item["defect_id"]: item for item in findings_doc["findings"]}
    expected = case_spec["deliberate_defects"]
    non_draft_ids = [
        item["id"]
        for item in classifications["sources"]
        if item["classification"] != "CANDIDATE_OUTPUT"
    ]
    missing_citations = [source_id for source_id in non_draft_ids if f"[{source_id}]" not in revised]

    defect_results = []
    for defect_id in expected:
        finding = finding_map.get(defect_id)
        unsafe_hits = [
            pattern
            for pattern in UNSAFE_PATTERNS.get(defect_id, [])
            if re.search(pattern, revised)
        ]
        corrected = bool(finding and finding.get("corrected")) and not unsafe_hits
        if defect_id == "recovery_variability_and_untested_consecutive_days_omitted":
            corrected = corrected and "recovery" in revised.lower() and "consecutive-day" in revised.lower()
        if defect_id == "source_authorities_blended_without_attribution":
            corrected = corrected and not missing_citations
        if corrected:
            result = "DETECTED_AND_CORRECTED"
        elif finding:
            result = "DETECTED_NOT_CORRECTED"
        else:
            result = "MISSED"
        defect_results.append(
            {
                "defect_id": defect_id,
                "result": result,
                "classification": finding.get("classification") if finding else None,
                "classification_expected": EXPECTED_CLASSIFICATION[defect_id],
                "classification_matches": bool(finding and finding.get("classification") == EXPECTED_CLASSIFICATION[defect_id]),
                "source_ids": finding.get("source_ids", []) if finding else [],
                "unsafe_revised_patterns": unsafe_hits,
            }
        )

    expected_set = set(expected)
    false_positive_ids = [
        item["defect_id"]
        for item in findings_doc["findings"]
        if item["classification"] != "ACCEPTABLE_AS_WRITTEN" and item["defect_id"] not in expected_set
    ]
    actual_lanes = {item["lane"] for item in pathway["lanes"]}
    expected_lanes = set(case_spec["expected_pathway_lanes"])
    qualitative_gates = [
        {"name": "client_direction_bounded", "passed": "client-defined direction" in revised.lower()},
        {"name": "capacity_interpretation_bounded", "passed": "do not establish medical clearance" in capacity["bounded_interpretation"].lower()},
        {"name": "ot_trial_bounded", "passed": "one equipment trial" in revised.lower() and "no take-home trial" in revised.lower()},
        {"name": "vr_authority_bounded", "passed": "no service, device, vendor, training, or funding decision" in revised.lower()},
        {"name": "benefits_authority_bounded", "passed": "authorized program representative" in revised.lower() and "no individualized calculation" in revised.lower()},
        {"name": "stale_plan_visible", "passed": any(item["currency"] == "STALE_UNCONFIRMED" for item in classifications["sources"]) and "stale and unconfirmed" in revised.lower()},
        {"name": "recovery_and_variability_visible", "passed": capacity["repeatability"] == "VARIABLE" and bool(capacity["recovery_cost"]["delayed"])},
        {"name": "all_sources_attributed", "passed": not missing_citations},
        {"name": "pathway_lanes_exact", "passed": actual_lanes == expected_lanes},
        {"name": "bridge_authorities_visible", "passed": all(item["proper_authority"] and item["review_trigger"] for item in pathway["bridges"])},
        {"name": "review_only_status", "passed": pathway["status"] == checkpoint["status"] == "READY_FOR_USER_REVIEW"},
        {"name": "packet_validator_passed", "passed": validation["status"] == "PASS"},
    ]

    corrected_count = sum(item["result"] == "DETECTED_AND_CORRECTED" for item in defect_results)
    classification_count = sum(item["classification_matches"] for item in defect_results)
    passed = (
        corrected_count == len(expected)
        and classification_count == len(expected)
        and not false_positive_ids
        and all(item["passed"] for item in qualitative_gates)
    )
    return {
        "case_id": case_spec["case_id"],
        "baseline_packet_commit": "13af4f9",
        "baseline_validator_commit": "2bd5665",
        "status": "PASS" if passed else "FAIL",
        "completion_status": "STAGE_3_DISTINCT_CASE_GENERALIZATION_TEST_PASSED" if passed else "STAGE_3_DISTINCT_CASE_GENERALIZATION_TEST_BLOCKED",
        "defect_score": {"detected_and_corrected": corrected_count, "possible": len(expected)},
        "classification_score": {"matches": classification_count, "possible": len(expected)},
        "critical_false_positives": false_positive_ids,
        "defect_results": defect_results,
        "qualitative_gates": qualitative_gates,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--packet-dir", type=Path, default=DEFAULT_PACKET)
    parser.add_argument("--case-spec", type=Path, default=DEFAULT_CASE_SPEC)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = score(args.packet_dir.resolve(), args.case_spec.resolve())
    write_json(args.output.resolve(), result)
    print(f"{result['completion_status']}: {result['defect_score']['detected_and_corrected']}/{result['defect_score']['possible']} defects; {len(result['critical_false_positives'])} critical false positives")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
