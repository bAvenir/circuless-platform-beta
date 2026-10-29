#!/usr/bin/env python3
"""Render the platform's API surface from the two committed OpenAPI documents.

    python3 scripts/api_surface.py <cloud openapi.json> <node openapi.json>

Generated rather than written, for the same reason the console's client is generated: a
hand-maintained endpoint list is wrong the week after somebody adds a route, and it is
wrong silently.

Neither API serves its own schema — both set `openapi_url=None`, because an
unauthenticated index of every route is worth a great deal to anyone scanning. So each
repository commits the document its application produces, and this reads both.

## Grouped by task, not by path

A reader arrives wanting to do something, not wanting an inventory. The two APIs also
sit at different layers — you find and agree in the Cloud, and read and invoke at a
node — so grouping by path would scatter one task across two sections.

**Every path must match a rule.** A path that matches none fails the build rather than
being dropped, because a quietly missing endpoint is the failure this file exists to
prevent.
"""

from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from typing import Any, NamedTuple

VERBS = ("get", "post", "put", "patch", "delete", "head", "options")


class Group(NamedTuple):
    title: str
    blurb: str
    #: (api, regex). `api` is "cloud" or "node".
    rules: tuple[tuple[str, str], ...]


GROUPS: tuple[Group, ...] = (
    Group(
        "Who am I",
        "Both APIs will tell you what they make of your token — the organisations it "
        "carries, whether you administer them, and what kind of principal you are. The "
        "first call to make when something is refused and you do not know why.",
        (("cloud", r"^/v1/whoami$"), ("node", r"^/v1/whoami$")),
    ),
    Group(
        "Find data and services",
        "The catalogue holds descriptions of everything published, from every node. "
        "Filtered by what each record's owner made discoverable; seeing a record is not "
        "permission to read it.",
        (("cloud", r"^/v1/catalogue$"),),
    ),
    Group(
        "Agree access",
        "A consumer requests, or a provider offers; the other side accepts or the "
        "provider approves. Both ends of the same lifecycle, which is why the "
        "collection has no `POST` — neither way in is the default.",
        (("cloud", r"^/v1/agreements"),),
    ),
    Group(
        "Read data and call services",
        "At the node that holds them, never through the Cloud. Every one of these is "
        "decided by that node at the moment of the request, against the agreements it "
        "has, and recorded.",
        (
            ("node", r"/resources/\{resource_id\}/data"),
            ("node", r"/resources/\{resource_id\}/invoke/"),
        ),
    ),
    Group(
        "Manage your organisation's resources",
        "On your own node, for your own tenant. Registering, uploading, withdrawing, "
        "and setting the credential the node uses to reach your upstream service — "
        "which no API ever returns.",
        (
            ("node", r"^/v1/tenants$"),
            ("node", r"^/v1/t/\{tenant_slug\}/resources$"),
            ("node", r"^/v1/t/\{tenant_slug\}/resources/\{resource_id\}$"),
            ("node", r"/resources/\{resource_id\}/credential$"),
        ),
    ),
    Group(
        "See what happened",
        "Two logs, in two places, answering different questions. The Cloud's audit "
        "trail records changes to agreements, organisations and the node registry. A "
        "node's access log records every decision about its own resources, allowed and "
        "refused. Both are append-only — no code path updates or deletes either.",
        (("cloud", r"^/v1/audit$"), ("node", r"/access-log$")),
    ),
    Group(
        "Operate the platform",
        "The organisation and node registries. Platform operator only.",
        (("cloud", r"^/v1/orgs"), ("cloud", r"^/v1/nodes$"), ("cloud", r"^/v1/nodes/\{")),
    ),
    Group(
        "Node principals only",
        "Called by a node with its own credential, never by a person or a service. The "
        "path says `self` rather than a node id, so there is no parameter to get wrong "
        "and no way to express a request on another node's behalf.",
        (("cloud", r"^/v1/nodes/self"), ("node", r"^/\.well-known/")),
    ),
)


def summarise(operation: dict[str, Any]) -> str:
    text = (operation.get("description") or operation.get("summary") or "").strip()
    first = text.split("\n\n")[0].replace("\n", " ").strip()
    return first if len(first) <= 160 else first[:157].rstrip() + "…"


def collect(documents: dict[str, dict]) -> tuple[dict[str, list], list[str]]:
    """Rows per group, and anything that matched no rule."""
    rows: dict[str, list[tuple[str, str, str, str]]] = defaultdict(list)
    unmatched: list[str] = []

    for api, document in documents.items():
        for path, operations in sorted(document.get("paths", {}).items()):
            group = next(
                (
                    g.title
                    for g in GROUPS
                    for rule_api, pattern in g.rules
                    if rule_api == api and re.search(pattern, path)
                ),
                None,
            )
            if group is None:
                unmatched.append(f"{api} {path}")
                continue
            for verb in VERBS:
                if verb in operations:
                    rows[group].append(
                        (verb.upper(), path, api, summarise(operations[verb]))
                    )
    return rows, unmatched


def main() -> int:
    documents = {
        "cloud": json.loads(open(sys.argv[1]).read()),
        "node": json.loads(open(sys.argv[2]).read()),
    }
    rows, unmatched = collect(documents)

    if unmatched:
        print(
            "::error::these paths match no group in api_surface.py, so the page would "
            f"silently omit them: {unmatched}",
            file=sys.stderr,
        )
        return 1

    counts = {api: len(d.get("paths", {})) for api, d in documents.items()}
    out = [
        "# API surface",
        "",
        "Every route the two APIs serve, generated from the OpenAPI documents each",
        "repository commits. If a route is not here, it does not exist.",
        "",
        "**Everything requires a token.** There are no anonymous endpoints, and a test in",
        "each repository asserts it by enumerating the application's own routes. A token",
        "carries **one** audience: `circuless-cloud` for the Cloud, `node:<node_id>` for a",
        "node. A token two systems accept is replayable between them, so the platform",
        "refuses one that names more than one.",
        "",
        "| | |",
        "|---|---|",
        "| **Cloud** | The catalogue, agreements, the registries, the audit trail. Holds no data |",
        "| **Node** | Holds the data and decides every request for it |",
        "",
    ]

    for group in GROUPS:
        if not rows[group.title]:
            continue
        out += [f"## {group.title}", "", group.blurb, "", "| | | Path | |", "|---|---|---|---|"]
        out += [
            f"| `{api}` | `{verb}` | `{path}` | {text} |"
            for verb, path, api, text in rows[group.title]
        ]
        out += [""]

    out += [
        "## Not here, and not reachable",
        "",
        "A node runs a **second application** on a separate socket, bound to loopback or",
        "the overlay. It carries `/internal/authz`, `/metrics` and `/healthz`, and it is",
        "never routed by the gateway — the gateway's rule matches `PathPrefix(/v1)` and",
        "nothing else, so the restriction is structural rather than a list somebody",
        "maintains.",
        "",
        "Those paths are deliberately absent from the node's published document. Trying",
        "them through the gateway gets a 404 from the edge, not from the node.",
        "",
        "---",
        "",
        f"Generated from {counts['cloud']} Cloud paths and {counts['node']} node paths.",
        "",
    ]
    print("\n".join(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
