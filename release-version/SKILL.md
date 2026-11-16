---
name: release-version
description: Plan, prepare, validate and coordinate safe, auditable package releases (including npm, pnpm workspaces, independent Git repositories, version tags and registry verification). Use for release planning, readiness checks, publishing gates, version policy, recoveries and post-release handoffs.
---

# Release Version — פרסום גרסה

Treat a release as a gated, evidence-backed process, not as a single `npm publish` command. A release calendar or a request to "prepare" does not approve registry writes. Follow the current source-owned release policy, scoped task and owning repositories; never treat this generic, public skill as the team's policy Source of Truth.

## Resolve live authority and scope

1. Identify the release owner, release task/Issue, intended package set, version-policy exceptions, distribution targets, review state and exact requested action. If this is a team task, also use `aime-collaboration` and read its live authorized Source of Truth.
2. Read the current release policy, SOP, amendments, task history, ownership, and repository instructions from the links and records available to this participant. Do not embed or infer private internal URLs, privileges, approvals or a past agent's local files. Before any external mutation, refresh those sources and check for competing claims.
3. Distinguish workspaces, packages and owning Git repositories. Use the actual package manifests and registry reads, not folder names, to define the release inventory. Identify packages with independently managed SemVer **only from documented owner decisions**, not because they have separate modules or Git repositories.
4. Record what is authorized now (read-only discovery, source modifications, merge, public publish, dist-tag promotion, Git tags/releases, deploy) and what is not. Each state-changing action class needs its own accountable approval under the current policy.

## Run gates in order

Use [the per-gate checklist](references/release-checklist.md) and the currently authorized SOP for concrete commands and pass/fail standards.

- **Gate 0 — Inventory and topology:** every candidate package, name, source version, latest and custom npm dist-tags, public/private status, Git repo/branch/dirty state, deps, supported runtimes and license; construct dependency DAG, highlight cycles and independently versioned exceptions.
- **Gate 1 — Baseline:** reproduce supported build, typecheck, unit/integration/smoke/security tests with local workspace manifests intact; distinguish tested profiles, historical evidence, skips and missing CI from actual passes.
- **Gate 2 — Version and notes:** propose SemVer per approved family and approved independent exceptions, check downstream dependency constraints, migration/breaking changes, README/CHANGELOG/licenses. Never blindly replace `workspace:*` in source; verify the package manager's packed output.
- **Gate 3 — Pack and freeze:** create exact distributable archives; audit packed `package.json` across all dependency fields for `workspace:`, `file:`, `link:`, correct versions and runtime files; scan archives for secrets/private data; record SHA256/SHA512, contents and source Git SHA/tree; verify a clean, pinned, archive-only consumer. Treat the manifest and archives as immutable after approval.
- **Gate 4 — Git source review:** review per-repository diffs, isolate unrelated and dirty work, create/review/merge source PRs only when approved; verify source commit → merge commit/tree → archive binding. Do not automatically tag Git or assume the workspace root is a repository.
- **Gate 5 — Controlled registry publication:** require a **new, explicit** owner authorization covering exact frozen archives, package/version order, public exposure, custom tags, interactive authentication, accepted limitations and stop conditions. Reverify identity, scope ACL, 2FA/trusted-publishing requirements, version absence, repository/ref and archive bytes before **each** write. Publish one exact approved archive at a time in dependency order without rebuild/repack or unapproved scripts. Handle native OTP/passkey only in the approved private interface; never log/share credentials, OTPs or bypass tokens.
- **Gate 5 readback:** `publish` exit 0 means attempted upload succeeded, **not** registry-qualified. Require independent package/version metadata, actual old/new dist-tags, downloaded registry tarball exact bytes/integrity and a fresh registry-only clean consumer for the published dependency prefix before proceeding. Keep separately visible statuses: `UPLOAD_SUCCEEDED`, `REGISTRY_VERIFIED`, `CONSUMER_VERIFIED`. Do not call an incomplete release complete.
- **Gate 6 — Promotion and Git record:** request separate authorization to change `latest` or other tags, and separately to create/push per-repository Git tags and GitHub Releases bound to verified source commits. npm dist-tags are not Git tags. Archive the final release matrix, release notes, checksums and evidence.
- **Gate 7 — Consumer integration / deployment:** if in scope, qualify actual downstream apps against the registry and frozen lockfiles. Staging, production, migrations and paid/live calls require their own approvals; npm publication never authorizes deployment.

## Publication-specific failure rules

- A custom non-`latest` tag is **not private**: the new package/version can still be installed explicitly or via dependency ranges. Record public/non-atomic/partial-publication risk before requesting approval.
- npm **first publication** of a new name may create `latest` pointing to the first version even when an alternate tag was requested, or show staged-publishing placeholder metadata. Verify what actually happened. Accept it only if the owner's approved plan explicitly allows that exact outcome. Do not silently repair or change tags.
- A newly published version may temporarily yield E404, ETARGET or stale package-root metadata. Pause subsequent uploads; reconcile with independent read-only registry checks, empty caches and a **pre-approved bounded wait/backoff**. An unchanged first failure remains evidence. Do not interpret delay as proved propagation root cause.
- If an upload returns an uncertain result, or version/permissions/metadata/tags/integrity/consumer differ from approved expectations, **STOP**. Inventory packages as `present-identical`, `present-mismatched`, `absent` or `unknown`; record dependencies and risk. Never blindly retry, overwrite a published version, modify ACL/2FA, unpublish, deprecate or retag to conceal the discrepancy. Request a new recovery decision; changed bytes need a new version and requalification.
- Treat independently versioned packages as documented exceptions and preserve their own SemVer. Detect additional candidates and **report** them for owner review; do not change an approved frozen release mid-flight.

## Evidence, human approvals and cadence

Maintain a versioned manifest containing exact package name/version, owning repo, source/merge/tree SHA, tarball SHA256/SHA512, publish sequence, expected and observed tags, verification states, tests, limitations and recovery history. Preserve all earlier evidence seals and original user work. Publish meaningful PROGRESS, STOP and final HANDOFF on the task record; distinguish new tests from historical ones and list executed vs prohibited actions.

Use a monthly **planning/review window only if the active owner's policy says so**; do not infer a mandatory SemVer bump or force a release to meet a date. Hotfixes may run outside the train under the same integrity and authorization principles. Record `GO` / `NO-GO` explicitly at each gated decision. Human acceptance, Git tagging and cloud deployment never follow from a published npm tarball by implication.

## Before claiming completion

The release is complete only when every intended package/exception has verified registry artifacts and clean consumers, required promotions and Git records are either separately approved and done or explicitly documented as deferred, and a human has accepted the results. Follow task status and closure rules of the live collaboration process; do not close a task simply because a command returned successfully.
