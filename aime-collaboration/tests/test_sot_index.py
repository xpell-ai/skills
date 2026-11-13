"""Synthetic policy only: no company records, URLs or workflow mappings."""
import copy
import importlib.util
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location(
    "checker", Path(__file__).parents[1] / "scripts/check_sot_index.py")
checker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(checker)


def fixture():
    content = {
        "base": "Safety, authorization, state and human acceptance apply.\n",
        "record": "Delivery acceptance does not approve design or implementation.\n",
        "change": "Refresh live ownership and automation before a state change.\n",
        "history": "Historical trial; no current authorization.\n",
    }
    snapshot = dict(source_id="synthetic", policy_version="example-1", revision="r1",
                    complete=True, text="".join(content.values()), blocks=[])
    index = dict(schema=1, source_id="synthetic", policy_version="example-1",
                 activation="disabled", review="pending", content_sha256=checker.digest(snapshot["text"]),
                 mandatory=["base"], safeguards={x: ["base"] for x in
                 ("security", "authorization", "state", "acceptance")},
                 routes={"discovery": ["base"], "research": ["record"], "mutation": ["change"]}, sections=[])
    offset = 0
    for key, text in content.items():
        snapshot["blocks"].append(dict(id=key, locator="tab/" + key, start=offset, end=offset + len(text)))
        index["sections"].append(dict(id=key, locator="tab/" + key, sha256=checker.digest(text),
                                      kind="history" if key == "history" else "normative",
                                      depends=["record"] if key == "change" else []))
        offset += len(text)
    return snapshot, index


class CandidateTests(unittest.TestCase):
    def setUp(self):
        self.snapshot, self.index = fixture()

    def check(self, scopes=None, revision="r1"):
        return checker.inspect_candidate(self.snapshot, self.index, revision, scopes or ["discovery"])

    def test_routes_and_dependency_union_against_explicit_oracle(self):
        oracle = {"discovery": ["base"], "research": ["base", "record"],
                  "mutation": ["base", "record", "change"]}
        for scope, expected in oracle.items():
            with self.subTest(scope=scope):
                self.assertEqual(self.check([scope])["candidate_sections"], expected)
        self.assertEqual(self.check(["research", "mutation"])["candidate_sections"], oracle["mutation"])

    def test_never_activates_even_with_accepted_metadata(self):
        self.index.update(review="accepted", approval_record="synthetic reviewer decision")
        result = self.check()
        self.assertTrue(result["valid_candidate"])
        self.assertEqual(result["action"], "read_full_sot")
        self.assertFalse(result["selective_loading"])

    def test_missing_index_and_unavailable_full_source(self):
        self.index = None
        self.assertFalse(self.check()["valid_candidate"])
        self.snapshot = None
        self.assertEqual(self.check()["action"], "block_dependent_writes")

    def test_concurrent_edit_or_revision_unavailable(self):
        for revision in ("r2", "", None):
            with self.subTest(revision=revision):
                self.assertFalse(self.check(revision=revision)["valid_candidate"])

    def test_negative_schema_coverage_and_approval_cases(self):
        cases = {
            "version": lambda s, i: i.update(policy_version="old"),
            "identity": lambda s, i: i.update(source_id="other"),
            "schema": lambda s, i: i.update(schema=2),
            "activation": lambda s, i: i.update(activation="enabled"),
            "approval": lambda s, i: i.update(review="accepted"),
            "conflicting approval": lambda s, i: i.update(review="both"),
            "truncated": lambda s, i: s.update(complete=False),
            "new text": lambda s, i: s.update(text=s["text"] + "New restriction\n"),
            "new block": lambda s, i: i["sections"].pop(),
            "new heading inventory": lambda s, i: s["blocks"][3].update(id="new-rule"),
            "duplicate ID": lambda s, i: i["sections"].append(copy.deepcopy(i["sections"][0])),
            "duplicate observed ID": lambda s, i: s["blocks"][1].update(id="base"),
            "stale locator": lambda s, i: i["sections"][0].update(locator="old"),
            "duplicate locator": lambda s, i: s["blocks"][1].update(locator="tab/base"),
            "gap": lambda s, i: s["blocks"][1].update(start=0),
            "unclassified tail": lambda s, i: s["blocks"].pop(),
            "stale block": lambda s, i: i["sections"][0].update(sha256="wrong"),
            "unknown dependency": lambda s, i: i["sections"][3].update(depends=["missing"]),
            "cycle": lambda s, i: i["sections"][0].update(depends=["base"]),
            "history safeguard": lambda s, i: i["sections"][0].update(kind="history"),
            "missing safeguard": lambda s, i: i["safeguards"].pop("security"),
            "omitted safeguard": lambda s, i: i["safeguards"].update(acceptance=["record"]),
            "invalid route": lambda s, i: i["routes"].update(unused=["missing"]),
        }
        for name, mutate in cases.items():
            with self.subTest(case=name):
                self.snapshot, self.index = fixture()
                mutate(self.snapshot, self.index)
                result = self.check()
                self.assertFalse(result["valid_candidate"])
                self.assertEqual(result["action"], "read_full_sot")

    def test_ambiguous_scope_requires_full_read(self):
        self.assertFalse(self.check(["unknown"])["valid_candidate"])

    def test_changed_text_with_updated_root_hash_still_fails_block_hash(self):
        self.snapshot["text"] = self.snapshot["text"].replace("Safety", "SAFETY")
        self.index["content_sha256"] = checker.digest(self.snapshot["text"])
        self.assertFalse(self.check()["valid_candidate"])

    def test_index_is_not_approval_or_user_authority(self):
        # Text semantics cannot be proved by structural hashes: never emit an execution action.
        self.assertEqual(self.check(["research"])["action"], "read_full_sot")


if __name__ == "__main__":
    unittest.main()
