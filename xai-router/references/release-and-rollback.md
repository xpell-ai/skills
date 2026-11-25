# Release and rollback

## Prepare and qualify

1. Identify the exact approved source revision, profile, artifact digest and inventory, predecessor, runtime/platform/ABI, and store compatibility. Follow that profile's verifier and runbook. Matching version labels, a linked workspace build, or an older receipt cannot substitute for verified bytes and platform evidence. The registry build uses a generated allowlisted context. Keep the repository root and live work out of Docker context.
2. Rehearse admission, restart and rollback on disposable or expressly approved copies with live dispatch disarmed. Record separate artifact, native, reconciliation and Console results. A missing trusted input blocks that lane. Preserve earlier failed attempts and the scope of any subsequent pass.

## Before authorized activation

3. Confirm the exact scope, target and launch mechanism. Stop only the approved writer. Verify host-level quiescence and keep other services available. Capture a verified cold whole-work backup with database and present WAL/SHM, markers, lock state, relevant config/view state and exact prior release provenance. Keep it private and verify its inventory and integrity. If the profile binds filesystem identity, preserve the original store's required path and inode bindings for rollback or rehearse the runbook's approved rebinding before activation.
4. Start only the approved artifact using its documented launcher. Ordinary startup can write ownership and reconciliation state. Check a single intended listener, readiness, authenticated account and Console access, and read-back of store identity, history, ledger, holds and catalog as applicable. Stop on divergence. Record sanitized evidence.

## On activation failure

5. Stop the candidate and retain the store, evidence, prior release and backup. Verify predecessor compatibility and compare durable effects before any rollback. A release rollback and a data restore are different operations. Rehearse the exact approved rollback on a copy. If committed effects, ownership epochs, bindings, or supported terminal states differ, preserve both states and escalate. Never overwrite the active database, hand-edit signed markers, remove a lock to force entry, or rewind fencing counters as a routine rollback.

**Historical lesson.** Device metadata drift was reproduced with an unchanged logical store. It did not prove the cause of a host incident or establish rollback freshness. Follow the selected launcher’s documented admission and maintenance rules when physical identity changes.

Sources in Router: `docs/release-composition-rc1.md`, `build/npm-only/README.md`, `docs/sqlite-backup-restore-r4a.md`, `docs/sqlite-rollback-preflight-gemini35.md`, `server/src/runtime/RouterWriterOwnership.ts`, and `server/src/candidate/ReleaseRuntime.ts`. Treat dated installation and qualification reports as historical evidence.
