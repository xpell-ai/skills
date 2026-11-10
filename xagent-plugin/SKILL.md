---
name: xagent-plugin
description: Create or extend application-local Xpell Agent Plugins under plugins/*, including AgentCapability contributions, protected ServerXVM system apps/entities, and model-safe application context. Use for products such as Pulse or Gator built on the current xpell-agent Starter; do not use for @xpell/agent runtime or provider-Channel changes.
---

# XAgent Plugin

Use this skill with `$xagent` and `$xpell-contract`. Treat the current
`xpell-agent` source and tests as authoritative for application-local plugin
APIs; do not infer fields or infrastructure from this skill.

## Placement rule

Product and domain behavior belongs under `plugins/<plugin-id>`, not in the
generic `server/src` or `client/src`.

- Change `@xpell/agent` only for provider-neutral Agent runtime contracts.
- Change `@xpell/agent-channels` for provider adapters.
- Keep generic conversation infrastructure in the Starter.
- Put product capabilities, policies, XVM entities, persistence services,
  application context, and future product UI in the product plugin.

The dependency direction is always:

```text
plugin -> generic Agent contracts
```

The generic Agent must never import Pulse, Gator, or other product code.

A plugin's protected ServerXVM system app supplies plugin schemas and its
current persistence scope. An installed user XVM app has a separate native
`(_env, _app_id)` identity. When a product needs one deployment-bound user app,
resolve that identity from trusted XVM/deployment settings at product startup,
validate the app's purpose, and freeze the binding before exposing the Agent.
Keep this product policy in the plugin composition; do not let model, owner, or
customer input select an app. A purpose marker alone does not grant access.
This is an optional product pattern, not a requirement for every plugin. Do
not infer that existing plugin records are scoped to the bound user app.
When a product uses the generic Starter's verified optional
`AgentApplicationScope`, pass the validated frozen XVM pair through trusted
bootstrap. The generic Conversation and Action records then carry an indexed
internal scope discriminator while their schema namespace remains the
protected Starter system app. Keep product repository migration separate.

## Current composition

```text
explicit bootstrap plugins[]
  -> plugin validation/composition
  -> generic capabilities + plugin capabilities
  -> CapabilityResolver
  -> allowed XAI tool projections
  -> argument validation
  -> reauthorization
  -> fixed handler
```

The current contract is exactly:

```ts
type AgentPluginSystemAppContribution = Readonly<{
  _path: string;
}>;

type AgentPluginXVMContribution = Readonly<{
  _system_apps?: readonly AgentPluginSystemAppContribution[];
}>;

type AgentPlugin = Readonly<{
  _id: string;
  _capabilities?: readonly AgentCapability[];
  _application_context?: ApplicationContextProvider;
  _xvm?: AgentPluginXVMContribution;
}>;
```

`ApplicationContextProvider` is the existing `ConversationContextManager`
provider contract:

```ts
type ApplicationContextProvider = (
  input: Readonly<{
    _actor: ActorContext;
    _conversation: PersistedInboundConversationTurn;
    _conversation_id: string;
    _inbound_message_id: string;
    _current_text: string;
  }>,
) => unknown | Promise<unknown>;
```

Current explicit composition has three independent contribution paths:

```text
registered plugins
  ├─ capabilities -> CapabilityResolver -> XAI tools
  ├─ application context -> namespaced _application._plugins -> Context Manager -> XAI
  └─ XVM system apps -> derived runtime system-app root -> ServerXVM -> EntityManager
```

Do not add lifecycle hooks, discovery, manifests, dependencies, installation,
registries, enable/disable state, sandboxing, or dynamic loading unless a task
explicitly requests new architecture.

For bootstrap, directory, placement, duplicate-ID, removal, XVM, persistence,
application-context, seed, and deferred client details, read
[references/architecture.md](references/architecture.md).

## Choose only the required contributions

| Need | Add |
| --- | --- |
| Model may perform a product read | `_capabilities` with fixed handlers |
| User requests a supported write/external effect | a side-effect capability through the existing durable Action boundary; see the capability reference |
| Product data must be durable | plugin-owned XVM system app/entity plus an EntityManager-backed repository/service |
| Model should know safe product facts | `_application_context` returning a minimal authorized projection |
| Local demo data is useful | an explicit opt-in development seed command |
| Product UI is required | inspect current client loading first; plugin client composition remains deferred |

Do not create unused directories or contributions. A product entity does not
automatically require a capability, model context, seed, or client surface.

## Create or extend a plugin

1. Inspect the current `AgentPlugin`, `AgentCapability`, resolver, Agent tool
   loop, and the nearest plugin tests before editing.
2. Create or reuse `plugins/<plugin-id>`; add only directories needed now.
3. Define `<Product>Plugin` with a stable lowercase-kebab `_id` and only the
   required `_capabilities`, `_xvm`, and `_application_context` contributions.
4. Put capability factories under `server/capabilities/`; keep product
   repositories/services under the plugin's `server/` tree; keep authoritative
   XVM resources under `plugins/<plugin-id>/xvm`.
5. Register the plugin explicitly in a product/bootstrap entrypoint by passing
   `_plugins: [plugin]`; never make the generic Starter import it.
6. Keep `CapabilityResolver` authoritative for turn-specific exposure and
   reauthorization.
7. Verify `agent.help` discovers authorized contributions without a second
   catalog.
8. If product data needs demo content, expose an explicit development-only seed
   command. Never run it during normal startup.
9. Test plugin-present, plugin-absent, unauthorized, fabricated-call, schema,
   duplicate-ID, contributed-system-app, application-context safety, durable
   persistence, and generic/Telegram regression behavior with mocked XAI.

When adding a capability, read
[references/capability.md](references/capability.md) before implementation.

## Hard guardrails

1. Product code stays under `plugins/<plugin-id>`.
2. Generic Agent code never imports a product plugin.
3. Plugins are statically composed; there is no magic discovery.
4. Registration does not imply authorization.
5. The LLM is never an authorization authority.
6. Model tool calls and arguments are untrusted.
7. Capabilities bind to fixed application handlers.
8. Never expose arbitrary `_module`, `_op`, tenant, actor, or authorization
   selection to the model.
9. `agent.help` derives from effective capabilities.
10. Keep generic persistence limited to product-neutral conversation records
    and the protected `agent_action` confirmation/execution audit.
11. Reads use `confirmation: "none"`; side effects require the existing Action
    preparation, explicit confirmation, reauthorization, integrity and execution
    claim path. Read-only questions and ambiguous requests must not prepare Actions.
12. XVM contributions are explicit complete system-app directories; do not scan
    plugin folders or imply arbitrary app/entity/view/flow merging.
13. The authoritative XVM source stays under `plugins/<plugin-id>/xvm`; never
    copy product entity definitions into generic Agent source.
14. Plugin application context is trusted, authorized, model-safe data passed
    through the existing `ConversationContextManager`; never add another context
    manager or expose storage/auth/provider internals.
15. Product repositories use the app-scoped EntityManager command surface and
    selected EntityProvider, never direct SQLite access.
16. Development/demo seeds are explicit opt-in commands, synthetic, and never
    automatic production-startup initialization or overwrite behavior.
17. Client contribution remains deferred; inspect current source before adding
    a plugin client surface.
18. Preserve the zero-plugin build/run path.

## Controlled provider operations

For a supervised live-provider experiment or diagnosis of an interrupted send,
read [controlled-provider-actions.md](references/controlled-provider-actions.md).
It covers consent, exact Action approval, single-use release, state reconciliation,
restricted ingress, rollback, and evidence-based Owner errors. It grants no live
execution permission and does not change product policy or Source of Truth.

## Source authority

Inspect these stable locations before API-sensitive work:

- `xpell-agent/server/src/plugins/AgentPlugin.ts`
- `xpell-agent/server/src/plugins/PluginSystemApps.ts`
- `xpell-agent/server/src/capabilities/AgentCapability.ts`
- `xpell-agent/server/src/capabilities/CapabilityResolver.ts`
- `xpell-agent/server/src/actions/ActionService.ts`
- `xpell-agent/server/src/conversation/ConversationContextManager.ts`
- `xpell-agent/server/src/Agent.ts`
- `xpell-agent/server/src/runtime.ts`
- `xpell-agent/plugins/pulse/server/PulsePlugin.ts`
- `xpell-agent/plugins/pulse/server/business/`
- `xpell-agent/plugins/pulse/xvm/`
- `xpell-agent/server/test/plugins.test.mjs`
- `xpell-agent/plugins/pulse/test/`

## Completion checks

- The generic Starter still works with `_plugins: []`.
- Removing registration removes the plugin's capabilities without generic edits.
- Authorized actors see only resolver-approved tools.
- External/Telegram actors do not receive private tools and fabricated calls fail.
- Arguments are validated and authorization is checked again before the handler.
- `agent.help` reflects the effective capability set exactly once.
- Duplicate plugin and capability IDs fail during composition.
- Contributed system apps are explicit, protected, and registered through
  ServerXVM/EntityManager; zero contributions preserve the base root.
- Application context is namespaced under `_application._plugins.<plugin-id>`
  and contains only authorized model-safe projections.
- Product repositories use EntityManager and persistence survives restart when
  durability is required.
- Demo seeds are explicit and do not run during ordinary startup.
- No client composition is claimed unless current source implements it.
- Tests use mocked XAI and do not require paid providers.
- State what is implemented now and what remains deferred.
