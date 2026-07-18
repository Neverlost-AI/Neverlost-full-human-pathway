# Stage 3 Defect Log

**Case:** `FHP-SYNTH-002`  
**Baseline packet commit:** `13af4f9`  
**Baseline validator commit:** `2bd5665`  
**Baseline score commit:** `d0f6b8e`  
**Current status:** `STAGE_3_PATCH_CYCLE_1_RETEST_PASSED`

## Baseline result

- Deterministic packet validation: PASS
- Frozen deliberate-defect score: 10 of 10 detected and corrected
- Classification score: 10 of 10
- Critical false positives: 0
- Qualitative scoring gates: 12 of 12
- Final status: `READY_FOR_USER_REVIEW`

The baseline remains immutable under `examples/stage3-baseline/FHP-SYNTH-002/`.

## Governed human-inspection finding

### `S3-MANUAL-001` — capacity observation conflation and counting

**Classification:** `REVISION_REQUIRED`  
**Affected output:** `03-capacity-record.json`  
**Affected logic:** `build_capacity_record`

The baseline capacity record combined the client report and the separate occupational-therapy simulation into one observation set. Its count was produced from raw duration mentions, which can count repeated references to the same activity and can miss word-based quantities such as “two 25-minute periods.”

Although the resulting count happened to equal four in this fixture, the method did not preserve source authority or measurement provenance precisely enough. The occupational-therapy trial belongs in the accessibility pathway and must not be silently merged into the client-reported capacity observation.

## Authorized patch cycle 1

- Restrict the primary capacity record to the synthetic user-report source.
- Parse explicit word or numeric quantities attached to duration observations.
- Ignore later narrative references to the same duration when determining observation count.
- Keep the occupational-therapy trial in the accessibility pathway, finding, and source-attributed revised output.
- Add deterministic validation and a regression assertion for capacity-source scope and the three-period client count.
- Generate a separate final Stage 3 packet; do not modify the locked baseline.

## Retest requirement

Patch cycle 1 passes only if:

- the final capacity record reports three client observations, with 40 minutes as the longest period;
- only the client report is used as the primary capacity-record source;
- the occupational-therapy observation remains separately visible elsewhere;
- the ten-defect and classification scores remain 10 of 10;
- all prior regression tests pass; and
- the final status remains `READY_FOR_USER_REVIEW`.

## Patch cycle 1 result

- Primary capacity source corrected from `S1 + S3` to `S1` only.
- Explicit quantity parsing now records two 25-minute periods plus one 40-minute period as three client observations.
- Later references to “the 40-minute period” no longer create duplicate observations.
- The OT simulation remains separately visible in the accessibility lane, bridge, finding, and revised output.
- Capacity-source validator added and passed.
- Stage 3 positive and negative regression tests added and passed.
- Final Stage 3 packet: 24 of 24 deterministic checks passed.
- Frozen defect and classification scores remained 10 of 10.
- Critical false positives remained 0.
- Full repository unit tests: 5 of 5 passed.

No additional patch cycle is required.
