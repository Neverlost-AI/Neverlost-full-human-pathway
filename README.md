# Neverlost: The Full Human Pathway

A governed, capacity-aware Codex workflow for turning scattered human reality into evidence-aligned action.

## Current status

`STAGE_3_DISTINCT_CASE_GENERALIZATION_TEST_PASSED`

The repository now contains the validated Stage 1 foundation, the completed `FHP-SYNTH-001` prototype, and a governed distinct-case retest using `FHP-SYNTH-002`. The untouched Stage 3 baseline caught and corrected all ten planted defects with zero critical false positives. A separate human inspection found one capacity-source fidelity issue; one reusable patch cycle corrected it without changing the locked baseline.

## Components

- `neverlost-review-workflow` — source custody, review lanes, controlled revision, QA, and checkpoints.
- `full-human-pathway` — whole-person lane mapping, pathway stages, and cross-system bridges.
- `capacity-output` — useful output documented with conditions, accommodations, variability, and recovery cost.

## Boundaries

The repository is an internal Build Week prototype. It does not diagnose, determine capacity or eligibility, approve services or funding, promise employment, contain real client records, establish external endorsement, or authorize operational use.

## Validation

Run the case with explicit `--case-spec`, `--fixture`, and `--output-dir` arguments. For Stage 3, follow packet validation with `python3 scripts/score_stage3_retest.py`. Repository regressions run with `python3 scripts/smoke_test.py` and `python3 -m unittest discover -s tests -v`.
