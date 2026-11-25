# Development and local runtime

## Select an isolated path

1. Confirm the Router Git boundary and the workspace/package graph. Read the root, server, and client manifests. The workspace `pnpm dev` chain builds sibling SDKs and starts the filesystem entrypoint. Check that script paths match the checkout. For a scoped test, use a disposable source/build tree with the correct dependencies and only the needed fixtures. Distinguish workspace-linked builds from the registry build profile.
2. Exclude live work directories, settings and environment files, credentials, databases and sidecars, backups, and route traces from fixture materialization. Derive schema-only fixtures from committed definitions and follow the selected suite's setup. Use a minimal credential-free environment, mock transports, and keep opt-in live cases skipped. Select tests for the real entry point, including browser, restart, or native tests where relevant. Report build, mock, native, browser, and live results at their actual scope.
3. For SQLite native failures, run `pnpm --dir server run test:native` in the isolated workspace with the runtime required by the target. The probe checks Node/ABI, package manager, driver, SQLite durability and flock on temporary files. Check the target's actual installed binaries and platform before any scoped rebuild. A successful probe does not establish installed-store readiness.

## Identify the local listener

The workspace default is port **3001**, with Console entry points at `/` and `/admin`. Its Vite build clears and writes `server/work/public`. Establish who owns the target listener and which working directory, entrypoint, store, and static root it uses. Use a free loopback port and distinct storage for a disposable instance. Revert any temporary change to the repository's development port setting to 3001.

Use the profile's readiness and read-only Wormholes v2 HELLO when available. A listener and HELLO establish reachability and handshake, with authorization and reconciliation checked separately. Verify host-level ownership before attempting a stopped-store operation. Restricted process visibility is insufficient evidence of exclusivity.

**Historical lessons.** Prior audits found workspace sibling aliases that did not match the checkout, missing fixtures in a clean source export, and a Node 24 native cleanup failure in a previously qualified lane. Check current paths, fixtures, and runtime requirements before diagnosing a fresh failure.

Sources in Router: `README.md`, `AGENTS.md`, `server/package.json`, `client/package.json`, `client/vite.config.js`, `server/scripts/verify-native-test-runtime.mjs`, `server/storage/xai-router-entities.json`, `docs/runtime-foundation.md`, and `build/npm-only/README.md`.
