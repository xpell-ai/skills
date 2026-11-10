---
name: xpell-vibe
description: XVibe engineering contract for @xpell/node. Use when working on XVibe architecture, terminology, processor ordering, execution pipeline, artifacts, structured editing, mutation plans, conversation state, runtime capability awareness, or persistence boundaries under packages/xnode/src/XVIBE. Source-derived only; do not use for implementation advice unless explicitly requested.
---

# Xpell VIBE Contract

Apply this contract when generating, reviewing, or documenting XVibe behavior in `@xpell/node`.

Requires:

- `xpell-contract`
- `xpell-core`
- `xpell-node`

## Current Truth vs Recommendation

- `Current Truth` means directly verified from current source and may be relied on as implemented behavior.
- `Recommendation` means preferred engineering direction and must not be treated as implemented unless source confirms it.
- Do not mix these labels. When a section contains both, split the claims under the correct label.

## Architecture invariants

- Current Truth: XVibe is an intent, planning, compilation, and execution orchestration layer, not a free-form JSON generator.
- Current Truth: `StructuredViewEdit` is the authoritative structured view mutation path; do not introduce a second view mutation engine.
- Current Truth: executable semantic edit actions are canonicalized and preflighted before an execution payload is accepted.
- Current Truth: view mutation execution resolves a real project view before persistence and object targeting uses the shared target resolver.
- Current Truth: server-side `xvibe`/`server-xvm` owns authoritative mutation, persistence, logging, and transport fanout boundaries; clients do not execute individual primitives.
- Current Truth: mutation plans contain `xvibe.apply-view-edit` primitive descriptors and execute sequentially through server commands.
- Current Truth: `xpell-node` remains authoritative for `_x.execute`, Wormholes, ServerXVM persistence, logging, and transport boundaries.
- Recommendation: generated persisted XUI objects should have stable `_id` values at persistence/render boundaries.
- Recommendation: eligibility, execution, retry/no-op detection, and plan execution should use the same resolution contract.
- Recommendation: sequential plan steps should load the latest persisted state before each step.
- Recommendation: conversation artifacts should be treated as immutable server records; local UI state may overlay them only by stable conversation id + message id.

## Common failure patterns

- Primitive-specific target resolver: extend shared canonicalization/view/target resolution; raw provider action validated before canonicalization: canonicalize first, then validate allowlists.
- Action marked executable before view/target preflight: create `_execution_payload` only after successful preflight; model-generated view/object ids trusted: resolve against persisted project views and current view JSON.
- Planning resolves objects against stale state: resolve during execution and reload between composed steps; client-side primitive execution: client may request/confirm/observe, server executes.
- Duplicate mutation path: route through `StructuredViewEdit`/existing module op only; direct JSON/file mutation outside `StructuredViewEdit` or `server-xvm`: use `server-xvm.push_update`.
- Helper-only tests pass while prompt/runtime/persistence fails: add real prompt acceptance coverage; exact-id-only tests: include visible-text and normalized-text target cases.
- Missing retry/idempotency coverage: assert no-op/already-completed or explicit failure behavior; later mutation-plan steps use stale state: reload latest persisted view per composed step.
- Server/client artifact payload mismatch: test end-to-end payload identity and rendering; artifact object identity or array index used for conversation state: use conversation id + message id.
- Success reported without persistence or refresh: verify ServerXVM result and broadcast/refresh path; untested capability advertised: guidance must list only tested user-visible capabilities.

## Debug flow

Follow this order and use the documented log families in `SKILL_API_MAP.md`:

1. Was the intended processor matched? Check `[xvibe] processor matched/null/fallback`.
2. Was semantic AI bypassed when deterministic behavior should own the prompt? Check capability, mutation-plan, deterministic, and semantic disabled/request logs.
3. Was the raw action canonicalized? Check semantic normalization and canonicalization fields.
4. Is the canonical action allowlisted? Check validation/non-executable reason logs.
5. Was the requested view resolved to a real persisted view? Check semantic view resolved and structured view edit source logs.
6. Was the target resolved through the shared resolver? Check resolved target fields or target rejection reason.
7. Did semantic preflight mark executable only after successful resolution? Check `_executable`, `_execution_payload`, and `_non_executable_reason`.
8. Was a valid `_execution_payload` created? It must target `xvibe.apply-view-edit` for view primitives.
9. Did execution use `_x.execute` and `StructuredViewEdit.apply(...)`? Check module op and structured edit logs.
10. Did the latest persisted view load for each composed step? Check `server-xvm.get_view`/step execution logs.
11. Did ServerXVM persist and create the expected backup/version? Check `server-xvm.push_update`, version, and backup logs.
12. Was the update broadcast? Check `wsBroadcastScoped`/`xvm:update` and structured active-view refresh logs.
13. Was conversation/action status updated? Check conversation action/artifact update logs.
14. Did XStudio refresh and render the returned state? Check client-side XVM update/render observation outside XVibe server code.

## 1) Applies to / Scope

- Applies to `packages/xnode/src/XVIBE/**`.
- Applies to `XVibeModule`, `XVibeIntentEngine`, processors, structured editing, conversation state, runtime context, capability registries, artifact execution, execution graph planning/execution, and run archives.
- Applies to code reachable through `@xpell/node` top-level XVIBE exports.
- Keep this file as the compact contract. Load `SKILL_API_MAP.md` for exact source symbols and `SKILL_CHECKLIST.md` before merge/review.

## 2) Core identity

XVibe is a server-side Xpell generation and intent orchestration layer inside `@xpell/node`.

It provides:

- module command surface: `XVibeModule` with module name `xvibe`;
- intent analysis: `XVibeIntentEngine` and ordered processors;
- artifact orchestration for views, apps, flows, entities, commands, generated module specs, artifact requests, and CRUD execution graphs;
- deterministic structured view editing through `xvibe.apply-view-edit`;
- compiled mutation-plan artifacts executed through `xvibe.apply-mutation-plan`;
- conversation storage and intent analysis records;
- runtime awareness from Project Memory, app assets, and runtime skills.

It is not:

- a browser/UI runtime;
- a persistence database;
- a replacement for `server-xvm`;
- a direct loader/compiler for generated XModules;
- a place for hidden AI mutation paths.

## 3) Public surface

- Package root `packages/xnode/src/index.ts` re-exports `./XVIBE/index.js`.
- XVIBE root exports include `XVibeModule`, `XVibePlanner`, `VibeOutputParser`, `VibeKnowledgeSelector`, `VibeIntentPlanner`, `VibeBehaviorPlanner`, `VibePromptBuilder` helpers, `XVibeCapabilityRegistry`, capability types, behavior/runtime asset types, and all `XVibeTypes`.
- `XVibeModule._name` is `xvibe`.
- `XVibeModule._skill` is a server-module API skill requiring `xmodule`, `xai`, `server-xvm`, and `module-creator`.

## 4) Module command surface

Current module ops are:

- `generate`
- `plan-app`
- `generate-view`
- `get-guide-recommendation`
- `confirm-project-plan`
- `apply-view-edit`
- `apply-mutation-plan`
- `fix-project-views`
- `analyze-project-views`
- `apply-artifact-request`
- `execute-execution-graph`
- `generate-app`
- `create_app_from_starter`
- `generate-module-spec`
- `get-latest-run`
- `create-conversation`
- `list-conversations`
- `get-conversation`
- `append-message`
- `analyze-message`
- `get-last-messages`
- `update-conversation-action`
- `update-conversation-artifact`
- `sync-skills`

Rules:

- External callers must route through `_x.execute({ _module: "xvibe", _op, _params })` or the XModule dispatch path.
- Do not treat private helper methods in `XVibeModule.ts` as module ops.
- Do not add runtime ops without updating `_ops`, `SKILL_API_MAP.md`, and tests.

## 5) Canonicalization contract

Current Truth:

- Structured edit action names are canonicalized by `canonicalizeSemanticViewEditParams(...)` and `readStructuredViewEditAction(...)`.
- Supported canonical structured actions are exactly:
  `set-property`, `update-property`, `remove-property`, `set-style`, `set-styles`, `remove-style`, `add-class`, `remove-class`, `replace-class`, `toggle-class`, `remove-object`, `hide-object`, `show-object`, `move-object`, `replace-object`, `duplicate-object`, `add-child`, `create-toolbar`, `set-interaction`.
- Alias groups include hide/show/remove/delete, duplicate/copy, move, class actions, property actions, style batch actions, child-add actions, toolbar-create actions, `set-interaction`, and `replace-object`.
- `update-style`, `update-styles`, `set-styles`, and style/property batch aliases canonicalize into supported edit actions before validation.
- Canonicalization rejection reasons are `invalid_edit_action`, `unsupported_edit_action`, `unsupported_property_batch`, and `ambiguous_edit_action`.
- `normalizeProjectViewId(...)` trims, lowercases, hyphenates camel/space/underscore forms, strips unsupported characters, collapses hyphens, and trims leading/trailing hyphens.
- `normalizedVisibleTargetText(...)` performs target text/id normalization for target resolution.
- Learned intent prompts are normalized by `normalize_learned_intent_prompt(...)` before lookup/storage.
- Execution graph and artifact processors perform their own entity/field normalization; do not reuse view-edit canonicalization for entity schema semantics.

Recommendation:

- Add a new alias only when it maps to one existing canonical action and has source tests at the canonicalization and execution boundary.
- Do not document a natural-language synonym as supported unless it is present in the alias map or processor code.

## 6) Intent engine and processor contracts

Current Truth:

- `XVibeIntentEngine.analyze(...)` validates request shape, `_message`, `_runtime_context`, `_runtime_context._app_id`, and `_runtime_context._env`.
- Before processors run, `RuntimeContextManager.attachProjectMemoryToRuntimeContext(...)` enriches runtime context when `_app_id` and `_env` are present.
- Processors implement `XVibeIntentProcessor.analyze(request): Promise<XVibeIntentResult | null>` and may expose `_diagnostic_reason()`.
- The engine returns the first non-null processor result.
- The fallback intent is conversation-only with `_execution_level: "none"`, `_should_mutate: false`, `_confidence: 0`, and no actions.

Processor order is exact:

1. `CapabilityGuidanceProcessor`
2. `MutationPlanningProcessor`
3. `DeterministicIntentProcessor`
4. `ProjectMemoryFocusProcessor`
5. `PlanningSessionProcessor`
6. `PlanningProcessor`
7. `LearnedIntentProcessor`
8. `EntityProcessor`
9. `FlowProcessor`
10. `FormProcessor`
11. `TableProcessor`
12. `CrudProcessor`
13. `AddFieldProcessor`
14. `RenameFieldProcessor`
15. `DeprecateFieldProcessor`
16. `DeleteFieldProcessor`
17. `RestoreDeprecatedFieldProcessor`
18. `SemanticIntentProcessor`

Processor contracts:

- Intent analysis does not mutate app/view/entity/flow state. It returns data artifacts, action descriptors, or module-op descriptors.
- `CapabilityGuidanceProcessor` must stay first so capability/help questions are answered deterministically before planning, generic artifact routing, or semantic routing.
- `MutationPlanningProcessor` must stay before direct deterministic edit routing so multi-step prompts become `mutation-plan` artifacts instead of a single edit.
- `LearnedIntentProcessor` must stay before generic artifact processors and before semantic routing so verified learned intents can short-circuit later inference.
- CRUD field processors must stay after the generic CRUD processor order shown above unless source tests are updated.
- `SemanticIntentProcessor` is last and is gated by `XVIBE_SEMANTIC_INTENT_ENABLED` plus provider availability/capability. It is an intent normalizer/preflight path, not a hidden mutation path.

## 7) Execution pipeline

Current Truth:

- `generate` / `generate-view` delegate to `GenerationManager`, which calls the module's artifact generator.
- `generate-app` creates an app shell through `server-xvm.create_app`, pushes a live shell view through `server-xvm.push_update`, sets the active app, plans the app, creates/locks intent and execution plans, generates planned artifacts, and marks generation complete.
- `apply-view-edit` delegates to `StructuredViewEdit.apply(...)`.
- `apply-mutation-plan` validates a compiled mutation plan and executes each primitive sequentially.
- `apply-artifact-request` delegates to `ArtifactExecutor`.
- `execute-execution-graph` delegates to `ExecutionGraphExecutor`.
- Conversation ops delegate to `ConversationManager`.
- `analyze-message` delegates to `IntentConversationBridge`, which invokes `XVibeIntentEngine` and appends a tool message with the intent result.

Rules:

- AI output must become data artifacts, intent results, plans, or explicit module commands before mutation.
- XVibe must not directly load generated XModules; generated module handling is delegated to `module-creator`.
- All app/view/flow/entity persistence goes through `server-xvm` module commands or explicit XVIBE-owned file stores.

## 8) Artifacts

Current Truth:

- Generation artifacts: `view`, `flow`, `entity`, `command`.
- Inferred artifact type: generation artifact plus `module`.
- Intent artifact requests: `entity`, `flow`, `view`, `form`, `table`, `crud-evolution`, `crud-field-suggestion`, `execution-graph`, `project-plan`, `capability-guidance`, `mutation-plan`.
- Structured mutation artifact: `_type: "deterministic-view-edit"`.
- Mutation plan artifact: `_type: "mutation-plan"`.
- Execution graph type: `crud`.
- Run archive files include request/task/runtime/prompt/plan/output/result/summary/timeline/validation diagnostics.

Rules:

- Persisted app/view/flow/entity artifacts must remain JSON/data-only.
- `command` artifacts are returned and announced; they are not persisted as app artifacts by `return_command_artifact`.
- Run archives are diagnostics under app `vibe-runs`, not authoritative app state.

## 9) Structured editing

Current Truth:

- `xvibe.apply-view-edit` is deterministic and has no AI fallback.
- `StructuredViewEdit.apply(...)` canonicalizes params, resolves view/source/target, builds a resolved task and structured intent, checks eligibility, applies a deterministic JSON mutation, verifies the mutated view id, persists, emits update signals, records project-memory completion when applicable, and archives the run.
- `SemanticViewEditPreflight.preflightSemanticViewEdit(...)` canonicalizes semantic edit params and resolves view/target before an intent result is accepted as executable.
- Preflight may annotate params with resolved target/destination fields or `_semantic_non_executable_reason`.
- `ensure_view_ids` may add missing ids during semantic preflight when a persisted view is loaded and ids are needed for target resolution.

Apply-view-edit pipeline:

1. Canonicalize structured view edit params.
2. Resolve the requested/current/source view.
3. Resolve target id/type/text when needed.
4. Build `XVibeResolvedTask` and `StructuredViewEditIntent`.
5. Check deterministic edit eligibility.
6. Apply deterministic mutation to the source view JSON.
7. Verify the mutated view id matches the source view id.
8. Persist via `server-xvm.push_update`.
9. Broadcast/emit update signals.
10. Archive the run.

Supported structured actions:

- `set-property`, `update-property`, `remove-property`
- `set-style`, `set-styles`, `remove-style`
- `add-class`, `remove-class`, `replace-class`, `toggle-class`
- `remove-object`, `hide-object`, `show-object`
- `move-object`, `replace-object`, `duplicate-object`
- `add-child`, `create-toolbar`, `set-interaction`

Rules:

- Source view mismatch must fail instead of persisting another view.
- `server-xvm.push_update` is the persistence boundary.
- `_xem.fire("vibe:view-updated", ...)` is a signal, not persistence.
- `wsBroadcastScoped(...)` is a transport update, not persistence.

## 10) View resolution

Current Truth:

- `resolveProjectViewId(...)` resolves against `server-xvm.list_views` results plus the current view id.
- Available view ids are read from strings or object fields `_id`, `id`, or `_view_id`.
- Strategies are exactly `exact`, `current-view`, `normalized`, `root-alias`, and `target-content-current`.
- If no requested view id is provided and current view exists in available ids, the current view is selected.
- Exact requested id wins before normalized matching.
- Root aliases include `main`, `current`, `active`, `current-view`, and `main-view`; they resolve to `main` or current view when present.
- If a target id/text is present and a current view exists, unresolved requested view text may resolve to current view through `target-content-current`.

Rules:

- Do not infer or create a view id when `resolveProjectViewId(...)` returns not found.
- Do not treat target text as view identity except through the explicit `target-content-current` fallback.

## 11) Target resolution

Current Truth:

- `resolveViewTarget(...)` traverses `_children` and returns a target object, path, type, and resolution strategy.
- Strategies are exactly `id`, `root`, `text`, `normalized_id`, `normalized_text`, and `text_type_id`.
- Visible target text is read from `_text`, `text`, `label`, `title`, `_label`, and `_title`.
- Type aliases are applied for button-like and label/text/title/heading-like targets.
- Root targets require explicit root allowance; otherwise root targeting is rejected.
- Text matching fails when ambiguous and returns an ambiguity reason instead of picking arbitrarily.
- Move-object preflight resolves the destination separately and may normalize `_destination_id`, `_before_id`, `_after_id`, `_resolved_destination_path`, and `_destination_resolved_by`.

Rules:

- Do not silently target the root object unless the source path explicitly allows it.
- Do not treat visible text matches as stable ids; persist the resolved id/path produced by source code when executing.

## 12) Mutation plans

Current Truth:

- `MutationPlanningProcessor` creates multi-step planning artifacts for supported multi-mutation prompts.
- It currently compiles supported plans for deterministic toolbar creation/moves and selected redesign/dashboard/screen planning patterns.
- Unsupported plan steps remain in the plan with `_status: "unsupported"` and a reason.
- Mutation-plan analysis returns `_message_type: "planning"`, `_execution_level: "planning"`, `_should_mutate: false`, and `_artifact_type: "mutation-plan"`.

Artifact shape:

- `_type: "mutation-plan"`
- `_title`, `_goal`, `_summary`
- `_steps`
- `_estimated_mutations`
- `_executable_steps`
- `_unsupported_steps`
- `_can_apply`
- `_status: "planned"`
- placeholder buttons: `apply-plan`, `edit-plan`, `cancel-plan`

Executable primitive shape:

```json
{
  "_module": "xvibe",
  "_op": "apply-view-edit",
  "_params": {}
}
```

Execution rules:

- `xvibe.apply-mutation-plan` accepts only compiled plans with `_type: "mutation-plan"` and `_can_apply: true`.
- Every planned step must contain a primitive exactly equal to `{ _module: "xvibe", _op: "apply-view-edit" }`.
- Primitive params are canonicalized and validated before execution.
- Plan app/env must match primitive app/env.
- Steps execute sequentially.
- Execution stops on the first failed step.
- Completed steps are not rolled back.
- Idempotent already-completed cases may be detected for stable child/move results.

## 13) Conversation artifacts and learned intent state

Current Truth:

- Conversation storage is file-backed under `<work_folder>/xvm/apps/<env>/<app_id>/conversations/`.
- Conversation files are `index.json`, `<conversation_id>/conversation.json`, `<conversation_id>/messages.jsonl`, and `<conversation_id>/attachments/`.
- Conversation documents include `_id`, `_app_id`, `_env`, `_created_at`, `_updated_at`, `_message_count`, and optional title/metadata/planning draft fields.
- Conversation messages include `_id`, `_role`, `_text`, `_created_at`, and optional `_attachments`, `_intent`, `_actions`, `_result`, and `_metadata`.
- Action statuses are `suggested`, `running`, `done`, `failed`, and `dismissed`.
- Artifact statuses are `done`, `failed`, and `dismissed`.
- `analyze-message` appends a tool message with `_intent` and metadata.
- `update-conversation-action` mutates action status/result/error in `messages.jsonl`.
- `update-conversation-artifact` mutates artifact status/result/error fields in `messages.jsonl`.
- `get-last-messages` defaults to 20 and caps at 100.
- Path handling uses safe segment/path-inside checks.

Learned intent storage:

`<work_folder>/xvm/apps/<env>/<app_id>/intent-memory/learned-intents.json`

Learned intent rules:

- Learned intents are validated before storage/use.
- Verified semantic action updates may write learned intents through `IntentMemoryStore`.
- Selected-object fields are placeholderized on learn and resolved on reuse.
- Placeholder fields include `_target_id`, `_target_type`, `_source_view_id`, and `_path`.
- Learned intent matching happens before generic artifact processors and before semantic intent.

## 14) Runtime and capability awareness

Current Truth:

- `RuntimeContextManager.resolveXvibeWorkFolder()` reads the `server-xvm` work folder and falls back to `./work`.
- `RuntimeContextManager.loadProjectMemory(...)` reads Project Memory through `server-xvm.get-project-memory`.
- `RuntimeContextManager.attachProjectMemoryToRuntimeContext(...)` removes inbound `project_memory`/`_project_memory` and attaches the current frozen Project Memory snapshot.
- `RuntimeContextManager.collectRuntimeAssets(...)` reads app asset ids through `server-xvm.get_app`.
- Runtime skills snapshots are held in `GenerationManager` memory via `sync-skills` and `refreshRuntimeSkillsAfterModuleCreation`.
- `XVibeCapabilityRegistry` describes user-visible/tested guidance capabilities for intent answers.
- `ExecutionGraph/CapabilityRegistry` describes execution graph artifact capabilities; `view` is present but unsupported.

Rules:

- Do not conflate guidance capabilities with execution graph capabilities.
- Runtime memory snapshots are not durable persistence.
- Project Memory writes go through `server-xvm.patch-project-memory` or XVM project memory helpers.

## 15) Persistence boundaries

Current Truth:

- ServerXVM app/view/flow/entity/project-memory state persists via `server-xvm` commands.
- Structured view edits persist via `server-xvm.push_update`.
- XVIBE conversation files persist under each app/env.
- XVIBE learned intents persist under each app/env.
- XVIBE run archives persist under each app/env `vibe-runs`.
- Starter app creation copies a starter directory and then loads through `server-xvm.load_app_from_disk`.

Not persistence:

- XData.
- `_xem` events.
- `wsBroadcastScoped` updates.
- Generation stage messages.
- Runtime skill snapshots.
- Intent engine intermediate results.

## 16) Logging

Current Truth:

- XVIBE logs through `_xlog.log`, `_xlog.warn`, and `_xlog.error`.
- Log messages use the `[xvibe]` prefix in XVIBE source.
- Logged areas include processor match/null/fallback, semantic gating and normalization, mutation-plan creation/execution, structured edit resolution/persistence, project memory load/update, learned-intent storage/hits, conversation updates, artifact execution, execution graph planning/execution, guide recommendations, starter app creation, generation stages, and failure paths.
- Structured editing emits `_xem.fire("vibe:view-updated", ...)` after persistence and may call `wsBroadcastScoped(...)` for active view refresh.

Recommendation:

- Treat logs as diagnostic only; do not make behavior depend on log text.
- Do not log secrets, provider tokens, or raw private payloads unless source already has an explicit diagnostic path for that payload.

## 17) Testing

Current Truth:

- Maintained source coverage is in `packages/xnode/src/test.ts`.
- Package test script is `npm run test`, which runs `npm run build && node ./dist/test.js`.
- Source tests cover module construction/ops, processor ordering, capability precedence, mutation-plan non-execution during analysis, deterministic selected-object edits, Project Memory focus, planning, guide recommendations, artifact processors, semantic gating/normalization/preflight, structured view edit persistence, mutation-plan execution, artifact requests, execution graphs, starter app flow, conversations, learned intents, path traversal, and invalid input rejection.

Recommendation:

- Any changed primitive, alias, processor order, persistence path, or artifact field should update `packages/xnode/src/test.ts` or add an equivalent source test following the repository's current test structure.

## 18) Engineering discipline

Mandatory rules:

- Every XVibe primitive must pass all five gates before merge: unit tests, pipeline integration, persistence, retry, and composition.
- Every new primitive must include at least one real prompt acceptance test that starts from a user prompt and verifies the resulting intent/pipeline behavior.
- Do not add primitive-specific resolvers. New primitives must use shared canonicalization, view resolution, target resolution, and validation paths. Extend shared resolvers only when the extension is generic and tested.
- No executable semantic action may be produced before this sequence completes: canonicalization -> view resolution -> target resolution -> validation.
- Do not create duplicate execution paths for the same primitive. Intent analysis may describe or plan execution; mutation must happen through the single server-side module path for that primitive.
- Mutation Plans execute only canonical primitives. A mutation-plan step must not carry aliases, semantic-only action names, client callbacks, or non-canonical primitive descriptors.
- No client-side primitive execution. Clients may request, display, confirm, or observe primitives, but execution belongs to `xvibe` server module ops.
- Server/client artifact contracts must be tested end-to-end when a primitive affects client-visible artifacts, buttons, action descriptors, conversation artifacts, or execution results.
- Logging is mandatory for new primitive boundaries: matched/accepted prompt, canonical action, resolved view id, resolved target id or rejection reason, validation result, persistence result, retry/idempotency outcome, and final execution status. Logs must use the `[xvibe]` prefix and must not add secrets or provider tokens.

Known regression prompt matrix:

| Category | Prompt | Expected processor/route | Expected artifact/action | Semantic AI |
| --- | --- | --- | --- | --- |
| Text | `Change "My App" to "Dashboard"` | `DeterministicIntentProcessor` | `apply-view-edit` / `update-property` `_text` | No |
| Style | `Make the "My App" label 32px, bold, with 16px margin below.` | `SemanticIntentProcessor` | `apply-view-edit` / `set-style` or `set-styles` | Yes |
| Structure | `Add a footer label to the main view.` | `SemanticIntentProcessor` | `apply-view-edit` / `add-child` | Yes |
| Structure | `Hide Refresh` | no intent processor; deterministic `generate_artifact`/`StructuredViewEdit` route | `hide-object` | No |
| Structure | `Remove New Record` | no intent processor; deterministic `generate_artifact`/`StructuredViewEdit` route | `remove-object` | No |
| Toolbar | `Create a toolbar` | `SemanticIntentProcessor` | `apply-view-edit` / `create-toolbar` | Yes |
| Toolbar | `Create a toolbar with Save and Cancel` | `MutationPlanningProcessor` | `mutation-plan` with `create-toolbar` + `add-child` primitives | No |
| Toolbar | `Create a toolbar and move Refresh and New Record into it` | `MutationPlanningProcessor` | `mutation-plan` with `create-toolbar` + `move-object` primitives | No |
| Planning | `I want to build a CRM` | `PlanningProcessor` or `PlanningSessionProcessor` by stage/context | `project-plan` / planning question | No |
| Planning | `confirm the current project plan` | `PlanningSessionProcessor` or `confirm-project-plan` module op by context | project plan confirmation / module op | No |
| Guidance | `What can I do with Visual Xpell?` | `CapabilityGuidanceProcessor` | `capability-guidance` | No |
| Guidance | `How do I change object text?` | `CapabilityGuidanceProcessor` | `capability-guidance` for `update-text` | No |

Codex implementation report:

- Every Codex implementation must report the result for unit tests, pipeline tests, persistence tests, retry tests, composition tests, and build.
- If a category is not run, the report must say why and identify the remaining risk.

## 19) Hard forbiddens

- Do not invent XVIBE APIs, ops, artifact fields, stores, or processor order.
- Do not bypass `server-xvm` for authoritative app/view/flow/entity persistence.
- Do not persist authoritative XVIBE state in XData.
- Do not directly compile, import, or load generated XModules from XVIBE.
- Do not reorder intent processors without updating tests and this skill.
- Do not add AI fallback to structured view edits.
- Do not execute mutation-plan primitives other than `xvibe.apply-view-edit`.
- Do not persist non-JSON values in conversation, learned intent, app, view, flow, entity, or plan artifacts.

## 20) Source truth

If this skill and source disagree, follow source and update:

- `packages/xnode/src/XVIBE/**`
- `packages/xnode/src/test.ts`
- `SKILL.md`
- `SKILL_API_MAP.md`
- `SKILL_CHECKLIST.md`
