#!/usr/bin/env bash
# Bring the guides in from the code repositories, at a pinned ref.
#
# **Why not submodules.** Both code repositories already describe *this* repository as
# their submodule at `docs/architecture/`. Taking them as submodules here as well would
# be a cycle. A shallow clone at a pinned ref gives the same reproducibility with none
# of that, and keeps `git status` in this repository about this repository.
#
# **Why copy rather than rewrite.** Every file below is tested where it lives:
# `test_tutorial.py` asserts that every path, file, Compose service and console script
# the tutorial names actually exists. A copy inherits that guarantee only as long as it
# stays a copy — so nothing here edits content, and the fetched files are gitignored so
# that nobody is tempted to.
set -euo pipefail

CLOUD_REF="${CIRCULESS_CLOUD_REF:-main}"
NODE_REF="${CIRCULESS_NODE_REF:-main}"
ORG="${CIRCULESS_GITHUB_ORG:-https://github.com/bAvenir}"

# **The directory and the repository are not the same name.** The cloud is checked out
# locally as `circuless-cloud` and lives on GitHub as `circuless-cloud-beta`; there is a
# separate, older `bAvenir/circuless-cloud` that is a different project entirely. Cloning
# by the directory name fetches the wrong repository and the mistake looks like a renamed
# file. Keyed here so it is stated once.
#   <local directory> <remote repository>
CLOUD_DIR=circuless-cloud;  CLOUD_REPO=circuless-cloud-beta
NODE_DIR=circuless-node;    NODE_REPO=circuless-node

here="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT

# Two sources, in order of preference — the same shape as the console's
# `fetch-schema.mjs`, and for the same reason:
#
#   1. a pinned clone from GitHub. This is what CI uses and what makes a published
#      site reproducible;
#   2. a sibling checkout, when one is present. This is the developer's path, and the
#      only one that can see work that is not pushed yet.
#
# Set CIRCULESS_DOCS_SOURCE=remote to force the first even with siblings present.
SOURCE="${CIRCULESS_DOCS_SOURCE:-auto}"

fetch() {  # fetch <directory> <repository> <ref>
  local sibling="$here/../$1"
  if [ "$SOURCE" != "remote" ] && [ -d "$sibling/.git" ]; then
    echo "▶ $1 — sibling checkout at $sibling"
    echo "  $(git -C "$sibling" log -1 --format='%h %s')"
    local dirty
    dirty="$(git -C "$sibling" status --porcelain | wc -l | tr -d ' ')"
    [ "$dirty" != "0" ] && echo "  note: $dirty uncommitted change(s) — this build is not reproducible"
    cp -R "$sibling" "$work/$1"
    return
  fi
  echo "▶ $2 @ $3  → $1"
  git clone --quiet --depth 1 --branch "$3" "$ORG/$2.git" "$work/$1"
  git -C "$work/$1" log -1 --format='  %h %s'
}

fetch "$CLOUD_DIR" "$CLOUD_REPO" "$CLOUD_REF"
fetch "$NODE_DIR"  "$NODE_REPO"  "$NODE_REF"

# Clear anything a previous run left behind. Without this, a fetch that fails halfway
# leaves the last run's files in place and `mkdocs build` succeeds against them — a
# green build of a stale site, which is the worst of the available outcomes.
git -C "$here" clean -fXq docs/ 2>/dev/null || true

# <source> <destination under docs/>
repo_of() { case "$1" in "$CLOUD_DIR") echo "$CLOUD_REPO";; *) echo "$NODE_REPO";; esac; }

place() {
  local src="$work/$1" dst="$here/docs/$2"
  local dir="${1%%/*}"
  [ -f "$src" ] || { echo "::error::$1 is not in that ref — has it been renamed?" >&2; exit 1; }
  mkdir -p "$(dirname "$dst")"
  {
    echo "<!-- Fetched by scripts/fetch-guides.sh. Do not edit here."
    echo "     Source: $(repo_of "$dir")/${1#*/} -->"
    echo
    cat "$src"
  } > "$dst"
}

place circuless-cloud/deploy/TUTORIAL.md              guides/deploying.md
place circuless-cloud/deploy/DEPLOYMENT.md            guides/deployment-reference.md
place circuless-cloud/deploy/TROUBLESHOOTING.md       guides/when-it-goes-wrong.md
place circuless-cloud/deploy/BACKUP-AND-RESTORE.md    guides/backups.md
place circuless-cloud/docs/identities-by-hand.md      guides/identities.md
place circuless-node/examples/manual-demo.md          guides/consuming-data.md
place circuless-node/deploy/README.md                 guides/running-a-node.md
place circuless-node/INTEGRATING-A-SERVICE.md         integrating-a-service/the-guide.md
place circuless-node/examples/acting-for-a-user/README.md integrating-a-service/acting-for-a-user.md
place circuless-node/examples/browser-app/README.md   guides/browser-applications.md
place circuless-node/examples/reference-service/README.md integrating-a-service/reference-service.md

# Links between these documents are relative to where they live, not to where they
# land. Rewriting them here keeps the sources untouched — editing them in their own
# repositories to suit this site would make them wrong for anyone reading on GitHub.
python3 "$here/scripts/relink.py" "$here/docs"

# The API surface, generated from the schema the Cloud API commits.
python3 "$here/scripts/api_surface.py" \
  "$work/circuless-cloud/api/openapi.json" \
  > "$here/docs/integrating-a-service/api-surface.md"

echo "✓ guides in place"
