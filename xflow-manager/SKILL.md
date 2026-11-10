---
name: Xpell Flow Manager Contract
id: xpell-flow-manager
version: 1.1.0
updated: 2026-07-13
description: Xpell Flow Manager contract for server flow execution and client flow triggering. Covers @xpell/node FlowManagerModule, @xpell/ui FlowManagerClient, XUI _flow fields, ServerXVM flow persistence, runtime references, XData outputs, and UI-triggered flow execution.
requires:
  - xpell-contract
  - xpell-core
  - xpell-node
  - xpell-ui
  - xpell-xvm
---

# Xpell Flow Manager Contract

Use this skill for Flow Manager architecture, flow JSON, UI-to-flow triggering, XData output handling, ServerXVM flow persistence, and XVibe flow-binding work.

Also read:

- `SKILL_API_MAP.md` for exact public modules, ops, fields, events, references, and source locations.
- `SKILL_CHECKLIST.md` before reviewing or implementing any flow-binding feature.

## Current Truth vs Recommendation

`Current Truth` means verified against the current source. `Recommendation` means intended engineering direction and must not be documented as implemented behavior until source proves it.

Do not invent Flow Manager APIs, flow fields, event names, runtime references, or persistence paths.

## Scope

Current Truth:

- Server runtime is `@xpell/node` `FlowManagerModule` with module name `flow`.
- Client runtime is `@xpell/ui` `FlowManagerClient` with module name `flow-client`.
- `server-xvm` owns flow persistence through `set_flow`, `get_flow`, and `list_flows`.
- XUI objects trigger flows by emitting `ui:flow-trigger` from existing `_flow` fields.
- Flow Manager orchestrates command execution only. It does not own view rendering, entity schemas, prompt generation, DOM behavior, or storage files.

## Architecture Invariants

Current Truth:

- Flow definitions are persisted data-only JSON.
- Server flow execution is sequential and deterministic.
- Every server flow step executes through `_x.execute`.
- `server-xvm` owns flow persistence but does not execute flows.
- `flow-client` bridges UI/runtime events to server flows.
- XData is runtime state, not authoritative persistence.
- UI-to-flow binding uses existing `_flow` conventions.

Recommendation:

- XVibe must not invent a parallel event execution system.
- XVibe flow binding should mutate XUI flow fields and let the existing XUI -> `flow-client` -> server `flow.run` pipeline execute.

## Public Module Names and Ops

Current Truth:

- Server module name: `flow`.
- Server public op: `run`.
- Server implementation method: `_run`.
- Server `help` is not currently implemented.
- Server `FlowManagerModule` does not currently declare a `static _ops` map for `flow`.
- Client module name: `flow-client`.
- Client public ops from `static _ops`: `bind`, `trigger`, `help`.
- Client implementation methods: `_bind`, `_trigger`, `_help`.

Public command shape:

```json
{
  "_module": "flow",
  "_op": "run",
  "_params": {
    "_app_id": "my-app",
    "_env": "default",
    "_flow_id": "create-project",
    "_event_payload": {}
  }
}
```

Do not document underscore-prefixed method names as public op names.

## Complete UI Trigger Pipeline

Current Truth:

1. An XUI object defines `_flow`.
2. If `_flow_auto !== false`, the object binds `_flow_event` or defaults to `click`.
3. If the same event already has `_on` or `_once`, automatic `_flow` binding is skipped.
4. The XUI object emits `ui:flow-trigger` with `_flow_id`, `_event_name`, `_event_payload`, `_object_id`, `_app_id`, and `_source: "ui"`.
5. `FlowManagerClient.onLoad` listens for `ui:flow-trigger`.
6. The listener sanitizes the payload and calls `_x.execute({ _module: "flow-client", _op: "trigger" })`.
7. `flow-client.trigger` normalizes payload, resolves `_app_id` and `_env` from payload or `XUIRuntime.requireClient()`, and queues a Wormholes/server command through `client.sendXcmd`.
8. The server command is `{ _module: "flow", _op: "run" }`.
9. `flow.run` loads the persisted flow with `server-xvm.get_flow`.
10. `flow.run` executes `_steps` sequentially through `_x.execute`.
11. Server output is returned under `_flow._outputs` and `_flow._last`.
12. `flow-client` reads `res._flow` or `res._result._flow`.
13. `flow-client` writes every `_flow._outputs` entry into `_xd` with `{ source: "flow-client" }`.
14. `flow-client` executes client-side `_on_success` or `_on_error` commands from the client-loaded flow definition when present.
15. `flow-client` fires `flow:completed`, updates UI flow state, and may render a success view.

## XUIObject Flow Fields

Current Truth:

- `_flow` is supported as a string flow id.
- `_flow` is supported as an object with `_id` and optional `_payload`.
- `_flow._id` is the flow id used in `ui:flow-trigger`.
- `_flow._payload` is an object template for `_event_payload`.
- `_flow_event` is the DOM event name. Default is `click`.
- `_flow_auto === false` disables automatic binding.
- `_success_view` is not emitted by `XUIObject` in `ui:flow-trigger`.
- `flow-client` can still discover success view from trigger payload, object `_success_view`, object `_submit._success_view`, object `_flow._success_view`, parent equivalents, or closest form metadata.

Supported XUI `_flow` forms:

```json
{
  "_type": "button",
  "_text": "Save",
  "_flow": "save-project"
}
```

```json
{
  "_type": "button",
  "_text": "Save",
  "_flow_event": "click",
  "_flow": {
    "_id": "save-project",
    "_payload": {
      "name": "$xdata.form.project.name"
    }
  }
}
```

Current object/event payload behavior:

- Without `_flow._payload`, XUI sends fallback event fields: `type`, `value`, `checked`, and `key`.
- With `_flow._payload`, XUI resolves the template before firing `ui:flow-trigger`.
- Payload templates support `$xdata.*`, `$event`, and `$event.*` in `resolveFlowPayload`.

Known contradiction:

- The current auto-bind caller passes a wrapper object into `resolveFlowPayload`, while `resolveFlowPayload` reads event fields from a DOM-like event object. This may make templated `$event.*` values resolve differently than the fallback event payload. Treat this as a source-level issue to test before relying on `$event.*` in XUI `_flow._payload`.

## Flow JSON Shape

Current Truth:

Persisted flow definitions require `_id` and `_steps`.

```json
{
  "_id": "create-project",
  "_steps": [
    {
      "_id": "add-project",
      "_command": {
        "_module": "entity-manager",
        "_op": "add",
        "_params": {
          "_entity": "project",
          "_data": {
            "name": "$event.name"
          }
        }
      },
      "_output": {
        "_to": {
          "_type": "xdata",
          "_key": "project.created"
        },
        "_value": "$step.add-project._result"
      }
    }
  ]
}
```

Step fields verified in `FlowManagerModule`:

- `_id?: string`
- `_command._module: string`
- `_command._op: string`
- `_command._params?: object`
- `_command._object?: string`
- `_input?: { [param]: { _from: "xdata", _key: string } }`
- `_output?: { _to: { _type: "xdata", _key: string }, _value?: any }`
- `_when?: { _type: "xdata" | "event", _key: string, _equals?: any, _not_equals?: any }`

## Runtime References

Current Truth:

Server `flow.run` parameter and output resolution supports:

- `$event.<path>` from `_event_payload`.
- `$xdata.<key>` from server runtime `_xd`.
- `$step.<path>` from accumulated `ctx.step_results`.

Server `_input` supports only `{ _from: "xdata", _key }`.

Server `_when` supports:

- `_type: "event"` with `_key` read from `ctx.event`.
- `_type: "xdata"` with `_key` read from `_xd`.
- `_key` beginning with `$`, resolved through the same server reference resolver.
- `_equals` and `_not_equals`.

Not current server behavior:

- No server-side `$flow.*` resolver.
- No documented support for bare `$event`, bare `$xdata`, or bare `$step` in server flow steps.

Client post-flow command resolution supports:

- `$flow.<path>` from returned flow result.
- `$event.<path>` from the normalized trigger event payload.

Client post-flow command resolution does not currently support `$xdata.*`.

## Outputs and Handlers

Current Truth:

- Server success returns a Flow Manager response containing `_flow._outputs` and `_flow._last`.
- Server step failure returns an error response containing `_flow._outputs` and `_flow._last` in error details.
- `flow-client` accepts flow output at either `res._flow` or `res._result._flow`.
- `flow-client` writes `_flow._outputs` into `_xd`.
- If an output value is an object with `_ok === true` and `_result`, `flow-client` writes `_result`; otherwise it writes the raw value.
- `_on_success` and `_on_error` are client-side post-flow handlers read from `client._flows.get(flow_id)`.
- `_on_success` and `_on_error` are not server `flow.run` params and are not executed by `FlowManagerModule`.
- `flow-client.trigger` returns immediately with `{ _ok: true, _queued: true, _flow_id }`; server completion is handled asynchronously.

## Persistence Boundaries

Current Truth:

- `server-xvm.set_flow` persists flow JSON into the app bundle.
- `server-xvm.get_flow` reads persisted flow JSON for server execution.
- `server-xvm.list_flows` returns flow summaries.
- `server-xvm` persists flow files and app bundle metadata but does not execute flows.
- `_xd` updates from `flow-client` are runtime client state and are not persisted view or flow definitions.

No direct flow file writes are permitted from features that can use `server-xvm`.

## Logging and Events

Current Truth:

- Server logs flow start, step execution, skipped steps, step results, and step execution errors with `[flow]` prefixes.
- Client logs UI trigger receipt, trigger payload, raw async flow response, handler failures, and send errors with `[flow-client]` or `FLOW SEND ERROR`.
- Server fires `flow:start`, `flow:step`, and `flow:end`.
- Client listens to `ui:flow-trigger`.
- Client fires `flow:completed`.
- Client may fire `studio:open-app` when the last flow result produces a new app id.

Logging requirements for new work:

- Log module/op, flow id, app id, env, source event, target object id when available, validation failures, persistence writes, retry attempts, and final result status.
- Do not log secrets or unredacted credential payloads.

## Hard Forbiddens

- No direct server business command embedded in button handlers when a persisted flow is intended.
- No client-side server business logic.
- No second event bus or flow executor.
- No direct flow file writes.
- No unvalidated module/op execution.
- No invented `_on.click` flow contract when `_flow` is the supported abstraction.
- No treating `_xd` as persistence.
- No duplicate execution paths for the same UI-to-flow behavior.
- No executable semantic action before canonicalization, view resolution, target resolution, and validation in XVibe-generated flow binding.

## XVibe Integration

Recommendation:

Use an XVibe canonical primitive such as `bind-flow` only as a view mutation primitive, not as a runtime executor.

Recommended boundary:

1. XVibe canonicalizes the prompt into a flow-binding primitive.
2. Shared target resolution selects the target XUI object.
3. Validation confirms target, flow id, event, and payload shape.
4. Structured editing mutates the target object using existing XUI fields: `_flow`, `_flow_event`, optional `_flow_auto`, and optional success-view metadata where already supported by the target structure.
5. StructuredViewEdit persists the modified view.
6. Runtime execution uses the normal XUI -> `ui:flow-trigger` -> `flow-client.trigger` -> `flow.run` path.

Recommended primitive shape:

```json
{
  "_primitive": "bind-flow",
  "_target": {
    "_id": "save-button"
  },
  "_flow": {
    "_id": "save-project",
    "_payload": {
      "name": "$xdata.form.project.name"
    }
  },
  "_flow_event": "click",
  "_flow_auto": true,
  "_success_view": "project-list"
}
```

This primitive shape is a recommendation unless and until an XVibe implementation defines it in source.

## Testing Discipline

For any UI-to-flow binding feature, require:

- XUI field mutation test.
- Persisted view JSON test.
- Reload test.
- Runtime `ui:flow-trigger` test.
- `flow-client.trigger` command-shape test.
- Server `flow.run` test.
- Output-to-XData test.
- Success/error command test.
- Exact prompt-to-runtime acceptance test.

Known regression prompts:

- "Change My App to Dashboard"
- "Add footer label"
- "Hide Refresh"
- "Create toolbar"
- "Create toolbar with Save and Cancel"
- "Toolbar + move Refresh"
- "Make Save run the create-project flow"
- "Bind the Submit button to create-vendors and go to vendors-list on success"

## Suspicious Source Declarations

Current Truth:

- `FlowManagerModule.ts` exports `XAUTH_OPS` and `XAUTH_SKILL` before `FlowManagerModule`.
- Those declarations describe XAuth commands, not Flow Manager commands.
- They are not referenced by `FlowManagerModule` execution.

Assessment:

- This appears to be accidental copied or dead unrelated metadata, not intentional shared Flow Manager content.
- Do not remove it as part of Flow Manager skill documentation work. Handle source cleanup separately.
