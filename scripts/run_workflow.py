#!/usr/bin/env python3
"""Generate the bounded Stage 2 packet for FHP-SYNTH-001."""

from __future__ import annotations

import argparse
from pathlib import Path

from neverlost_core import (
    build_capacity_record,
    build_change_log,
    build_checkpoint,
    build_findings,
    build_intake,
    build_pathway_plan,
    build_revised_output,
    classify_sources,
    load_json,
    write_json,
    write_text,
)


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CASE_SPEC = ROOT / "fixtures/synthetic-intake/case-spec.json"
DEFAULT_FIXTURE = ROOT / "fixtures/synthetic-intake/FHP-SYNTH-001/fixture-manifest.json"
DEFAULT_OUTPUT = ROOT / "examples/generated-review-packet/FHP-SYNTH-001"


def run(case_spec_path: Path, fixture_path: Path, output_dir: Path) -> list[Path]:
    case_spec = load_json(case_spec_path)
    fixture = load_json(fixture_path)
    if case_spec.get("case_id") != "FHP-SYNTH-001" or fixture.get("case_id") != "FHP-SYNTH-001":
        raise ValueError("Stage 2 is authorized only for FHP-SYNTH-001")
    if case_spec.get("synthetic_only") is not True or fixture.get("synthetic_only") is not True:
        raise ValueError("Stage 2 requires a synthetic-only fixture")

    source_root = fixture_path.parent
    sources = [load_json(source_root / relative) for relative in fixture["source_files"]]
    if any(source.get("synthetic_only") is not True for source in sources):
        raise ValueError("Every runnable source must be marked synthetic_only=true")

    outputs = {
        "01-intake.json": build_intake(case_spec, sources),
        "02-source-classification.json": classify_sources(case_spec["case_id"], sources),
        "03-capacity-record.json": build_capacity_record(case_spec["case_id"]),
        "04-pathway-plan.json": build_pathway_plan(case_spec),
        "05-findings.json": build_findings(case_spec),
        "08-checkpoint.json": build_checkpoint(case_spec),
    }
    written: list[Path] = []
    for name, data in outputs.items():
        target = output_dir / name
        write_json(target, data)
        written.append(target)

    for name, content in {
        "06-revised-output.md": build_revised_output(case_spec),
        "07-change-log.md": build_change_log(),
    }.items():
        target = output_dir / name
        write_text(target, content)
        written.append(target)
    return sorted(written)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case-spec", type=Path, default=DEFAULT_CASE_SPEC)
    parser.add_argument("--fixture", type=Path, default=DEFAULT_FIXTURE)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    written = run(args.case_spec.resolve(), args.fixture.resolve(), args.output_dir.resolve())
    for path in written:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
