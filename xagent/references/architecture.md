# Current XAgent Architecture

Use this reference for the current runtime API, Channel contract, routing, and XNode hosting. Verify details against source before changing public behavior.

## Source Map

- `packages/xagent/package.json`, `src/index.ts`
- `packages/xagent/src/XAgent.ts`
- `packages/xagent/src/XChannel.ts`
- `packages/xagent/src/XAgentChannelError.ts`
- `packages/xagent/tests/`
- `packages/xnode/src/XServer/XNode.ts`
- `packages/xnode/src/XServer/XWebServer.ts`
- `packages/xpell-core/src/XModule.ts`
- `packages/xpell-core/src/Xpell.ts`
- `packages/xpell-core/src/XProtocol.ts`

## Layering and Dependency Direction

`@xpell/node` exports the server runtime and re-exports the relevant core module primitives. `@xpell/agent` peer-depends on Node and implements `XAgent` as an `XModule`. `@xpell/agent-channels` peer-depends on Agent for Channel contracts and Node for provider route contribution types.

Do not reverse this direction:

- Core knows neither XNode nor Agents.
- XNode knows neither Agents nor provider adapters.
- Agent runtime knows no provider implementation.
- Provider adapters depend on the generic Agent boundary and, when needed, generic XNode infrastructure.
- Applications/products compose runtime, providers, lifecycle implementations, and domain capabilities.

## XAgent

`XAgent` extends `XModule`. Its `_name` is both stable Agent identity and Xpell module name. Agent names, Channel IDs, and provider IDs use lowercase kebab-case.

Construction accepts `XAgentData`:

```ts
type XAgentData = XModuleData & {
  _description?: string;
  _version?: string;
  _channels?: readonly XChannel[];
  _message_lifecycle?: XAgentMessageLifecycle;
};
```

Current public and extension methods:

- `new XAgent(data)` or a subclass constructor using the same data.
- `registerChannel(channel)` before module loading starts only.
- `listChannels()` for safe Agent-scoped Channel status.
- `stopChannels()` for explicit, idempotent Channel shutdown; XNode has no generic XModule unload integration for this.
- `getStatus()` for Agent runtime state.
- protected `onMessage(message, context)` for behavior; return an outbound message to reply or `undefined` for no reply.

Agent state is `created → starting → ready`, derived from the inherited module load state. Loading starts every registered Channel. One Channel startup failure becomes `not_ready`, is isolated, and does not stop later Channels or prevent the Agent module from becoming ready.

## Runtime Operations

Xpell operation names map to underscore-prefixed methods through normal `XModule.execute` dispatch.

- `status`: returns Agent identity, optional description/version, status, and readiness.
- `list-channels`: returns safe Channel discovery for this Agent only.
- `receive-message`: validates a normalized Agent inbound message and registered `_channel_id`, runs lifecycle and `onMessage`, and may send an automatic response.
- `send-message`: validates an Agent outbound message and uses the exact selected owned Channel.

`receive-message` does not independently redefine Channel readiness before handler execution. Normal provider ingress only receives a bound runtime after successful Channel startup, and providers should reject ingress while not ready. If an automatic response reaches the send path, canonical send enforces readiness.

Operations return `XResponseOK`/`XResponseError` data. External callers should inspect the normal Xpell envelope (`_ok`, `_ts`, `_pt`, `_result`), not invent a second protocol.

## XChannel Ownership and Lifecycle

`XChannel` is a plain interface:

```ts
interface XChannel {
  readonly _id: string;
  readonly _provider: string;
  start(runtime: XChannelRuntime): Promise<void> | void;
  stop(): Promise<void> | void;
  getStatus(): XChannelStatusData;
  send(message: XChannelOutboundMessage): Promise<XChannelSendResult>;
}
```

- `_id` identifies one Channel instance within an Agent.
- `_provider` identifies the implementation/provider type.
- Duplicate `_id` values on one Agent fail.
- Multiple IDs may share one provider, for example two Telegram Channels.
- The same adapter instance cannot be owned by two Agents.
- There is no global Channel or provider registry.
- `registerChannel()` rejects after Agent loading starts.

The lifecycle vocabulary is:

```text
registered → starting → ready
                    ↘ not_ready
ready → stopped
```

Implementations must make `start()` and `stop()` safe when repeated and expose only safe status errors. There is no automatic retry. `listChannels()` reports `_id`, `_provider`, `_status`, `_ready`, and an optional safe `_error`.

## Message DTOs

Provider-normalized inbound data:

```ts
type XChannelInboundMessage = {
  _external_user_id: string;
  _external_conversation_id: string;
  _external_message_id: string;
  _text: string;
  _timestamp?: number;
  _reply_to_external_message_id?: string;
};
```

At the Agent boundary, `XAgentInboundMessage` adds `_channel_id`. The bound runtime constructs it; the provider payload does not.

Generic outbound data:

```ts
type XChannelOutboundMessage = {
  _external_conversation_id: string;
  _text: string;
  _reply_to_external_message_id?: string;
};
```

At the Agent boundary, `XAgentOutboundMessage` adds `_channel_id`. Before calling the provider adapter, Agent routing removes that Agent-only field.

Successful provider acceptance is:

```ts
type XChannelSendResult = {
  _accepted: true;
  _external_message_id: string;
  _accepted_at: number;
};
```

This is provider acceptance, never proof of human delivery or reading. Do not expand these DTOs with raw payloads, arbitrary metadata, profiles, application entity IDs, or attachments without a deliberate contract change.

## Inbound Routing

```text
provider-specific adapter
  → normalize to XChannelInboundMessage
  → bound XChannelRuntime.receive(message)
  → inject the runtime-bound Channel ID
  → _x.execute({ _module: agentName, _op: "receive-message", _params })
  → XAgent lifecycle
  → onMessage(message, context)
```

Binding Agent name and Channel ID during `start()` establishes the trust boundary. A provider cannot route into another Channel by including `_channel_id`; the runtime creates a new Agent message from allowed normalized fields and inserts its own bound ID.

Do not call an Agent instance directly from provider ingress. `_x.execute` preserves standard module discovery, operation dispatch, and Xpell response/error behavior.

## Outbound Routing

Automatic reply:

```text
onMessage returns XChannelOutboundMessage
  → XAgent adds originating `_channel_id`
  → canonical send path
  → same owned Channel.send()
```

Explicit send:

```ts
await _x.execute({
  _module: "centrum",
  _op: "send-message",
  _params: {
    _channel_id: "telegram-customers",
    _external_conversation_id: "-222",
    _text: "Hello"
  }
});
```

Both paths share the same private canonical send path, including ownership/readiness checks, lifecycle callbacks, provider result validation, and safe error normalization. Outbound calls the selected owned adapter directly; it does not re-enter `_x.execute` or publish through XEM.

## Minimal XAgent

```ts
import {
  XAgent,
  type XAgentInboundMessage,
  type XAgentMessageContext,
  type XChannelOutboundMessage,
} from "@xpell/agent";

class GreetingAgent extends XAgent {
  protected override async onMessage(
    message: XAgentInboundMessage,
    _context: XAgentMessageContext,
  ): Promise<XChannelOutboundMessage | void> {
    if (message._text !== "hello") return undefined;
    return {
      _external_conversation_id: message._external_conversation_id,
      _text: "hi",
      _reply_to_external_message_id: message._external_message_id,
    };
  }
}

const agent = new GreetingAgent({ _name: "centrum" });
```

An Agent with zero Channels is valid and loads normally.

## XNode Hosting and Routes

XNode accepts application modules and generic route contributors:

```ts
await node.start({
  _routes: [providerRouteContributor],
  _modules: [agent],
});
```

Startup validates module identities and route contributor functions. It queues `_routes`, builds XWeb, applies contributed routes during `XWebServer.load()`, starts HTTP/Wormholes, and then loads application modules through `_x.loadModuleAsync`. The fallback is installed after contributed routes and Wormholes.

This ordering means a webhook route can be reachable before its Channel becomes ready. Provider handlers must gate readiness and return a retryable/non-success response rather than dropping authenticated input. `_routes` and `XWebRouteContributor` are generic XNode infrastructure, not Agent APIs.

Do not add an Agent-specific route registry or make XNode import Agent/provider packages.
