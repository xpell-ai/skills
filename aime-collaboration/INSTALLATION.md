# Install and invoke aime-collaboration

Each developer installs a copy and connects their own authorized GitHub and Drive accounts. The skill shares a procedure; it does not share credentials, local checkouts, chat history or permissions. Task repositories, Projects and linked SOT documents require independent access.

## Source and revision

The shared source is [xpell-ai/skills](https://github.com/xpell-ai/skills), with `aime-collaboration/` at repository root. For review, use the specific proposed PR revision without treating it as installed. Distribution after separate authorization must name the exact reviewed commit, not an old example branch or moving default branch. Record the exact installed commit on each machine; do not assume copies are synchronized.

If your local skills folder is itself a checkout of this repository, add/update the skill at its root on the appropriate branch. Do not clone another repository inside it or copy the same skill to a second discovery location. Verify the Git remote, branch and working tree first. Local discovery and remote publication are separate checks even when synchronization is configured.

## Installation for each developer

Use the bundled installer in Codex (select the PR branch for review):

```text
$skill-installer Install aime-collaboration from https://github.com/xpell-ai/skills/tree/REVIEWED_REVISION/aime-collaboration
```

Replace `REVIEWED_REVISION` only with the separately approved revision; do not run installation as part of a review task. Preserve an existing installation and inspect its revision before updating. A missing source or denied connection is an access/setup blocker, not a reason to recreate the protocol from memory.

For manual installation, use a fresh checkout at a chosen revision:

```sh
git clone https://github.com/xpell-ai/skills.git aime-shared-skills
git -C aime-shared-skills checkout --detach REVIEWED_REVISION
git -C aime-shared-skills rev-parse HEAD
mkdir -p "$HOME/.agents/skills"
test ! -e "$HOME/.agents/skills/aime-collaboration" && test ! -L "$HOME/.agents/skills/aime-collaboration" && cp -R aime-shared-skills/aime-collaboration "$HOME/.agents/skills/aime-collaboration"
```

The final command refuses to overwrite an existing folder or symlink. Copy the entire directory, including `agents/` and `references/`. Current Codex supports `~/.agents/skills` for user skills and `.agents/skills` for repository skills; some bundled installers use `${CODEX_HOME:-$HOME/.codex}/skills`. Use one recognized location and confirm the skill appears. Restart if automatic discovery does not show it. See [official skill documentation](https://learn.chatgpt.com/docs/build-skills).

## Invoke and verify

Mention `$aime-collaboration` or select it in the skill picker. Normal automatic selection remains enabled. Replace the bracketed task repository/Issue below with the authorized source; use its actual Issue number, not a title prefix.

```text
$aime-collaboration What are our open tasks in [task repository]?
```

```text
$aime-collaboration Execute [Issue URL] according to its acceptance criteria and report the handoff to that Issue.
```

For a safe onboarding check, each developer independently runs:

```text
$aime-collaboration Read [pilot Issue URL], resolve the current approved policy authority, and read the complete policy from that source. Report the current owner, executor, status evidence, unmet acceptance criteria and next action. Read only: do not claim, comment, relabel, dispatch a workflow or close it.
```

The skill resolves the private SOT, exact status/executor mappings and workflow behavior through authorized reads at runtime. No internal URLs or private protocol copies need to be added to this repository. Each developer records the installed revision and sanitized check results in the authorized task record. One developer's success cannot establish the other's access. Cross-account update visibility requires a separately authorized real handoff test. Installation and label changes do not create autonomous agent triggers.

## Source-switch distribution gate

Read [policy-authority.md](references/policy-authority.md). A public PR merge does not update installed Codex copies, other machines, Dot or ChatGPT. Before any later approved cutover, inventory each participating runtime/account and actual discovery location, record its loaded Skill commit/blob and current behavior, and obtain separate authorization for distribution. Preserve local changes and duplicate-location findings; do not install during review.

After separately authorized distribution, start a fresh agent session and verify the loaded Skill bytes/revision, not just its picker name. Use a read-only request to resolve the live approved authority, read the full policy and report source/version/revision plus approval evidence. Test pre-cutover document selection and post-cutover approved Git selection, denied Git access, stale/conflicting authority and rejection of archived-document fallback. An isolated fixture/process or subagent test must be labeled with its actual runtime and does not prove a fresh desktop/product tab or another account.

Do not cut over while a required participant still loads legacy source-selection instructions or cannot verify the current authority. Record per-account results, untested runtimes, rollback approval gate and exact next operator action in the authorized private task. Keep private source URLs and observations out of this public repository.
