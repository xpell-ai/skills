#!/usr/bin/env python3
"""Offline candidate review only. Never returns permission for selective loading."""
import hashlib
import json
import sys


def digest(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def ids(value):
    require(isinstance(value, list) and bool(value), "expected nonempty ID list")
    require(all(isinstance(x, str) and x for x in value), "invalid ID")
    require(len(value) == len(set(value)), "duplicate ID reference")
    return value


def inspect_candidate(snapshot, index, current_revision, scopes):
    """Inspect a complete independently extracted snapshot, with no I/O or effects."""
    if snapshot is None:
        return {"action": "block_dependent_writes", "reason": "full source inaccessible"}
    result = {"action": "read_full_sot", "selective_loading": False}
    try:
        require(isinstance(index, dict), "index missing or inaccessible")
        require(type(index["schema"]) is int and index["schema"] == 1, "unsupported schema")
        require(index["activation"] == "disabled", "activation is not authorized")
        require(index["review"] in ("pending", "accepted"), "ambiguous review state")
        require(index["review"] != "accepted" or bool(index.get("approval_record")),
                "accepted index lacks approval record")
        require(snapshot["complete"] is True, "incomplete source snapshot")
        for key in ("source_id", "policy_version"):
            require(isinstance(snapshot[key], str) and bool(snapshot[key])
                    and index[key] == snapshot[key], "source identity/version mismatch")
        require(isinstance(current_revision, str) and bool(current_revision)
                and current_revision == snapshot["revision"],
                "source revision unavailable or changed; fetch fresh full source")
        text = snapshot["text"]
        require(isinstance(text, str) and bool(text), "empty source text")
        require(digest(text) == index["content_sha256"], "source content digest mismatch")
        observed = {}
        cursor = 0
        locators = set()
        for block in snapshot["blocks"]:
            start, end = block["start"], block["end"]
            require(type(start) is int and type(end) is int
                    and start == cursor and start < end <= len(text), "gap/overlap in inventory")
            require(isinstance(block["id"], str) and bool(block["id"])
                    and block["id"] not in observed, "duplicate/invalid observed ID")
            require(isinstance(block["locator"], str) and bool(block["locator"])
                    and block["locator"] not in locators, "duplicate/invalid observed locator")
            observed[block["id"]] = block
            locators.add(block["locator"])
            cursor = end
        require(cursor == len(text), "unclassified source text")
        sections = {}
        for section in index["sections"]:
            key = section["id"]
            require(isinstance(key, str) and key in observed and key not in sections,
                    "unknown/duplicate indexed section")
            block = observed[key]
            require(section["locator"] == block["locator"], "stale locator")
            require(section["sha256"] == digest(text[block["start"]:block["end"]]),
                    "section digest mismatch")
            require(section["kind"] in ("normative", "mixed", "metadata", "history"),
                    "unclassified section kind")
            require(isinstance(section["depends"], list), "invalid dependencies")
            if section["depends"]:
                ids(section["depends"])
            sections[key] = section
        require(set(sections) == set(observed), "unindexed source block")

        def closure(seeds):
            done, active = set(), set()

            def visit(key):
                require(key in sections, "unknown dependency/route ID")
                require(key not in active, "cyclic dependency")
                if key in done:
                    return
                active.add(key)
                for dep in sections[key]["depends"]:
                    visit(dep)
                active.remove(key)
                done.add(key)

            for key in seeds:
                visit(key)
            return done

        closure(sections)  # Validate even currently unselected dependencies.
        mandatory = closure(ids(index["mandatory"]))
        for category in ("security", "authorization", "state", "acceptance"):
            protected = ids(index["safeguards"][category])
            require(set(protected) <= mandatory, "safeguard missing from mandatory closure")
            require(all(sections[x]["kind"] in ("normative", "mixed") for x in protected),
                    "safeguard classified as history/metadata")
        require(isinstance(index["routes"], dict) and bool(index["routes"]), "missing routes")
        for route in index["routes"].values():
            closure(ids(route))
        seeds = set(mandatory)
        for scope in ids(scopes):
            require(scope in index["routes"], "ambiguous/unknown task scope")
            seeds.update(index["routes"][scope])
        selected = closure(seeds)
        result.update(valid_candidate=True, review=index["review"],
                      candidate_sections=[key for key in observed if key in selected],
                      reason="offline review only; full source remains required")
    except (KeyError, TypeError, ValueError, RecursionError, UnicodeError) as error:
        result.update(valid_candidate=False, reason=str(error))
    return result


def main(argv):
    if len(argv) < 5:
        print("Usage: check_sot_index.py SNAPSHOT INDEX CURRENT_REVISION SCOPE [SCOPE ...]", file=sys.stderr)
        return 2

    def read(path):
        try:
            with open(path, encoding="utf-8") as source:
                return json.load(source)
        except (OSError, ValueError):
            return None

    result = inspect_candidate(read(argv[1]), read(argv[2]), argv[3], argv[4:])
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result.get("valid_candidate") else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
