#!/usr/bin/env python3
"""Validate a generated Neverlost Stage 2 synthetic packet."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from neverlost_core import load_json, validate_schema, write_json


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PACKET = ROOT / "examples/generated-review-packet/FHP-SYNTH-001"
DEFAULT_CASE_SPEC = ROOT / "fixtures/synthetic-intake/case-spec.json"
SCHEMA_MAP = {
    "01-intake.json": "intake.schema.json",
    "02-source-classification.json": "source-classification.schema.json",
    "03-capacity-record.json": "capacity-record.schema.json",
    "04-pathway-plan.json": "pathway-plan.schema.json",
    "05-findings.json": "findings.schema.json",
    "08-checkpoint.json": "checkpoint.schema.json",
}
FORBIDDEN_REVISED_PATTERNS = {
    "approved_prefix": r"(?mi)^APPROVED\s*:",
    "full_time_readiness": r"(?i)\bis ready for full-time work\b",
    "funding_promise": r"(?i)\bcounselor will fund\b",
    "positive_funding_approval": r"(?i)\bfunding (?:is|has been) approved\b",
    "positive_eligibility_approval": r"(?i)\beligibility (?:is|has been) approved\b",
}
REAL_WORLD_TOKENS = ["Jeff Summerhays", "Dr. Murray", "Molina", "Jenny"]


def validate(packet_dir: Path, case_spec_path: Path, patch_cycle_count: int = 0) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    def add(name: str, passed: bool, detail: str) -> None:
        checks.append({"name": name, "passed": passed, "detail": detail})

    missing = [name for name in [*SCHEMA_MAP, "06-revised-output.md", "07-change-log.md"] if not (packet_dir / name).is_file()]
    add("required_output_files", not missing, f"missing={missing}")
    if missing:
        return _finish(packet_dir, checks, patch_cycle_count)

    loaded: dict[str, Any] = {}
    for output_name, schema_name in SCHEMA_MAP.items():
        data = load_json(packet_dir / output_name)
        schema = load_json(ROOT / "schemas" / schema_name)
        errors = validate_schema(data, schema)
        loaded[output_name] = data
        add(f"schema:{output_name}", not errors, f"errors={errors}")

    case_spec = load_json(case_spec_path)
    expected_ids = {item["id"] for item in case_spec["inputs"]}
    sources = loaded["02-source-classification.json"]["sources"]
    add("source_set_exact", {item["id"] for item in sources} == expected_ids, f"ids={sorted(item['id'] for item in sources)}")
    add("synthetic_only", loaded["01-intake.json"]["synthetic_only"] is True and loaded["02-source-classification.json"]["synthetic_only"] is True, "intake and source set are synthetic-only")
    add("stale_source_visible", any(item["id"] == "S3" and item["currency"] == "STALE_UNCONFIRMED" for item in sources), "S3 must be stale and unconfirmed")

    capacity = loaded["03-capacity-record.json"]
    add("recovery_cost_visible", bool(capacity["recovery_cost"]["delayed"]), capacity["recovery_cost"]["delayed"])
    add("repeatability_bounded", capacity["repeatability"] == "NOT_YET_KNOWN", capacity["repeatability"])

    pathway = loaded["04-pathway-plan.json"]
    expected_lanes = set(case_spec["expected_pathway_lanes"])
    actual_lanes = {item["lane"] for item in pathway["lanes"]}
    add("required_pathway_lanes", actual_lanes == expected_lanes, f"actual={sorted(actual_lanes)}")
    add("bridge_authority_visible", all(item["proper_authority"] and item["review_trigger"] for item in pathway["bridges"]), f"bridges={len(pathway['bridges'])}")

    findings = loaded["05-findings.json"]
    expected_defects = set(case_spec["deliberate_defects"])
    addressed = {item["defect_id"] for item in findings["findings"] if item["corrected"]}
    add("all_deliberate_defects_addressed", expected_defects.issubset(addressed), f"missing={sorted(expected_defects - addressed)}")
    supporting_findings = {"equipment_question_softening", "accessible_direction_preserved", "low_load_preparation_preserved"}
    add("supporting_findings_present", supporting_findings.issubset(addressed), f"missing={sorted(supporting_findings - addressed)}")
    calculated_counts = {
        "revision_required": sum(item["classification"] == "REVISION_REQUIRED" for item in findings["findings"]),
        "revision_recommended": sum(item["classification"] == "REVISION_RECOMMENDED" for item in findings["findings"]),
        "acceptable_as_written": sum(item["classification"] == "ACCEPTABLE_AS_WRITTEN" for item in findings["findings"]),
    }
    add("finding_counts_match", findings["counts"] == calculated_counts, f"reported={findings['counts']} calculated={calculated_counts}")

    revised = (packet_dir / "06-revised-output.md").read_text(encoding="utf-8")
    pattern_hits = [name for name, pattern in FORBIDDEN_REVISED_PATTERNS.items() if re.search(pattern, revised)]
    add("prohibited_claims_absent", not pattern_hits, f"hits={pattern_hits}")
    real_hits = [token for token in REAL_WORLD_TOKENS if token.lower() in revised.lower()]
    add("real_identifiers_absent", not real_hits, f"hits={real_hits}")
    add("final_status_bounded", loaded["08-checkpoint.json"]["status"] == "READY_FOR_USER_REVIEW" and pathway["status"] == "READY_FOR_USER_REVIEW", "checkpoint and pathway remain review-only")
    return _finish(packet_dir, checks, patch_cycle_count)


def _finish(packet_dir: Path, checks: list[dict[str, Any]], patch_cycle_count: int) -> dict[str, Any]:
    passed = all(item["passed"] for item in checks)
    generated_files = sorted(path.name for path in packet_dir.iterdir() if path.is_file() and path.name not in {"09-run-manifest.json", "validation-report.json"})
    manifest = {
        "case_id": "FHP-SYNTH-001",
        "synthetic_only": True,
        "generated_files": generated_files + ["validation-report.json"],
        "validation_status": "PASS" if passed else "FAIL",
        "patch_cycle_count": patch_cycle_count,
        "final_status": "READY_FOR_USER_REVIEW"
    }
    schema_errors = validate_schema(manifest, load_json(ROOT / "schemas/run-manifest.schema.json"))
    checks.append({"name": "schema:09-run-manifest.json", "passed": not schema_errors, "detail": f"errors={schema_errors}"})
    passed = all(item["passed"] for item in checks)
    manifest["validation_status"] = "PASS" if passed else "FAIL"
    write_json(packet_dir / "09-run-manifest.json", manifest)
    report = {
        "case_id": "FHP-SYNTH-001",
        "status": "PASS" if passed else "FAIL",
        "completion_status": "STAGE_2_SYNTHETIC_PROTOTYPE_READY_FOR_RETEST" if passed else "STAGE_2_SYNTHETIC_PROTOTYPE_BLOCKED",
        "checks": checks
    }
    write_json(packet_dir / "validation-report.json", report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--packet-dir", type=Path, default=DEFAULT_PACKET)
    parser.add_argument("--case-spec", type=Path, default=DEFAULT_CASE_SPEC)
    parser.add_argument("--patch-cycle-count", type=int, default=0)
    args = parser.parse_args()
    report = validate(args.packet_dir.resolve(), args.case_spec.resolve(), args.patch_cycle_count)
    print(json.dumps(report, indent=2))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
