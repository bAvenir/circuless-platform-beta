#!/usr/bin/env python3
"""Repoint the links in fetched guides, now that those guides live somewhere else.

    python3 scripts/relink.py docs/

A guide's links are relative to the repository it comes from. Copied onto this site,
some of them land on a page that is here under a different name, and some point at
something that is deliberately **not** published — `deploy/security/`, the NetBird
policies, an examples directory.

Both are fixed here rather than at the source. The sources are read on GitHub as well,
and a link rewritten to suit this site would be broken for that reader. The site is the
copy, so the site adapts.

Which repository a page came from is read from the provenance header
`scripts/fetch-guides.sh` writes, so there is one mapping rather than two that can
disagree.
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import PurePosixPath
from pathlib import Path

ORG = os.environ.get("CIRCULESS_GITHUB_ORG_WEB", "https://github.com/bAvenir")
#: Keyed by the **repository** name, which is not the directory name: the cloud is
#: `circuless-cloud` on disk and `circuless-cloud-beta` on GitHub.
REFS = {
    "circuless-cloud-beta": os.environ.get("CIRCULESS_CLOUD_REF", "main"),
    "circuless-node": os.environ.get("CIRCULESS_NODE_REF", "main"),
}

#: Source basename → the page it became, as a path under `docs/`.
MOVED = {
    "TUTORIAL.md": "guides/deploying.md",
    "DEPLOYMENT.md": "guides/deployment-reference.md",
    "TROUBLESHOOTING.md": "guides/when-it-goes-wrong.md",
    "BACKUP-AND-RESTORE.md": "guides/backups.md",
    "identities-by-hand.md": "guides/identities.md",
    "manual-demo.md": "guides/consuming-data.md",
    "INTEGRATING-A-SERVICE.md": "integrating-a-service/the-guide.md",
}

LINK = re.compile(r"\]\(([^)\s]+)(\s+\"[^\"]*\")?\)")
SOURCE = re.compile(r"Source: (\S+?)/(\S+) -->")


def main() -> int:
    root = Path(sys.argv[1])
    changed = 0

    for page in sorted(root.rglob("*.md")):
        text = page.read_text()
        provenance = SOURCE.search(text)
        if not provenance:
            continue  # written here, not fetched; its links are already right
        repo, source_path = provenance.group(1), provenance.group(2)
        source_dir = PurePosixPath(source_path).parent
        depth = len(page.relative_to(root).parts) - 1

        def repoint(match: re.Match[str]) -> str:
            target, title = match.group(1), match.group(2) or ""
            if target.startswith(("http://", "https://", "#", "mailto:")):
                return match.group(0)

            path, _, anchor = target.partition("#")
            anchor = f"#{anchor}" if anchor else ""

            moved = MOVED.get(path.rsplit("/", 1)[-1])
            if moved:
                return f"]({'../' * depth}{moved}{anchor}{title})"

            # Not published. Send the reader to the file in its own repository, which
            # is where it actually is, rather than to a 404 here.
            resolved = PurePosixPath(os.path.normpath(source_dir / path))
            return f"]({ORG}/{repo}/blob/{REFS.get(repo, 'main')}/{resolved}{anchor}{title})"

        rewritten = LINK.sub(repoint, text)
        if rewritten != text:
            page.write_text(rewritten)
            changed += 1

    print(f"  relinked {changed} page(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
