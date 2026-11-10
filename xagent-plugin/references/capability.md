# AgentCapability and Action boundary

Read before adding or changing a product capability. Check current definitions
in `server/src/capabilities/AgentCapability.ts`, `CapabilityResolver.ts`,
`server/src/Agent.ts`, and `server/src/actions/ActionService.ts`; package runtime
and application orchestration remain separate authorities.

## Capability, tool, handler

An `AgentCapability` binds a semantic ID, description, closed `_input_schema`,
`_effect`, `_confirmation`, and fixed `_handler`. The XAI tool is a temporary
projection of an allowed capability, not an independent execution authority.
`capabilityToXAITool` projects its name, description, and schema; side-effect
descriptions also explain that calling the tool prepares rather than executes.
The model must never select trusted actor, tenant, Business App, authorization,
or arbitrary `_module`/`_op` dispatch.

Use stable semantic IDs. Composition rejects duplicates. `agent.help` derives
from effective capabilities; registration alone grants no permission.

## Current execution contracts

- Reads use `_effect: "read"`, `_confirmation: "none"` and the fixed handler.
- Side effects require `_effect: "side_effect"`, `_confirmation: "required"`,
  a stable non-empty `_revision`, and `_prepare_action`.
- `_prepare_action` derives `_arguments`, `_authorized_scope` and an exact
  `_confirmation_summary` from trusted current state. It must not issue the
  Reward or send a message while preparing the proposal.
- Optional `_can_prepare` checks the original request before Action creation.
  Its bounded `_assess_request` is semantic evidence, never authorization;
  confirmation re-preparation does not invoke this creation-only hook.
- Optional `_authoritative` applies only to unconfirmed reads. `_matches_request`
  is a product routing guard, not an authorization or consent mechanism.
- Optional `_render_reply` handles `proposal`, `result`, or `preparation_denied`
  presentation from trusted results/prepared terms. It grants no permission.

The Agent resolves authorized capabilities for the trusted turn, routes/selects,
validates untrusted arguments, and reauthorizes before a read handler or Action
preparation. A side-effect tool call creates a pending Action and exposes its
confirmation summary; it does not execute the handler. Pending Actions restrict
further side-effect exposure. Inspect current routing and bounded model-round
limits rather than assuming the original two-generation read-only loop.

`ActionService.confirmAndExecute` checks current app/actor/conversation ownership,
expiry and capability revision; reauthorizes; re-prepares and compares arguments,
scope and summary; then claims the state transition before calling the handler
with `_action` execution context. Preserve its durable audit, idempotency and
failure/uncertainty semantics. Do not call the side-effect handler directly or
create a second approval path.

Read-only eligibility questions must return current availability, even if an
older completed outcome exists. A business goal, ambiguity or a proposed model
action is not a request to persist that Action. Clarify before preparation where
needed; do not rely on keyword matching alone. Direct trusted calls to
`createPendingAction` must also be justified by an authorized preparation request;
the creation-only Agent hook is not automatically run by ActionService itself.

## Input schemas

The current validator accepts a closed object with no properties or string
properties, optional `required`, and supported string `description`, `minLength`
and `maxLength` constraints. Extra arguments fail. Unsupported schema types or
constraints are not made safe by provider-native schema adaptation; inspect
`validateCapabilityArguments` before extending the contract.

For no arguments:

```ts
_input_schema: Object.freeze({
  type: "object",
  properties: Object.freeze({}),
  additionalProperties: false,
})
```

## Errors and tests

Keep machine-readable capability, Action and domain error codes. Do not flatten
expected domain errors into generic preparation failures. Map sanitized expected
cases in the existing UI; do not expose provider payloads, credentials or stacks.
A successful Action or valid schema does not prove the requested business effect.
Use independent persisted business and send outcomes for result wording.

Use focused mocked tests for the affected contracts:

- resolver exposure, fabricated calls, invalid arguments, reauthorization and
  zero-plugin compatibility;
- unsolicited/ambiguous requests cannot prepare Actions, while legitimate requests
  can; role impersonation and client-selected scope never grant access;
- exact proposal confirmation, revision/integrity/expiry changes, ownership,
  concurrent/replayed approvals and durable duplicate suppression;
- correct current-state interpretation and sanitized error presentation, including
  failed versus uncertain sends and partial business effects.

For controlled provider execution and reconciliation, read
[controlled-provider-actions.md](controlled-provider-actions.md). Keep product
policy, persistence, consent and provider-release restrictions downstream from
the generic Action boundary.
