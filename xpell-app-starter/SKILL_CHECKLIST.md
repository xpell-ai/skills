# Xpell App Starter Contract Checklist

Use this checklist before merging any starter or starter-contract change.

- [ ] The starter is reusable across more than one final app domain.
- [ ] `app.json` exists and `app.json -> _meta._starter` is valid JSON metadata.
- [ ] `_id`, `_title`, `_description`, `_entry_view`, `_starter_version`, `_keywords`, `_archetypes`, `_starter_capabilities`, `_preserve_object_ids`, and `_replaceable_object_ids` are correct.
- [ ] `_adaptation_strategy._mode` matches implemented behavior: `blank-canvas`, `starter-to-plan-delta`, or legacy-compatible fallback only.
- [ ] XVibe strategy compatibility is explicit: `empty` means `none`; dashboard-style adaptation means `adapt-entry-dashboard`.
- [ ] Required `_adaptation_targets` resolve to existing object ids.
- [ ] Optional `_adaptation_targets` are either absent or resolve to existing object ids.
- [ ] No target id contains unresolved placeholders.
- [ ] Preserved ids are not listed as removable/replaceable demo targets.
- [ ] `_fixed_object_ids` and `_preserve_object_ids` cover ids that must survive placeholder expansion.
- [ ] Placeholder usage is limited to the supported placeholder list.
- [ ] Required placeholders are declared in `_required_placeholders` and resolve during copy.
- [ ] ID-like placeholder expansions produce safe ids.
- [ ] No global find/replace can rewrite stable ids, public paths, or unrelated text.
- [ ] Public files live only under `style/` and `assets/`.
- [ ] Public references use relative `style/...` or `assets/...` paths before copy.
- [ ] Copied public references rewrite to `/public/<app_id>/...`.
- [ ] Starter CSS is isolated by starter-specific class names.
- [ ] CSS-only changes did not unnecessarily change semantic metadata.
- [ ] Every persisted XUI object has a valid `_type`.
- [ ] Structured slots such as `_nav`, `_control`, `_actions`, `_image`, `_logo`, and `_footer` use object-pack-approved shapes.
- [ ] Image slots use canonical image objects with `_type: "image"`, `src`, and `alt`.
- [ ] Persisted starter JSON contains no JavaScript functions.
- [ ] Dashboard-like starters use xdashboard types where available instead of raw generic objects.
- [ ] Entry view stays stable and no duplicate `main` view is introduced.
- [ ] Adaptation inserts primary content into the declared content container, not the root view.
- [ ] Generic/demo content is replaceable or optional-remove, not accidentally preserved.
- [ ] Adaptation remains idempotent and does not duplicate `starter-adaptation-primary-experience`.
- [ ] Stale starter mutation plans are rebuilt before execution.
- [ ] Atomic adaptation prevalidation applies zero changes on failure.
- [ ] Runtime verification is required before marking starter adaptation complete.
- [ ] Legacy starter metadata fallback still works if compatibility is affected.
- [ ] Tests were updated for metadata, placeholders, assets, copy/load, adaptation, rollback, idempotency, and image contracts.
- [ ] `SKILL.md`, `SKILL_API_MAP.md`, and this checklist are updated when public starter behavior changes.
