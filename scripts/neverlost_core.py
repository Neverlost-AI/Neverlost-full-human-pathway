"""Deterministic builders and validation helpers for the Stage 2 prototype."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def validate_schema(data: Any, schema: dict[str, Any], location: str = "$") -> list[str]:
    """Validate the JSON-Schema subset used by this prototype."""
    errors: list[str] = []
    expected_type = schema.get("type")
    type_map = {
        "object": dict,
        "array": list,
        "string": str,
        "integer": int,
        "boolean": bool,
    }
    if expected_type in type_map and not isinstance(data, type_map[expected_type]):
        return [f"{location}: expected {expected_type}, got {type(data).__name__}"]

    if "const" in schema and data != schema["const"]:
        errors.append(f"{location}: expected constant {schema['const']!r}, got {data!r}")
    if "enum" in schema and data not in schema["enum"]:
        errors.append(f"{location}: {data!r} not in permitted values {schema['enum']!r}")

    if isinstance(data, dict):
        for key in schema.get("required", []):
            if key not in data:
                errors.append(f"{location}: missing required field {key!r}")
        for key, child_schema in schema.get("properties", {}).items():
            if key in data:
                errors.extend(validate_schema(data[key], child_schema, f"{location}.{key}"))

    if isinstance(data, list):
        minimum = schema.get("minItems")
        if minimum is not None and len(data) < minimum:
            errors.append(f"{location}: expected at least {minimum} items, got {len(data)}")
        item_schema = schema.get("items")
        if item_schema:
            for index, item in enumerate(data):
                errors.extend(validate_schema(item, item_schema, f"{location}[{index}]"))
    return errors


def build_intake(case_spec: dict[str, Any], sources: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "case_id": case_spec["case_id"],
        "synthetic_only": True,
        "person": case_spec["person"],
        "audience": case_spec["audience"],
        "real_question": case_spec["real_question"],
        "requested_action": case_spec["requested_action"],
        "authorized_source_ids": [source["id"] for source in sources],
        "exclusions": [
            "No medical, work-capacity, eligibility, funding, or employment conclusion.",
            "No real personal records or identifying information.",
            "No external distribution, endorsement, acceptance-test claim, or operational approval."
        ]
    }


def classify_sources(case_id: str, sources: list[dict[str, Any]]) -> dict[str, Any]:
    mapping = {
        "synthetic_provider_note": ("ORIGINAL_EVIDENCE", "PROVIDER_SOURCE", "CURRENT"),
        "synthetic_user_report": ("USER_REPORTED", "CLIENT", "CURRENT"),
        "synthetic_counselor_message": ("ORIGINAL_EVIDENCE", "COUNSELOR_SOURCE", "CURRENT"),
        "synthetic_prior_intake": ("USER_GUIDANCE", "CLIENT", "STALE_UNCONFIRMED"),
        "synthetic_draft_output": ("CANDIDATE_OUTPUT", "NEVERLOST_DRAFT", "CURRENT")
    }
    classified = []
    for source in sources:
        classification, authority, currency = mapping[source["type"]]
        classified.append({
            "id": source["id"],
            "type": source["type"],
            "date": source["date"],
            "classification": classification,
            "authority": authority,
            "currency": currency,
            "content": source["content"]
        })
    return {"case_id": case_id, "synthetic_only": True, "sources": classified}


def build_capacity_record(case_id: str) -> dict[str, Any]:
    return {
        "case_id": case_id,
        "observation_id": "CAP-001",
        "source_ids": ["S2"],
        "observation_window": {"date": "2026-07-15", "duration_minutes": 70},
        "output_achieved": "Completed one bounded document session.",
        "conditions": ["Reclined working position", "Single bounded session"],
        "accommodations": ["Adaptive keyboard", "Reclined setup"],
        "constraints": ["Increased symptoms after the session", "Most of the following day required for recovery"],
        "recovery_cost": {
            "immediate": "Increased symptoms after the session.",
            "delayed": "Most of the next day was spent recovering."
        },
        "repeatability": "NOT_YET_KNOWN",
        "bounded_interpretation": "The session demonstrates a useful output under specific accommodations once; it does not establish sustainable work capacity or work readiness.",
        "prohibited_conclusions_withheld": [
            "Full-time capacity",
            "Work readiness",
            "Disability status",
            "Sustainable employment"
        ]
    }


def build_pathway_plan(case_spec: dict[str, Any]) -> dict[str, Any]:
    lanes = [
        {
            "lane": "health_and_function",
            "stage": "1_STABILIZE",
            "current_purpose": "Protect recovery while clarifying what low-load preparation is workable.",
            "can_proceed_now": ["Use pacing and accessibility supports for bounded preparation."],
            "remains_premature": ["A durable or full-time work-capacity conclusion."],
            "review_trigger": "After another bounded observation or new provider guidance."
        },
        {
            "lane": "environment_and_accessibility",
            "stage": "2_ORGANIZE_AND_PREPARE",
            "current_purpose": "Identify which workspace supports reduce strain and what remains uncertain.",
            "can_proceed_now": ["Document the effect of the adaptive keyboard and reclined setup."],
            "remains_premature": ["Claiming that equipment removes the underlying limitation."],
            "review_trigger": "After repeated use under comparable conditions."
        },
        {
            "lane": "resources_and_capacity",
            "stage": "2_ORGANIZE_AND_PREPARE",
            "current_purpose": "Frame equipment and support needs for proper review.",
            "can_proceed_now": ["Prepare a bounded equipment question and supporting observation."],
            "remains_premature": ["Treating a discussion as approval or entitlement."],
            "review_trigger": "When the fictional counselor completes eligibility and planning review."
        },
        {
            "lane": "education_and_training",
            "stage": "3_TRAIN_AND_BUILD_EVIDENCE",
            "current_purpose": "Explore low-load skill development without assuming employment readiness.",
            "can_proceed_now": ["Define a small training trial with pacing and a recovery review."],
            "remains_premature": ["A full course load or employment timetable."],
            "review_trigger": "After one small training trial and recovery observation."
        },
        {
            "lane": "vocational_rehabilitation",
            "stage": "2_ORGANIZE_AND_PREPARE",
            "current_purpose": "Prepare questions for the proper vocational authority.",
            "can_proceed_now": ["Discuss training and equipment supports after eligibility review."],
            "remains_premature": ["Funding, service, eligibility, or employment claims."],
            "review_trigger": "After the fictional counselor issues an actual decision."
        }
    ]
    bridges = [
        {
            "bridge_id": "BR-001",
            "need_or_opportunity": "Accessible equipment may reduce strain during bounded document work.",
            "desired_outcome": "A properly reviewed accessibility-support question.",
            "responsible_lane": "environment_and_accessibility",
            "proper_authority": "Fictional vocational counselor or agency after eligibility and planning review",
            "source_ids": ["S2", "S4"],
            "missing_information": ["Eligibility decision", "Equipment assessment", "Funding criteria"],
            "next_bounded_action": "Prepare the observation and ask what assessment or documentation is required.",
            "dependency": "No funding claim until the proper authority decides.",
            "owner": "Rowan for preparation; fictional counselor for agency decision",
            "status": "AWAITING_EXTERNAL_DECISION",
            "review_trigger": "Receipt of a fictional written agency decision."
        },
        {
            "bridge_id": "BR-002",
            "need_or_opportunity": "Low-load training may build evidence without requiring immediate employment.",
            "desired_outcome": "One paced training trial with output and recovery recorded.",
            "responsible_lane": "education_and_training",
            "proper_authority": "Rowan, with provider and vocational guidance where applicable",
            "source_ids": ["S1", "S2"],
            "missing_information": ["Tolerable duration", "Delayed recovery pattern", "Repeatability"],
            "next_bounded_action": "Define one small training task and a next-day recovery check.",
            "dependency": "The trial must remain within the current pacing boundary.",
            "owner": "Rowan",
            "status": "DRAFT",
            "review_trigger": "Completion of the first paced training observation."
        },
        {
            "bridge_id": "BR-003",
            "need_or_opportunity": "A stale full-time goal must be replaced with a current client-confirmed direction.",
            "desired_outcome": "A current vocational direction that does not overstate capacity.",
            "responsible_lane": "vocational_rehabilitation",
            "proper_authority": "Rowan defines the goal; the fictional counselor determines agency planning decisions",
            "source_ids": ["S3"],
            "missing_information": ["Current goal confirmation", "Preferred conditions", "Acceptable pace"],
            "next_bounded_action": "Confirm or revise the old goal before using it in a vocational packet.",
            "dependency": "Client confirmation is required before sharing the goal as current.",
            "owner": "Rowan",
            "status": "DRAFT",
            "review_trigger": "Client review of the synthetic pathway packet."
        }
    ]
    return {
        "case_id": case_spec["case_id"],
        "status": "READY_FOR_USER_REVIEW",
        "client_direction": case_spec["person"]["life_direction"],
        "lanes": lanes,
        "bridges": bridges,
        "minimum_necessary_sharing": "Share only the current goal, relevant observations, bounded questions, and explicit authority boundaries needed for the fictional vocational discussion.",
        "next_authorized_step": "Human review of the synthetic packet before any distinct-case retest.",
        "still_unauthorized": [
            "Real-client use",
            "Funding or eligibility claims",
            "Work-capacity conclusions",
            "External distribution",
            "Operational use"
        ]
    }


def build_findings(case_spec: dict[str, Any]) -> dict[str, Any]:
    findings = [
        {
            "defect_id": "stale_goal_presented_as_current",
            "classification": "REVISION_REQUIRED",
            "source_ids": ["S3", "S5"],
            "issue": "A 2025 full-time goal was not reconfirmed and cannot be presented as current.",
            "disposition": "Label the old goal stale and require client confirmation before use.",
            "corrected": True
        },
        {
            "defect_id": "short_output_session_treated_as_sustainable_capacity",
            "classification": "REVISION_RECOMMENDED",
            "source_ids": ["S2", "S5"],
            "issue": "One 70-minute accommodated session was generalized into durable capacity.",
            "disposition": "Describe the session as observed once with repeatability unknown.",
            "corrected": True
        },
        {
            "defect_id": "provider_note_overstated_into_work_readiness",
            "classification": "REVISION_REQUIRED",
            "source_ids": ["S1", "S5"],
            "issue": "Permission to explore low-load training does not establish work readiness.",
            "disposition": "Remove the unsupported readiness conclusion and preserve the provider note's limit.",
            "corrected": True
        },
        {
            "defect_id": "counselor_discussion_overstated_into_funding_approval",
            "classification": "REVISION_REQUIRED",
            "source_ids": ["S4", "S5"],
            "issue": "A possible future discussion was converted into a funding promise.",
            "disposition": "Frame equipment as a question awaiting the fictional agency's decision.",
            "corrected": True
        },
        {
            "defect_id": "equipment_question_softening",
            "classification": "REVISION_RECOMMENDED",
            "source_ids": ["S2", "S4"],
            "issue": "Even after removing the funding promise, the equipment need should be presented as a bounded accessibility question rather than an entitlement.",
            "disposition": "Ask what assessment or documentation the proper authority requires and preserve the pending-decision status.",
            "corrected": True
        },
        {
            "defect_id": "draft_status_incorrectly_collapsed_into_approved",
            "classification": "REVISION_REQUIRED",
            "source_ids": ["S5"],
            "issue": "The candidate draft was labeled APPROVED without human or external authority.",
            "disposition": "Set the revised packet to READY_FOR_USER_REVIEW.",
            "corrected": True
        },
        {
            "defect_id": "recovery_cost_omitted_from_capacity_interpretation",
            "classification": "REVISION_REQUIRED",
            "source_ids": ["S2", "S5"],
            "issue": "The draft omitted the increased symptoms and next-day recovery cost.",
            "disposition": "Restore immediate and delayed recovery cost to the capacity record.",
            "corrected": True
        },
        {
            "defect_id": "source_types_blended_without_attribution",
            "classification": "REVISION_REQUIRED",
            "source_ids": ["S1", "S2", "S3", "S4", "S5"],
            "issue": "The draft blended provider, client, counselor, historical, and derived statements.",
            "disposition": "Classify every source and cite source IDs in derived records.",
            "corrected": True
        },
        {
            "defect_id": "accessible_direction_preserved",
            "classification": "ACCEPTABLE_AS_WRITTEN",
            "source_ids": [],
            "issue": "The client-defined direction toward accessible research-support or documentation work is bounded as a goal.",
            "disposition": "Preserve as client direction, not a capacity or employment conclusion.",
            "corrected": True
        },
        {
            "defect_id": "low_load_preparation_preserved",
            "classification": "ACCEPTABLE_AS_WRITTEN",
            "source_ids": ["S1"],
            "issue": "Exploring low-load preparation with pacing stays within the source boundary.",
            "disposition": "Preserve with recovery monitoring and no readiness claim.",
            "corrected": True
        }
    ]
    counts = {
        "revision_required": sum(item["classification"] == "REVISION_REQUIRED" for item in findings),
        "revision_recommended": sum(item["classification"] == "REVISION_RECOMMENDED" for item in findings),
        "acceptable_as_written": sum(item["classification"] == "ACCEPTABLE_AS_WRITTEN" for item in findings)
    }
    return {
        "case_id": case_spec["case_id"],
        "status": "REVIEW_COMPLETED_REVISION_REQUIRED",
        "findings": findings,
        "counts": counts
    }


def build_revised_output(case_spec: dict[str, Any]) -> str:
    return f"""# Synthetic Vocational-Planning Bridge Summary

Status: `READY_FOR_USER_REVIEW`  
Case: `{case_spec['case_id']}`  
Data boundary: Synthetic-only demonstration

## Current direction

{case_spec['person']['display_name']} describes a direction toward accessible research-support or documentation work while protecting health and daily stability. This is a client-defined direction, not a work-capacity or employment conclusion.

## Current evidence

- A synthetic provider note supports exploring low-load training with pacing and accessibility supports; it offers no opinion on full-time work capacity. [S1]
- One synthetic user report records a 70-minute document session using an adaptive keyboard and reclined setup, followed by increased symptoms and most of the next day spent recovering. Repeatability is not yet known. [S2]
- A prior full-time goal is stale and has not been reconfirmed. [S3]
- A synthetic counselor message says equipment and training supports may be discussed only after eligibility and planning review; no service or funding decision exists. [S4]

## What may proceed now

1. Confirm or revise the old vocational goal.
2. Record another small, paced activity with same-day and next-day recovery effects.
3. Prepare a bounded accessibility-equipment question and ask what assessment or documentation the proper authority would require.
4. Explore one low-load training task without setting an employment timetable.

## What remains premature

- Any conclusion about full-time or sustainable work capacity.
- Any claim of vocational eligibility, service approval, equipment funding, or employment.
- Treating one successful session as repeatable capacity.
- Sharing the packet outside the synthetic demonstration.

## Next review trigger

Human review of this synthetic packet, followed—only if separately authorized—by a distinct synthetic case retest.
"""


def build_change_log() -> str:
    return """# FHP-SYNTH-001 Controlled Change Log

Status: `REVISIONS_COMPLETED_FOR_REVIEW`

## Changes applied

- Replaced the unsupported `APPROVED` label with `READY_FOR_USER_REVIEW`.
- Removed the unsupported full-time work-readiness conclusion.
- Removed the unsupported computer-funding promise.
- Labeled the old full-time goal stale and unconfirmed.
- Restored the accommodation conditions and immediate/delayed recovery cost.
- Separated provider, client, counselor, historical, and draft sources.
- Converted equipment funding into a bounded question for the proper authority.
- Preserved the accessible vocational direction and low-load preparation language within their source limits.

## Untouched boundaries

- No diagnosis, eligibility, funding, employment, or work-capacity decision was created.
- No real personal information was introduced.
- No acceptance-test or operational-use claim was made.
"""


def build_checkpoint(case_spec: dict[str, Any]) -> dict[str, Any]:
    return {
        "artifact": "FHP-SYNTH-001 synthetic governed review packet",
        "case_id": case_spec["case_id"],
        "as_of": "2026-07-17",
        "timezone": "America/Denver",
        "status": "READY_FOR_USER_REVIEW",
        "source_set": ["S1", "S2", "S3", "S4", "S5"],
        "reviews_completed": [
            "Authority and source-set review",
            "Role and boundary review",
            "Current-facts and evidence review",
            "Substantive alignment review",
            "Controlled revision and version review",
            "Deterministic privacy and status validation"
        ],
        "changes_made": [
            "Corrected status, work-readiness, funding, staleness, recovery-cost, and attribution defects.",
            "Created capacity context, pathway stages, bridge records, findings, and bounded revision."
        ],
        "boundaries_preserved": [
            "Synthetic information only.",
            "No medical, work-capacity, eligibility, funding, or employment decision.",
            "No third-party approval, endorsement, acceptance-test pass, or operational approval."
        ],
        "known_gaps": [
            "No distinct-case retest has occurred.",
            "The prototype is deterministic and bounded to FHP-SYNTH-001.",
            "No marketplace installation or real-world use has been authorized."
        ],
        "next_authorized_step": "Human review of this Stage 2 synthetic output before authorizing a distinct synthetic retest.",
        "still_unauthorized": [
            "Real-client use",
            "External distribution",
            "Marketplace or public release",
            "Acceptance-test claim",
            "Operational use"
        ]
    }
