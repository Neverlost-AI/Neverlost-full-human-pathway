"""Case-neutral deterministic builders and validation helpers for Neverlost."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


SOURCE_RULES: dict[str, tuple[str, str, str]] = {
    "synthetic_provider_note": ("ORIGINAL_EVIDENCE", "PROVIDER_SOURCE", "CURRENT"),
    "synthetic_user_report": ("USER_REPORTED", "CLIENT", "CURRENT"),
    "synthetic_counselor_message": ("ORIGINAL_EVIDENCE", "COUNSELOR_SOURCE", "CURRENT"),
    "synthetic_prior_intake": ("USER_GUIDANCE", "CLIENT", "STALE_UNCONFIRMED"),
    "synthetic_occupational_therapy_note": ("ORIGINAL_EVIDENCE", "OCCUPATIONAL_THERAPY_SOURCE", "CURRENT"),
    "synthetic_prior_employment_plan": ("ORIGINAL_EVIDENCE", "EMPLOYMENT_PLAN_SOURCE", "STALE_UNCONFIRMED"),
    "synthetic_vocational_rehabilitation_message": ("ORIGINAL_EVIDENCE", "VOCATIONAL_REHABILITATION_SOURCE", "CURRENT"),
    "synthetic_benefits_information_note": ("ORIGINAL_EVIDENCE", "BENEFITS_INFORMATION_SOURCE", "CURRENT"),
    "synthetic_draft_output": ("CANDIDATE_OUTPUT", "NEVERLOST_DRAFT", "CURRENT"),
}

SOURCE_LABELS = {
    "synthetic_provider_note": "Provider note",
    "synthetic_user_report": "Client report",
    "synthetic_counselor_message": "Vocational counselor message",
    "synthetic_prior_intake": "Prior intake",
    "synthetic_occupational_therapy_note": "Occupational-therapy observation",
    "synthetic_prior_employment_plan": "Prior employment plan",
    "synthetic_vocational_rehabilitation_message": "Vocational-rehabilitation message",
    "synthetic_benefits_information_note": "Benefits information",
    "synthetic_draft_output": "Candidate draft",
}


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


def sources_of_type(sources: list[dict[str, Any]], source_type: str) -> list[dict[str, Any]]:
    return [source for source in sources if source["type"] == source_type]


def first_source(sources: list[dict[str, Any]], source_type: str) -> dict[str, Any] | None:
    matches = sources_of_type(sources, source_type)
    return matches[0] if matches else None


def source_ids(sources: list[dict[str, Any]], *source_types: str) -> list[str]:
    permitted = set(source_types)
    return [source["id"] for source in sources if source["type"] in permitted]


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
            "No medical, work-capacity, eligibility, benefits, equipment, funding, or employment conclusion.",
            "No real personal records or identifying information.",
            "No external distribution, endorsement, acceptance-test claim, or operational approval.",
        ],
    }


def classify_sources(case_id: str, sources: list[dict[str, Any]]) -> dict[str, Any]:
    classified = []
    for source in sources:
        if source["type"] not in SOURCE_RULES:
            raise ValueError(f"Unsupported source type: {source['type']}")
        classification, authority, currency = SOURCE_RULES[source["type"]]
        classified.append(
            {
                "id": source["id"],
                "type": source["type"],
                "date": source["date"],
                "classification": classification,
                "authority": authority,
                "currency": currency,
                "content": source["content"],
            }
        )
    return {"case_id": case_id, "synthetic_only": True, "sources": classified}


def _mentioned_accommodations(text: str) -> list[str]:
    candidates = [
        ("adaptive keyboard", "Adaptive keyboard"),
        ("reclined setup", "Reclined setup"),
        ("split keyboard", "Split keyboard"),
        ("vertical mouse", "Vertical mouse"),
        ("dictation", "Dictation"),
    ]
    lowered = text.lower()
    return [label for phrase, label in candidates if phrase in lowered]


def build_capacity_record(case_id: str, sources: list[dict[str, Any]]) -> dict[str, Any]:
    user = first_source(sources, "synthetic_user_report")
    if user is None:
        raise ValueError("A synthetic_user_report is required to build capacity context")
    ot = first_source(sources, "synthetic_occupational_therapy_note")
    combined = " ".join(source["content"] for source in [user, ot] if source)
    durations = [int(value) for value in re.findall(r"\b(\d+)-minute\b", combined, flags=re.IGNORECASE)]
    longest = max(durations) if durations else 1
    separate_observations = len(durations) > 1 or "separate day" in user["content"].lower()

    if separate_observations:
        output = f"Reported {len(durations)} separate computer-task observations; the longest recorded period was {longest} minutes."
    else:
        output = f"Reported one bounded computer or document-task observation lasting {longest} minutes."

    conditions = ["Synthetic self-reported observation"]
    if separate_observations:
        conditions.append("Activities occurred on separate days")
    if "consecutive-day" in combined.lower():
        conditions.append("Consecutive-day performance was not tested")

    accommodations = _mentioned_accommodations(combined) or ["Pacing and breaks"]
    constraints = ["The observation does not establish a sustainable work schedule"]
    if "recovery" in user["content"].lower():
        constraints.append("Recovery time varied after the reported activity")
    if "consecutive-day" in user["content"].lower():
        constraints.append("Repeatability across consecutive days is unknown")

    if "one to three hours" in user["content"].lower():
        immediate = "Recovery took one to three hours after the shorter reported periods."
    elif "increased symptoms" in user["content"].lower():
        immediate = "Increased symptoms were reported after the activity."
    else:
        immediate = "Immediate recovery cost was not fully quantified."

    if "remainder of the day" in user["content"].lower():
        delayed = "The remainder of the day was required after the longest reported period; consecutive-day performance was not tested."
    elif "next day" in user["content"].lower():
        delayed = "Most of the next day was reportedly required for recovery."
    else:
        delayed = "Delayed and consecutive-day recovery remain unverified."

    record_source_ids = [user["id"]]
    if ot:
        record_source_ids.append(ot["id"])
    return {
        "case_id": case_id,
        "observation_id": "CAP-001",
        "source_ids": record_source_ids,
        "observation_window": {"date": user["date"], "duration_minutes": longest},
        "output_achieved": output,
        "conditions": conditions,
        "accommodations": accommodations,
        "constraints": constraints,
        "recovery_cost": {"immediate": immediate, "delayed": delayed},
        "repeatability": "VARIABLE" if separate_observations else "NOT_YET_KNOWN",
        "bounded_interpretation": "These observations show bounded activity under stated conditions. They do not establish medical clearance, sustainable weekly capacity, work readiness, or employment readiness.",
        "prohibited_conclusions_withheld": [
            "Medical clearance",
            "Sustainable weekly capacity",
            "Work readiness",
            "Employment readiness",
            "Disability or benefits status",
        ],
    }


def _lane(
    name: str,
    stage: str,
    purpose: str,
    can_proceed: str,
    premature: str,
    trigger: str,
) -> dict[str, Any]:
    return {
        "lane": name,
        "stage": stage,
        "current_purpose": purpose,
        "can_proceed_now": [can_proceed],
        "remains_premature": [premature],
        "review_trigger": trigger,
    }


def build_pathway_plan(case_spec: dict[str, Any], sources: list[dict[str, Any]]) -> dict[str, Any]:
    has_benefits = first_source(sources, "synthetic_benefits_information_note") is not None
    has_ot = first_source(sources, "synthetic_occupational_therapy_note") is not None
    has_vr = first_source(sources, "synthetic_vocational_rehabilitation_message") is not None
    has_variable_recovery = "consecutive-day" in " ".join(source["content"].lower() for source in sources)

    lanes = [
        _lane(
            "health_and_function",
            "1_STABILIZE",
            "Protect recovery while clarifying tolerable bounded activity.",
            "Continue small paced observations within existing guidance.",
            "Medical clearance or a durable work-capacity conclusion.",
            "After another bounded observation or new provider guidance.",
        ),
        _lane(
            "environment_and_accessibility",
            "2_ORGANIZE_AND_PREPARE",
            "Identify which access supports reduce strain and what remains untested.",
            "Document observed effects and prepare an evaluation question.",
            "Treating one trial as proof, prescription, entitlement, or long-term effectiveness.",
            "After a repeated or take-home trial reviewed by the proper authority.",
        ),
    ]
    if has_variable_recovery:
        lanes.append(
            _lane(
                "daily_life_and_recovery",
                "1_STABILIZE",
                "Keep activity, recovery, and daily stability visible together.",
                "Record same-day, delayed, and consecutive-day effects.",
                "Converting separate observations into a sustainable schedule.",
                "After comparable observations include consecutive-day recovery.",
            )
        )
    lanes.append(
        _lane(
            "resources_and_benefits" if has_benefits else "resources_and_capacity",
            "2_ORGANIZE_AND_PREPARE",
            "Route resource questions to the authority that can make the decision.",
            "Prepare bounded equipment, service, or benefits questions.",
            "Eligibility, benefits continuity, service, equipment, or funding promises.",
            "After a written decision from the relevant program authority.",
        )
    )
    lanes.extend(
        [
            _lane(
                "education_and_training",
                "3_TRAIN_AND_BUILD_EVIDENCE",
                "Explore low-load skill development without assuming employment readiness.",
                "Define one paced training task and review its recovery cost.",
                "A course load, weekly schedule, or employment timetable.",
                "After one bounded training observation and recovery review.",
            ),
            _lane(
                "vocational_rehabilitation",
                "2_ORGANIZE_AND_PREPARE",
                "Prepare questions for the proper vocational authority.",
                "Clarify eligibility, evaluation, planning, and documentation steps.",
                "A service, vendor, training, equipment, funding, or employment decision.",
                "After the fictional vocational authority issues a written decision.",
            ),
        ]
    )

    owner = case_spec["person"]["display_name"]
    user_ids = source_ids(sources, "synthetic_user_report")
    provider_ids = source_ids(sources, "synthetic_provider_note")
    ot_ids = source_ids(sources, "synthetic_occupational_therapy_note")
    vr_ids = source_ids(sources, "synthetic_counselor_message", "synthetic_vocational_rehabilitation_message")
    stale_ids = source_ids(sources, "synthetic_prior_intake", "synthetic_prior_employment_plan")
    benefits_ids = source_ids(sources, "synthetic_benefits_information_note")

    bridges: list[dict[str, Any]] = []

    def add_bridge(
        need: str,
        outcome: str,
        lane: str,
        authority: str,
        ids: list[str],
        missing: list[str],
        action: str,
        dependency: str,
        bridge_owner: str,
        status: str,
        trigger: str,
    ) -> None:
        bridges.append(
            {
                "bridge_id": f"BR-{len(bridges) + 1:03d}",
                "need_or_opportunity": need,
                "desired_outcome": outcome,
                "responsible_lane": lane,
                "proper_authority": authority,
                "source_ids": ids,
                "missing_information": missing,
                "next_bounded_action": action,
                "dependency": dependency,
                "owner": bridge_owner,
                "status": status,
                "review_trigger": trigger,
            }
        )

    add_bridge(
        "Observed computer activity needs repeatability and recovery context.",
        "A bounded observation record that does not imply a work schedule.",
        "daily_life_and_recovery" if has_variable_recovery else "health_and_function",
        f"{owner} for self-report; provider for medical guidance",
        user_ids + provider_ids,
        ["Consecutive-day performance", "Delayed recovery pattern", "Repeatability"],
        "Record one comparable paced activity with same-day and next-day effects.",
        "No weekly-capacity claim until adequate evidence and proper review exist.",
        owner,
        "DRAFT",
        "Completion of another comparable observation.",
    )
    if has_ot or any("equipment" in source["content"].lower() for source in sources):
        add_bridge(
            "Assistive technology may reduce strain under specific conditions.",
            "A properly reviewed evaluation or trial question.",
            "environment_and_accessibility",
            "Occupational-therapy authority for functional evaluation; vocational authority for any service or funding decision",
            ot_ids + user_ids + vr_ids,
            ["Repeated or take-home trial", "Longer-term fit", "Eligibility and funding criteria"],
            "Ask what evaluation, trial, or documentation is required.",
            "Observation does not equal prescription, approval, entitlement, or funding.",
            f"{owner} for preparation; external authorities for their decisions",
            "AWAITING_EXTERNAL_DECISION",
            "Receipt of a written evaluation or agency decision.",
        )
    if stale_ids:
        add_bridge(
            "A stale vocational plan requires current client confirmation.",
            "A current direction that stays separate from capacity conclusions.",
            "vocational_rehabilitation",
            "Client for goal direction; vocational authority for agency planning decisions",
            stale_ids + user_ids,
            ["Current goal confirmation", "Preferred conditions", "Acceptable pace"],
            "Confirm, revise, or retire the old plan before presenting it as current.",
            "Stale evidence cannot establish present readiness.",
            owner,
            "DRAFT",
            "Client review of the synthetic pathway packet.",
        )
    if has_vr:
        add_bridge(
            "Training or assistive-technology services may be considered.",
            "A properly sequenced vocational-rehabilitation question.",
            "vocational_rehabilitation",
            "Fictional vocational-rehabilitation agency",
            vr_ids,
            ["Eligibility decision", "Individualized plan", "Service criteria"],
            "Ask which eligibility and planning steps precede any service decision.",
            "Possible consideration is not approval.",
            "Fictional vocational authority",
            "AWAITING_EXTERNAL_DECISION",
            "Receipt of a written eligibility or planning decision.",
        )
    if benefits_ids:
        add_bridge(
            "Possible earned income creates an individualized benefits-information question.",
            "Accurate case-specific reporting guidance from the proper program authority.",
            "resources_and_benefits",
            "Authorized benefits-program representative",
            benefits_ids + user_ids,
            ["Applicable program rules", "Individualized calculation", "Reporting timeline"],
            "Prepare the question and request program-specific guidance.",
            "Generic information cannot guarantee benefits continuity.",
            f"{owner} for the question; program authority for the decision",
            "AWAITING_EXTERNAL_DECISION",
            "Receipt of individualized written program guidance.",
        )

    return {
        "case_id": case_spec["case_id"],
        "status": "READY_FOR_USER_REVIEW",
        "client_direction": case_spec["person"]["life_direction"],
        "lanes": lanes,
        "bridges": bridges,
        "minimum_necessary_sharing": "Share only the current client direction, relevant source-attributed observations, bounded questions, and authority limits needed for the synthetic review.",
        "next_authorized_step": "Human review of the synthetic packet before any further test or use.",
        "still_unauthorized": [
            "Real-client use",
            "Medical or work-capacity conclusions",
            "Eligibility, benefits, service, equipment, or funding claims",
            "External distribution",
            "Operational use",
        ],
    }


def _finding(
    defect_id: str,
    classification: str,
    ids: list[str],
    issue: str,
    disposition: str,
) -> dict[str, Any]:
    return {
        "defect_id": defect_id,
        "classification": classification,
        "source_ids": ids,
        "issue": issue,
        "disposition": disposition,
        "corrected": True,
    }


def _legacy_findings(sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        _finding("stale_goal_presented_as_current", "REVISION_REQUIRED", source_ids(sources, "synthetic_prior_intake", "synthetic_draft_output"), "A stale goal was presented as current readiness evidence.", "Label the goal stale and require current client confirmation."),
        _finding("short_output_session_treated_as_sustainable_capacity", "REVISION_RECOMMENDED", source_ids(sources, "synthetic_user_report", "synthetic_draft_output"), "One bounded activity was generalized into sustainable capacity.", "Keep the observation bounded and repeatability unknown."),
        _finding("provider_note_overstated_into_work_readiness", "REVISION_REQUIRED", source_ids(sources, "synthetic_provider_note", "synthetic_draft_output"), "Limited provider guidance was converted into work readiness.", "Remove the readiness claim and preserve the provider's limit."),
        _finding("counselor_discussion_overstated_into_funding_approval", "REVISION_REQUIRED", source_ids(sources, "synthetic_counselor_message", "synthetic_draft_output"), "A possible future discussion became a funding promise.", "Route the equipment question to the proper authority without promising funding."),
        _finding("equipment_question_softening", "REVISION_RECOMMENDED", source_ids(sources, "synthetic_user_report", "synthetic_counselor_message"), "Equipment should remain a bounded accessibility question.", "Ask what assessment or documentation the proper authority requires."),
        _finding("draft_status_incorrectly_collapsed_into_approved", "REVISION_REQUIRED", source_ids(sources, "synthetic_draft_output"), "The candidate draft used an unauthorized APPROVED label.", "Replace it with READY_FOR_USER_REVIEW."),
        _finding("recovery_cost_omitted_from_capacity_interpretation", "REVISION_REQUIRED", source_ids(sources, "synthetic_user_report", "synthetic_draft_output"), "The draft omitted immediate and delayed recovery costs.", "Restore recovery context to the capacity interpretation."),
        _finding("source_types_blended_without_attribution", "REVISION_REQUIRED", [source["id"] for source in sources], "The candidate draft blended distinct source authorities without attribution.", "Classify and cite every source in derived records."),
        _finding("accessible_direction_preserved", "ACCEPTABLE_AS_WRITTEN", [], "The client-defined accessible vocational direction is appropriately bounded.", "Preserve it as direction, not capacity."),
        _finding("low_load_preparation_preserved", "ACCEPTABLE_AS_WRITTEN", source_ids(sources, "synthetic_provider_note"), "Low-load preparation remains within the provider boundary.", "Preserve pacing and recovery monitoring without a readiness claim."),
    ]


def _distinct_case_findings(sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    draft_source = first_source(sources, "synthetic_draft_output")
    if draft_source is None:
        raise ValueError("A synthetic_draft_output is required for governed review")
    draft = draft_source["content"].lower()
    user = first_source(sources, "synthetic_user_report")
    provider = first_source(sources, "synthetic_provider_note")
    ot = first_source(sources, "synthetic_occupational_therapy_note")
    prior = first_source(sources, "synthetic_prior_employment_plan")
    vr = first_source(sources, "synthetic_vocational_rehabilitation_message")
    benefits = first_source(sources, "synthetic_benefits_information_note")
    findings: list[dict[str, Any]] = []

    if user and ("hope" in user["content"].lower() or "goal" in user["content"].lower()) and "sustainable" in draft:
        findings.append(_finding("client_goal_promoted_to_verified_capacity", "REVISION_RECOMMENDED", [user["id"], draft_source["id"]], "A client-defined hours goal was promoted into verified sustainable capacity.", "Retain the hours only as a desired direction pending evidence and proper review."))
    if user and len(re.findall(r"\b\d+-minute\b", user["content"], flags=re.IGNORECASE)) > 1 and "sustainable" in draft:
        findings.append(_finding("episodic_activity_promoted_to_sustainable_schedule", "REVISION_REQUIRED", [user["id"], draft_source["id"]], "Separate activity observations with variable recovery were converted into a sustainable weekly schedule.", "Keep the observations separate and state that consecutive-day repeatability is untested."))
    if provider and "does not give medical clearance" in provider["content"].lower() and "medically cleared" in draft:
        findings.append(_finding("provider_guidance_overstated_as_medical_clearance", "REVISION_REQUIRED", [provider["id"], draft_source["id"]], "Permission to explore bounded tasks was converted into medical clearance.", "Remove medical-clearance language and preserve the provider's explicit limit."))
    if ot and ("trial" in ot["content"].lower() or "no take-home" in ot["content"].lower()) and ("proved" in draft or "required" in draft):
        findings.append(_finding("single_ot_trial_overstated_as_prescription_and_proof", "REVISION_RECOMMENDED", [ot["id"], draft_source["id"]], "One occupational-therapy trial was promoted into proof and a required-device conclusion.", "Describe the observation once and route prescription or longer-term fit to further evaluation."))
    if vr and "no service" in vr["content"].lower() and ("will purchase" in draft or "pay for training" in draft):
        findings.append(_finding("vr_possibility_overstated_as_service_and_funding_approval", "REVISION_REQUIRED", [vr["id"], draft_source["id"]], "Possible future consideration was converted into service and funding approval.", "Restore the eligibility and individualized-planning prerequisites and remove all promises."))
    if benefits and "no individualized" in benefits["content"].lower() and "continue unchanged" in draft:
        findings.append(_finding("generic_benefits_information_overstated_as_continuity_guarantee", "REVISION_REQUIRED", [benefits["id"], draft_source["id"]], "Generic benefits information was converted into an individualized continuity guarantee.", "Remove the guarantee and route the question to an authorized program representative."))
    if prior and "not been reviewed or confirmed as current" in prior["content"].lower() and ("confirms" in draft or "employment ready" in draft):
        findings.append(_finding("stale_pre_interruption_plan_used_as_current_readiness_evidence", "REVISION_REQUIRED", [prior["id"], draft_source["id"]], "A stale pre-interruption plan was used as current readiness evidence.", "Label the plan stale and require current client confirmation before use."))
    if user and "recovery" in user["content"].lower() and "recovery" not in draft:
        findings.append(_finding("recovery_variability_and_untested_consecutive_days_omitted", "REVISION_REQUIRED", [user["id"], draft_source["id"]], "The candidate draft omitted variable recovery and the absence of consecutive-day testing.", "Restore immediate, delayed, and repeatability limits."))
    authority_claims = sum(term in draft for term in ("medically", "occupational therapy", "vocational rehabilitation", "benefits", "employment ready"))
    if authority_claims >= 3 and not re.search(r"\[S\d+\]", draft_source["content"]):
        findings.append(_finding("source_authorities_blended_without_attribution", "REVISION_REQUIRED", [source["id"] for source in sources], "The candidate draft blended multiple authorities without source attribution.", "Separate and cite client, provider, occupational-therapy, vocational, benefits, historical, and draft statements."))
    if re.match(r"\s*approved\s*:", draft_source["content"], flags=re.IGNORECASE):
        findings.append(_finding("review_only_draft_incorrectly_marked_approved", "REVISION_REQUIRED", [draft_source["id"]], "The review-only candidate output was labeled APPROVED without authority.", "Replace the label with READY_FOR_USER_REVIEW."))

    findings.extend(
        [
            _finding("accessible_direction_preserved", "ACCEPTABLE_AS_WRITTEN", source_ids(sources, "synthetic_user_report"), "Accessible remote coordination or documentation work remains a bounded client-defined direction.", "Preserve it as direction, not verified capacity."),
            _finding("bounded_preparation_preserved", "ACCEPTABLE_AS_WRITTEN", source_ids(sources, "synthetic_provider_note", "synthetic_occupational_therapy_note", "synthetic_vocational_rehabilitation_message"), "Small paced tasks and properly routed evaluation questions remain supportable.", "Preserve them with source attribution and review triggers."),
        ]
    )
    return findings


def build_findings(case_spec: dict[str, Any], sources: list[dict[str, Any]]) -> dict[str, Any]:
    is_legacy_fixture = first_source(sources, "synthetic_prior_intake") is not None
    findings = _legacy_findings(sources) if is_legacy_fixture else _distinct_case_findings(sources)
    counts = {
        "revision_required": sum(item["classification"] == "REVISION_REQUIRED" for item in findings),
        "revision_recommended": sum(item["classification"] == "REVISION_RECOMMENDED" for item in findings),
        "acceptable_as_written": sum(item["classification"] == "ACCEPTABLE_AS_WRITTEN" for item in findings),
    }
    return {
        "case_id": case_spec["case_id"],
        "status": "REVIEW_COMPLETED_REVISION_REQUIRED",
        "findings": findings,
        "counts": counts,
    }


def build_revised_output(case_spec: dict[str, Any], sources: list[dict[str, Any]]) -> str:
    evidence_lines = []
    for source in sources:
        if source["type"] == "synthetic_draft_output":
            continue
        label = SOURCE_LABELS[source["type"]]
        currency = "; stale and unconfirmed" if SOURCE_RULES[source["type"]][2] == "STALE_UNCONFIRMED" else ""
        evidence_lines.append(f"- **{label}{currency}:** {source['content']} [{source['id']}]")

    actions = [
        "Confirm the current vocational direction without treating the goal as verified capacity.",
        "Record another small paced activity with same-day, delayed, and consecutive-day recovery effects.",
    ]
    if first_source(sources, "synthetic_occupational_therapy_note"):
        actions.append("Ask what assistive-technology evaluation or take-home trial the proper authority recommends.")
    if first_source(sources, "synthetic_vocational_rehabilitation_message") or first_source(sources, "synthetic_counselor_message"):
        actions.append("Clarify which eligibility and individualized-planning steps precede any vocational service decision.")
    if first_source(sources, "synthetic_benefits_information_note"):
        actions.append("Prepare an individualized income-reporting question for an authorized benefits-program representative.")

    premature = [
        "Any medical-clearance, sustainable weekly capacity, work-readiness, or employment-readiness conclusion.",
        "Treating separate observations or one equipment trial as proof of repeatability or long-term effectiveness.",
        "Any eligibility, service, equipment, training, vendor, benefits-continuity, or funding promise.",
        "Using stale evidence as a current plan without client confirmation.",
        "Sharing the packet outside the synthetic review boundary.",
    ]
    action_text = "\n".join(f"{index}. {action}" for index, action in enumerate(actions, 1))
    premature_text = "\n".join(f"- {item}" for item in premature)
    evidence_text = "\n".join(evidence_lines)
    return f"""# Synthetic Full Human Pathway Review Summary

Status: `READY_FOR_USER_REVIEW`  
Case: `{case_spec['case_id']}`  
Data boundary: Synthetic-only demonstration

## Current direction

{case_spec['person']['display_name']} identifies this direction: {case_spec['person']['life_direction']} This remains a client-defined direction, not medical clearance, verified work capacity, or an employment conclusion.

## Source-attributed evidence

{evidence_text}

## What may proceed now

{action_text}

## What remains premature

{premature_text}

## Next review trigger

Human review of this synthetic packet. Any later test, real-world use, or external sharing requires separate authorization.
"""


def build_change_log(case_spec: dict[str, Any], findings: dict[str, Any]) -> str:
    applied = [
        f"- `{item['defect_id']}` — {item['disposition']}"
        for item in findings["findings"]
        if item["classification"] != "ACCEPTABLE_AS_WRITTEN"
    ]
    preserved = [
        f"- `{item['defect_id']}` — {item['disposition']}"
        for item in findings["findings"]
        if item["classification"] == "ACCEPTABLE_AS_WRITTEN"
    ]
    return f"""# {case_spec['case_id']} Controlled Change Log

Status: `REVISIONS_COMPLETED_FOR_REVIEW`

## Changes applied

{chr(10).join(applied)}

## Bounded content preserved

{chr(10).join(preserved)}

## Untouched boundaries

- No medical, work-capacity, occupational-therapy, eligibility, benefits, service, funding, or employment decision was created.
- No real personal information was introduced.
- No acceptance-test or operational-use claim was made.
"""


def build_checkpoint(case_spec: dict[str, Any], sources: list[dict[str, Any]], findings: dict[str, Any]) -> dict[str, Any]:
    corrected = [
        item["defect_id"]
        for item in findings["findings"]
        if item["corrected"] and item["classification"] != "ACCEPTABLE_AS_WRITTEN"
    ]
    return {
        "artifact": f"{case_spec['case_id']} synthetic governed review packet",
        "case_id": case_spec["case_id"],
        "as_of": "2026-07-17",
        "timezone": "America/Denver",
        "status": "READY_FOR_USER_REVIEW",
        "source_set": [source["id"] for source in sources],
        "reviews_completed": [
            "Authority and source-set review",
            "Role and boundary review",
            "Current-facts and evidence review",
            "Capacity and recovery review",
            "Substantive alignment review",
            "Controlled revision and deterministic validation",
        ],
        "changes_made": [f"Detected and corrected {len(corrected)} deliberate candidate-output defects.", "Created source-attributed capacity context, pathway lanes, bridge records, findings, and bounded revision."],
        "boundaries_preserved": [
            "Synthetic information only.",
            "No medical, work-capacity, occupational-therapy, eligibility, benefits, service, equipment, funding, or employment decision.",
            "No third-party approval, endorsement, acceptance-test pass, or operational approval.",
        ],
        "known_gaps": [
            "Synthetic testing does not establish real-world reliability.",
            "External authorities have made no decisions.",
            "No marketplace installation or operational use has been authorized.",
        ],
        "next_authorized_step": "Human review and governed scoring of this synthetic packet before any further test or use.",
        "still_unauthorized": [
            "Real-client use",
            "External distribution",
            "Marketplace or public release",
            "Real-world acceptance-test claim",
            "Operational use",
        ],
    }
