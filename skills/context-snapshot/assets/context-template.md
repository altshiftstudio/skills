# Agent Context Handoff

## Snapshot

- Created: `<YYYY-MM-DD HH:MM local timezone>`
- Scope: `<what this handoff covers>`
- Current status: `<single-sentence state>`
- Mode: `<quick|standard|forensic>`
- Confidence: `<high|medium|low>`
- Coverage: `<time range or message range included>`

## Source Tag Format

Use this format for major claims:

`(source: <user message | assistant message | command output | file path>)`

## User Intent

- Primary goal: `<what the user wants>` `(source: <...>)`
- Success criteria: `<how completion is judged>` `(source: <...>)`
- Non-goals: `<what is out of scope>` `(source: <...>)`

## Key Decisions

| Decision | Rationale | Date | Owner | Source |
| :--- | :--- | :--- | :--- | :--- |
| `<decision>` | `<why>` | `<YYYY-MM-DD>` | `<user/agent/team>` | `<source>` |

## Constraints and Assumptions

- Fact: `<hard constraint>` `(source: <...>)`
- Assumption: `<assumption>` `(source: <...>)`

## Work Completed

- `<completed step + outcome>` `(source: <...>)`

## Files and Artifacts

- `<path>`: `<what changed or why it matters>` `(source: <...>)`

## Commands and Results

- `<command>` -> `<key result>` `(source: command output)`

## Issues, Risks, and Blockers

| Item | Impact | Owner | Mitigation | Source |
| :--- | :--- | :--- | :--- | :--- |
| `<issue/risk/blocker>` | `<impact>` | `<owner>` | `<next action>` | `<source>` |

## Open Questions

- `<question>`; owner: `<who can answer>`; priority: `<high|medium|low>`; source: `<...>`

## Next Steps (Ordered)

1. `<next action>`; owner: `<who>`; depends on: `<dependency or None>`; source: `<...>`
2. `<next action>`; owner: `<who>`; depends on: `<dependency or None>`; source: `<...>`

## Contradictions and TODOs

- `TODO: <conflicting detail or missing information>` `(source: <...>)`
- `None`

## Handoff Prompt for Next Agent

Use this as the next session opener:

```text
Continue from this handoff. Preserve listed decisions and constraints exactly as written.
Treat "Fact" as authoritative and "Assumption" as provisional.
Start by confirming "Current status" and "Confidence", resolve TODO items, then execute "Next Steps (Ordered)" in sequence.
```
