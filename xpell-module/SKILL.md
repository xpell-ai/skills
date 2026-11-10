---
name: xpell-module
description: Create, modify, register, test, and verify reusable Xpell modules under modules/* using the canonical Xpell module contract, including server, client, and shared/multi-target profiles.
---

# Xpell Module

Use this skill when creating, modifying, registering, testing, or verifying reusable Xpell modules under `modules/*`.

This skill covers:

- server modules loaded by XNode or another server Xpell runtime
- client modules loaded by the browser/XUI runtime
- shared or multi-target packages that expose separate client/server entrypoints plus shared contracts

This skill does not create new runtime APIs unless the user explicitly asks for runtime implementation work.

## Binding Contract

At the start of every task:

1. Read `docs/xpell-module-contract.md`.
2. Treat it as the normative source of truth for reusable module work.
3. Inspect existing module/runtime code before changing files.
4. Check whether the requested capability or operation already exists.
5. Determine runtime target: `server`, `client`, or `shared`.
6. Never invent Xpell APIs, runtime behavior, module paths, upload systems, hot-loading semantics, or registration conventions.

This skill is operational guidance only. If it appears to conflict with `docs/xpell-module-contract.md`, follow the contract.

## Current Runtime Truths

Apply these source-derived constraints:

- Client modules are first-class `XModule`s.
- Server modules are first-class `XModule`s.
- Invocation uses `_x.execute({ _module, _op, _params })`.
- Operation metadata uses the proven keyed `_ops` contract: `Record<string, XpellSkillCommand>`.
- Normal npm/workspace modules require install, build, explicit registration, and restart today.
- Hot loading applies only to `module-creator` generated server JavaScript modules.
- `module-creator` is not a generic npm/workspace module loader.
- Generic Xpell file refs and generic upload are not implemented yet.
- Existing `.xapp` upload is specialized app-package transfer, not a generic file service.
- Client modules use explicit browser/XUI runtime registration.
- XVibe discovery differs for server skills and client-synced skills.
- XMCP remains curated and permissioned; it does not automatically expose every module operation.

## Module Location

Reusable modules belong under:

```text
modules/<module-id>/
```

Each `modules/<module-id>/` folder is an independent npm-ready package. `modules/` is a container folder, not one combined package.

Prefer capability-first package structure:

```text
modules/<module-id>/
```

For shared or multi-target modules, split entrypoints inside the package:

```text
modules/<module-id>/
  src/
    client/
    server/
    shared/
```

Do not use top-level `modules/client/*` or `modules/server/*` as the default structure unless the repository already establishes that pattern or the user explicitly requests it.

## Discover

Before creating or changing a module:

- inspect the current repository tree, package manager setup, and workspace config
- inspect existing modules under `modules/*` and runtime-local module folders
- inspect server bootstrap and explicit XNode module registration for server targets
- inspect browser/XUI runtime registration for client targets
- inspect current runtime skill/capability discovery paths
- search `_ops`, `_skill`, `_name`, `_runtime`, `_scope`, and existing `_x.execute` usage
- determine whether an existing module or operation already satisfies the request

Do not create a new module merely because an existing module is missing one operation. Prefer extending the existing module when that preserves the capability boundary.

## Target Decision

Before editing, classify the requested capability.

Choose `server` when the module needs:

- Node APIs
- filesystem or server persistence
- provider secrets
- server-side auth policy
- server-side network/provider calls
- XMCP-visible server capability summaries

Choose `client` when the module needs:

- browser APIs
- DOM, canvas, WebGPU, Web Workers, local browser storage, or local browser AI
- no provider secrets
- direct browser `_x.execute` execution
- XUI runtime registration

Choose `shared` when the package legitimately needs:

- a browser module
- a server module
- shared types, schemas, constants, or operation contracts

For shared packages, keep client and server entrypoints separate. Shared code must stay platform-neutral.

## Plan

Before editing, determine:

- stable module ID
- npm package name
- runtime target
- package entrypoints
- operation IDs
- input and output schemas
- structured error contract
- app/runtime scope
- side effects
- config requirements
- secret requirements
- readiness checks
- permissions
- file-reference needs
- registration path
- runtime discovery path
- test strategy
- semver impact for existing modules

Keep modules reusable across apps. App-owned operations must explicitly respect `_app_id` and `_env`; runtime-global operations must declare the correct scope.

## Implement Common Contract

Create or update only the files required by the selected target profile.

Common implementation rules:

- extend `XModule`
- expose a stable `_name`
- define and export `_ops`
- define and export `_skill`
- make `_skill + _ops` the canonical capability metadata
- preserve the keyed `_ops` shape: `Record<string, XpellSkillCommand>`
- use operation methods that match `_op` dispatch, such as `_analyze_image` for `analyze-image`
- accept canonical command execution through `_x.execute({ _module, _op, _params })`
- keep command params JSON-compatible
- return structured success/error payloads or existing Xpell response helpers serialized to transport-safe data
- keep generated/runtime handlers data-only
- declare `_skill._runtime._target`

When modifying an existing module:

- preserve the module ID
- preserve existing operation contracts unless intentionally making a versioned breaking change
- update `_ops`
- update `_skill`
- update exported types
- update README examples
- update tests
- document semver impact when relevant

## Server Profile

Use the server profile when the module runs in XNode or another server Xpell runtime.

Server module package shape usually includes:

```text
modules/<module-id>/
  package.json
  tsconfig.json
  README.md
  src/
    index.ts
    <ModuleName>Module.ts
    contract.ts
    types.ts
  tests/
```

Server profile rules:

- keep Node/server dependencies out of client bundles
- declare `_skill._scope` as `"server"` or `"app"` as appropriate
- declare `_skill._runtime._target` as `"server"`
- use a factory as the preferred registration surface
- register explicitly in server bootstrap
- do not scan `modules/*`
- do not auto-load installed packages
- do not hide enabled capabilities behind import side effects

Normal source/npm server modules currently require:

```text
install -> build -> explicit registration -> restart
```

Do not claim live loading for normal workspace/npm modules.

## Client Profile

Use the client profile when the module runs in the browser/XUI runtime.

Client module rules:

- extend `XModule`
- expose `static _ops` and `static _skill`
- declare `_skill._type` or exported metadata compatible with `client-module-api`
- declare `_skill._scope` as `"client"` or `"app"` as appropriate
- declare `_skill._runtime._target` as `"client"`
- register explicitly through browser/XUI runtime loading
- avoid Node APIs, filesystem access, server persistence, and server-only packages
- avoid arbitrary remote script loading
- treat client-authored auth/session fields as untrusted

Client registration must follow the repository's current XUI runtime pattern, such as built-in XUI runtime module loading or caller-provided modules passed to the browser runtime.

Client discovery must be verified in the browser runtime with `_x.getSkills()` and, when relevant, through client runtime skill sync to XVibe.

## Shared / Multi-target Profile

Use the shared profile only when one reusable package legitimately exports both client and server capabilities.

Preferred shape:

```text
modules/<module-id>/
  src/
    client/
    server/
    shared/
```

Rules:

- client entrypoints must not import server entrypoints
- server entrypoints must not import browser-only client entrypoints
- shared code must remain platform-neutral
- shared code may contain schemas, types, operation IDs, constants, and JSON-compatible helpers
- package exports must make target boundaries explicit
- each runtime entrypoint must expose its own `_skill`, `_ops`, and runtime target metadata when behavior differs

Do not force a shared package when separate packages better preserve runtime boundaries.

## Config, Secrets, And Readiness

Distinguish public config, secrets, and readiness.

- Declare required and optional config in metadata.
- Declare secrets without exposing values.
- Missing required config should make the module discoverable but not ready.
- Operation handlers that require missing config must produce structured not-ready errors.
- Never write real credentials into source, tests, README, `_skill`, `_ops`, logs, XData, or examples.

## File-Consuming Modules

Generic Xpell file refs and generic upload are not implemented yet.

For modules that consume files:

- read the file-reference section in `docs/xpell-module-contract.md`
- inspect current file/upload APIs before implementing
- do not invent a new upload system inside an individual module
- do not treat `.xapp` package upload as a generic file service
- do not pass large binary payloads raw through `_params`
- use the provisional `XpellFileRef` only as a documented placeholder until a canonical file service exists
- validate type, size, scope, and authorization for any supported file reference

If a requested feature requires generic upload, document that runtime support is missing unless the user explicitly asks to build that service.

## Hot Loading

Hot loading today applies only to `module-creator` generated server JavaScript modules.

Use `module-creator` semantics only when the task is specifically about generated modules.

Do not apply generated-module hot loading rules to reusable npm/workspace packages.

Do not create:

- a live npm loader
- arbitrary package path loading
- runtime module scanning
- reload/unload behavior

unless the user explicitly asks for runtime implementation work and the security model is designed first.

## Register

Registration must be explicit in the correct runtime.

For server modules:

- update dependencies as needed
- update server bootstrap according to the current repository structure
- keep enabled capabilities auditable

For client modules:

- update browser/XUI runtime registration according to existing patterns
- ensure the module is included by the relevant client bundle or app bootstrap
- keep enabled client capabilities auditable

Do not:

- add filesystem scanning for `modules/*`
- add side-effect auto-registration
- auto-load all installed packages
- expose every module operation through MCP

## Test

At minimum, verify:

- package builds
- module constructs
- `_name` is correct
- `_ops` exists and is keyed
- `_skill` exists
- `_skill._runtime._target` is correct
- runtime registration succeeds
- `_x.execute` can call an operation
- invalid params produce structured errors
- readiness/config behavior works
- app/env scoping works where relevant
- file references are validated where relevant
- no live external secrets are required by default tests

For server modules, verify server runtime registration and server `_x.getSkills()`.

For client modules, verify browser/XUI runtime registration, browser `_x.execute`, browser `_x.getSkills()`, and XVibe skill sync when relevant.

Use mocks or opt-in integration tests for external providers.

## Verify Runtime Discovery

Verify the loaded module appears through the current supported runtime skill/capability path, such as:

```ts
_x.getSkills()
```

Target-specific discovery:

- server skills are visible from the loaded server runtime
- client skills are visible from the browser runtime after client registration
- XVibe sees client skills only after client runtime skill sync
- XVibe sees server skills after server skill refresh/sync
- XMCP can summarize loaded/synced capabilities through curated capability tooling

Do not claim every module operation is automatically exposed as an MCP tool.

## Security

Always:

- validate external params
- reject unknown file ref types
- validate file types and sizes
- avoid arbitrary local file access
- avoid shell execution unless explicitly required by the module
- add timeouts for external services
- declare side effects
- preserve host authorization boundaries
- keep provider/network permissions narrow and documented
- redact secrets from logs and errors

Admin/developer-only operations must include:

- module generation
- module loading
- package live loading if added later
- arbitrary local path access
- generic file service administration
- MCP-exposed mutation/runtime-control operations

MCP exposure remains intentional and permissioned. XVibe discovers and uses loaded capabilities; do not make XVibe responsible for creating source modules.

## Report

When finished, report:

- files changed
- module/package identity
- runtime target
- operations
- config/secrets
- permissions/scope
- registration
- tests run
- runtime discovery result
- XVibe visibility if applicable
- XMCP visibility if applicable
- any contract gap discovered

## Do Not Use This Skill To

- copy `docs/xpell-module-contract.md` into the skill
- recreate `docs/server-module-contract.md`
- design a new module runtime architecture unless explicitly requested
- create a file upload service
- create a food analyzer
- create a client example module unless explicitly requested
- make a live npm loader
- make an MCP auto-exposure mechanism
- make an XVibe module-generation mechanism
- create a module that is app-specific when the request is for a reusable capability
