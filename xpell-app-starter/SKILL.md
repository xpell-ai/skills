---
name: Xpell App Starter Contract
id: xpell-app-starter
version: 1.0.0
updated: "2026-08-02"
description: >
  Governs reusable Xpell application starter authoring and maintenance. Use when
  creating, modifying, validating, or adapting app starters, including starter
  manifests, semantic adaptation metadata, placeholders, assets, stable IDs,
  XUI composition, validation, and compatibility with ServerXVM and XVibe.
requires:
  - xpell-contract
  - xpell-core
  - xpell-ui
  - xpell-node
  - xpell-vibe
---

## 1) Applies to / Scope
- Applies to reusable app starters under `system-xapps/app-starters/<starter-id>/`.
- Applies to starter `app.json`, views, flows, entities, generated modules, `style/`, `assets/`, and starter-local tests.
- Applies to starter loading, copying, placeholder expansion, metadata validation, and `create_app_from_starter`.
- Applies to XVibe starter-to-plan adaptation metadata, Guide recommendations, mutation-plan rebuild, atomic application, and runtime verification.
- This skill explains how to compose XUI and package objects into reusable starters. It does not define individual object-pack behavior; use `xdashboard` for dashboard component contracts and `xpell-ui` for browser XUI object rules.
- Keep this file as the compact contract. Load `SKILL_API_MAP.md` for exact source paths, symbols, and test locations; load `SKILL_CHECKLIST.md` before merge/review.

## 2) Core identity
- An Xpell app starter is a reusable initial application structure that is valid and loadable before adaptation.
- A starter is self-describing through metadata under `app.json -> _meta._starter`.
- A starter is adaptable through declared object id lists and adaptation target ids, not through guessed CSS or visible text.
- A starter must be independent of one final app domain. A Dashboard starter must not be shopping-list-specific, CRM-specific, scheduler-specific, or any other single domain.
- Current starters are `Empty`/`empty` and `dashboard`.

## 3) Starter folder and manifest contract
Current folder shape:

```text
system-xapps/app-starters/
  Empty/
    app.json
    views/main.json
  dashboard/
    app.json
    views/main.json
    style/custom.css
    assets/logo.svg
    assets/empty-state.svg
    assets/placeholder-record.svg
```

Runtime copy rules:
- `app.json` is required.
- Runtime files are copied to `<work_folder>/xvm/apps/<env>/<app_id>/`.
- Public folders are exactly `style` and `assets`; they are copied to `<work_folder>/public/<app_id>/`.
- JSON files under the copied app directory are rewritten after copy.
- Public references beginning with `style/` or `assets/` rewrite to `/public/<app_id>/style/...` or `/public/<app_id>/assets/...`.
- Creation fails if the app folder or public app folder already exists.
- Copy/rewrite failures remove the target app and public folders before returning failure.
- The copied app is loaded through `server-xvm.load_app_from_disk`.

Required starter metadata is normalized from `app.json -> _meta._starter`:

```json
{
  "_id": "dashboard",
  "_title": "Dashboard Starter",
  "_description": "Operations-style XUI dashboard shell...",
  "_keywords": ["dashboard"],
  "_archetypes": ["dashboard", "record_management"],
  "_entry_view": "main",
  "_adaptation_strategy": { "_mode": "starter-to-plan-delta" },
  "_preserve_object_ids": [],
  "_replaceable_object_ids": [],
  "_starter_capabilities": [],
  "_starter_version": "1.1.0"
}
```

Optional metadata fields currently read by starter copy/load:
- `_required_placeholders`
- `_optional_placeholders`
- `_fixed_object_ids`
- `_adaptation_targets`
- any extra JSON-compatible starter fields, preserved as data

Legacy fallback: if `_meta._starter` is absent, metadata falls back to app title, `_meta._entry_view_id`, empty id lists, `_adaptation_strategy: { "_mode": "preserve-compatible" }`, and `_starter_version: "1.0.0"`.

## 4) Semantic roles and anchors
Current truth: there is no implemented `_semantic_role` field or role enum stored on starter objects. Semantic targeting is implemented with manifest metadata and object ids.

Manifest-level categories:
- `_preserve_object_ids`: reusable shell/layout/runtime controls to keep.
- `_replaceable_object_ids`: generic/demo starter objects to remove or repurpose.
- `_adaptable_object_ids`: objects whose labels/properties may be updated.
- `_optional_remove_object_ids`: generic/demo objects that may be removed when present.
- `_fixed_object_ids`: ids preserved during placeholder expansion; this also includes `_preserve_object_ids`.
- `_starter_capabilities`: descriptive capability tags such as `server-xvm-loadable`, `xui-view`, `minimal-shell`, `xdashboard-shell`, `public-assets`, `theme-selector`, `modal-demo`, `toast-demo`, and `starter-adaptation-metadata`.

Current dashboard target fields:
- `_content_container_id`: primary content insertion container.
- `_page_title_id`: page title object used by starter server validation.
- `_primary_navigation_id`: navigation slot.
- `_sidebar_title_id`: sidebar object.
- `_toolbar_id`: toolbar object.
- `_toolbar_title_group_id`: title group in toolbar.
- `_page_subtitle_id`: subtitle object.
- `_record_search_id`: search/filter control.
- `_refresh_button_id`: toolbar action.
- `_create_record_button_id`: creation action.
- `_overview_nav_item_id`, `_records_nav_item_id`, `_activity_nav_item_id`, `_settings_nav_item_id`: navigation item ids.

XVibe-normalized adaptation targets:
- `_content_container_id`
- `_title_object_ids`
- `_navigation_object_ids`
- `_toolbar_object_ids`

Role principle: these ids describe reusable starter purpose, not final app-domain content. The same dashboard content container can receive a shopping list, CRM customer workspace, or scheduler appointment workspace. Do not create a separate role set per app type.

## 5) Adaptation modes
Two levels are implemented today.

Starter manifest modes in `_meta._starter._adaptation_strategy._mode`:
- `blank-canvas`: used by the Empty starter; preserve the minimal app/view shell and append or replace planned content later.
- `starter-to-plan-delta`: used by Dashboard; preserve reusable shell/runtime controls, update navigation/title language, replace generic demo content, and optionally remove modal/toast demo objects.
- `preserve-compatible`: fallback mode when legacy metadata has no strategy object.

XVibe execution strategies:
- `none`: no starter adaptation is required; Empty resolves to this.
- `adapt-entry-dashboard`: deterministic dashboard entry-view adaptation; Dashboard resolves to this.

Dashboard strategy arrays:
- `_preserve`: keep unchanged.
- `_adapt`: update properties such as title, subtitle, navigation, search, and toolbar actions.
- `_replace`: remove or replace generic/demo content.
- `_optional_remove`: remove demo modal/toast objects if present; skip if absent.

Current XVibe atomic operations are:
- `remove-object`: remove replaceable/demo objects, excluding preserved ids.
- `set-property` / `update-property`: update title `_text` and navigation `_items` when targets exist.
- `add-child`: insert confirmed primary content into `_content_container_id`.

Do not mutate the root view when child-level adaptation is intended.

## 6) Required and optional anchors
Server-side validation reads `_adaptation_targets` from starter metadata:
- `_required`: array of required target field names.
- `_optional`: array of optional target field names.
- any key ending in `_id` is treated as a target field.
- target values may be a string id or an object with `_id`.

Rules:
- Required target fields must resolve to an explicit object id.
- Optional target fields may be absent.
- Any declared target id that is present must exist in a starter view JSON file.
- Target ids must not contain unresolved placeholders.
- Missing required anchors fail validation with `E_STARTER_INVALID_ADAPTATION_TARGET`.
- Missing optional anchors are allowed; present-but-invalid optional anchors fail.
- Adaptation must not guess undeclared ids.
- Preserved objects cannot be removal targets.
- Inserted content cannot duplicate declared child ids or existing view ids.

Current validation does not implement nested property-path validation in starter metadata. When a starter needs nested slots such as `_nav`, `_control`, `_actions`, or `_image`, declare the owning object id and use the object-pack contract for the slot shape.

## 7) Co-located semantic markers
Current source-of-truth storage is manifest metadata in `app.json -> _meta._starter`. Starter objects do not currently carry co-located semantic marker fields.

Maintenance rules:
- CSS or visual-only changes normally do not require metadata changes.
- Structural changes require metadata updates when ids, role ownership, target anchors, preserved objects, replaceable objects, optional removals, or entry-view ownership change.
- Do not infer semantic targets from CSS classes. Classes are visual selectors, not semantic anchors.

## 8) Placeholder contract
Supported placeholders are exactly:
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

Input params are `_app_id`, `_app_name`, `_app_title`, `_app_description`, `_vision`, `_app_archetype`, `_app_scope`, `_primary_entity`, `_primary_entity_title`, `_primary_view`, and `_primary_view_title`.

Defaults:
- `<app-id>` comes from sanitized `_app_id`.
- `<app-name>` falls back to starter app `_title`, then starter `_title`, then title-cased app id.
- `<app-title>` falls back to starter app `_title`, then app name.
- `<app-description>` falls back to `_vision`, starter description, then `<app-title> app`.
- `<app-archetype>` falls back to the starter's first `_archetypes` item, then `custom`.
- `<app-scope>` falls back to `single-app`.
- `<primary-entity>` falls back to `record`.
- `<primary-entity-title>` falls back to title-cased primary entity.
- `<primary-view>` falls back to starter `_entry_view`, then `main`.
- `<primary-view-title>` falls back to title-cased primary view.

Expansion rules:
- Placeholders expand after starter files are copied and before the app is loaded.
- Only tokens matching `<[a-z][a-z0-9-]*>` are considered placeholders.
- Required placeholders declared in `_required_placeholders` must resolve; unresolved required placeholders fail with `E_STARTER_UNRESOLVED_PLACEHOLDER`.
- Optional placeholders may remain unchanged when no value is available.
- ID-like keys are sanitized after expansion: `_id`, `id`, `_app_id`, `_view_id`, `_flow_id`, `_entity_id`, `_entry_view_id`, `_entry_view`, `_primary_view`, `_primary_entity`, `_source_view_id`, and `_target_id`.
- Fixed ids and preserved ids are not rewritten when the whole id string already equals that id.
- Unrestricted global string replacement is forbidden because it can rewrite stable shell ids, public paths, or unrelated literal text.

## 9) Stable ID rules
- Use deterministic, meaningful starter prefixes, for example `dashboard-main-scroll` and `dashboard-page-title`.
- Do not duplicate `_id` values in starter views or inserted adaptation content.
- Preserve ids declared in `_fixed_object_ids` and `_preserve_object_ids` across placeholder expansion and adaptation.
- Keep semantic anchor ids predictable and declared in `_adaptation_targets`.
- Inserted plan content must use confirmed semantic ids where source has them; current deterministic inserted ids are `starter-adaptation-primary-experience`, `starter-adaptation-primary-list`, and `starter-adaptation-primary-form`.
- CSS classes are not stable semantic identifiers.

## 10) XUI object composition
- Every persisted object must have a valid `_type`; `view` is the root type used by current starters.
- Child ownership follows the object-pack skill. Container-like objects may own `_children`; leaf and structured-slot objects must not own arbitrary children unless their contract says so.
- Nested slots such as `_nav`, `_control`, `_actions`, `_image`, `_logo`, and `_footer` are not automatically `_children`.
- Persisted handlers must be Nano-Commands/data-only objects or strings. Do not embed JavaScript functions in starter JSON.
- Prefer canonical image objects in starter JSON. Runtime URL shorthand may be supported by object packs, but starter defaults should use canonical shapes:

```json
{
  "_id": "dashboard-sidebar-logo",
  "_type": "image",
  "src": "assets/logo.svg",
  "alt": "Xpell Dashboard Starter logo"
}
```

## 11) Styles, themes, and assets
- Put starter-local CSS under `style/`; current Dashboard uses `style/custom.css`.
- Put starter-local public assets under `assets/`.
- Reference public files relatively as `style/...` or `assets/...`; creation rewrites them to `/public/<app_id>/...`.
- Avoid external CDN dependencies in reusable starters.
- Preserve rendering after copy by keeping CSS and asset references inside `style/` and `assets/`.
- Use isolated class names with a starter prefix, for example `dashboard-*` or `dash-*`.
- Theme ids are ordinary view/control data; current starters use view `_theme: "terminal"` and a persisted theme selector with `_data_source`, `_data_output`, `_persist`, `_on_data`, and `_on`.
- CSS-only edits should not require semantic metadata changes unless selectors depend on changed structural ids or role ownership changes.

## 12) Starter adaptation model
Generic flow:

```text
starter metadata + current runtime view + confirmed semantic plan
  -> validated starter-to-plan delta
  -> deterministic mutation plan
  -> atomic structured edits
  -> runtime verification
```

Adaptation must:
- preserve reusable shell/layout/runtime controls;
- remove or repurpose generic/demo content;
- update semantic slots such as title and navigation from the confirmed plan;
- insert confirmed primary content into the declared content container;
- keep the existing entry view when intended;
- avoid duplicate `main` views;
- remain app-domain-neutral.

The Dashboard starter has source tests adapting the same generic starter to shopping list, CRM, and scheduler plans. Do not add shopping-specific, CRM-specific, or scheduler-specific metadata to the Dashboard starter.

## 13) Atomicity and retry safety
- Prevalidate all targets before mutation.
- Apply zero changes when prevalidation fails.
- Starter adaptation mutation plans execute atomically by cloning the current view, applying supported steps in memory, then persisting once through `server-xvm.push_update`.
- If commit fails, the code attempts a best-effort rollback by pushing the original view.
- Stale starter mutation plans are rebuilt from current starter metadata and runtime state before execution.
- Retries do not replay stale guessed root or child ids.
- Idempotent retry returns completed/already-completed without duplicating inserted content.
- Completion occurs only after runtime verification records Project Memory completion.

## 14) Creating a new starter
1. Choose one reusable starter purpose and keep it app-domain-neutral.
2. Build a valid standalone app with `app.json` and at least one loadable entry view.
3. Add `_meta._starter` metadata.
4. Add only supported placeholders.
5. Declare semantic anchors through `_adaptation_targets` and object id lists.
6. Classify content into preserve, adapt, replace, and optional-remove lists.
7. Add `style/` and `assets/` only when needed.
8. Add validation tests for metadata, placeholders, assets, and load/copy behavior.
9. Test starter copy through `create_app_from_starter`.
10. Test at least two different semantic adaptations when the starter has an adaptation strategy.

A new reusable starter must prove it works across more than one final app domain.

## 15) Modifying an existing starter
- CSS-only changes: update CSS and visual tests if needed; metadata changes are not required unless selectors/ids/ownership change.
- Text changes: update generic starter copy/tests when asserted text changes; keep text domain-neutral.
- ID changes: update `_preserve_object_ids`, `_replaceable_object_ids`, `_adaptable_object_ids`, `_optional_remove_object_ids`, `_fixed_object_ids`, `_adaptation_targets`, tests, CSS selectors, and any XVibe builtin metadata.
- Moving objects: update metadata only when ownership, preserved ancestry, target container, or remove eligibility changes.
- Changing nested slots: preserve canonical slot shapes and update target metadata/tests when slot owner ids change.
- Replacing navigation: update `_primary_navigation_id` and XVibe `_navigation_object_ids`; tests must cover missing optional nav and property update behavior.
- Adding/removing demo content: update replaceable/optional-remove lists and generic-content verification tests.
- Changing entry view: update app `_meta._entry_view_id`, starter `_entry_view`, XVibe `_entry_view_id`, copy/load tests, and no-duplicate-main tests.
- Changing required semantic roles: update `_adaptation_targets._required`, validation tests, guide recommendation tests, and failure tests.

## 16) Required tests
Current coverage locations are listed in `SKILL_API_MAP.md`. Required coverage for starter changes:
- starter manifest normalization and legacy fallback;
- required role/target presence and existing id validation;
- optional role handling;
- declared id existence;
- placeholder expansion and unresolved required placeholders;
- fixed id preservation;
- asset path rewriting and copied public files;
- starter copy/load through `server-xvm.load_app_from_disk`;
- semantic adaptation recommendation and delta;
- preserve/remove correctness;
- atomic rollback and prevalidation failure;
- retry/idempotency and stale plan rebuild;
- no duplicate entry view/root replacement;
- compatibility with legacy starters;
- canonical image object shape.

## 17) Canonical examples
Empty starter:
- folder: `system-xapps/app-starters/Empty`
- starter id: `empty`
- entry view: `main`
- manifest mode: `blank-canvas`
- XVibe strategy: `none`
- preserved id: `view-style-sheet`
- no adaptation targets after copy in the server starter tests.

Dashboard starter:
- folder: `system-xapps/app-starters/dashboard`
- starter id: `dashboard`
- entry view: `main`
- manifest mode: `starter-to-plan-delta`
- XVibe strategy: `adapt-entry-dashboard`
- content container: `dashboard-main-scroll`
- title anchor: `dashboard-page-title`
- navigation anchor: `dashboard-primary-nav`
- preserved shell includes `dashboard-shell`, `dashboard-sidebar`, `dashboard-toolbar`, and `dashboard-theme-select`
- replaceable/demo content includes overview, KPI, records, activity, settings, modal, and toast objects.

Dashboard adaptation examples are illustrative only:
- Dashboard -> Shopping List inserts `Shopping Item` table/form content.
- Dashboard -> CRM inserts `Customer` table/form content.
- Dashboard -> Scheduler inserts `Appointment` table/form content.

Do not encode these domains into Dashboard starter metadata.

## 18) Hard forbiddens
- Do not hard-code one final app domain into reusable starter metadata.
- Do not infer semantic targets from CSS classes.
- Do not guess undeclared object ids.
- Do not use unrestricted placeholder replacement.
- Do not mark generic content as preserved merely because its container is preserved.
- Do not mutate the root view when child-level adaptation is intended.
- Do not leave an app partially adapted after validation or apply failure.
- Do not mark adaptation complete before runtime verification.
- Do not create duplicate `main` views.
- Do not embed functions in persisted JSON.
- Do not use invalid scalar image/child shapes in starter JSON.
- Do not modify starter output after user content has been created unless using an explicit migration.
- Do not document proposed starter APIs as implemented behavior.

## 19) Validation commands
Use the relevant command set for the files changed:

```bash
pnpm -C /Users/tamirfridman/Documents/projects/xpell.ai/packages/xvibe run build
pnpm -C /Users/tamirfridman/Documents/projects/xpell.ai/packages/xvibe run test
pnpm -C /Users/tamirfridman/Documents/projects/xpell.ai/packages/xnode run build
pnpm -C /Users/tamirfridman/Documents/projects/xpell.ai/packages/xnode run test
npm --prefix /Users/tamirfridman/Documents/projects/xpell.ai/xpell-vibe-starter/server run build
npm --prefix /Users/tamirfridman/Documents/projects/xpell.ai/xpell-vibe-starter/server run test:starters
python3 /Users/tamirfridman/.codex/skills/.system/skill-creator/scripts/quick_validate.py /Users/tamirfridman/.codex/skills/xpell-app-starter
```

Run skill validation whenever this skill changes. Run package/starter tests whenever starter contracts, runtime metadata, copy/load, placeholders, images, or adaptation behavior change.

## 20) Source truth
If this skill and source disagree, follow source and update this skill plus companion files.
