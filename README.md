# Neverlost: The Full Human Pathway

**A governed, capacity-aware workflow for turning scattered human reality into evidence-aligned action without erasing uncertainty, source authority, or human review.**

[![OpenAI Build Week](https://img.shields.io/badge/OpenAI%20Build%20Week-Work%20%26%20Productivity-1769AA)](#build-week-history)
[![Data: Synthetic only](https://img.shields.io/badge/Data-Synthetic%20only-1B7F4B)](#boundaries-and-limitations)
[![Tests: 6 passing](https://img.shields.io/badge/Tests-6%20passing-1B7F4B)](#validated-prototype)

Neverlost: The Full Human Pathway is a prototype created for OpenAI Build Week. It combines three reusable workflow skills with structured synthetic data, deterministic validation, governed checkpoints, negative testing, and a reproducible demonstration.

The core design question is simple: **how can AI help organize complex human situations without silently turning observations into conclusions, possibilities into approvals, or visible output into proof of sustainable capacity?**

## Portfolio status

Build Week judging is complete. This repository now serves as a **portfolio and continued-development project**.

The exact submission-era state is preserved on the branch [`build-week-2026-submission-final`](https://github.com/Neverlost-AI/Neverlost-build-week/tree/build-week-2026-submission-final). Changes made to `main` after that snapshot are post-competition maintenance, security hardening, documentation, or future development and should not be interpreted as part of the original judged submission.

See [`POST_COMPETITION_STATUS.md`](POST_COMPETITION_STATUS.md) for the current repository boundary.

## Demo

- **Build Week demonstration:** [YouTube](https://youtu.be/5DefEcMeJ6w)
- **Full Human Pathway walkthrough:** [YouTube](https://youtu.be/7zIodESXarQ)
- **Historical six-frame project tour:** [Neverlost Build Week experience](https://neverlost-judge-experience.ivory-moon-9960.chatgpt.site)

All included case data used for technical validation is synthetic.

## Quickstart

No API key, package installation, external service, or real record is required.

### macOS or Linux

```bash
git clone https://github.com/Neverlost-AI/Neverlost-build-week.git
cd neverlost-build-week
python3 scripts/run_stage4_demo.py
```

### Windows PowerShell

```powershell
git clone https://github.com/Neverlost-AI/Neverlost-build-week.git
Set-Location neverlost-build-week
py -3 scripts/run_stage4_demo.py
```

Expected result:

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

For the full reproduction path, see [`demo/07_REPRODUCIBILITY_GUIDE.md`](demo/07_REPRODUCIBILITY_GUIDE.md).

## The problem

AI can produce a polished answer while quietly changing what the underlying evidence actually supports. In complex human systems, those changes can matter.

Examples include converting:

- a person's goal into proof of present capacity;
- an observation into a professional conclusion;
- general information into a personal guarantee;
- a possible service into an approval; or
- completed work into proof that the same work is sustainable without recording the conditions, supports, interruption cost, or recovery cost behind it.

Neverlost makes those transformations visible and reviewable before the output reaches a human decision-maker.

## What the project does

The prototype combines three reusable skills:

1. **Neverlost governed review** — preserves source custody, separates evidence from guidance, checks role boundaries, controls revisions, and records approval gates.
2. **Full Human Pathway** — maps coordinated next steps across medical, daily-living, vocational, benefits, financial, and other relevant lanes without assigning authority the workflow does not have.
3. **Capacity & Output** — records useful output together with the conditions, supports, variability, interruption cost, and recovery cost required to produce it.

The implementation adds machine-readable schemas, deliberately flawed synthetic cases, a generalized workflow runner, validators, a frozen defect scorer, negative tests, governed patch history, and a reproducible demonstration package.

## Validated prototype

The first synthetic case established the pipeline. A distinct second case introduced seven records across different authority types and ten deliberately unsafe transformations. Its answer key and retest protocol were frozen before the generalized runner was executed.

| Measure | Result |
| --- | ---: |
| Deliberate defects detected and corrected | 10 / 10 |
| Finding classifications matched | 10 / 10 |
| Critical false positives | 0 |
| Packet checks | 24 / 24 |
| Qualitative gates | 12 / 12 |
| Unit tests | 6 / 6 |
| Governed human-review patch cycles | 1 |
| Real identifiers in validated case package | 0 |
| Prohibited conclusions retained | 0 |

Human inspection also found a separate measurement-fidelity issue after the baseline passed: client activity and an occupational-therapy simulation had been combined in one capacity observation. The workflow preserved the passing baseline, logged the finding, patched reusable logic, and reran the suite. The correction remains visible as part of the evidence rather than being hidden by the final result.

## Design principles demonstrated

- **Preserve before you understand.** Source meaning and custody should survive synthesis.
- **Human authority remains explicit.** AI can organize, classify, flag, and propose; it does not inherit professional or institutional authority.
- **Uncertainty stays visible.** Unknown, proposed, observed, and approved are not interchangeable states.
- **Capacity is contextual.** Output should be interpreted together with the conditions and recovery cost required to produce it.
- **Corrections are evidence.** A governed patch history is more useful than pretending the first implementation was perfect.
- **Synthetic data first.** The repository demonstrates mechanics without requiring real client records.

## Build Week history

The project was originally submitted to **OpenAI Build Week** in the **Work & Productivity** track as a Codex plugin / reusable-skill workflow with deterministic validation.

### What predated the submission period

- the Neverlost governed-review method and review model;
- the Capacity & Output concept; and
- the Neverlost identity and visual direction.

### What was created or meaningfully extended during Build Week

- the Full Human Pathway concept and initial framework;
- the installable plugin structure and three packaged skills;
- seven data contracts and two synthetic case systems;
- generalized workflow, validation, scoring, negative tests, and regressions;
- frozen baseline and governed correction history;
- one-command demonstration and evidence package; and
- submission compliance, development-delta, and reproducibility records.

The detailed origin record is preserved in [`submission/BUILD_WEEK_DELTA_AND_CODEX_COLLABORATION_RECORD.md`](submission/BUILD_WEEK_DELTA_AND_CODEX_COLLABORATION_RECORD.md). Other files under `submission/` are retained as historical contest artifacts and may still contain judge-facing language that is no longer current operational guidance.

## How Codex and GPT-5.6 Sol were used

During the Build Week implementation, Codex with GPT-5.6 Sol helped inspect and organize the source framework, scaffold the plugin and schemas, implement the synthetic workflow, write validators and tests, diagnose the distinct-case retest, apply a bounded reusable correction, and produce technical documentation and demonstration evidence.

The creator retained the central product and governance decisions, including:

- the Full Human Pathway as the organizing framework;
- recovery cost and variability as necessary parts of capacity evidence;
- separation of user report, record evidence, Neverlost synthesis, and third-party authority;
- preservation of the first distinct-case run before scoring or correction;
- deliberate defects as a measurable safety test;
- visible human-review patch history; and
- explicit limits on vocational, medical, agency, employer, or funding authority.

The private Codex session identifier used for the historical submission was intentionally kept outside the repository.

## Installation and supported platforms

The demonstration uses the Python standard library and has no build step.

- **Required:** Python 3.10+ and Git
- **API key:** not required
- **Network after clone:** not required for the deterministic demonstration
- **Recorded clean-test environment:** Linux x86_64 with Python 3.12.13
- **Command-line targets:** Windows, macOS, and Linux with Python 3.10+

See [`docs/PLUGIN_INSTALLATION.md`](docs/PLUGIN_INSTALLATION.md) for the original optional plugin-installation path.

## Full validation

### macOS or Linux

```bash
python3 scripts/run_stage4_demo.py
python3 scripts/validate_stage4_package.py
python3 scripts/smoke_test.py
python3 -m unittest discover -s tests -v
```

### Windows PowerShell

```powershell
py -3 scripts/run_stage4_demo.py
py -3 scripts/validate_stage4_package.py
py -3 scripts/smoke_test.py
py -3 -m unittest discover -s tests -v
```

## Repository map

| Location | Purpose |
| --- | --- |
| `.codex-plugin/plugin.json` | Original Codex plugin manifest |
| `skills/` | Governed review, Full Human Pathway, and Capacity & Output skills |
| `schemas/` | Machine-readable data contracts |
| `fixtures/` | Synthetic cases and frozen defect specifications |
| `scripts/` | Workflow, validation, scoring, and demo runners |
| `tests/` | Positive, negative, regression, and clean-demo tests |
| `examples/` | Generated packets and preserved baseline evidence |
| `demo/` | Results, before/after evidence, architecture, storyboard, and reproducibility |
| `governance/` | Scope decisions, change logs, defect records, and checkpoints |
| `submission/` | Historical Build Week compliance and submission records |

## Related work

- [The Full Human Pathway](https://youtu.be/7zIodESXarQ) — a visual explanation of the whole-person coordination framework.
- [The Patient's Paradox](https://youtu.be/eST8JpADyYY) — lived-experience and philosophical context that influenced the broader Neverlost direction.

## Boundaries and limitations

Neverlost is a bounded prototype operating on fictional records. It demonstrates governance patterns and deterministic behavior on the included cases. It does not:

- diagnose or provide medical, legal, benefits, or vocational advice;
- determine work capacity, eligibility, services, equipment, funding, or employment;
- contain real client records or private appointment information in the validated demonstration package;
- establish counselor, provider, agency, employer, OpenAI, or Devpost endorsement;
- prove accuracy on unseen real records;
- authorize operational or real-client use; or
- replace human review or the authority of the responsible professional or institution.

The final human-facing workflow status remains `READY_FOR_USER_REVIEW`.

## Historical submission snapshot

For the exact repository state preserved after judging, use:

[`build-week-2026-submission-final`](https://github.com/Neverlost-AI/Neverlost-build-week/tree/build-week-2026-submission-final)
