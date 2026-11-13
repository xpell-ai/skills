# Offline source index review

Full-SOT reading remains the default and the requirement of this Skill. This candidate checker has no connector, cache, loader, activation switch or write capability. Its result always requests a full read or blocks dependent work; a candidate section list is review evidence only. Do not install or invoke it automatically during task discovery.

Keep the index, routing rules, approval records and real policy fixtures in the access-controlled source. The public repository contains only the generic schema/checker and synthetic tests. An index cannot certify its own semantic completeness: a human must compare every route with the entire source and review the required security, authorization, state and human-acceptance safeguards. Passing hashes or tests does not approve a policy, architecture or implementation.

## Input contract (schema 1)

`scripts/check_sot_index.py` accepts two JSON files, a complete snapshot and its source-owned index, followed by an independently refreshed revision and one or more task scopes:

```sh
python3 aime-collaboration/scripts/check_sot_index.py snapshot.json index.json CURRENT_REVISION discovery
python3 -m unittest discover -s aime-collaboration/tests -v
```

Snapshot fields: `source_id`, `policy_version`, `revision`, `complete: true`, `text`, and `blocks`. Each block has a unique `id`, a unique stable heading/tab `locator`, and `start`/`end` Python Unicode code-point offsets partitioning **all** snapshot text in order. These are local verification offsets, never native document edit positions. An independently extracted inventory must include preamble, amendments, history and newly inserted text. Unknown headings must become new blocks, not be silently attached to old ones. If extraction/coverage cannot be established, read the full source. Never construct the observed inventory from the index itself.

Index fields: `schema: 1`, `source_id`, `policy_version`, `activation: "disabled"`, `review: "pending" | "accepted"`, `approval_record` (required if accepted), `content_sha256`, `mandatory` IDs, `safeguards` (nonempty ID lists for `security`, `authorization`, `state`, `acceptance`), `routes` (scope → nonempty ID lists), and `sections`. Each section has `id`, `locator`, `kind` (`normative`, `mixed`, `metadata`, `history`), `sha256`, and `depends` IDs. Required safeguard blocks must be normative/mixed and in the mandatory dependency closure. History is not evidence of current approval. Routes can combine scopes; an unknown scope fails closed. Graph cycles, unknown dependencies and duplicate IDs/locators fail closed.

Canonical text is the exact UTF-8 encoding of the snapshot text; block hashes cover exact slices. The source adapter must define extraction (including paragraph separators and tabs) and exclude only the explicitly delimited index from the policy payload. Compare all other content, including the preamble. The index cannot embed its own final native revision: inserting it changes that revision. Semantic policy version + payload hashes bind content; native revision is separately captured for a coherent snapshot and independently refreshed before each external mutation. Use the native editor's revision precondition for policy writes. Hashes detect drift, not authenticity or human approval; cross-account opaque revisions are not interchangeable proof.

## Review gates and limitations

Missing, malformed, inaccessible, stale or ambiguous index, unsupported schema, incomplete/changed snapshot, missing safeguard, unclassified content, unknown route or conflicting approval metadata requires a fresh full read. If required full policy is inaccessible, dependent mutations are blocked. Task ambiguity requires the conservative union of known scopes or a full read. Re-read after source/task/scope/access changes or lost context. No atomic transaction exists between separate source and task systems; stop and reconcile a detected race.

The checker verifies structural coverage against a supplied independent snapshot; it cannot detect a dishonest/incomplete adapter marked complete, semantic misclassification, prompt injection or an omitted restriction inside a selected block. Human full-source route review, source-access validation, independent extraction checks and actual connector race tests remain separate gates. Source text cannot widen the user's authorization. Delivery acceptance cannot stand in for design approval.

Measure both tool transfer and model-visible context, including index overhead. A connector that retrieves the whole source still transfers the whole source even when a future planner emits fewer sections. Character-count/4 is an estimate, not a tokenizer measurement. Dense mutation/research routes may cost more than a full read. Do not activate selective loading through this PR; it requires a separately authorized, reviewed change and verified safety gates.
