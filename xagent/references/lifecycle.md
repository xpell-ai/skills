# XAgent Message Lifecycle V0.2

Use this reference for the optional deterministic boundary around inbound processing and outbound provider acceptance.

## Source of Truth

- `packages/xagent/src/XAgentMessageLifecycle.ts`
- `packages/xagent/src/XAgent.ts`
- `packages/xagent/src/XAgentChannelError.ts`
- `packages/xagent/tests/lifecycle.test.mjs`

## Contract

`XAgentData` accepts one optional construction-time `_message_lifecycle`. There is no lifecycle registry, callback array, or dynamic post-load installation API.

```ts
type XAgentMessageContext = Readonly<{
  _agent_name: string;
  _origin: "inbound" | "explicit";
}>;

interface XAgentMessageLifecycle {
  beforeInbound?(context, message):
    | void
    | { readonly _action: "handled" }
    | Promise<void | { readonly _action: "handled" }>;
  afterInbound?(context, message, outcome): void | Promise<void>;
  beforeSend?(context, message): void | Promise<void>;
  afterSend?(context, message, outcome): void | Promise<void>;
}
```

Lifecycle message views, contexts, outcomes, safe errors, and accepted result views are frozen snapshots. Lifecycle code observes them; it does not mutate routing.

## Ordering

Inbound with response:

```text
beforeInbound
→ onMessage
→ afterInbound({ _status: "processed" })
→ beforeSend
→ Channel.send
→ afterSend({ _status: "accepted" | "send_failed", ... })
```

Inbound without response:

```text
beforeInbound
→ onMessage
→ afterInbound({ _status: "processed" })
```

Explicit outbound:

```text
beforeSend
→ Channel.send
→ afterSend({ _status: "accepted" | "send_failed", ... })
```

If `beforeInbound` returns `{ _action: "handled" }`, the operation succeeds with a null result and does not call `onMessage`, `afterInbound`, or send. Any other non-`undefined` control shape is a lifecycle failure.

An `afterInbound` failure after successful processing prevents an automatic response, because canonical send comes later. A no-response inbound still runs successful `afterInbound`.

## Context Identity

- One context object is created per inbound `receive-message` execution.
- The same object reference is passed through inbound callbacks, `onMessage`, and any automatic response callbacks.
- Each explicit `send-message` execution receives a distinct context.
- `_origin: "inbound"` identifies inbound and automatic-response work.
- `_origin: "explicit"` identifies an explicit outbound operation.
- `_agent_name` is the bound Agent identity.

The context deliberately contains no participant, customer, Channel identity, conversation, message, dedupe, database, or transaction IDs. Applications may correlate their own state without extending Agent core:

```ts
import type {
  XAgentMessageContext,
  XAgentMessageLifecycle,
} from "@xpell/agent";

type AppMessageState = { _application_message_key: string };
const applicationState = new WeakMap<
  XAgentMessageContext,
  AppMessageState
>();

const lifecycle: XAgentMessageLifecycle = {
  beforeInbound(context, message) {
    applicationState.set(context, {
      _application_message_key:
        `${message._channel_id}:${message._external_message_id}`,
    });
  },
  beforeSend(context) {
    const state = applicationState.get(context);
    if (state) void state._application_message_key;
  },
};
```

This `WeakMap` is an application/lifecycle implementation technique, not Agent-owned persistence or memory. Explicit sends have no preceding inbound state unless the application establishes it externally.

## Outcomes

`afterInbound` receives:

- `{ _status: "processed" }`, or
- `{ _status: "processing_failed", _error: { _code, _message } }`.

`afterSend` receives:

- `{ _status: "accepted", _result: XChannelSendResult }`, or
- `{ _status: "send_failed", _error: { _code, _message } }`.

No raw provider error, payload, token, secret, or response body is exposed.

## Error Semantics and Precedence

Agent error codes:

- `E_AGENT_CHANNEL_INVALID`: invalid Channel/configuration or illegal late registration.
- `E_AGENT_CHANNEL_DUPLICATE`: duplicate Channel ID inside an Agent.
- `E_AGENT_CHANNEL_NOT_FOUND`: selected Channel is not owned by the Agent.
- `E_AGENT_CHANNEL_NOT_READY`: canonical send selected a non-ready Channel.
- `E_AGENT_CHANNEL_BAD_MESSAGE`: normalized inbound/outbound shape is invalid.
- `E_AGENT_CHANNEL_SEND_FAILED`: provider adapter failed to return valid acceptance.
- `E_AGENT_MESSAGE_HANDLER_FAILED`: `onMessage` threw or returned an invalid outbound message.
- `E_AGENT_MESSAGE_LIFECYCLE_FAILED`: lifecycle configuration/callback/control failed.

Precedence is deliberate:

- A `beforeInbound` failure stops before the handler.
- A handler failure is reported as `E_AGENT_MESSAGE_HANDLER_FAILED`; failure in the `afterInbound(processing_failed)` observer does not replace it.
- A successful-processing `afterInbound` failure is lifecycle failure and prevents automatic send.
- A `beforeSend` failure is lifecycle failure and the provider is not called.
- A provider send failure remains `E_AGENT_CHANNEL_SEND_FAILED`; failure in the `afterSend(send_failed)` observer does not replace it.
- If the provider accepted the message and `afterSend(accepted)` then fails, the result is `E_AGENT_MESSAGE_LIFECYCLE_FAILED`, not send failure. Safe error metadata preserves `_provider_accepted: true`, external message ID, accepted timestamp, and Channel ID.

## Boundary: Not Persistence

The lifecycle is a deterministic integration seam. `@xpell/agent` does not own XDB persistence, participants, Channel identity records, conversations, messages, customers, dedupe keys, history, memory, queues, or inbox/outbox.

An application or future Starter can implement those externally and participate through the lifecycle. Do not add domain IDs to `XAgentMessageContext` merely to support one application.

## Auth and Identity Boundary

XAuth principals represent authentication/authorization state. An external messaging customer is not automatically an XAuth user, and a provider Channel identity is not an authentication identity. XAgent creates neither users nor an identity framework.

## Memory Boundary

Keep these separate:

- Conversation history: durable prior conversation/message records.
- Derived customer memory/preferences: domain projections or summaries.
- Agent runtime/working memory: transient execution state.

Installing `@xpell/agent` provides none of them. Add each only in the application/capability layer that owns its lifecycle, retention, authorization, and persistence semantics.

## Why Not XEM

XEM is event notification infrastructure, not the authoritative message transaction path. The lifecycle is awaited, ordered, and has defined errors; use it when external persistence/observation must affect or record message processing deterministically.
