# Neverlost Build Week Compliance Checklist

**As-of date:** 2026-07-18<br>
**Operating timezone:** America/Denver  
**Official source checked:** [OpenAI Build Week Official Rules](https://openai.devpost.com/rules)  
**Planned track:** Work & Productivity  
**Status:** `COMPLIANCE_AUDIT_COMPLETE_OPEN_SUBMISSION_GATES_RECORDED`

## Bounded review question

What must be true, evidenced, confirmed, or completed before **Neverlost: The Full Human Pathway** can be entered as a compliant OpenAI Build Week submission?

This checklist audits submission readiness. It does not determine legal eligibility, grant permission to publish, or submit the entry.

## Status legend

- `VERIFIED_COMPLETE` — supported by the official rules and committed project evidence.
- `PARTIAL_PACKAGING_REQUIRED` — underlying evidence exists, but the judge-facing requirement is not complete.
- `OPEN_ACTION` — an artifact or external action still must be completed.
- `USER_CONFIRMATION_REQUIRED` — only the entrant can accurately confirm the item.
- `NOT_APPLICABLE` — reviewed and not triggered by the current project.

## A. Entrant and timing

| ID | Official requirement | Neverlost evidence / action | Status |
| --- | --- | --- | --- |
| C-01 | Entrant is at least the age of majority where they reside. | Entrant confirmed age-of-majority status on 2026-07-17. No identity document is stored in the repository. | `VERIFIED_COMPLETE` |
| C-02 | Entrant resides in an eligible country or territory and is not otherwise excluded. | Entrant confirmed United States residence on 2026-07-17. | `VERIFIED_COMPLETE` |
| C-03 | If entering for a team or organization, the submitter is its authorized representative. | Jeff Summerhays confirmed entry as an individual; no team or organization representative claim is required. | `VERIFIED_COMPLETE` |
| C-04 | Registration and submission occur during the official periods. | Entrant confirmed Build Week registration. Official submission deadline is July 21, 2026 at 5:00 p.m. Pacific Time; actual submission remains open. | `PARTIAL_PACKAGING_REQUIRED` |
| C-05 | Submission is not changed after the deadline except where expressly permitted. | Preserve a final submission snapshot and receipt before the deadline. | `OPEN_ACTION` |

## B. Project qualification

| ID | Official requirement | Neverlost evidence / action | Status |
| --- | --- | --- | --- |
| C-06 | Project is built with Codex and GPT-5.6 and fits a listed track. | Codex collaboration is evidenced by the project thread and dated repository work. Entrant confirmed GPT-5.6 Sol for the project thread. Planned track is Work & Productivity. | `VERIFIED_COMPLETE` |
| C-07 | Project installs and runs consistently on its stated platform. | A fresh local clone on Linux/Python 3.12.13 reproduced the demo, passed 17 of 17 package checks, passed the smoke test, and passed all six unit tests. Supported and tested platforms are distinguished in the README. | `VERIFIED_COMPLETE` |
| C-08 | A project is newly created during the submission period or, if pre-existing, meaningfully extended after the period begins; prior and new work must be distinguished when applicable. | The broader Neverlost governed-review foundation, Capacity & Output concept, and identity predated the submission period. The creator confirmed that Full Human Pathway was created during the submission period before Stage 1. `governance/PRIOR_AND_BUILD_WEEK_WORK_LEDGER.md`, the submission delta record, and commits `bb0bdb1` through `d6e144f` distinguish those origins from the Stage 1–4 implementation. | `VERIFIED_COMPLETE` |
| C-09 | Entrant is authorized to use any third-party SDKs, APIs, or data. | Current Python implementation uses the standard library and repository-owned synthetic data. Final media, font, logo, dependency, and license audit remains required. | `PARTIAL_PACKAGING_REQUIRED` |
| C-10 | Project is original, owned by the entrant, and does not violate third-party rights. | Jeff Summerhays confirmed ownership of the Neverlost submission and materials. The selected private-repository path does not require a public open-source license; final rights review remains. | `PARTIAL_PACKAGING_REQUIRED` |
| C-11 | Project did not receive disqualifying financial or preferential support from OpenAI or Devpost. | Entrant confirmed no financial or preferential project support from OpenAI or Devpost. | `VERIFIED_COMPLETE` |

## C. Required submission materials

| ID | Official requirement | Neverlost evidence / action | Status |
| --- | --- | --- | --- |
| C-12 | Choose the best-aligned category. | Work & Productivity is frozen in the Stage 1 scope decision; it still must be selected on Devpost. | `PARTIAL_PACKAGING_REQUIRED` |
| C-13 | Include an English text description explaining features and functionality. | Stage 4 evidence supports the description. Devpost-ready copy has not yet been drafted. | `OPEN_ACTION` |
| C-14 | Include a public YouTube demonstration video under three minutes, with audio explaining what was built and how Codex and GPT-5.6 were used. | Storyboard exists at `demo/05_DEMO_SCRIPT_AND_VIDEO_STORYBOARD.md`. Recording, captions, upload, model-usage explanation, and signed-out playback test remain. | `OPEN_ACTION` |
| C-15 | Video uses no third-party trademarks, copyrighted music, or other material without permission. | Use repository-owned visuals, the approved NVLT mark, original narration, and no unlicensed music. Perform a final rights audit. | `OPEN_ACTION` |
| C-16 | Provide a judge-accessible repository URL: public with relevant licensing, or private and shared with both required addresses. | Entrant selected a private repository. Repository creation and sharing with `testing@devpost.com` and `build-week-event@openai.com` remain open. | `OPEN_ACTION` |
| C-17 | README explains Codex collaboration, acceleration, key human decisions, and Codex/GPT-5.6 contributions. | README now documents Codex acceleration, GPT-5.6 Sol use, the creator's controlling decisions, Build Week additions, accessibility value, and the private Session ID boundary. | `VERIFIED_COMPLETE` |
| C-18 | Provide the `/feedback` Codex Session ID for the thread where most core functionality was built. | Feedback was submitted and the current thread ID was captured. The value is retained privately for the Devpost field and intentionally excluded from the repository. | `VERIFIED_COMPLETE` |
| C-19 | Plugins/dev tools include install instructions, supported platforms, and a judge test path that avoids rebuilding from scratch. | README and `docs/PLUGIN_INSTALLATION.md` provide platform-specific commands, optional local-plugin installation, synthetic sample data, and a no-build judge path. The Linux clean-clone test passed. | `VERIFIED_COMPLETE` |
| C-20 | Provide free, unrestricted working access for testing through the judging period. | Repository/demo access must remain available through August 5, 2026 at 5:00 p.m. Pacific Time; access mode has not yet been selected. | `OPEN_ACTION` |
| C-21 | Submission materials are in English or include English translations. | Repository, demonstration package, and planned submission materials are in English. | `VERIFIED_COMPLETE` |

## D. Neverlost-specific safety and submission integrity

| ID | Requirement / control | Neverlost evidence / action | Status |
| --- | --- | --- | --- |
| C-22 | Public materials contain no real client record, private appointment information, or unsupported third-party endorsement. | Stage 4 validation found zero real identifiers and zero prohibited endorsement or operational claims. Repeat the audit against the final video, screenshots, README, and Devpost copy. | `PARTIAL_PACKAGING_REQUIRED` |
| C-23 | Demonstrated results remain accurately labeled synthetic, governed, and review-only. | Stage 4 manifest and checkpoint preserve these boundaries. Maintain them in every submission surface. | `VERIFIED_COMPLETE` |
| C-24 | If Modern Paradox is also submitted, the two entries are unique and substantially different. | Separate repository, product identity, demo, narrative, and judging case are required. Modern Paradox remains outside this Neverlost submission lane. | `OPEN_ACTION` |

## Current readiness summary

- `VERIFIED_COMPLETE`: 12
- `PARTIAL_PACKAGING_REQUIRED`: 5
- `OPEN_ACTION`: 7
- `USER_CONFIRMATION_REQUIRED`: 0
- `NOT_APPLICABLE`: 0

No rule conflict was found that makes Neverlost ineligible on the current evidence. All entrant confirmations are complete. Submission is not yet compliance-ready because private repository creation and judge sharing, README packaging, the video, final rights/privacy review, and Devpost assembly remain open.

## Entrant confirmations captured

1. Age-of-majority confirmed.
2. United States residence confirmed.
3. Individual entrant status confirmed.
4. Ownership confirmed; final rights audit remains a separate gate.
5. No financial or preferential project support from OpenAI or Devpost confirmed.
6. Build Week Devpost registration confirmed.
7. GPT-5.6 Sol confirmed for the project thread.
8. Private repository selected.
9. `/feedback` Session ID captured and retained outside the repository.

## Exit gate

`NEVERLOST_BUILD_WEEK_COMPLIANCE_READY_FOR_FINAL_SUBMISSION_QA`

Pass only when every `OPEN_ACTION`, `PARTIAL_PACKAGING_REQUIRED`, and `USER_CONFIRMATION_REQUIRED` item has evidence or an explicit, rule-consistent disposition.
