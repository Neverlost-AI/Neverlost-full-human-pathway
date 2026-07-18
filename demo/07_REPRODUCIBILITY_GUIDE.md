# Reproducibility Guide

## Requirements

- Python 3.10 or newer
- Repository files from the completed Stage 4 commit
- No API key, internet connection, private record, or external service

## Fast demonstration

```bash
python scripts/run_stage4_demo.py
```

Expected completion status:

```text
STAGE_4_DEMONSTRATION_PACKAGE_READY_FOR_HUMAN_REVIEW
```

## Regenerate machine-readable demo evidence

```bash
python scripts/run_stage4_demo.py --output demo/stage4-demo-evidence.json
```

## Rebuild the final Stage 3 packet

```bash
python scripts/run_demo_validation.py \
  --case-spec fixtures/synthetic-intake/FHP-SYNTH-002/case-spec.json \
  --fixture fixtures/synthetic-intake/FHP-SYNTH-002/fixture-manifest.json \
  --output-dir examples/generated-review-packet/FHP-SYNTH-002 \
  --patch-cycle-count 1
```

Then score it:

```bash
python scripts/score_stage3_retest.py \
  --packet-dir examples/generated-review-packet/FHP-SYNTH-002 \
  --output examples/generated-review-packet/FHP-SYNTH-002/stage3-final-scorecard.json
```

## Run regressions

```bash
python -m unittest discover -s tests -p 'test_*.py'
python scripts/smoke_test.py
```

## Validate the demonstration package

```bash
python scripts/validate_stage4_package.py
```

## Evidence lineage

| Evidence | Location |
| --- | --- |
| Frozen second-case specification | `fixtures/synthetic-intake/FHP-SYNTH-002/case-spec.json` |
| Untouched baseline packet | `examples/stage3-baseline/FHP-SYNTH-002/` |
| Baseline packet commit | `13af4f9` |
| Baseline score commit | `d0f6b8e` |
| Human-inspection defect | `governance/STAGE_3_DEFECT_LOG.md` |
| Patched final packet | `examples/generated-review-packet/FHP-SYNTH-002/` |
| Final validation | `examples/generated-review-packet/FHP-SYNTH-002/validation-report.json` |
| Final score | `examples/generated-review-packet/FHP-SYNTH-002/stage3-final-scorecard.json` |
| Stage 3 completion | `governance/STAGE_3_CHECKPOINT.md` |
| Stage 4 clean-run evidence | `demo/stage4-demo-evidence.json` |

## Interpretation boundary

Reproduction confirms that the committed deterministic prototype behaves as documented on the fictional fixtures. It does not establish accuracy for unseen real records or authorize operational use.
