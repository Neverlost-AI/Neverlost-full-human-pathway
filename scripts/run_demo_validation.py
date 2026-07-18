#!/usr/bin/env python3
"""Run and validate the complete Stage 2 synthetic demonstration."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from run_workflow import DEFAULT_CASE_SPEC, DEFAULT_FIXTURE, DEFAULT_OUTPUT, run
from validate_packet import validate


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case-spec", type=Path, default=DEFAULT_CASE_SPEC)
    parser.add_argument("--fixture", type=Path, default=DEFAULT_FIXTURE)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--patch-cycle-count", type=int, default=0)
    args = parser.parse_args()
    run(args.case_spec.resolve(), args.fixture.resolve(), args.output_dir.resolve())
    report = validate(args.output_dir.resolve(), args.case_spec.resolve(), args.patch_cycle_count)
    print(json.dumps(report, indent=2))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
