# Architecture

## Trace the selected profile

- The normal `server/src/main.ts` composes the filesystem XDB Router and Auth modules in XNode. Guarded SQLite candidate and staging launchers have distinct composition, storage, and operation allowlists. Trace the running launcher and its admission result before drawing conclusions about the deployed database or feature set.
- Follow the allowed Wormholes v2 command through the gateway, `_x.execute`, module authorization, and the relevant service or repository. External HTTP compatibility stays at the transport boundary. Keep authorization in trusted server context and persistence in repositories. Use the existing Xpell structured response and `_snake_case` conventions.
- Trace provider dispatch through `generate`. The standalone `route` operation is a placeholder in the reviewed source. The existing generate contract accepts explicit provider/model inputs in supported paths. Preserve those callers and leave default routing policy in Router. Provider tools and responses are data. The authorized consumer owns tool execution.
- Read the selected profile's entity definitions and tests for actual IDs, scopes, and operations. Use `AGENTS.md` for architectural constraints. Confirm exact storage and API contracts in source before changing them. Check Knowledge decisions before treating a new backend or migration plan as approved.

Start with `server/src/main.ts`, `server/src/runtime/RouterGateway.ts`, `server/src/candidate/RC1Composition.ts`, `server/src/staging/StagingMain.ts`, and `server/src/modules/XAIRouter/XAIRouterModule.ts`. Use `docs/runtime-foundation.md` and the Router Knowledge capability matrix to locate specific repositories and tests.
