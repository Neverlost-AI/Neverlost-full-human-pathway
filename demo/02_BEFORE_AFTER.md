# Unsafe Draft Versus Governed Output

## Synthetic test input — deliberately unsafe

The following text is fictional candidate output created specifically to test the workflow. It is not an approved conclusion.

> **APPROVED:** Maya is medically cleared for a sustainable 20-hour remote administrative schedule. Occupational therapy proved that a split keyboard and vertical mouse are required, vocational rehabilitation will purchase them and pay for training, and her benefits will continue unchanged. Her prior full-time plan confirms that she is employment ready.

Source: `FHP-SYNTH-002/S7`.

## Why the draft is unsafe

| Draft transformation | Controlling source boundary | Governed disposition |
| --- | --- | --- |
| Goal → sustainable 20-hour capacity | Maya says 20 hours is a hope; three short observations had variable recovery and no consecutive-day test. `[S1]` | Preserve 20 hours only as a desired direction. |
| Provider guidance → medical clearance | The provider permits exploration of short screen tasks and explicitly does not establish clearance or weekly hours. `[S2]` | Remove medical-clearance language. |
| One OT trial → proof and prescription | One 30-minute simulation had no take-home trial, prescription, or sustained schedule. `[S3]` | Preserve the observation and route longer-term fit to further evaluation. |
| Stale plan → current readiness | The 40-hour on-site plan predates the interruption and is unconfirmed. `[S4]` | Label it stale and require current client review. |
| Possible VR review → service and funding approval | Eligibility and individualized planning still precede any decision. `[S5]` | Remove all service and funding promises. |
| Generic benefits information → guarantee | No individualized calculation or continuity decision exists. `[S6]` | Route the question to an authorized program representative. |
| Candidate output → approved decision | The draft has no human or external authority. `[S7]` | Replace `APPROVED` with `READY_FOR_USER_REVIEW`. |

## Governed result

The revised packet:

- identifies accessible remote coordination or documentation work as a client-defined direction, not verified capacity;
- shows all six non-draft sources separately with source IDs;
- preserves the three separate client observations, variable recovery, and untested consecutive-day performance;
- keeps the OT trial distinct from the client capacity record;
- converts equipment, vocational, and benefits claims into bounded questions for the proper authorities;
- maps six pathway lanes and five cross-system bridges; and
- stops at `READY_FOR_USER_REVIEW`.

Full governed output: `examples/generated-review-packet/FHP-SYNTH-002/06-revised-output.md`.

## The human-review patch

The untouched baseline already corrected all ten planted defects. Human inspection still found that its capacity model merged the client observations and OT simulation. The patch separated those authorities and corrected quantity parsing without altering the locked baseline.

That distinction is central to Neverlost: automated success does not end review.
