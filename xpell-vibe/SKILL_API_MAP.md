# XVibe API Map (Code-Derived)

Source snapshot inspected:

- `packages/xnode/src/XVIBE/**`
- `packages/xnode/src/index.ts`
- `packages/xnode/src/test.ts`
- `packages/xnode/package.json`

## Package Entry Points

- Package name: `@xpell/node`
- Version in `packages/xnode/package.json`: `2.0.4`
- Type: `module`
- Entrypoints:
  - `main`: `./dist/index.js`
  - `module`: `./dist/index.js`
  - `types`: `./dist/index.d.ts`
- `packages/xnode/src/index.ts` re-exports `./XVIBE/index.js`.

## XVIBE Root Exports (`src/XVIBE/index.ts`)

Runtime/classes:

- `XVibeModule`
- `XVibePlanner`
- `VibeOutputParser`
- `VibeOutputParserError`
- `VibeKnowledgeSelector`
- `VibeIntentPlanner`
- `normalize_string_array`
- `VibeBehaviorPlanner`
- `XVibeCapabilityRegistry`
- `VibePromptBuilder`
- `budgetSkills`
- `isWeakSkill`
- `rankSkillsForPrompt`
- `skillRelevanceDiagnostics`
- all exports from `XVibeTypes.ts`

Types:

- `XVibeAppPlan`
- `XVibeArtifactExecutionItem`
- `XVibeArtifactPlanType`
- `XVibeLogicLevel`
- `VibeIntentPlan`
- `VibeRuntimeCapabilityRegistry`
- `XVibeCapabilityCategory`
- `XVibeCapabilityDefinition`
- `XVibeCapabilityGuidanceArtifact`
- `XVibeCapabilityGuidanceItem`
- `XVibeCapabilityGuidanceSection`
- `XVibeCapabilityMode`
- `XVibeCapabilityStatus`
- `RuntimeAssets`
- `RuntimeAssetRef`
- `VibeBehaviorIntent`
- `VibeBehaviorPlannerInput`
- `BudgetedSkillRelevance`
- `SkillRelevance`

## XVibeModule (`src/XVIBE/XVibeModule.ts`)

Identity:

- `class XVibeModule extends XModule`
- `static _name = "xvibe"`
- `static _skill._id = "xvibe"`
- `static _skill._type = "server-module-api"`
- `static _skill._requires = ["xmodule", "xai", "server-xvm", "module-creator"]`

Constructor-owned collaborators:

- `VibeKnowledgeSelector`
- `VibePromptBuilder`
- `VibeViewBuilder`
- `VibeOutputParser`
- `XVibePlanner`
- `VibeIntentPlanner`
- `VibeBehaviorPlanner`
- `XVibeIntentEngine`
- `GenerationManager`
- `ArtifactExecutor`
- `ExecutionGraphExecutor`
- `GuideRecommendationEngine`
- in-memory guide recommendation cache

Module ops:

- `_generate` -> `generate`
- `_plan_app` -> `plan-app`
- `_generate_view` -> `generate-view`
- `_get_guide_recommendation` -> `get-guide-recommendation`
- `_confirm_project_plan` -> `confirm-project-plan`
- `_apply_view_edit` -> `apply-view-edit`
- `_apply_mutation_plan` -> `apply-mutation-plan`
- `_fix_project_views` -> `fix-project-views`
- `_analyze_project_views` -> `analyze-project-views`
- `_apply_artifact_request` -> `apply-artifact-request`
- `_execute_execution_graph` -> `execute-execution-graph`
- `_generate_app` -> `generate-app`
- `_create_app_from_starter` -> `create_app_from_starter`
- `_generate_module_spec` -> `generate-module-spec`
- `_get_latest_run` -> `get-latest-run`
- `_create_conversation` -> `create-conversation`
- `_list_conversations` -> `list-conversations`
- `_get_conversation` -> `get-conversation`
- `_append_message` -> `append-message`
- `_analyze_message` -> `analyze-message`
- `_get_last_messages` -> `get-last-messages`
- `_update_conversation_action` -> `update-conversation-action`
- `_update_conversation_artifact` -> `update-conversation-artifact`
- `_sync_skills` -> `sync-skills`

Key events/signals:

- `_xem.fire("vibe:view-updated", ...)`
- `_xem.fire("vibe:flow-updated", ...)`
- `_xem.fire("vibe:entity-updated", ...)`
- `_xem.fire("vibe:command-generated", ...)`
- `wsBroadcastScoped(...)` for generation/stage/update transport notifications

## XVibeTypes (`src/XVIBE/XVibeTypes.ts`)

Artifact type unions:

- `VibeSelectionArtifactType = "view" | "flow" | "entity" | "command"`
- `VibeArtifactType = "view" | "flow" | "entity" | "command"`
- `VibeRequestedArtifactType = VibeArtifactType | "auto"`
- `XVibeInferredArtifactType = VibeArtifactType | "module"`

Resolved task:

- `XVibeResolvedTask`
- `_action`: `create`, `update`, `delete`, `disable`, `archive`, `rename`, `inspect`, `unknown`
- `_artifact_type`: `view`, `flow`, `entity`, `module`, `command`, `app`, `unknown`
- structured edit fields such as `_edit_action`, `_edit_target_id`, `_edit_target_text`, `_edit_destination_id`, `_edit_child_value`, `_edit_handler`, `_edit_styles`
- module fields: `_module_name`, `_module_ops`

Runtime:

- `XVibeRuntimeAssets`
- `XVibeRuntimePlan`
- `XVibeValidationPlan`
- `XVibeProjectMemory`
- `XVibeGuideRecommendation`

Intent:

- `XVibeIntentMessageType`: `conversation`, `question`, `inspect`, `edit`, `generate`, `plan`, `planning`, `debug`
- `XVibeIntentExecutionLevel`: `none`, `deterministic`, `artifact`, `planning`, `model`
- `XVibeIntentActionType`: `apply-view-edit`, `generate-artifact`, `inspect-runtime`, `module-op`, `module-generate`, `module-edit`, `open-panel`, `ask-user`, `reply`
- `XVibeIntentArtifactRequestType`: `entity`, `flow`, `view`, `form`, `table`, `crud-evolution`, `crud-field-suggestion`, `execution-graph`, `project-plan`, `capability-guidance`, `mutation-plan`
- `XVibeIntentResult`
- `XVibeIntentRuntimeContext`
- `XVibeIntentEngineRequest`
- `XVibeIntentEngineResponse`

## Intent Engine (`src/XVIBE/XVibeIntentEngine.ts`)

Class:

- `XVibeIntentEngine`
- option `_intent_memory_store?: IntentMemoryStore`
- option `_semantic_generate_json?: XVibeSemanticIntentGenerateJson`

`analyze(request)`:

- validates object request, `_message`, `_runtime_context`, `_runtime_context._app_id`, `_runtime_context._env`;
- enriches runtime context with Project Memory;
- runs processors in constructor order;
- returns first non-null intent;
- logs processor matches/nulls;
- returns stub conversation intent when no processor matches.

Processor order:

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

## Processor Map (`src/XVIBE/Processors/*`)

Shared interface:

- `XVibeIntentProcessor.analyze(request): Promise<XVibeIntentResult | null>`
- optional `_diagnostic_reason(): string | undefined`

Processor contract:

- `XVibeIntentEngine` returns the first non-null result.
- Non-matching processors return `null`.
- Intent analysis returns intent data/action descriptors/artifacts; app/view/entity/flow mutation is performed by explicit module ops.
- Processor null/match/fallback paths are logged through `_xlog` by the engine.

Processors:

- `CapabilityGuidanceProcessor`: deterministic `capability-guidance` artifacts for supported capability questions/manual/prompts.
- `MutationPlanningProcessor`: deterministic `mutation-plan` artifacts for multi-step view mutation prompts.
- `DeterministicIntentProcessor`: deterministic selected-object and simple structured view edit actions, plus project view fix commands.
- `ProjectMemoryFocusProcessor`: deterministic project-memory focus patch command through `server-xvm.patch-project-memory`.
- `PlanningSessionProcessor`: project planning session question/answer/continuation handling.
- `PlanningProcessor`: project plan artifacts.
- `LearnedIntentProcessor`: reads verified learned intents, resolves selected-object placeholders, records hit counts.
- `EntityProcessor`: entity artifact request.
- `FlowProcessor`: flow artifact request.
- `FormProcessor`: form artifact request.
- `TableProcessor`: table artifact request.
- `CrudProcessor`: CRUD execution graph and field suggestion intents.
- `AddFieldProcessor`: CRUD evolution add-field request.
- `RenameFieldProcessor`: CRUD evolution rename-field request.
- `DeprecateFieldProcessor`: CRUD evolution deprecate-field request.
- `DeleteFieldProcessor`: CRUD evolution delete-field/deprecate request path.
- `RestoreDeprecatedFieldProcessor`: CRUD evolution restore-field request.
- `SemanticIntentProcessor`: provider-backed semantic intent normalization and preflight; last in chain.

## Structured Editing

Files:

- `StructuredEditing/StructuredViewEdit.ts`
- `StructuredEditing/ProjectViewResolution.ts`
- `StructuredEditing/ViewTargetResolution.ts`
- `StructuredEditing/SemanticViewEditPreflight.ts`

Core exports:

- `StructuredViewEdit`
- `StructuredViewEditAction`
- `StructuredViewEditIntent`
- `StructuredViewEditEligibility`
- `StructuredViewEditMutation`
- `StructuredViewEditDeterministicResult`
- `StructuredViewEditSourceResolution`
- `StructuredViewEditDependencies`
- `canonicalizeSemanticViewEditParams`
- `isStructuredViewEditAction`
- `readStructuredViewEditAction`
- `resolveProjectViewId`
- `normalizeProjectViewId`
- `resolveViewTarget`
- `normalizedVisibleTargetText`
- `preflightSemanticViewEdit`

Canonicalization primitives:

- `readStructuredViewEditAction(value)`
- `isStructuredViewEditAction(value)`
- `canonicalizeSemanticViewEditParams(params)`
- `normalizeProjectViewId(value)`
- `normalizedVisibleTargetText(value)`

Canonicalization rejection reasons:

- `invalid_edit_action`
- `unsupported_edit_action`
- `unsupported_property_batch`
- `ambiguous_edit_action`

Supported action values:

- `set-property`, `update-property`, `remove-property`
- `set-style`, `set-styles`, `remove-style`
- `add-class`, `remove-class`, `replace-class`, `toggle-class`
- `remove-object`, `hide-object`, `show-object`
- `move-object`, `replace-object`, `duplicate-object`
- `add-child`, `create-toolbar`, `set-interaction`

View resolution strategies:

- `exact`
- `current-view`
- `normalized`
- `root-alias`
- `target-content-current`

Target resolution strategies:

- `id`
- `root`
- `text`
- `normalized_id`
- `normalized_text`
- `text_type_id`

Target resolution error reasons observed in source:

- `target_not_found`
- `target_is_root`
- `missing_target_id`
- `text_target_not_found`
- `ambiguous_text_target`
- `ambiguous_normalized_text_target`

Semantic preflight:

- file: `StructuredEditing/SemanticViewEditPreflight.ts`
- export: `preflightSemanticViewEdit`
- canonicalizes params before preflight
- uses `server-xvm.list_views` and `server-xvm.get_view`
- may persist ids after `ensure_view_ids`
- resolves target and move destination before returning executable params
- may set `_semantic_non_executable_reason`

Architectural invariant enforcement points:

- Canonicalization: `src/XVIBE/StructuredEditing/StructuredViewEdit.ts:668` `readStructuredViewEditAction`, `:672` `isStructuredViewEditAction`, `:997` `canonicalizeSemanticViewEditParams`
- View resolution: `src/XVIBE/StructuredEditing/ProjectViewResolution.ts:89` `resolveProjectViewId`
- Target resolution: `src/XVIBE/StructuredEditing/ViewTargetResolution.ts:261` `resolveViewTarget`
- Semantic preflight: `src/XVIBE/StructuredEditing/SemanticViewEditPreflight.ts:483` `preflightSemanticViewEdit`
- Semantic executable payload creation: `src/XVIBE/Processors/SemanticIntentProcessor.ts:1904` preflight call, `:1935` executable flag, `:1944` `_execution_payload`
- Structured mutation execution: `src/XVIBE/StructuredEditing/StructuredViewEdit.ts:1934` `StructuredViewEdit.apply`
- Module apply path: `src/XVIBE/XVibeModule.ts:16327` `_apply_view_edit`, `:16355` `_apply_mutation_plan`
- Structured persistence: `src/XVIBE/StructuredEditing/StructuredViewEdit.ts:2192` `server-xvm.push_update`, `:2232` structured persistence log, `:2482` `vibe:view-updated`
- ServerXVM persistence/version/backup: `src/XVM/ServerXVMModule.ts:1036` `_push_update`, `:1056` version increment, `:1869` backup helper, `:1894` backup log
- Conversation status: `src/XVIBE/Conversation/ConversationManager.ts:1691` `updateConversationAction`, `:1856` `updateConversationArtifact`

## Mutation Plans

Creation:

- `Processors/MutationPlanningProcessor.ts`
- returns `XVibeIntentResult` with `_message_type: "planning"`, `_execution_level: "planning"`, `_should_mutate: false`, `_artifact_type: "mutation-plan"`.

Artifact fields:

- `_type: "mutation-plan"`
- `_title`
- `_goal`
- `_summary`
- `_steps`
- `_estimated_mutations`
- `_executable_steps`
- `_unsupported_steps`
- `_can_apply`
- `_status: "planned"`
- `_buttons`

Executable primitive:

- `_module: "xvibe"`
- `_op: "apply-view-edit"`
- `_params`

Execution:

- `XVibeModule._apply_mutation_plan(...)`
- validates `_plan._type === "mutation-plan"`
- requires `_plan._can_apply === true`
- validates every step and primitive app/env boundary
- executes steps sequentially through `_x.execute(...)`
- returns failed result on first failed step

Validated primitive boundary:

- `_module` must be `xvibe`
- `_op` must be `apply-view-edit`
- `_params` must canonicalize through `canonicalizeSemanticViewEditParams`
- primitive `_app_id` and `_env` must match the mutation-plan execution context

## Runtime Context

File:

- `Runtime/RuntimeContextManager.ts`

Exports:

- `XVibeRuntimeContextInput`
- `RuntimeContextManager`

Methods:

- `errorPayload(error)`
- `resolveXvibeWorkFolder()`
- `resolveTargetAppDir(env, app_id)`
- `loadProjectMemory({ _app_id, _env })`
- `attachProjectMemoryToRuntimeContext(runtime_context)`
- `collectRuntimeAwarenessContext(input)`
- `collectRuntimeAssets({ _app_id, _env, _runtime_skills })`

Persistence/command dependencies:

- `server-xvm.get-project-memory`
- `server-xvm.get_app`

## Capability Registries

Guidance capability registry:

- file: `Capability/CapabilityRegistry.ts`
- export: `XVibeCapabilityRegistry`
- categories: `view-editing`, `project-planning`, `maintenance`
- modes: `deterministic`, `AI-assisted`
- statuses: `supported`, `internal`, `unsupported`
- methods: `all()`, `userVisibleTested()`, `byIds(ids)`, `byCategory(category)`

Execution graph capability registry:

- file: `ExecutionGraph/CapabilityRegistry.ts`
- export: `CapabilityRegistry`
- artifact types: `entity`, `flow`, `form`, `table`, `view`
- supported executor: `ArtifactExecutor`
- `view` is present but `_supported: false`
- methods: `lookupCapability`, `requireCapability`, `artifactExists`, `buildArtifactRequest`

## Conversation

Files:

- `Conversation/ConversationManager.ts`
- `Intent/IntentConversationBridge.ts`
- `IntentMemory/IntentMemoryStore.ts`

Conversation types:

- `XVibeConversationMessage`
- `XVibeConversationDocument`
- `XVibeAnalyzeMessageRequest`

Conversation role values:

- `user`
- `assistant`
- `system`
- `tool`

Conversation action status values:

- `suggested`
- `running`
- `done`
- `failed`
- `dismissed`

Conversation artifact status values:

- `done`
- `failed`
- `dismissed`

ConversationManager methods:

- `errorPayload(error)`
- `readPlanningDraft(input)`
- `writePlanningDraft(input)`
- `clearPlanningDraft(input)`
- `readAnalyzeMessageRequest(xcmd)`
- `createConversation(xcmd)`
- `listConversations(xcmd)`
- `getConversation(xcmd)`
- `appendMessage(xcmd)`
- `updateConversationAction(xcmd)`
- `updateConversationArtifact(xcmd)`
- `getLastMessages(xcmd)`

Storage layout:

- `<work_folder>/xvm/apps/<env>/<app_id>/conversations/index.json`
- `<work_folder>/xvm/apps/<env>/<app_id>/conversations/<conversation_id>/conversation.json`
- `<work_folder>/xvm/apps/<env>/<app_id>/conversations/<conversation_id>/messages.jsonl`
- `<work_folder>/xvm/apps/<env>/<app_id>/conversations/<conversation_id>/attachments/`

Intent bridge:

- `IntentConversationBridge.analyze(...)`
- reads request through `ConversationManager.readAnalyzeMessageRequest`
- invokes `XVibeIntentEngine.analyze`
- normalizes action ids
- appends a tool message with `_intent`

Intent memory:

- file: `IntentMemory/IntentMemoryStore.ts`
- `learned-intents.json`
- path: `<work_folder>/xvm/apps/<env>/<app_id>/intent-memory/learned-intents.json`
- methods include `read_learned_intents`, `learn`, `record_hit`
- exports `normalize_learned_intent_prompt`, `validate_learned_intent_result`, `read_valid_learned_intent_entry`
- selected-object placeholders: `_target_id`, `_target_type`, `_source_view_id`, `_path`

## Artifact and Execution Graph

Artifact files:

- `Artifact/ArtifactExecutor.ts`
- `Artifact/ArtifactResolver.ts`
- `Artifact/ArtifactRelationshipRegistry.ts`

ArtifactExecutor supports:

- entity create
- flow create
- form create
- table create
- CRUD evolution add-field
- CRUD evolution rename-field
- CRUD evolution deprecate-field
- CRUD evolution restore-field

Execution graph files:

- `ExecutionGraph/ExecutionGraphPlanner.ts`
- `ExecutionGraph/ExecutionGraphExecutor.ts`
- `ExecutionGraph/ExecutionRecipes.ts`
- `ExecutionGraph/CapabilityRegistry.ts`

Execution recipe:

- graph type: `crud`
- artifacts:
  - entity `{entity}`, required
  - flow `create-{entity}`, depends on entity, required
  - form `create-{entity}`, depends on entity and flow, required
  - view `{entity}-list`, depends on form, optional and unsupported
  - table `{entity}-list`, child of view, optional

Execution result summary:

- `_existing`
- `_created`
- `_skipped`
- `_failed`

## Generation and Archive

Generation file:

- `Generation/GenerationManager.ts`

GenerationManager methods:

- `getRuntimeSkills(app_id?, env?, mode?)`
- `refreshRuntimeSkillsAfterModuleCreation(app_id, env, mode)`
- `generate(xcmd)`
- `generateView(xcmd)`
- `getLatestRun(xcmd)`
- `planApp(xcmd)`
- `generateModuleSpec(xcmd)`
- `generateApp(xcmd)`
- `syncSkills(xcmd)`

Archive file:

- `Archive/RunArchiveManager.ts`

Run archive artifacts:

- `request.json`
- `resolved-task.json`
- `runtime-context.json`
- `prompt.txt`
- `final-prompt.txt`
- `intent-plan.json`
- `module-plan.json`
- `artifact-plan.json`
- `runtime-plan.json`
- `validation-plan.json`
- `ai-output.json`
- `result.json`
- `summary.json`
- `timeline.json`
- `validation.json`

## Logging

Logging primitive:

- `_xlog.log(...)`
- `_xlog.warn(...)`
- `_xlog.error(...)`

Observed XVIBE log prefix:

- `[xvibe]`

Logged areas:

- intent processor match/null/fallback
- semantic gating/request/normalization/preflight
- mutation-plan creation/compilation/execution
- structured view edit resolution/persistence/application
- Project Memory load/update
- learned intent validation/storage/hits
- conversation action/artifact updates
- artifact request execution
- execution graph plan/node/completion
- guide recommendation and starter app paths
- generation stages and failures

Debug-stage source/log map:

- Processor matched/null/fallback: `src/XVIBE/XVibeIntentEngine.ts:98`, `:111`, `:118`
- Deterministic text route: `src/XVIBE/Processors/DeterministicIntentProcessor.ts:220` `[xvibe] deterministic text replacement matched`
- Semantic route: `src/XVIBE/Processors/SemanticIntentProcessor.ts:2479` semantic processor, `:2562` request begin, `:2630` normalized, `:2656` accepted
- Mutation plan route: `src/XVIBE/Processors/MutationPlanningProcessor.ts:631` plan created, `:636` plan compiled
- Structured edit route: `src/XVIBE/StructuredEditing/StructuredViewEdit.ts:1991` semantic view resolved, `:2105` source resolved, `:2232` persisted, `:2490` applied
- Conversation route: `src/XVIBE/Conversation/ConversationManager.ts:1693` action update received, `:1856` artifact update received, `:1942` artifact status updated
- ServerXVM route: `src/XVM/ServerXVMModule.ts:1092` push update broadcast, `:1894` view backup created

## Tests

Maintained source test:

- `packages/xnode/src/test.ts`

Generated test artifacts:

- `packages/xnode/dist/test.js`
- `packages/xnode/dist/test-xvibe.js`

Package script:

- `npm run test` = `npm run build && node ./dist/test.js`

Source test coverage includes:

- XVibe public helpers and module construction
- processor chain ordering
- capability guidance processor precedence over semantic generation
- mutation plan creation and non-execution during analysis
- deterministic selected-object/text replacement intents
- Project Memory focus actions
- project planning and planning sessions
- guide recommendations
- entity/flow/form/table/CRUD field processors
- semantic intent gating, normalization, and preflight
- structured view edit application and persistence boundaries
- mutation-plan primitive validation/execution
- artifact request execution
- execution graph planning/execution and dependency failure behavior
- starter app copy/load path
- conversation CRUD, analyze-message, action/artifact status updates
- learned intent storage/reload/placeholder behavior
- path traversal and invalid input rejection
