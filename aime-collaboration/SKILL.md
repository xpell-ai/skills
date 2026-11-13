---
name: aime-collaboration
description: Discover and carry out shared Aime tasks through connected task records, including claims, evidence, handoffs and human acceptance. Use for team task discovery or an explicitly identified collaboration Issue.
---

# Aime Collaboration

Coordinate tasks through persistent records using each participant's own authorized connections. Resolve company-specific rules from live, access-controlled sources; this public skill does not embed private protocol documents, task contents or internal workflow mappings.

## Resolve the task and protocol

1. Identify the task repository and actual GitHub Issue number from the user's request or established context. A title prefix is not a separate identifier. For discovery without an established repository, inspect accessible repository metadata; resolve ambiguity before mutating anything.
2. Use available GitHub and Drive connectors first; an authorized CLI is a fallback. Discover supported capabilities rather than assuming tool names, shared credentials, local files or another chat's memory. See [installation and invocation](INSTALLATION.md) for setup.
3. Read the task's linked Source of Truth (SOT), including amendments, and relevant owning-repository instructions. For discovery, follow protocol links from relevant task records. If the source is absent or Drive access fails, report that blocker; do not invent rules. Read-only inventory may continue with that limitation stated.
   Full-SOT reading remains required. A source-owned index is navigation, not permission to omit rules. The [offline index review checks](references/sot-index-review.md) can assess a candidate without activating selective loading. Before an external mutation, refresh the source revision and live task/ownership state; changes, lost context or uncertainty require a fresh full read, and unavailable required policy blocks dependent writes.
4. Use task records for ownership, blockers, handoffs and execution evidence; use linked company knowledge sources for durable decisions and owning repositories for code, branches, PRs and tests. Preserve the live protocol's system boundaries rather than creating a competing task database.

## Discover and claim

- Retrieve live open Issues, following pagination. Read relevant bodies, all comment pages, assignees, dependencies and linked evidence. Summarize the participant's tasks, team blockers and next actions. Separate current facts from historical comments, screenshots and inaccessible fields; distinguish native Issue fields from Project fields.
- Before execution, verify acceptance criteria, scope, repository access, accountable human and current claim. Resolve missing information before dependent work. Discovery or read-only validation does not authorize claims, comments or label changes on sampled tasks.
- Re-read the Issue and latest comments immediately before claiming. Do not take over active work merely because its executor type matches this agent. Claims are not atomic locks: if competing claims appear, stop overlapping work and reconcile with the accountable human.
- For authorized work, record a claim with executor, accountable owner, scope, starting branch/workspace and next update. Keep Assignee as the accountable human; change it only for an explicitly agreed responsibility transfer. Executor identifies the current worker, not the accountable owner.

## Resolve and change state

Read the live repository labels, linked protocol and actual automation source before a transition. Derive the supported status and executor values, their exact label spellings, Project mappings and triggers from those sources. Recognize the protocol's human and agent executor types without treating an executor as a human assignee. Report discrepancies; do not invent labels, board columns or unsupported capabilities.

For each workflow-defined single-select label family:

1. Re-read current labels and remove conflicting values in that family before or with adding the desired value. Preserve unrelated labels and the other family. If replacing the full list, calculate it from that fresh read.
2. Verify the result. If concurrent changes conflict, reconcile rather than repeatedly overwriting another actor's work.
3. Verify automation separately: a successful label write proves Issue metadata changed, not that a board updated. Where supported, inspect the matching Actions run/job and target; otherwise identify synchronization as unverified and give an authorized viewer the exact check.

Check whether additions, removals, unchanged labels, manual dispatch, closure or PR events actually trigger the implementation. Do not toggle labels or dispatch workflows as an unrequested repair. If review or blocked states have no supported board representation, record them in the Issue/PR and follow the SOT's existing-state fallback.

Labels and successful Actions runs do not wake agents. Name the next actor and exact action; an autonomous trigger requires a separately implemented and verified integration.

## Execute, update and hand off

Follow the owning repository's instructions and contracts. Verify its Git boundary, branch and working tree, preserve other work, and implement within scope on a feature branch. Record reproducible checks, results and limitations; link PRs/commits and CI. Do not claim unrun tests or deployment.

Write meaningful progress, decisions and blockers to the Issue. A blocker needs its impact, required decision/access, next actor and exact unblocking action. Continue independent authorized work where possible.

Use [record templates](references/record-templates.md) for task creation, progress and handoff. Map every acceptance criterion to evidence or an explicit gap; include changed artifacts, exact checks/results, blockers, reviewer and next action. A no-code result still needs evidence. Transfer Executor only for an agreed takeover; it does not transfer Assignee automatically.

## Review and complete

The accountable human checks acceptance criteria and evidence, requests changes or approves. A commit, PR, comment or passing mock test alone is not acceptance. Keep review/blocker state according to the live protocol until acceptance.

Complete a task only after every acceptance criterion is verified and the accountable human approves closure within the user's authorized scope. Record that approval and final artifacts, apply the protocol's exclusive completion state, close the Issue when authorized, then verify state/labels. Report Project synchronization separately. Missing evidence or approval requires a specific next reviewer action, not a completion claim. Implementation requests alone are not acceptance of the finished result.

## Access and information boundaries

Verify each participant's repository, Project and Drive access independently. One connection's success does not establish another person's permissions. Preserve the source systems' privacy and least-privilege boundaries.

Never put credentials, customer personal data, billing exports, secret-bearing logs or unapproved production information in task records or artifacts. Keep protected data in the approved system and use sanitized evidence links. Do not copy private task/SOT contents, private URLs or internal workflow details into this public Skills repository; resolve them at runtime through the authorized task context.

Paid provider calls, deployment, production writes and external outreach require explicit authorization and applicable policy. This skill grants none. Protocol changes belong in the authoritative knowledge source with human review, version/date and linked task; surface source/workflow gaps rather than silently rewriting the contract.
