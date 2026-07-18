# Neverlost: The Full Human Pathway

**A governed, capacity-aware Codex workflow for turning scattered human reality into evidence-aligned action.**

[![Track: Work & Productivity](https://img.shields.io/badge/Track-Work%20%26%20Productivity-1769AA)](#build-week-submission)
[![Data: Synthetic only](https://img.shields.io/badge/Data-Synthetic%20only-1B7F4B)](#boundaries-and-limitations)
[![Tests: 6 passing](https://img.shields.io/badge/Tests-6%20passing-1B7F4B)](#validated-result)

Neverlost is an OpenAI Build Week project that combines three reusable Codex skills with structured synthetic data, deterministic validation, governed checkpoints, and a reproducible judge demonstration. It is designed for work where a polished summary is not enough: source authority, uncertainty, human capacity, accommodations, recovery cost, and cross-system responsibility must remain visible.

## Judge quickstart

No API key, internet connection, package installation, or real record is required.

### macOS or Linux

```bash
git clone <PRIVATE_REPOSITORY_URL>
cd neverlost-build-week
python3 scripts/run_stage4_demo.py
```

### Windows PowerShell

```powershell
git clone <PRIVATE_REPOSITORY_URL>
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

Start with [`demo/README.md`](demo/README.md) for the judge-facing tour. Full reproduction and validation commands are in [`demo/07_REPRODUCIBILITY_GUIDE.md`](demo/07_REPRODUCIBILITY_GUIDE.md).

## The problem

AI can turn scattered records into a confident-looking answer while silently converting:

- a person's goal into proof of present capacity;
- an observation into a professional conclusion;
- general information into a personal guarantee;
- a possible service into an approval; or
- visible output into sustainable work without recording the conditions and recovery cost behind it.

Neverlost makes those transformations reviewable before the output reaches a human decision-maker.

## What the project does

The plugin combines three reusable skills:

1. **Neverlost governed review** — preserves source custody, separates evidence from guidance, checks role boundaries, controls revisions, and records approval gates.
2. **Full Human Pathway** — maps coordinated next steps across medical, daily-living, vocational, benefits, financial, and other relevant lanes without assigning authority the workflow does not have.
3. **Capacity & Output** — records useful output together with the conditions, supports, variability, interruption cost, and recovery cost required to produce it.

The Build Week implementation adds machine-readable schemas, two deliberately flawed synthetic cases, a generalized workflow runner, validators, a frozen defect scorer, negative tests, governed patch history, and an eleven-file demonstration package.

## Validated result

The first synthetic case established the pipeline. A distinct second case introduced seven records across different authority types and ten unsafe transformations. Its answer key and retest protocol were frozen before the generalized runner was executed.

| Measure | Result |
| --- | ---: |
| Deliberate defects detected and corrected | 10 / 10 |
| Finding classifications matched | 10 / 10 |
| Critical false positives | 0 |
| Packet checks | 24 / 24 |
| Qualitative gates | 12 / 12 |
| Unit tests | 6 / 6 |
| Governed human-review patch cycles | 1 |
| Real identifiers | 0 |
| Prohibited conclusions retained | 0 |

Human inspection found a separate measurement-fidelity issue after the baseline passed: client activity and an occupational-therapy simulation had been combined in one capacity observation. The workflow preserved the passing baseline, logged the finding, patched reusable logic, and reran the suite. The correction is part of the evidence, not hidden from it.

## Build Week submission

- **Track:** Work & Productivity
- **Project type:** Codex plugin, reusable skills, governed workflow, and deterministic demonstration tool
- **Model confirmed for the core project thread:** GPT-5.6 Sol
- **Repository access:** private judge repository
- **Data:** synthetic only
- **Submission boundary:** contest packaging is separate from the frozen Stage 1–4 evidence

### What existed before Build Week

- the Neverlost governed-review method and review model;
- the Full Human Pathway concept;
- the Capacity & Output concept; and
- the Neverlost identity and blue/white visual direction.

### What was meaningfully added during Build Week

- the installable plugin structure and three packaged skills;
- seven data contracts and two synthetic case systems;
- generalized workflow, validation, scoring, negative tests, and regressions;
- frozen baseline and governed correction history;
- one-command demonstration and judge evidence package; and
- submission compliance, development-delta, and reproducibility records.

The detailed origin and commit evidence is recorded in [`submission/BUILD_WEEK_DELTA_AND_CODEX_COLLABORATION_RECORD.md`](submission/BUILD_WEEK_DELTA_AND_CODEX_COLLABORATION_RECORD.md).

## How Codex and GPT-5.6 Sol were used

Codex with GPT-5.6 Sol helped inspect and organize the source framework, scaffold the plugin and schemas, implement the synthetic workflow, write validators and tests, run and diagnose the distinct-case retest, apply a bounded reusable correction, and produce the technical and judge-facing evidence package.

Codex also accelerated repetitive work that normally creates significant physical strain: repository inspection, structured drafting, consistency checks, test execution, formatting, and documentation. The result was not simply faster output; it reduced the amount of manual repetition required to preserve a rigorous evidence trail.

### Decisions retained by the creator

Jeff Summerhays / Neverlost controlled the central product and governance decisions, including:

- the Full Human Pathway as the organizing framework;
- recovery cost and variability as necessary parts of capacity evidence;
- separation of user report, record evidence, Neverlost synthesis, and third-party authority;
- preservation of the first distinct-case run before scoring or correction;
- use of deliberate defects to make safety behavior measurable;
- the human-review patch as visible governance evidence;
- vocational relevance without counselor, agency, provider, employer, or funding endorsement; and
- separation of Neverlost from the Modern Paradox Studio project.

The core Codex Session ID is retained privately for the required Devpost field and is intentionally not published here.

## Installation and supported platforms

### Judge test path — recommended

The demonstration is a Python standard-library project. Clone the repository and run the quickstart command above; there is no build step and no dependency installation.

- **Required:** Python 3.10 or newer and Git
- **No API key:** required
- **No network after clone:** required
- **Current clean-test environment:** Linux x86_64 with Python 3.12.13
- **Supported command-line targets:** Windows, macOS, and Linux with Python 3.10+
- **Plugin surfaces:** local plugin installation is intended for the ChatGPT desktop app in Work mode or Codex, and for Codex CLI

Windows and macOS use only Python standard-library code, but the final Build Week clean-checkout verification recorded in this repository was performed on Linux. See [`docs/PLUGIN_INSTALLATION.md`](docs/PLUGIN_INSTALLATION.md) for optional local-plugin installation.

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
| `.codex-plugin/plugin.json` | Codex plugin manifest |
| `skills/` | Governed review, Full Human Pathway, and Capacity & Output skills |
| `schemas/` | Machine-readable data contracts |
| `fixtures/` | Synthetic cases and frozen defect specifications |
| `scripts/` | Workflow, validation, scoring, and demo runners |
| `tests/` | Positive, negative, regression, and clean-demo tests |
| `examples/` | Generated packets and preserved Stage 3 baseline evidence |
| `demo/` | Judge results, before/after evidence, architecture, storyboard, and reproducibility |
| `governance/` | Scope decisions, change logs, defect records, and checkpoints |
| `submission/` | Compliance, Build Week delta, and submission planning |

## Boundaries and limitations

Neverlost is a bounded, rule-based prototype operating on fictional records. It demonstrates governance patterns and deterministic behavior on the included cases. It does not:

- diagnose or provide medical, legal, benefits, or vocational advice;
- determine work capacity, eligibility, services, equipment, funding, or employment;
- contain real client records or private appointment information;
- establish counselor, provider, agency, employer, OpenAI, or Devpost endorsement;
- prove accuracy on unseen real records;
- authorize operational or real-client use; or
- replace human review or the authority of the responsible professional or agency.

The final human-facing status remains `READY_FOR_USER_REVIEW`.
