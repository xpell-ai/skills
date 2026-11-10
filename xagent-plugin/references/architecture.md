# Agent Plugin V1 architecture

Read this reference when creating a plugin, changing composition/bootstrap,
deciding code placement, or considering persistence, context, XVM, or client
contributions.

## Boundary and dependency direction

An Agent Plugin is an application/product extension of the generic Agent
Starter. It is not an `XModule`, Channel, XVM app, or dynamically installed
package. It may explicitly contribute complete protected XVM system apps, but
the plugin and each contributed XVM app remain distinct concepts.

```text
@xpell/agent + @xpell/agent-channels
                 ↓
         generic Agent Starter
                 ↑
       explicitly composed plugin
```

The plugin may import the Starter's public contracts. The Starter must not
import the product plugin.

Use `plugins`, not `apps`: in Xpell, an app already means an XVM application.
An Agent Plugin may own XVM resources under its directory and explicitly
contribute them to bootstrap; it does not become an XVM app itself.

## Current contract and validation

`server/src/plugins/AgentPlugin.ts` exports:

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

`composeAgentPlugins(...)` receives generic capabilities and an optional plugin
array. It validates definitions, preserves generic-first/plugin-order capability
composition, composes application-context providers, and returns frozen plugin
and capability arrays plus the optional composed provider.

Plugin IDs must match lowercase kebab case:

```text
^[a-z0-9]+(?:-[a-z0-9]+)*$
```

Plugin IDs are unique. Capability IDs are globally unique across generic
capabilities and every plugin. Current composition errors are:

- `E_STARTER_AGENT_PLUGIN_INVALID`
- `E_STARTER_AGENT_PLUGIN_DUPLICATE_ID`
- `E_STARTER_AGENT_PLUGIN_DUPLICATE_CAPABILITY_ID`

Invalid application-context and XVM contribution shapes use
`E_STARTER_AGENT_PLUGIN_INVALID`. Capability definition failures use the Starter
capability errors rather than a separate plugin validation runtime.

## Static composition

`createStarterRuntime(...)` constructs the generic capabilities:

```text
agent.conversation_stats
agent.help
```

It then calls `composeAgentPlugins` with `_plugins`, and passes the resulting
capability array into the existing `StarterAgent`. The default is an empty
plugin array.

A product entrypoint follows the current Pulse pattern:

```ts
import { main as startAgentStarter } from "xpell-agent-starter-server";
import { productPlugin } from "./ProductPlugin.js";

startAgentStarter({ _plugins: [productPlugin] });
```

This entrypoint is the one obvious registration point. Do not scan the
filesystem, use dynamic imports, or register by import side effect.

## Directory convention

Use the current workspace pattern when those parts are needed:

```text
xpell-agent/
├── server/                       # generic Agent runtime
├── client/                       # generic protected Agent Console
└── plugins/
    └── <plugin-id>/
        ├── server/
        │   ├── <Product>Plugin.ts
        │   ├── main.ts           # explicit composition entrypoint
        │   ├── index.ts
        │   ├── capabilities/
        │   └── <domain>/         # repositories/services/projections as needed
        ├── client/               # reserved; no automatic composition today
        ├── xvm/                  # authoritative contributed system-app source
        │   ├── app.json
        │   └── entities/         # only when product persistence is needed
        ├── test/
        ├── package.json
        └── tsconfig.json
```

Do not create unused placeholders merely to match the diagram. `plugins/pulse`
is the authoritative example.

## Placement decisions

| Concern | Owner today |
| --- | --- |
| Agent identity, routing, lifecycle, Channel ownership | `@xpell/agent` |
| Telegram/provider adaptation | `@xpell/agent-channels` |
| Generic conversation records and orchestration | generic Starter |
| Product capabilities and business rules | `plugins/<plugin-id>/server` |
| Product/domain persistence | plugin XVM entity + plugin repository/service through EntityManager |
| Model-safe product/domain context | plugin `_application_context` through existing Context Manager |
| Product UI | `plugins/<plugin-id>/client`; composition deferred |
| Protected product XVM system app/entities | `plugins/<plugin-id>/xvm`; explicitly contributed through `_xvm._system_apps` |

The generic Starter owns `conversation_participant`, `channel_identity`,
`conversation`, `message`, and the protected `agent_action` confirmation/execution
audit. Business, customer, consent, reward, follow-up, and similar domain entities
belong to the product plugin.

## Protected XVM system-app contribution

`AgentPlugin._xvm._system_apps` is an explicit list of complete ServerXVM
system-app source directories:

```ts
const productPlugin: AgentPlugin = Object.freeze({
  _id: "product",
  _xvm: Object.freeze({
    _system_apps: Object.freeze([
      Object.freeze({ _path: PRODUCT_XVM_PATH }),
    ]),
  }),
});
```

The implemented bootstrap flow is:

```text
registered plugins
  -> explicit _xvm._system_apps paths
  -> validate each complete app and unique app ID
  -> copy base + contributed apps to derived work/runtime/xpell-agent/system-xapps
  -> pass that single derived root to ServerXVM
  -> ServerXVM registers app entities with EntityManager
  -> selected EntityProvider persists records
```

ServerXVM accepts one system-app root, so `PluginSystemApps.ts` materializes a
derived root only when contributions exist. With zero contributions it returns
the original base system-app path unchanged. The derived root is runtime output,
not source of truth.

Keep authoritative product XVM files under `plugins/<plugin-id>/xvm`. Do not
copy product definitions into the generic Starter, discover plugin folders by
filesystem scan, or treat `_system_apps` as loose-resource merging. Current
composition copies complete system-app directories keyed by their `app.json`
application ID; it does not merge a plugin's entities/views/flows into another
application. Duplicate app IDs and invalid sources fail before startup with the
safe materialization errors implemented in `PluginSystemApps.ts`.

## Application context contribution

`AgentPlugin._application_context` uses the existing Context Manager provider:

```ts
type ApplicationContextInput = Readonly<{
  _actor: ActorContext;
  _conversation: PersistedInboundConversationTurn;
  _conversation_id: string;
  _inbound_message_id: string;
  _current_text: string;
}>;

type ApplicationContextProvider = (
  input: ApplicationContextInput,
) => unknown | Promise<unknown>;
```

Composition calls registered plugin providers in plugin order, omits undefined
results, and namespaces defined results by plugin ID. The Context Manager then
places the composed value under `_context._application` for XAI. A minimal
Pulse business projection has this shape (not the full current inventory):

```ts
{
  _application: {
    _plugins: {
      pulse: {
        business: {
          name,
          business_type,
          description?,
          timezone,
          currency,
          status,
        },
      },
    },
  },
}
```

If a base application-context provider and plugin providers both contribute,
the composed value is `{ _base, _plugins }`. With only the base provider, the
base provider remains unchanged. With no defined contribution, application
context is omitted. Do not add another Context Manager.

Application context is knowledge, not permission. Derive it from trusted
application data, return only model-safe fields, and enforce the policy supported
by the trusted input. The current input includes the persisted inbound turn.
Pulse checks the frozen Business App scope, participant, authoritative Owner
Console authentication, or independently authorized Customer channel/entry.
Owner and Customer projections are separate; an external actor is not an Owner.
Owner preferences do not grant permissions. Verify current product source before
extending these projections. Do not expose raw entity records, auth internals,
secrets, provider credentials, raw provider payloads, or unrelated customers.
If the trusted input cannot establish the required scope, fail closed rather
than trusting client/model fields or constructing a second context system.

## Product persistence

The proven persistence path is:

```text
plugin-owned XVM entity
  -> ServerXVM
  -> app-scoped EntityManager command surface
  -> selected EntityProvider
```

Keep repositories and services inside the plugin. They should use the
`entity-manager` command surface rather than import or query SQLite directly.
Provider selection stays an application/runtime concern. Pulse's `business`
entity currently proves durable SQLite storage, but SQLite is not part of the
plugin contract.

Generic Participant, ChannelIdentity, Conversation, Message, and Action records
remain Starter-owned, outside `@xpell/agent`. Do not move product records into
those schemas or product entities into generic Agent source.

## Development seeds

Development/demo data is explicit and opt-in. Follow the Pulse convention:

- expose a named development seed command;
- make demo values clearly synthetic;
- do not invoke seeds during ordinary startup;
- do not silently initialize, replace, or overwrite product data in production.

A seed is a development convenience, not plugin lifecycle or migration behavior.

## Authorization and removal

Composition establishes what capabilities are available to policy; it does not
authorize them. `CapabilityResolver` receives trusted Actor/Conversation context
and the available list for each turn.

Current default policy permits the authenticated configured private Console
owner and returns no capabilities for Telegram/external actors. Product-specific
authorization rules belong in an explicitly designed resolver policy, never in
tool descriptions or model prompts.

Maintain both invariants:

```text
zero plugins -> generic Agent builds and runs
plugin removed from bootstrap -> contributions disappear; generic code unchanged
```

## Pulse ownership example

The initial `plugins/pulse` contribution demonstrates:

- read-only `pulse.info` and `business.info` capabilities;
- the protected `xpell-agent-pulse` system app with its `business` entity;
- a model-safe business application-context projection;
- an explicit development demo seed command.

`BusinessService`, the `business` entity, `business.info`, and
`createPulseApplicationContext(...)` are examples of correct product ownership,
not requirements for every plugin. The reusable pattern is:

```text
product entity -> product repository/service -> model-safe capability/context
```

The business projection deliberately omits stored phone/address data. The
capability uses a fixed service-backed handler, and `agent.help` discovers it
from effective capabilities without a product-specific catalog.

## Deferred boundaries

Current source does not implement:

- client resources or generic Console extensions;
- arbitrary merging into an existing XVM app;
- filesystem discovery of plugin XVM resources;
- plugin lifecycle, discovery, installation, migrations, dependencies, or
  enable/disable state.

Side-effect capabilities are implemented through the existing Action boundary;
see [capability.md](capability.md). Do not design a replacement confirmation system.

Dropping files into `plugins/<id>/xvm` alone has no runtime effect; the complete
system app must be explicitly registered through `_xvm._system_apps`. Dropping
files into `plugins/<id>/client` has no automatic effect at all. Inspect current
source before extending either boundary.
