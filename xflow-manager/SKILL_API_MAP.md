# Xpell Flow Manager API Map

All entries are Current Truth verified against source on 2026-07-13.

## Source Files

- Server module: `xnode/src/XFM/FlowManagerModule.ts`
- Client module: `xpell-ui/src/XFM/FlowManagerClient.ts`
- XUI flow trigger: `xpell-ui/src/XUI/XUIObject.ts`
- XUI runtime loading: `xpell-ui/src/XUI/XUIRuntime.ts`
- Flow persistence: `xnode/src/XVM/ServerXVMModule.ts`
- Flow-related tests: `xnode/src/test.ts`

## Modules and Public Ops

| Runtime | Module name | Public ops | Implementation methods |
| --- | --- | --- | --- |
| server | `flow` | `run` | `_run` |
| client | `flow-client` | `bind`, `trigger`, `help` | `_bind`, `_trigger`, `_help` |
| server persistence | `server-xvm` | `set_flow`, `get_flow`, `list_flows` | `_set_flow`, `_get_flow`, `_list_flows` |

Notes:

- Server `flow.help` is not currently implemented.
- Server `FlowManagerModule` does not currently expose a `static _ops` map.
- Underscore method names are implementation details, not public op names.

## Trigger Payload

`flow-client.trigger` accepts:

```ts
{
  _flow_id: string;
  _event_name?: string;
  _event_payload?: object;
  _object_id?: string;
  _success_view?: string;
  _app_id?: string;
  _env?: string;
  _source?: "ui" | "event";
}
```

`flow-client` sends this server command:

```json
{
  "_module": "flow",
  "_op": "run",
  "_params": {
    "_flow_id": "flow-id",
    "_app_id": "app-id",
    "_env": "default",
    "_event_payload": {},
    "_event_name": "click"
  }
}
```

`flow.run` currently reads `_flow_id`, `_app_id`, `_env`, and `_event_payload`. `_event_name` is forwarded by the client but not used by server flow execution.

## Flow JSON Step Shape

```ts
{
  _id?: string;
  _command: {
    _module: string;
    _op: string;
    _params?: Record<string, any>;
    _object?: string;
  };
  _input?: Record<string, { _from: "xdata"; _key: string }>;
  _output?: {
    _to: { _type: "xdata"; _key: string };
    _value?: any;
  };
  _when?: {
    _type: "xdata" | "event";
    _key: string;
    _equals?: any;
    _not_equals?: any;
  };
}
```

## Runtime References

Server `flow.run`:

- `$event.<path>` -> `_event_payload`
- `$xdata.<key>` -> server `_xd.get(key)`
- `$step.<path>` -> accumulated step results
- `_input` -> only `{ _from: "xdata", _key }`
- `_when._type: "event"` -> event payload path
- `_when._type: "xdata"` -> server `_xd.get`

Client `_on_success` and `_on_error` command resolution:

- `$flow.<path>` -> returned flow object
- `$event.<path>` -> normalized trigger event payload

XUI `_flow._payload` template resolution:

- `$xdata.<key>` -> XData value
- `$event` -> event context object
- `$event.<key>` -> event context key

Known caveat: current XUI auto-bind passes a wrapper into `resolveFlowPayload`, so templated `$event.*` must be tested before relying on it.

## Output Contract

Server response carries:

```json
{
  "_flow": {
    "_outputs": {},
    "_last": {}
  }
}
```

Depending on response wrapping, `flow-client` accepts:

- `res._flow`
- `res._result._flow`

Client output application:

- For every key in `_flow._outputs`, call `_xd.set(key, value, { source: "flow-client" })`.
- If output value is `{ _ok: true, _result: value }`, write `value`.
- Otherwise write the raw output value.

## Relevant XEM Events

Server:

- `flow:start`
- `flow:step`
- `flow:end`

Client:

- listens to `ui:flow-trigger`
- fires `flow:completed`
- may fire `studio:open-app` when the final server result returns a generated app id

## XUI Flow Fields

- `_flow`: string flow id or object with `_id` and optional `_payload`
- `_flow._id`: flow id
- `_flow._payload`: event payload template
- `_flow_event`: DOM event name, default `click`
- `_flow_auto`: automatic flow binding disabled when `false`
- `_success_view`: discovered by `flow-client` from trigger payload, object, `_submit`, `_flow`, parents, or closest form metadata; not emitted directly by `XUIObject`

## ServerXVM Dependencies

`flow.run` depends on:

```json
{
  "_module": "server-xvm",
  "_op": "get_flow",
  "_params": {
    "_app_id": "app-id",
    "_flow_id": "flow-id",
    "_env": "default"
  }
}
```

Persistence ops:

- `server-xvm.set_flow` validates `_flow` and `_flow._id`, stores it in the app bundle, updates app metadata, and persists.
- `server-xvm.get_flow` loads a persisted flow by `_app_id`, `_env`, and `_flow_id`.
- `server-xvm.list_flows` returns summaries with `_id`, `_type`, and `_title`.

## Suspicious Unrelated Declarations

`xnode/src/XFM/FlowManagerModule.ts` also exports:

- `XAUTH_OPS`
- `XAUTH_SKILL`

These are XAuth metadata declarations, not flow declarations, and are not used by `FlowManagerModule` execution. Treat them as likely accidental copied or dead unrelated code for a separate cleanup.
