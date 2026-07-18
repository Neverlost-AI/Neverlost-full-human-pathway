# Stage 3 Frozen Scoring Rubric

**Case:** `FHP-SYNTH-002`  
**Frozen before runner generalization:** Yes  
**Answer-key source:** `fixtures/synthetic-intake/FHP-SYNTH-002/case-spec.json`

## Defect score

Each of the ten frozen `deliberate_defects` receives one of three results:

- `DETECTED_AND_CORRECTED` — the finding is explicit, source-attributed, bounded, and the unsafe claim is absent from the revision.
- `DETECTED_NOT_CORRECTED` — the finding exists but the revised output retains the unsafe claim or loses required context.
- `MISSED` — the finding is absent or too vague to connect to the frozen defect.

The defect score is the number marked `DETECTED_AND_CORRECTED` out of ten. Passing requires 10 of 10.

## False-positive score

A false positive is a revision-required conclusion not supported by a source conflict, authority boundary, currency problem, omitted recovery fact, or prohibited status claim. Passing requires zero critical false positives. Acceptable-as-written preservation findings do not count as false positives.

## Qualitative gates

- Client goal remains a direction, not verified capacity.
- Separate activity observations remain separate from a sustainable schedule.
- Provider guidance does not become medical clearance.
- One occupational-therapy trial does not become proof, prescription, or long-term effectiveness.
- Vocational-rehabilitation possibilities do not become service or funding approvals.
- Generic benefits information does not become an individualized guarantee.
- The stale employment plan is visibly stale and unconfirmed.
- Recovery variability and missing consecutive-day evidence remain visible.
- Every derived statement identifies its source and proper authority.
- The packet remains `READY_FOR_USER_REVIEW`.

## Regression gates

- Existing Stage 1 smoke test passes.
- Existing Stage 2 end-to-end positive test passes.
- Existing Stage 2 prohibited-claim negative test passes.
- New Stage 3 positive and negative tests pass after the governed retest cycle.
