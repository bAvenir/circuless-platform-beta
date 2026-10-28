# CIRCULess — platform documentation

Two things live here:

- **the documentation site** — everything under `docs/`, published to
  [bavenir.github.io/circuless-platform-beta](https://bavenir.github.io/circuless-platform-beta/);
- **the architecture and compliance record** — everything at the repository root. Not
  published, and read by people who need the detail: the security requirements, the
  compliance assessment, the audit document, the arc42 chapters and the decision log.

## The one rule

**What is published is exactly what is under `docs/`.**

MkDocs will happily build and serve a page that is missing from the navigation, warning
and carrying on. So the separation is *physical*: whether a document is public is
answered by which directory it is in, not by whether somebody remembered to leave it out
of `mkdocs.yml`. Move a file into `docs/` and you have published it.

## Running it locally

Needs Python 3.12 and either [uv](https://docs.astral.sh/uv/) or pip.

```sh
./scripts/fetch-guides.sh                                    # bring the guides in
uv run --with-requirements requirements-docs.txt mkdocs serve
```

Then <http://localhost:8000>. `mkdocs serve` reloads on save.

With pip instead:

```sh
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements-docs.txt
./scripts/fetch-guides.sh && mkdocs serve
```

### Why there is a fetch step

Fourteen pages are not written here. They are the deployment tutorial, the
troubleshooting table, the integration guide and the rest — and they live in
`circuless-cloud` and `circuless-node`, where they are **tested**: a CI test there
asserts that every path, file, Compose service and console script the tutorial names
actually exists. A copy maintained here would lose that the first time something was
renamed, and nobody would notice.

So `scripts/fetch-guides.sh` copies them in at build time and they are **gitignored**.
If you edit one in `docs/`, your change is gone on the next fetch. Edit it in the
repository it comes from.

It takes two sources, preferring whichever can see your work:

| | |
|---|---|
| a **sibling checkout**, if `../circuless-cloud` or `../circuless-node` exists | the developer's path — it can see commits you have not pushed. Warns if the sibling is dirty, because that build is not reproducible |
| a **pinned clone** from GitHub otherwise | what CI uses. `CIRCULESS_DOCS_SOURCE=remote` forces it |

Pin with `CIRCULESS_CLOUD_REF` and `CIRCULESS_NODE_REF`; both default to `main`.

> **The directory and the repository are not the same name.** The cloud is
> `circuless-cloud` on disk and **`circuless-cloud-beta`** on GitHub. There is a
> separate, older `bAvenir/circuless-cloud` which is a different project — cloning that
> one fetches a repository with no tutorial in it, and the error looks like a renamed
> file.

### `scripts/relink.py`

A guide's links are relative to the repository it came from, so copying it breaks them.
This repoints the ones that moved, and turns links to things that are **not** published —
`deploy/security/`, the NetBird policies — into GitHub URLs, so a reader lands on the
real file rather than a 404.

Fixed here rather than at the source: those documents are read on GitHub too, and a link
rewritten to suit this site would be broken for that reader.

## Adding a page

1. Write it under `docs/`, in the part it belongs to.
2. Add it to `nav:` in `mkdocs.yml`.
3. `mkdocs build` locally before pushing.

`strict: true` is on, so **a broken internal link or a page missing from the navigation
fails the build**. That is deliberate: the commonest defect in a documentation site is a
link to a page that moved, and it is invisible until a reader hits it.

Headings use GitHub's slugger — `## Part 4 · A node` becomes `#part-4--a-node`, two
hyphens, because the `·` disappears and the spaces either side do not. An anchor that
works in the repository works on the site.

Diagrams are [Mermaid](https://mermaid.js.org/) in a fenced block, so they can be
reviewed in a diff rather than re-exported as an image somebody has lost the source for.

## How it publishes

`.github/workflows/docs.yml` builds on every push and keeps the site as an artifact.
On `main` it also deploys to GitHub Pages. The first run creates the Pages site itself.

If the deploy fails on permissions, check **Settings → Pages → Source = GitHub Actions**.

## What is here but not published

| | |
|---|---|
| `security_requirements.md` | The TRL 5 security requirements, mandatory and recommended |
| `compliance-assessment.md` | Every requirement, with a verdict and the evidence |
| `audit-functionality-and-security.md` | What the platform does and what it must satisfy, with how to demonstrate each |
| `CLAUDE.md` | The repository's own conventions, including the stable identifier series |

The arc42 chapters, the decision log (D1–D35 as ADRs) and the working design documents
belong here too and are not all in yet.

## Releasing

Released with the bAvenir release tool (`bvr-ci`). Config is in `.ci-config.yml`.
