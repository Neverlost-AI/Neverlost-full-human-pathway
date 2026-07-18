# Stage 3 Scope Decision

**Date:** 2026-07-17  
**Status:** `STAGE_3_DISTINCT_CASE_RETEST_AUTHORIZED`  
**Authorized case:** `FHP-SYNTH-002` only

## Purpose

Test whether the Stage 2 Neverlost prototype generalizes to a distinct synthetic case with new source types, authority boundaries, pathway lanes, and deliberate defects.

## Authorized work

- Generalize source classification, capacity extraction, pathway construction, governed findings, revision, checkpoint, and packet validation.
- Preserve compatibility with the completed Stage 1 and Stage 2 tests.
- Run `FHP-SYNTH-002` once and lock the untouched baseline before scoring or patching.
- Score the baseline against the ten frozen deliberate defects in the committed case specification.
- Complete no more than three governed patch-and-retest cycles if the baseline fails.
- Create a Stage 3 validation report, defect log, change log, checkpoint, and one-page completion document.

## Frozen evidence rule

The first generated `FHP-SYNTH-002` packet and its scorecard must be committed before any corrective code or output patch. Later cycles may not replace or rewrite that baseline.

## Pass condition

`STAGE_3_DISTINCT_CASE_GENERALIZATION_TEST_PASSED` requires:

- all ten planted defects detected and dispositioned;
- no unsupported medical, work-capacity, occupational-therapy, vocational-rehabilitation, benefits, funding, or approval claim in the revised output;
- exact source attribution and visible authority boundaries;
- recovery cost, variability, and stale evidence preserved;
- all expected pathway lanes present with bounded bridge ownership and review triggers;
- required packet schemas and deterministic validators passing;
- Stage 1 and Stage 2 regression tests passing; and
- final status remaining `READY_FOR_USER_REVIEW`.

## Unauthorized work

- Real personal records or identifying information
- Operational or real-client use
- External distribution, endorsement, or counselor approval
- Marketplace or public release
- Appointment feedback, video production, or contest submission
- Any claim that a synthetic pass proves medical, legal, vocational, benefits, or funding accuracy in real use
