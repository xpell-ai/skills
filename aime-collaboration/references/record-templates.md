# Issue record templates

Adapt these fields to the task. Omit irrelevant fields; replace bracketed prompts with facts. Post only within the authorized task scope. Keep sensitive details in approved protected systems and use sanitized links here. These are record formats, not additional board states.

## New task

```markdown
## Outcome and scope
[Concrete outcome, affected repositories, explicit non-goals]

## Ownership and context
- Accountable human / Assignee: [GitHub login]
- Executor: [type supported by the live protocol]
- Priority / Workstream: [value and source, or unverified]
- Dependencies: [linked Issues or explicitly verified none; unknown if not checked]
- Sources: [Drive SOT and owning repository links]

## Acceptance criteria
- [ ] [Observable outcome and how it will be verified]

## Blocker and next action
[Current blocker or none; next actor and exact action]
```

Avoid a static status field in the body; comments and current labels carry lifecycle updates.

## Claim

```text
CLAIM | executor: [type/session] | owner: [accountable human]
Scope: [authorized work and relevant acceptance criteria]
Starting branch/workspace: [repository, base revision, branch or no-code]
Next update: [meaningful milestone or agreed time]
Issue labels: [observed values or exact change]
Project sync: [verified run/target evidence, or unverified]
```

## Progress or blocker

```text
PROGRESS / BLOCKED | executor: [type/session] | owner: [human]
Completed/evidence: [facts and links]
Remaining/impact: [work and blocker]
Required decision/access: [specific requirement, without credentials]
Next actor/action: [who does exactly what]
State: [current Issue labels; Project verification or limitation]
```

## Handoff for review or takeover

```markdown
HANDOFF | executor: [type/session] | accountable owner: [human]

Result: [concrete behavior/artifacts]
Changes: [owning repository, branch, commit and PR links; no-code if applicable]

| Acceptance criterion | Evidence / gap |
| --- | --- |
| [criterion] | [verified result + link, or pending reason] |

Validation: [exact commands/checks, result and relevant environment]
Limitations/blockers: [untested behavior, dependencies, access or none]
Next actor: [reviewer or agreed new executor]
Exact next action: [review criteria, reproduce check or unblock step]
State: [current state pending acceptance; actual labels]
Project sync: [matching run/target evidence or unverified]
```

## Completion after human acceptance

```text
DONE | accountable human approval: [link or explicit session authorization]
Acceptance: [every criterion verified; evidence links]
Final artifacts: [PR/commit/doc/CI links]
Outcome and remaining limitations: [facts]
Issue: [verified closed state and exclusive completion label]
Project sync: [verified result or exact viewer follow-up]
```
