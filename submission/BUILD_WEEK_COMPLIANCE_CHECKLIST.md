# Neverlost Build Week Compliance Checklist

**As-of date:** 2026-07-17  
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
| C-01 | Entrant is at least the age of majority where they reside. | Entrant confirmation must be recorded before submission. | `USER_CONFIRMATION_REQUIRED` |
| C-02 | Entrant resides in an eligible country or territory and is not otherwise excluded. | Entrant country and eligibility confirmation must be recorded; no sensitive identity document belongs in the public repository. | `USER_CONFIRMATION_REQUIRED` |
| C-03 | If entering for a team or organization, the submitter is its authorized representative. | Decide whether the entrant is Jeff Summerhays individually or Neverlost as an organization/team; record the correct representation. | `USER_CONFIRMATION_REQUIRED` |
| C-04 | Registration and submission occur during the official periods. | Official submission deadline is July 21, 2026 at 5:00 p.m. Pacific Time. Internal target remains July 21 morning. Devpost registration status must be confirmed. | `USER_CONFIRMATION_REQUIRED` |
| C-05 | Submission is not changed after the deadline except where expressly permitted. | Preserve a final submission snapshot and receipt before the deadline. | `OPEN_ACTION` |

## B. Project qualification

| ID | Official requirement | Neverlost evidence / action | Status |
| --- | --- | --- | --- |
| C-06 | Project is built with Codex and GPT-5.6 and fits a listed track. | Codex collaboration is evidenced by the project thread and dated repository work. Planned track is Work & Productivity. GPT-5.6 use must be confirmed from session/product metadata before it is stated as verified. | `PARTIAL_PACKAGING_REQUIRED` |
| C-07 | Project installs and runs consistently on its stated platform. | `python3 scripts/run_stage4_demo.py` reproduces the demonstration; package validation and six unit tests passed at Stage 4. Clean-checkout testing and platform statement remain. | `PARTIAL_PACKAGING_REQUIRED` |
| C-08 | A pre-existing project is meaningfully extended during the submission period, with prior and new work distinguished. | `governance/PRIOR_AND_BUILD_WEEK_WORK_LEDGER.md`, the submission delta record, and commits `bb0bdb1` through `d6e144f` distinguish the foundation from new implementation. | `VERIFIED_COMPLETE` |
| C-09 | Entrant is authorized to use any third-party SDKs, APIs, or data. | Current Python implementation uses the standard library and repository-owned synthetic data. Final media, font, logo, dependency, and license audit remains required. | `PARTIAL_PACKAGING_REQUIRED` |
| C-10 | Project is original, owned by the entrant, and does not violate third-party rights. | Repository identifies Jeff Summerhays / Neverlost as creator. Ownership and rights confirmation must come from the entrant; a repository license is not yet present. | `USER_CONFIRMATION_REQUIRED` |
| C-11 | Project did not receive disqualifying financial or preferential support from OpenAI or Devpost. | The entrant must confirm the full support history. Missing the optional free-credit allocation is not itself proof of this broader rule. | `USER_CONFIRMATION_REQUIRED` |

## C. Required submission materials

| ID | Official requirement | Neverlost evidence / action | Status |
| --- | --- | --- | --- |
| C-12 | Choose the best-aligned category. | Work & Productivity is frozen in the Stage 1 scope decision; it still must be selected on Devpost. | `PARTIAL_PACKAGING_REQUIRED` |
| C-13 | Include an English text description explaining features and functionality. | Stage 4 evidence supports the description. Devpost-ready copy has not yet been drafted. | `OPEN_ACTION` |
| C-14 | Include a public YouTube demonstration video under three minutes, with audio explaining what was built and how Codex and GPT-5.6 were used. | Storyboard exists at `demo/05_DEMO_SCRIPT_AND_VIDEO_STORYBOARD.md`. Recording, captions, upload, model-usage explanation, and signed-out playback test remain. | `OPEN_ACTION` |
| C-15 | Video uses no third-party trademarks, copyrighted music, or other material without permission. | Use repository-owned visuals, the approved NVLT mark, original narration, and no unlicensed music. Perform a final rights audit. | `OPEN_ACTION` |
| C-16 | Provide a judge-accessible repository URL: public with relevant licensing, or private and shared with both required addresses. | No repository URL or access mode is recorded. If private, share with `testing@devpost.com` and `build-week-event@openai.com`. | `OPEN_ACTION` |
| C-17 | README explains Codex collaboration, acceleration, key human decisions, and Codex/GPT-5.6 contributions. | The collaboration record now exists, but the current README does not yet contain the required submission narrative. | `PARTIAL_PACKAGING_REQUIRED` |
| C-18 | Provide the `/feedback` Codex Session ID for the thread where most core functionality was built. | Session ID has not been recorded in the repository or submission file. | `OPEN_ACTION` |
| C-19 | Plugins/dev tools include install instructions, supported platforms, and a judge test path that avoids rebuilding from scratch. | One-command demo and synthetic sample data exist. Installation steps, supported/tested platforms, and clean judge path require README expansion and verification. | `PARTIAL_PACKAGING_REQUIRED` |
| C-20 | Provide free, unrestricted working access for testing through the judging period. | Repository/demo access must remain available through August 5, 2026 at 5:00 p.m. Pacific Time; access mode has not yet been selected. | `OPEN_ACTION` |
| C-21 | Submission materials are in English or include English translations. | Repository, demonstration package, and planned submission materials are in English. | `VERIFIED_COMPLETE` |

## D. Neverlost-specific safety and submission integrity

| ID | Requirement / control | Neverlost evidence / action | Status |
| --- | --- | --- | --- |
| C-22 | Public materials contain no real client record, private appointment information, or unsupported third-party endorsement. | Stage 4 validation found zero real identifiers and zero prohibited endorsement or operational claims. Repeat the audit against the final video, screenshots, README, and Devpost copy. | `PARTIAL_PACKAGING_REQUIRED` |
| C-23 | Demonstrated results remain accurately labeled synthetic, governed, and review-only. | Stage 4 manifest and checkpoint preserve these boundaries. Maintain them in every submission surface. | `VERIFIED_COMPLETE` |
| C-24 | If Modern Paradox is also submitted, the two entries are unique and substantially different. | Separate repository, product identity, demo, narrative, and judging case are required. Modern Paradox remains outside this Neverlost submission lane. | `OPEN_ACTION` |

## Current readiness summary

- `VERIFIED_COMPLETE`: 3
- `PARTIAL_PACKAGING_REQUIRED`: 7
- `OPEN_ACTION`: 8
- `USER_CONFIRMATION_REQUIRED`: 6
- `NOT_APPLICABLE`: 0

No rule conflict was found that makes Neverlost ineligible on the current evidence. Submission is not yet compliance-ready because entrant confirmations, repository access/licensing, README requirements, the `/feedback` Session ID, the video, final rights/privacy review, and Devpost assembly remain open.

## Entrant confirmations to capture

1. Age-of-majority and eligible-country confirmation.
2. Individual versus team/organization entrant status and representative authority.
3. Ownership and rights confirmation.
4. Financial/preferential-support confirmation.
5. Devpost registration status.
6. GPT-5.6 use confirmation from the project session or product metadata.
7. Public versus private repository decision.
8. `/feedback` Codex Session ID.

## Exit gate

`NEVERLOST_BUILD_WEEK_COMPLIANCE_READY_FOR_FINAL_SUBMISSION_QA`

Pass only when every `OPEN_ACTION`, `PARTIAL_PACKAGING_REQUIRED`, and `USER_CONFIRMATION_REQUIRED` item has evidence or an explicit, rule-consistent disposition.
