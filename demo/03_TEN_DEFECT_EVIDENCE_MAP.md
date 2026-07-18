# Ten-Defect Evidence Map

| # | Frozen defect | Sources | Required handling | Result |
| ---: | --- | --- | --- | --- |
| 1 | Client goal promoted to verified capacity | S1, S7 | Keep 20 hours as desired direction only. | Detected and corrected |
| 2 | Episodic activity promoted to sustainable schedule | S1, S7 | Preserve three separate observations, recovery variability, and missing consecutive-day evidence. | Detected and corrected |
| 3 | Provider guidance overstated as medical clearance | S2, S7 | Remove clearance and preserve the provider’s explicit limit. | Detected and corrected |
| 4 | Single OT trial overstated as prescription and proof | S3, S7 | Describe one trial; route prescription and long-term fit to further evaluation. | Detected and corrected |
| 5 | VR possibility overstated as service and funding approval | S5, S7 | Restore eligibility and individualized-planning prerequisites; remove promises. | Detected and corrected |
| 6 | Generic benefits information overstated as continuity guarantee | S6, S7 | Remove guarantee; route to the authorized program representative. | Detected and corrected |
| 7 | Stale pre-interruption plan used as readiness evidence | S4, S7 | Label stale and require current client confirmation. | Detected and corrected |
| 8 | Recovery variability and untested consecutive days omitted | S1, S7 | Restore immediate, delayed, and repeatability limits. | Detected and corrected |
| 9 | Source authorities blended without attribution | S1–S7 | Classify and cite client, provider, OT, historical, VR, benefits, and draft statements separately. | Detected and corrected |
| 10 | Review-only draft incorrectly marked approved | S7 | Replace `APPROVED` with `READY_FOR_USER_REVIEW`. | Detected and corrected |

## Scoring result

- Defect score: **10 / 10**
- Classification score: **10 / 10**
- Critical false positives: **0**
- Qualitative gates: **12 / 12**

Machine-readable proof: `examples/generated-review-packet/FHP-SYNTH-002/stage3-final-scorecard.json`.

## Separate governance finding

`S3-MANUAL-001` was not one of the planted defects. Human review discovered that the baseline capacity record combined client activity with the OT simulation. The baseline remained preserved; patch cycle 1 separated the sources and added a regression gate.

Governance proof: `governance/STAGE_3_DEFECT_LOG.md`.
