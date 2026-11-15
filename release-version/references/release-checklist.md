# Release Version — evidence and gate checklist

This is a **generic template**. The active team's SOP and owner approval decide which specific commands and release constraints apply. Never copy private task records or credentials into this public repository.

## Release manifest (one row per package)

| Field | Required information |
| --- | --- |
| Identification | package name; independent/coordinated SemVer policy; intended version |
| Source | owning Git repo; source commit SHA; approved merge commit SHA and tree; original dirty work preserved |
| Eligibility | public/private; npm write access; 2FA/publisher policy evidence (verified vs unverified); license |
| Artifact | immutable file path, SHA256, SHA512, packed manifest, files/exports/types/assets, secret scan |
| Dependencies | all internal edges, resolved publish versions; no unresolved local workspace/file/link protocols |
| Publication | batch/order; exact `npm publish` scope/flags; approved custom tag; expected first-publish behavior |
| Verification | CLI upload result; direct registry metadata; downloaded archive bytes; final tags; clean consumer profile |
| Recovery | original failure receipts; classified actual registry state; next human decision/stop condition |

## Gate checkpoints

### 0. Scope
- [ ] Release task and accountable owner linked.
- [ ] Current policy/SOT and all amendments read; no competing claim.
- [ ] Workspace/package/Git-repo matrix including exclusions.
- [ ] Internal DAG and independent SemVer exceptions agreed.
- [ ] npm versions/tags checked; distinguish private/404/uncertain.
- [ ] GO/NO-GO evidence and next actor.

### 1. Baseline
- [ ] Supported toolchain pinned in evidence.
- [ ] Builds/typechecks/tests run; skipped/unsupported environments visible.
- [ ] No unapproved workspace-source edits or secret-bearing logs.

### 2. Version
- [ ] Semantic version proposal approved per package family.
- [ ] Internal dependency versions and changelogs validated.
- [ ] Source `workspace:*` preserved unless narrowly justified by actual pack behavior.

### 3. Immutable artifacts
- [ ] Build/pack method recorded, exact tarballs frozen and hashed.
- [ ] All runtime files, exports, entrypoints, declaration types and licenses present.
- [ ] Packed deps free of `workspace:`, `file:`, `link:` and local absolute paths.
- [ ] Archive contains no keys, .env, DBs, logs, private or accidental files.
- [ ] Fresh consumer installs exact approved archives only.
- [ ] Manifest records source/merge/tree → archive bindings.

### 4. Git review
- [ ] PRs or owned source edits separately approved.
- [ ] Commits, merges, trees, source diffs and preserved dirty work verified.
- [ ] Exact publish commands, expected tags and failure modes reviewed.
- [ ] **New approval required before any public registry write.**

### 5. Per-package npm release
- [ ] Re-read owner scope and mutable live prerequisites before writing.
- [ ] Version still absent, unchanged pre-existing tags, correct identity/permissions/2FA.
- [ ] Exact sealed archive file and checksums unchanged; correct dependency order.
- [ ] One authorized publication attempt; no hidden rebuild or workspace publish.
- [ ] Private human completes native passkey/OTP; no token/OTP copied to logs.
- [ ] Distinct states: upload result, registry metadata/integrity/tag readback, consumer validation.
- [ ] For new packages, public ACL/policy and actual first-publish `latest`/placeholder checked.
- [ ] Fresh registry-only prefix consumer with exact versions and empty cache passes.
- [ ] On unexpected state: STOP, classify entire release and seek owner recovery decision.

### 6. Promotion and Git record
- [ ] All intended packages are registry-verified and consumer-verified.
- [ ] Human separately approves `latest`/tag promotion or documents deferral.
- [ ] Human separately approves per-repository Git tags / GitHub Releases.
- [ ] Tag targets correspond to accepted source SHA/tree; release notes link exact versions.
- [ ] Preserve evidence, scope exceptions and review decisions.

### 7. Downstream qualification
- [ ] Actual app consumers tested from registry with frozen locks.
- [ ] CI, security, native builds, browser/server and cloud gaps explicitly stated.
- [ ] Deployment/migrations paid/live actions separately approved if applicable.

## Required HANDOFF

State: `GO`, `NO-GO`, `STOPPED`, or `PARTIAL` (never use GO to imply public publish approval).

Provide: task and owner; current approval ID and scope; actual package-version matrix and status; sealed manifest; exact commands and independent receipts; passed/failed/unrun checks; observed tags and public exposure; original failures; preserved user work; risks/limitations; next actor and exact action.

## Recovery rules

Use a bounded read-only registry verification window *only when approved*; independently fetch package root and exact version, compare HTTP response/caching patterns, downloaded bytes and consumer behavior. An unresolved readback is not permission to retry upload. On partial publication, classify ALL intended versions. No overwrite, unpublish, retag, automatic repair, bypass of authentication or resume after STOP without a new owner decision.
