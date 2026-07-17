# Neverlost Review Skill Source State

As-of date: 2026-07-17  
Operating timezone: America/Denver  
Status: `CORE_SKILL_SOURCE_PRESERVED`

## Authoritative source

- Skill name: `neverlost-review-workflow`
- Source commit: `95caa40ec0da20e46dab63df5e5e042f1a86f0f8`
- Source commit time: `2026-07-17T04:56:31Z`
- Preserved snapshot: `governance/source-snapshots/neverlost-review-workflow/`

## Source hashes

| File | SHA-256 |
| --- | --- |
| `SKILL.md` | `36c8e9bebe250bc4b494d1e928cd99538b92685079af752cdb36182fe419693d` |
| `agents/openai.yaml` | `6dab2b4eaf5b974a6b6488f7627861c6d2f891a6778223e5e8fbc5074b708b5d` |
| `references/review-model.md` | `488b9236e9e352cd0048b33e7c1738c13c2a965966b6f7a349c1bc2f740569d5` |

## Packaging note

The preserved snapshot is byte-identical to the July 17 source. The runtime plugin copy keeps `SKILL.md` and `references/review-model.md` unchanged. Its `agents/openai.yaml` omits only the source-level `policy.products` list because the plugin validator does not accept that field. No governed-review logic was changed.
