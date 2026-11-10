# Xpell App Starter API Map (Code-Derived)

## Skill files
- Skill directory: `/Users/tamirfridman/.codex/skills/xpell-app-starter`
- Main contract: `SKILL.md`
- API map: `SKILL_API_MAP.md`
- Review checklist: `SKILL_CHECKLIST.md`

## Starter source
- Starter root inspected: `/Users/tamirfridman/Documents/projects/xpell.ai/xpell-vibe-starter/server/system-xapps/app-starters`
- Empty starter:
  - `Empty/app.json`
  - `Empty/views/main.json`
- Dashboard starter:
  - `dashboard/app.json`
  - `dashboard/views/main.json`
  - `dashboard/style/custom.css`
  - `dashboard/assets/logo.svg`
  - `dashboard/assets/empty-state.svg`
  - `dashboard/assets/placeholder-record.svg`

## Starter manifest schema
Starter metadata source:
- `app.json -> _meta._starter`

Current `StarterMetadata` fields in `xpell-vibe-starter/server/src/modules/Starter/StarterModule.ts`:
- `_id: string`
- `_title: string`
- `_description: string`
- `_keywords: string[]`
- `_archetypes: string[]`
- `_entry_view: string`
- `_adaptation_strategy: JsonObject`
- `_preserve_object_ids: string[]`
- `_replaceable_object_ids: string[]`
- `_starter_capabilities: string[]`
- `_starter_version: string`
- `_required_placeholders?: string[]`
- `_optional_placeholders?: string[]`
- `_fixed_object_ids?: string[]`
- `_adaptation_targets?: JsonObject`

Dashboard manifest strategy arrays:
- `_adaptation_strategy._mode`
- `_adaptation_strategy._summary`
- `_adaptation_strategy._preserve`
- `_adaptation_strategy._adapt`
- `_adaptation_strategy._replace`
- `_adaptation_strategy._optional_remove`

Dashboard `_adaptation_targets` fields:
- `_required`
- `_optional`
- `_content_container_id`
- `_page_title_id`
- `_primary_navigation_id`
- `_sidebar_title_id`
- `_toolbar_id`
- `_toolbar_title_group_id`
- `_page_subtitle_id`
- `_record_search_id`
- `_refresh_button_id`
- `_create_record_button_id`
- `_overview_nav_item_id`
- `_records_nav_item_id`
- `_activity_nav_item_id`
- `_settings_nav_item_id`

## Starter server module
Source path:
- `/Users/tamirfridman/Documents/projects/xpell.ai/xpell-vibe-starter/server/src/modules/Starter/StarterModule.ts`

Exports:
- `StarterMetadata`
- `StarterExpansionInput`
- `STARTER_PLACEHOLDERS`
- `sanitize_app_id(value)`
- `read_starter_metadata(app_file, fallback_starter_id)`
- `create_starter_placeholder_values(input)`
- `validate_starter_adaptation_targets(input)`
- `expand_starter_placeholders(input)`
- `resolve_starter_source_dir(starter_id, starters_root?)`
- `load_starter_contract(starter_dir, starter_id)`
- `create_app_from_starter(params)`
- `StarterModule`
- default export `StarterModule`

Module command:
- module name: `starter`
- op: `create_app_from_starter`
- params: `StarterExpansionInput`

Important constants:
- `STARTER_PUBLIC_FOLDERS = new Set(["style", "assets"])`
- `PLACEHOLDER_PATTERN = /<([a-z][a-z0-9-]*)>/gu`
- `SAFE_SEGMENT_PATTERN = /^[a-z0-9][a-z0-9_-]*$/u`
- `ID_LIKE_KEYS`: `_id`, `id`, `_app_id`, `_view_id`, `_flow_id`, `_entity_id`, `_entry_view_id`, `_entry_view`, `_primary_view`, `_primary_entity`, `_source_view_id`, `_target_id`

Supported placeholders:
- `<app-id>`
- `<app-name>`
- `<app-title>`
- `<app-description>`
- `<app-archetype>`
- `<app-scope>`
- `<primary-entity>`
- `<primary-entity-title>`
- `<primary-view>`
- `<primary-view-title>`

Validation/error codes observed:
- `E_STARTER_INVALID_SEGMENT`
- `E_STARTER_INVALID_APP_ID`
- `E_STARTER_INVALID_OBJECT_ID`
- `E_STARTER_INVALID_ADAPTATION_TARGET`
- `E_STARTER_UNRESOLVED_PLACEHOLDER`
- `E_STARTER_INVALID_JSON`
- `E_STARTER_NOT_FOUND`
- `E_STARTER_COPY_FAILED`
- `E_STARTER_APP_ALREADY_EXISTS`
- `E_STARTER_LOAD_FAILED`
- `E_STARTER_CREATE_APP_FAILED`

## XVibe starter creation copy path
Source path:
- `/Users/tamirfridman/Documents/projects/xpell.ai/packages/xvibe/src/XVIBE/XVibeModule.ts`

Relevant symbols/sections:
- `STARTER_PUBLIC_FOLDERS`
- `copy_starter_runtime_files(...)`
- `copy_starter_public_files(...)`
- `rewrite_starter_public_reference(...)`
- `rewrite_starter_public_references(...)`
- `resolve_starters_root()`
- `resolve_starter_source_dir(starter_id)`
- `_create_app_from_starter(xcmd)`

Module command:
- module name: `xvibe`
- op: `create_app_from_starter`

Behavior:
- resolves starter root from `server-xvm._system_xapps_path`, falling back to package `system-xapps/app-starters`;
- copies runtime files to XVM app storage;
- copies `style` and `assets` into public app storage;
- rewrites public references only, not the full placeholder set used by `StarterModule`;
- writes copied app metadata including `_starter_id`, `_starter_title`, `_starter_entry_view_id`, `_starter_preserve_object_ids`, `_starter_replaceable_object_ids`, `_starter_adaptation_strategy`, `_starter_capabilities`, `_starter_keywords`, `_starter_archetypes`, and `_starter`;
- loads with `server-xvm.load_app_from_disk`.

## XVibe starter adaptation
Source path:
- `/Users/tamirfridman/Documents/projects/xpell.ai/packages/xvibe/src/XVIBE/Starter/StarterAdaptation.ts`

Exports:
- `XVibeStarterAdaptationStrategy`
- `XVibeStarterMetadata`
- `XVibeStarterPlanDelta`
- `XVibeStarterAdaptationExecutionPlan`
- `XVibeStarterAdaptationCompletion`
- `starter_metadata_for_id(starter_id)`
- `normalize_starter_metadata(value)`
- `starter_metadata_from_context(input)`
- `evaluate_starter_to_plan_delta(input)`
- `starter_adaptation_completion_criteria(input)`
- `build_starter_adaptation_execution_plan(input)`
- `verify_starter_adaptation_completion(input)`

Current `XVibeStarterAdaptationStrategy` values:
- `none`
- `adapt-entry-dashboard`

Current `XVibeStarterMetadata` fields:
- `_starter_id`
- `_starter_title`
- `_entry_view_id`
- `_preserve_object_ids`
- `_replaceable_object_ids`
- `_adaptation_targets._content_container_id`
- `_adaptation_targets._title_object_ids`
- `_adaptation_targets._navigation_object_ids`
- `_adaptation_targets._toolbar_object_ids`
- `_adaptation_strategy`
- `_capabilities`
- `_keywords`
- `_archetypes`

Built-in starters:
- `dashboard`
- `empty`

XVibe metadata sources accepted by normalization:
- `_starter`
- `_starter_metadata`
- `_meta._starter`
- `_meta._starter_metadata`
- `_meta`
- direct object fields

Legacy/alternate fields accepted:
- `_starter_id` or `_id`
- `_entry_view_id`, `_starter_entry_view_id`, `_target_view_id`
- `_preserve_object_ids`, `_starter_preserve_object_ids`
- `_replaceable_object_ids`, `_starter_replaceable_object_ids`
- `_adaptation_targets`, `_starter_adaptation_targets`
- `_content_container_id`, `_required_content_container_id`, `_content_container`, `_target_container_id`
- `_title_object_ids`, `_title_anchor_ids`
- `_navigation_object_ids`, `_navigation_anchor_ids`, `_nav_object_ids`
- `_toolbar_object_ids`, `_toolbar_anchor_ids`
- `_capabilities`, `_starter_capabilities`
- `_keywords`, `_starter_keywords`
- `_archetypes`, `_starter_archetypes`

Deterministic inserted ids:
- `starter-adaptation-primary-experience`
- `starter-adaptation-primary-list`
- `starter-adaptation-primary-form`
- `starter-adaptation-field-summary`
- `starter-adaptation-field-<field-name>`
- `starter-adaptation-follow-up-behaviors`
- `starter-adaptation-flow-<flow-id>`
- `starter-adaptation-primary-nav`

Failure codes:
- `E_XVIBE_STARTER_ADAPTATION_METADATA_MISSING`
- `E_XVIBE_STARTER_ADAPTATION_NOT_REQUIRED`
- `E_XVIBE_STARTER_ADAPTATION_VIEW_MISSING`
- `E_XVIBE_STARTER_ADAPTATION_ENTRY_VIEW_MISMATCH`
- `E_XVIBE_STARTER_ADAPTATION_CONTAINER_MISSING`
- `E_XVIBE_STARTER_ADAPTATION_PRESERVE_TARGET_MISSING`
- `E_XVIBE_STARTER_ADAPTATION_SEMANTIC_STRUCTURE_MISSING`
- `E_XVIBE_STARTER_ADAPTATION_TARGET_MISSING`
- `E_XVIBE_STARTER_ADAPTATION_ROOT_TARGET`
- `E_XVIBE_STARTER_ADAPTATION_PRESERVED_TARGET_REMOVAL`
- `E_XVIBE_STARTER_ADAPTATION_INVALID_INSERT_TARGET`
- `E_XVIBE_STARTER_ADAPTATION_TARGET_NOT_FOUND`
- `E_XVIBE_STARTER_ADAPTATION_CHILD_MISSING`
- `E_XVIBE_STARTER_ADAPTATION_DUPLICATE_INSERT_ID`
- `E_XVIBE_STARTER_ADAPTATION_DUPLICATE_EXISTING_ID`
- `E_XVIBE_STARTER_ADAPTATION_ATOMIC_APPLY_FAILED`
- `E_XVIBE_STARTER_ADAPTATION_COMMIT_FAILED`
- `E_XVIBE_STARTER_ADAPTATION_REBUILD_METADATA_MISSING`
- `E_XVIBE_STARTER_ADAPTATION_EDIT_FAILED`
- `E_XVIBE_STARTER_ADAPTATION_VERIFICATION_FAILED`

## XVibe processor and guide integration
Source paths:
- `/Users/tamirfridman/Documents/projects/xpell.ai/packages/xvibe/src/XVIBE/Processors/StarterAdaptationProcessor.ts`
- `/Users/tamirfridman/Documents/projects/xpell.ai/packages/xvibe/src/XVIBE/Guide/GuideRecommendationEngine.ts`
- `/Users/tamirfridman/Documents/projects/xpell.ai/packages/xvibe/src/XVIBE/Runtime/RuntimeContextManager.ts`

Relevant behavior:
- Guide recommendation type: `starter-adaptation`
- Requirement capability id: `starter-adaptation`
- Guide action field: `_action._starter_adaptation`
- Processor emits artifact type `mutation-plan`
- Processor action execution payload routes to `{ _module: "xvibe", _op: "apply-starter-adaptation" }`
- Runtime assets collect starter metadata from `server-xvm.get_app`.
- Verified completion writes Project Memory `_completed` item id `starter-adaptation` and `_starter_adaptation` status data through `server-xvm.patch-project-memory`.

## Atomic adaptation execution
Source path:
- `/Users/tamirfridman/Documents/projects/xpell.ai/packages/xvibe/src/XVIBE/XVibeModule.ts`

Relevant methods:
- `rebuild_starter_adaptation_mutation_plan_for_execution(input)`
- `mutation_plan_is_starter_adaptation_plan(plan)`
- `prevalidate_atomic_starter_adaptation_plan(input)`
- `apply_atomic_starter_adaptation_step(input)`
- `execute_atomic_starter_adaptation_mutation_plan(input)`
- `_apply_mutation_plan(xcmd)`
- `_apply_starter_adaptation(xcmd)`

Supported atomic starter actions:
- `remove-object`
- `set-property`
- `update-property`
- `add-child`

Persistence boundary:
- `server-xvm.push_update`

Runtime signal after successful commit:
- `_xem.fire("vibe:view-updated", { _app_id, _env, _view_id })`

## ServerXVM view starter note
Source path:
- `/Users/tamirfridman/Documents/projects/xpell.ai/packages/xnode/src/XVM/ServerXVMModule.ts`

Relevant methods:
- `resolve_view_starter_candidate(...)`
- `resolve_view_starter_file(...)`
- `load_view_starter_template(...)`
- `replace_view_starter_placeholders(...)`

This is the view-starter path under `system-xapps/view-starters`, not the app-starter contract. Do not confuse it with `system-xapps/app-starters`.

## XUI/XDashboard object contracts used by current starters
Skill sources:
- `/Users/tamirfridman/.codex/skills/xpell-ui/SKILL.md`
- `/Users/tamirfridman/.codex/skills/xdashboard/SKILL.md`

Current Dashboard starter `_type` values observed:
- `view`
- `style-sheet`
- `sidebar`
- `image`
- `navlist`
- `badge`
- `scroll`
- `toolbar`
- `stack`
- `label`
- `igroup`
- `search`
- `select`
- `button`
- `xsection`
- `grid`
- `kpi-card`
- `table`
- `card`
- `field`
- `xselect`
- `text`
- `modal`
- `toast`

Canonical image assertions:
- `dashboard-sidebar._logo._type === "image"`
- `dashboard-sidebar._logo._id === "dashboard-sidebar-logo"`
- `dashboard-sidebar._logo.src === "assets/logo.svg"` before copy
- `dashboard-settings-card._image._type === "image"`
- `dashboard-settings-card._image._id === "dashboard-settings-card-image"`
- `dashboard-settings-card._image.src === "assets/placeholder-record.svg"` before copy

## Test locations
- Starter contract tests: `/Users/tamirfridman/Documents/projects/xpell.ai/xpell-vibe-starter/server/src/test-starter-contract.ts`
- XVibe tests: `/Users/tamirfridman/Documents/projects/xpell.ai/packages/xvibe/src/test.ts`
- XNode image starter tests: `/Users/tamirfridman/Documents/projects/xpell.ai/packages/xnode/src/test.ts`

Key starter contract coverage:
- `run_metadata_tests`
- `run_dashboard_marker_tests`
- `run_adaptation_anchor_tests`
- `run_placeholder_tests`
- `run_unresolved_required_placeholder_tests`
- `run_optional_fallback_tests`
- `run_fixed_id_and_legacy_tests`
- `run_real_copy_tests`

Key XVibe starter coverage:
- `assert_operations_starter_creation_image_contract`
- `assert_starter_aware_guide_recommendation_matrix`
- `assert_starter_adaptation_completion_matrix`
- `assert_starter_adaptation_guide_runtime_verification`
- `assert_starter_runtime_metadata_nested_get_app`
- `assert_dashboard_starter_get_guide_nested_metadata_ordering`
- `assert_starter_adaptation_execution_planning_matrix`
- `assert_starter_adaptation_processor_deterministic_route`
- `assert_starter_adaptation_module_execution_contract`
- `assert_stale_starter_mutation_plan_direct_apply_rebuilds`
- `assert_starter_adaptation_atomic_failure_contracts`
- `assert_rebuilt_starter_plan_updates_same_conversation_card`

Key XNode starter coverage:
- `run_operations_starter_image_contract_tests`

## Validation commands
Skill validation:

```bash
python3 /Users/tamirfridman/.codex/skills/.system/skill-creator/scripts/quick_validate.py /Users/tamirfridman/.codex/skills/xpell-app-starter
```

Package/starter validation:

```bash
pnpm -C /Users/tamirfridman/Documents/projects/xpell.ai/packages/xvibe run build
pnpm -C /Users/tamirfridman/Documents/projects/xpell.ai/packages/xvibe run test
pnpm -C /Users/tamirfridman/Documents/projects/xpell.ai/packages/xnode run build
pnpm -C /Users/tamirfridman/Documents/projects/xpell.ai/packages/xnode run test
npm --prefix /Users/tamirfridman/Documents/projects/xpell.ai/xpell-vibe-starter/server run build
npm --prefix /Users/tamirfridman/Documents/projects/xpell.ai/xpell-vibe-starter/server run test:starters
```
