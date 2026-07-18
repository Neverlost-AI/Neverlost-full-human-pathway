# Neverlost Stage 4 Demonstration Package

**Status:** `STAGE_4_DEMONSTRATION_PACKAGE_READY_FOR_HUMAN_REVIEW`

This package explains and reproduces the synthetic Neverlost demonstration without requiring a reviewer to read the full repository.

## Run the demonstration

From the repository root:

```bash
python scripts/run_stage4_demo.py
```

The command creates a temporary `FHP-SYNTH-002` packet, validates it, scores it against the frozen ten-defect rubric, runs the repository tests, prints the results, and deletes the temporary packet. It does not modify the locked Stage 3 baseline.

Expected terminal result:

```text
Status: STAGE_4_DEMONSTRATION_PACKAGE_READY_FOR_HUMAN_REVIEW
Defects handled: 10/10
Classifications correct: 10/10
Critical false positives: 0
Packet checks: 24/24
Qualitative gates: 12/12
Regression tests: 6/6
Final artifact status: READY_FOR_USER_REVIEW
```

## Package order

1. `01_JUDGE_RESULTS.md` — concise value and evidence summary
2. `02_BEFORE_AFTER.md` — unsafe synthetic input versus governed handling
3. `03_TEN_DEFECT_EVIDENCE_MAP.md` — defect-by-defect proof
4. `04_TECHNICAL_ARCHITECTURE.md` — software structure and limitations
5. `05_DEMO_SCRIPT_AND_VIDEO_STORYBOARD.md` — recorded-demo plan
6. `06_VR_SAFE_DEMONSTRATION_NOTE.md` — bounded vocational-review framing
7. `07_REPRODUCIBILITY_GUIDE.md` — exact commands and expected results
8. `stage4-demo-evidence.json` — machine-readable clean-run evidence
9. `stage4-package-manifest.json` — package inventory and authority boundary

## Boundary

Every person, record, source, decision, and event in the demonstration is fictional. The package proves bounded synthetic workflow behavior, not medical, vocational, benefits, funding, legal, or real-world operational accuracy.
