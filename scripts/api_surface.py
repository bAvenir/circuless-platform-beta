#!/usr/bin/env python3
"""Render the Cloud API's surface from its committed OpenAPI document.

    python3 scripts/api_surface.py <openapi.json> > docs/integrating-a-service/api-surface.md

Generated rather than written, for the same reason the console's client is generated:
a hand-maintained endpoint list is wrong the week after somebody adds a route, and it
is wrong silently.

The schema is **not served** by the Cloud API — `openapi_url=None`, because an
unauthenticated index of every route is worth a great deal to anyone scanning. So this
reads the copy the repository commits.
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict

VERBS = ("get", "post", "put", "patch", "delete")

#: Paths a partner integrating a service never calls, grouped away rather than dropped —
#: "it is not in the list" and "it is not for you" are different answers.
INTERNAL_PREFIXES = ("/v1/nodes/self",)


def summarise(operation: dict) -> str:
    text = (operation.get("description") or operation.get("summary") or "").strip()
    # The first sentence of the handler's docstring, which is written for a reader.
    first = text.split("\n\n")[0].replace("\n", " ").strip()
    return first if len(first) <= 160 else first[:157].rstrip() + "…"


def main() -> int:
    document = json.loads(open(sys.argv[1]).read())
    paths = document.get("paths", {})

    groups: dict[str, list[tuple[str, str, str]]] = defaultdict(list)
    for path, operations in sorted(paths.items()):
        for verb in VERBS:
            if verb not in operations:
                continue
            section = "Node-only" if path.startswith(INTERNAL_PREFIXES) else path.split("/")[2]
            groups[section].append((verb.upper(), path, summarise(operations[verb])))

    out = [
        "# API surface",
        "",
        "Every route the Cloud API serves, generated from `api/openapi.json` at build",
        "time. If a route is not here, it does not exist.",
        "",
        "Every one of them requires a valid bearer token — there are no anonymous",
        "endpoints, and a CI test asserts it by enumerating the application's own routes.",
        "A token carries **one** audience: ask for `circuless-cloud` to call these.",
        "",
    ]
    # `Node-only` last: it is the least likely thing a reader wants.
    for section in sorted(groups, key=lambda s: (s == "Node-only", s)):
        out += [f"## `/{section}`" if section != "Node-only" else "## Node principals only", ""]
        if section == "Node-only":
            out += [
                "Called by a node with its own credential, never by a person or a",
                "service. The path says `self` rather than a node id, so there is no",
                "parameter to get wrong and no way to express a request on another",
                "node's behalf.",
                "",
            ]
        out += ["| | Path | |", "|---|---|---|"]
        out += [f"| `{v}` | `{p}` | {d} |" for v, p, d in groups[section]]
        out += [""]

    out += [
        "---",
        "",
        f"Generated from a document describing {len(paths)} paths. The node's own API is",
        "separate and is documented in the integration guide.",
        "",
    ]
    print("\n".join(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
