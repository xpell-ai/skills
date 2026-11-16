# Install and invoke release-version

The skill is a **public, reusable procedure**. It does not grant npm, GitHub, Drive, cloud or other credentials and is not the organization's policy source. The active human owner must grant distinct approvals before publication, tag promotion, Git tags/releases and deployment.

## Review source and install

Review this skill's Pull Request and the current organization's release policy first. After acceptance, install from the approved commit/branch, rather than assuming a local `~/.codex/skills` checkout is automatically updated.

```text
$skill-installer Install release-version from https://github.com/xpell-ai/skills/tree/main/release-version
```

To review a proposed PR before merge, substitute that PR's branch in the URL. If `~/.codex/skills` is itself the Git checkout, do not clone a nested copy. Check its remote, worktree and selected commit first, then add/update only the reviewed skill. Each developer (including collaborators) installs or updates independently, with their own authorized app connections.

## Safe dry run

```text
$release-version Audit the next release scope and build an evidence-based gate plan from the linked release task and its current SOP. Read only; do not publish, tag, commit, merge or deploy.
```

## Execution on an approved task

```text
$release-version Resume the release task at [authorized Issue URL]. Read live owner approvals, check exact immutable package artifacts and execute only the currently approved gate. Stop on drift; post a HANDOFF.
```

A dry run verifies discovery and scope, not registry write permissions. Installed skill revision, authorized SOT access, actual npm authentication/2FA and source checkouts all need independent verification. No scheduled run or automatic agent wake-up is implied by creating this skill or an Issue.
