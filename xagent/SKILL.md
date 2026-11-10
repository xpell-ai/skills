---
name: xagent
description: Develop and review the current Xpell Agent runtime, provider Channels, XNode integration, and Agent applications. Use for @xpell/agent, @xpell/agent-channels, XAgent routing or message lifecycle, provider adapters such as Telegram, and deciding whether Agent work belongs in runtime, provider, starter, or product code. Use package source for runtime contracts and the current xpell-agent Starter for application orchestration; never restore the removed legacy implementation.
---

# XAgent

Use this skill for current Xpell Agent work. Treat current source and tests as authoritative; this skill is a routing and architecture guide, not a substitute for checking implementation before API-sensitive changes.

## Start With Authority

Inspect the relevant current files before changing behavior:

- `packages/xagent/src/XAgent.ts`, `XChannel.ts`, `XAgentMessageLifecycle.ts`, `XAgentChannelError.ts`, and `packages/xagent/tests/`
- `packages/xagent-channels/src/telegram/` and `packages/xagent-channels/tests/`
- `packages/xnode/src/XServer/XNode.ts` and `XWebServer.ts` for hosting and routes
- `packages/xpell-core/src/XModule.ts`, `Xpell.ts`, and `XProtocol.ts` for module dispatch and response conventions

README files communicate intent but do not override source and tests. If this skill differs from current implementation, follow source and update the skill separately.

The current `/xpell-agent` is the application Starter. Inspect it for application orchestration, persistence, confirmation, and plugin contracts; it does not redefine package runtime APIs. Never copy the removed legacy implementation as architectural authority. For application-local product work, also use `$xagent-plugin`.

## Current Package Boundary

```text
@xpell/core
      ↓
@xpell/node
      ↓
@xpell/agent
      ↓
@xpell/agent-channels
      ↓
Agent application / product
```

This is a conceptual layer sequence. Actual manifests matter: `@xpell/agent` peer-depends on `@xpell/node`; `@xpell/agent-channels` peer-depends on both `@xpell/agent` and `@xpell/node` because provider adapters may contribute generic XNode routes. `@xpell/node` must not depend on Agent or provider packages.

- `packages/xagent` / `@xpell/agent`: provider-neutral runtime, contracts, routing, lifecycle, safe errors.
- `packages/xagent-channels` / `@xpell/agent-channels`: provider implementations such as Telegram.
- `/xpell-agent`: current application Starter, owning generic conversation persistence and Action orchestration. Keep it separate from runtime packages.
- Product code such as Pulse or Gator: domain behavior, customers, and product-specific persistence.

## Non-Negotiable Architecture

1. `XAgent` is an `XModule` hosted and loaded by XNode. Do not create another Agent runtime around XNode.
2. Channels are plain provider adapters owned by exactly one `XAgent`; they are not `XModule`s and have no global registry.
3. Keep provider code out of `@xpell/agent` and persistence out of `@xpell/agent`.
4. External Channel ingress must use the bound `XChannelRuntime.receive()`, which injects `_channel_id` and calls `_x.execute` for `receive-message`.
5. Provider input must never select or spoof `_channel_id`.
6. Agent outbound delivery selects an owned Channel and calls `channel.send()` directly. Do not route Agent-to-Channel delivery through `_x.execute` or XEM.
7. Use `XAgentMessageLifecycle` for deterministic external observation/control around message processing. Do not use XEM for authoritative message processing.
8. Agent readiness and Channel readiness are separate. A failed Channel does not redefine Agent readiness or block other Channels.
9. Do not turn external customers or Channel identities into XAuth users automatically.
10. Do not add polling or background workers without an explicit lifecycle and shutdown design.
11. Do not modify XNode to know about XAgent, Telegram, or another provider.
12. Do not resurrect legacy `AgentRuntime`, `ChannelsModule`, `UsersModule`, `TelegramConnectorModule`, AIME, or legacy custom flow/auth/settings architecture.

## Current Runtime Shape

Inbound:

```text
provider → Channel normalize → bound runtime.receive()
→ _x.execute(agent.receive-message) → XAgent → onMessage()
```

Automatic outbound:

```text
onMessage() → canonical Agent send → originating Channel → provider
```

Explicit outbound:

```text
_x.execute(agent.send-message) → canonical Agent send
→ explicitly selected Channel → provider
```

Provider acceptance means the provider accepted the request. It is not human delivery, reading, or engagement.

For exact APIs, DTOs, operations, examples, ownership, and XNode startup, read [architecture.md](references/architecture.md).

## Generic Starter application scope (verified)

The current `xpell-agent` Starter accepts an optional immutable
`AgentApplicationScope` native XVM pair `(_env, _app_id)` from trusted
server-side composition. Unscoped mode remains explicit. The generic Starter
never resolves product default-app settings or markers. Its protected
ServerXVM Agent entities remain under `xpell-agent-starter/default`; indexed
record scope, scoped deterministic keys, and Action binding checks isolate
Participants, ChannelIdentity, Conversations, Messages, and Actions. Legacy
unscoped records remain unassigned. Product plugins such as Pulse validate
their own app selection and supply the resulting pair; generic Agent runtime
and provider Channels do not choose an app.

## Message Lifecycle

One optional construction-time `XAgentMessageLifecycle` supplies `beforeInbound`, `afterInbound`, `beforeSend`, and `afterSend`. It wraps the canonical Agent path; it is not persistence and does not own routing or provider results.

An inbound execution receives one frozen `XAgentMessageContext` with `_origin: "inbound"`; an automatic response reuses that exact context reference. Each explicit send receives a new context with `_origin: "explicit"`. Domain and persistence IDs are deliberately absent.

For ordering, the `handled` short-circuit, error precedence, `WeakMap` extension technique, and persistence/auth/memory boundaries, read [lifecycle.md](references/lifecycle.md).

## Telegram

The current provider is `TelegramChannel` from `@xpell/agent-channels/telegram` (also re-exported from the package root). It supports webhook-delivered text messages and Bot API `sendMessage` only. The host contributes its exact webhook route through XNode `_routes`.

For current exports, route behavior, secret verification, normalization, send mapping, safe errors, and non-goals, read [telegram.md](references/telegram.md).

## Route Common Tasks

- Add a messaging provider: usually `packages/xagent-channels`, not `packages/xagent`.
- Change Agent identity, routing, Channel ownership, DTOs, or message lifecycle: `packages/xagent`.
- Add persistent conversations, messages, participants, identity mapping, inbox/outbox, history, or memory: application/Starter/capability work, not Agent core.
- Add Pulse customer logic: Pulse product/domain code.
- Add a provider-neutral HTTP route contribution mechanism: XNode concern. Reuse current `_routes` before changing it.
- Add provider webhook handling: provider package using generic XNode route contribution; XNode stays provider-neutral.

## PLANNED / NOT YET IMPLEMENTED

The current `xpell-agent` Starter implements generic `conversation_participant`, `channel_identity`, `conversation`, `message`, and protected `agent_action` persistence. Product plugins such as Pulse own `customer` and other business entities. These remain application-layer contracts, not `@xpell/agent` runtime entities or DTOs.

`@xpell/agent` itself provides no persistent conversation system, customer/user model, identity framework, history, memory, XAI behavior, tools/actions, queue, inbox/outbox, scheduler, campaign system, or capability installer.

## Completion Checks

- Preserve `_snake_case` runtime fields and Xpell structured response/error conventions.
- Verify public APIs against package exports and package manifests.
- Add or update package-local tests at the layer being changed; keep provider tests network-free through injected dependencies where current patterns permit.
- Confirm external ingress uses `_x.execute`, outbound uses direct owned-Channel send, and no raw provider payloads, secrets, tokens, or response bodies cross safe boundaries.
- State explicitly which work is implemented now and which is only planned.
