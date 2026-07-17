#!/usr/bin/env python3
"""Run the bounded Neverlost Build Week Stage 1 structure smoke test."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_SKILLS = {
    "neverlost-review-workflow",
    "full-human-pathway",
    "capacity-output",
}
SOURCE_HASHES = {
    "SKILL.md": "36c8e9bebe250bc4b494d1e928cd99538b92685079af752cdb36182fe419693d",
    "agents/openai.yaml": "6dab2b4eaf5b974a6b6488f7627861c6d2f891a6778223e5e8fbc5074b708b5d",
    "references/review-model.md": "488b9236e9e352cd0048b33e7c1738c13c2a965966b6f7a349c1bc2f740569d5",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        raise ValueError(f"missing YAML frontmatter: {path}")
    values: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            values[key.strip()] = value.strip()
    return values


def run() -> dict[str, object]:
    checks: list[dict[str, object]] = []

    def check(name: str, passed: bool, detail: str) -> None:
        checks.append({"name": name, "passed": passed, "detail": detail})

    required_paths = [
        ".codex-plugin/plugin.json",
        "skills/neverlost-review-workflow/SKILL.md",
        "skills/full-human-pathway/SKILL.md",
        "skills/capacity-output/SKILL.md",
        "fixtures/synthetic-intake/case-spec.json",
        "fixtures/expected-results/stage-1-gates.json",
        "governance/STAGE_1_SCOPE_DECISION.md",
        "governance/PRIOR_AND_BUILD_WEEK_WORK_LEDGER.md",
    ]
    missing = [path for path in required_paths if not (ROOT / path).is_file()]
    check("required_paths", not missing, "missing=" + repr(missing))

    manifest = json.loads((ROOT / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
    check("plugin_name", manifest.get("name") == "neverlost-build-week", str(manifest.get("name")))
    check("plugin_skills_path", manifest.get("skills") == "./skills/", str(manifest.get("skills")))

    discovered: set[str] = set()
    skill_errors: list[str] = []
    for skill_file in sorted((ROOT / "skills").glob("*/SKILL.md")):
        text = skill_file.read_text(encoding="utf-8")
        try:
            frontmatter = parse_frontmatter(skill_file)
        except ValueError as exc:
            skill_errors.append(str(exc))
            continue
        name = frontmatter.get("name", "")
        description = frontmatter.get("description", "")
        if not name or not description:
            skill_errors.append(f"missing name/description: {skill_file}")
        if "TODO" in text:
            skill_errors.append(f"placeholder remains: {skill_file}")
        discovered.add(name)
    check("skill_discovery", discovered == EXPECTED_SKILLS and not skill_errors, f"discovered={sorted(discovered)} errors={skill_errors}")

    snapshot_root = ROOT / "governance/source-snapshots/neverlost-review-workflow"
    hash_errors: list[str] = []
    for relative, expected in SOURCE_HASHES.items():
        target = snapshot_root / relative
        actual = sha256(target) if target.is_file() else "MISSING"
        if actual != expected:
            hash_errors.append(f"{relative}: {actual}")
    check("core_source_preserved", not hash_errors, "mismatches=" + repr(hash_errors))

    case = json.loads((ROOT / "fixtures/synthetic-intake/case-spec.json").read_text(encoding="utf-8"))
    check("synthetic_only", case.get("synthetic_only") is True, f"synthetic_only={case.get('synthetic_only')}")
    check("expected_status", case.get("expected_final_status") == "READY_FOR_USER_REVIEW", str(case.get("expected_final_status")))
    check("deliberate_defects", len(case.get("deliberate_defects", [])) >= 7, f"count={len(case.get('deliberate_defects', []))}")
    check("privacy_rules", len(case.get("privacy_rules", [])) >= 5, f"count={len(case.get('privacy_rules', []))}")

    passed = all(bool(item["passed"]) for item in checks)
    return {
        "stage": 1,
        "status": "PASS" if passed else "FAIL",
        "completion_status": "STAGE_1_FOUNDATION_READY_FOR_PROTOTYPE_BUILD" if passed else "STAGE_1_BLOCKED",
        "checks": checks,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", type=Path)
    args = parser.parse_args()
    result = run()
    output = json.dumps(result, indent=2) + "\n"
    if args.write_report:
        report_path = args.write_report if args.write_report.is_absolute() else ROOT / args.write_report
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(output, encoding="utf-8")
    print(output, end="")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
