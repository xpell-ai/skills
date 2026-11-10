# Controlled provider Actions and reconciliation

Read for a supervised live-provider experiment or an interrupted outbound Action.
This is an application workflow, not a new framework, provider integration or
permission to send. Respect the active task's limits; a successful experiment
does not authorize production rollout, another recipient/channel or automatic work.

## 1. Locate ownership and existing state

Use the repository instructions, current source/tests and product Source of Truth.
If no designated Source of Truth is available, report that gap; do not invent
approved product decisions from implementation reports. Keep decisions in product
documents, procedures here, and sanitized run evidence in task-local artifacts.

Reuse the existing Console, launcher, Channel, authorization and persistence path.
Verify which process, port, work folder and frozen Business App binding the user
actually uses. Inspect only relevant, sanitized state; do not print process
environments or credential files. Do not create another environment just to
repeat a consumed allowance. Use a verified explicit synthetic reset only when
authorized, preserving evidence; never reset real consent or send history.
Do not stop/restart a process without verifying ownership and pending Actions.
Prepare a short-lived Action after required readiness/restarts to avoid expiry
loops. Respect configured TTL; never revive or silently extend an expired Action.

| Boundary | Owner |
| --- | --- |
| Provider-neutral routing, lifecycle and Channel ownership | `@xpell/agent` |
| Provider protocol, normalized ingress and acceptance result | canonical `@xpell/agent-channels` adapter |
| Generic conversation persistence and confirmation/execution audit | application Starter |
| Customer eligibility, consent, incentives, attribution and release policy | product plugin |
| Tenant-scoped durable transport/ACK, if already composed | XNet |

XNet acceptance or processed ACK cannot atomically prove a provider/business effect
in another store. Do not add XNet, queues or workers merely to connect an existing
Channel. Inspect the existing composition instead of assuming a synthetic handoff
is a live business integration.

## 2. Establish scope and independent permissions

Derive app/tenant, authenticated Owner, Customer and verified ChannelIdentity from
trusted server bindings. A name, URL, UI-selected app or model argument cannot
select authority. Do not copy profiles, permissions, consent, Rewards or history
across businesses. Authenticated identity, preferences and communication identity
are distinct; Owner and Customer context projections remain separately authorized.

Keep these gates independent:

- **Recipient consent:** auditable, purpose-specific permission from the verified
  participant flow, bound to business, recipient and channel with scope, expiry
  and withdrawal evidence. An existing chat, registration, Owner statement or
  LLM assertion is not consent. A queued update is not consent until verified.
- **Owner Action:** a requested, complete exact proposal with recipient, message,
  incentive and expected measurable outcome, followed by fresh explicit approval.
  Read-only availability questions create no Action. Composer text, a failed
  submission and approval of an expired/different Action cannot confirm it.
- **Operator/provider release:** where a controlled environment is locked, release
  only the reviewed operation under the user's explicit authorization. This
  neither confirms the Action nor replaces participant consent.

For an approved single-attempt release, bind the existing permit to the Action ID
and immutable fingerprint of app/Owner/recipient/bot or account/channel/message/
incentive. Keep unrelated Actions and automatic Customer replies locked. Recheck
ownership, unchanged proposal, current consent/revocation, Reward state and one-time
eligibility immediately before dispatch. Consume the permit with a concurrency-safe
guard before any provider attempt, preserving the durable follow-up claim and
idempotency protections. Fail closed on restart, expiry, rejection or cancellation;
failed and uncertain attempts do not renew the allowance. If current boundaries
cannot provide this guarantee, stop and identify the smallest missing mechanism.

## 3. Limit live readiness work

Use focused mocked checks first for duplicates/concurrency, restart, changed
proposal, revoked/expired permission, wrong scope, partial effects and safe errors.
Readiness is not permission to issue an incentive, acknowledge a customer or send.
Reuse existing credentials without displaying or copying them into artifacts.
Verify the actual provider account/bot and current webhook before changing it;
never unknowingly replace another active integration.

When public webhook restoration is required by the approved task:

- Verify hostname ownership read-only using the intended configured account;
  local configuration or an unauthenticated hostname response is not ownership.
- Prove the actual remote ingress policy is attached and enforced while the
  business upstream is closed. A locally parsed policy is insufficient.
- Permit only the exact required webhook method/path/host. Deny Console/admin,
  generic XNode/Wormholes routes and WebSocket upgrades; verify loopback origin
  and absence of alternate ingress paths. Preserve canonical provider verification.
- Run external negative controls and a safe positive control before forwarding
  real updates. Account for actual intermediary-added headers and distinguish
  protocol rejection/redirects from upstream responses. Stop if isolation cannot
  be demonstrated; do not broaden access to make the webhook pass.
- Keep unrelated/queued events from mutating business state. Use the reviewed
  participant-only admission policy; never drop queued updates as a shortcut.

Prepare rollback before exposure: restore the send lock, apply verified remote
deny-all or stop only the owned ingress, and confirm the private Console remains
private. Preserve identities and business evidence. Record actual webhook changes;
restoring an offline or unrelated old endpoint is not a safe default rollback.

## 4. Reconcile before any proposed retry

A timeout, generic UI error, restored draft or failed observer is not evidence
that nothing happened. Read the scoped persisted Action, consent, Reward,
follow-up, outbound attempt and provider receipt first. Diagnose UI submission,
model inference, routing, argument semantics, handler, transport and presentation
independently; retain confirmed causes separately from hypotheses.

Use existing provider receipts/status evidence without sending again. Distinguish
a definitive rejection from an uncertain attempted send. Park uncertain work;
never automatically resend it, reissue its Reward or prepare a replacement that
bypasses the one-time claim. A provider-accepted attempt followed by a local audit
or UI error must not be reported as definitive provider failure. Do not trigger
an outbound retry or consume inbound updates just to query state.

Reward issuance, follow-up progression and send outcome need independent durable
evidence. If an incentive already exists after a failed send, report its real
state and recovery requirement; do not promise rollback/compensation that has
not happened. Do not discard claims or evidence during cleanup.

## 5. Report only the state supported by evidence

- Proposal/pending Action is not approval or execution.
- Console acceptance is not provider acceptance.
- Provider acceptance is not device delivery/read or a return visit.
- Participant-observed receipt is separate human evidence, not an invented
  provider delivery status.
- Staff-authorized Redemption proves the recorded entitlement was redeemed;
  registration alone is not a physical Visit, and a second visit requires earlier
  qualifying evidence. Attribution to a Reward is not proof of causal uplift.

Use typed sanitized domain errors through the existing Action/UI boundary and
preserve internal machine codes. Distinguish locked, expired, missing/revoked
consent, unauthorized/invalid Action, definitive send failure and uncertain send.
Use the Owner's language and a practical next step; do not expose stacks/provider
secrets or advise retrying uncertainty. Say that no message/Reward was created
only when persisted evidence supports that statement. Availability questions must
report current eligibility rather than substitute an older completion report.

Finish with actual Action, incentive and send states, permit/lock status, partial
effects and remaining blockers. Request device observation separately when needed.
Keep recipient IDs, credentials, temporary endpoints, concrete business fixtures
and experiment outcomes out of reusable Skills. Do not create a new benchmark,
framework or set of demo environments to finish a single supervised experiment.
