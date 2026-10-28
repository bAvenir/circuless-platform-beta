# CIRCULess architecture

The authoritative architecture of the **CIRCULess core platform** — the CIRCULess Cloud and the CIRCULess Nodes — and the documentation site built from part of it.

Both code repositories' `CLAUDE.md` describe this repository as a submodule at `docs/architecture/`. **It is not, and that is deliberate** (28 Oct 2026): the documentation site pulls *from* the code repositories at build time, and a submodule in the other direction as well would be a cycle. Those two sentences need correcting where they appear.

Owner: J (Bavenir, architect / technical lead). Changes to decisions and requirements need J's approval. Documentation changes do not.

## Layout

**What is published is exactly what is under `docs/`.** MkDocs serves a page that is
missing from the navigation with only a warning, so the separation is physical: whether
a document is public is answered by which directory it is in. Moving a file into `docs/`
publishes it. `README.md` has the build, the fetch step and the local commands.

### Published — `docs/`

| Path | What | Status |
|---|---|---|
| `docs/index.md` | The landing page: four routes for four readers | Present |
| `docs/understanding/` | Non-technical. What it is, the pieces, how data is shared, who runs what, what it does not do | **Five stubs to write** |
| `docs/understanding/glossary.md` | **Partner-facing** terms. Was `12_glossary.md` | v1.0 |
| `docs/understanding/security-measures.md` | **Partner-facing**, technical audience. Was `security_measures.md` | v1.0, **and still says APISIX** — the edge has been Traefik since D32/D33 |
| `docs/guides/`, `docs/integrating-a-service/` | Fetched from the code repositories at build time, and **gitignored**. Editing them here is discarded on the next fetch | Generated |
| `docs/integrating-a-service/integration-requirements.md` | The contract a service must meet. Was planned as `service_integration_requirements.md` | **To write** |
| `docs/integrating-a-service/api-surface.md` | Generated from the Cloud's `openapi.json` | Generated |

### Not published — repository root

| Path | What | Status |
|---|---|---|
| `security_requirements.md` | T2.7 security requirements, the cleaned TRL 5 set | Present |
| `compliance-assessment.md` | Every requirement, a verdict and the evidence | Present |
| `audit-functionality-and-security.md` | What the platform does and must satisfy, with how to demonstrate each | Present |
| `01_scope_and_context.md` … `11_risks_and_limitations.md` | arc42 chapters | **Absent from this repository** |
| `09_decisions/` | ADRs in MADR format, one per decision, `ADR-0NN` ↔ `DNN` | **Absent.** To write, from the decision log |
| `WP1_requirements.md` | Verbatim baseline from D1.1 §3 | **Absent.** **Never edit** once here |
| `D2.1_requirements.md` | **The authoritative beta requirement set** | **Absent** |
| `security_requirements_review.md` | Conflicts, decisions, coverage, validation plan | **Absent** — and cited by `circuless-cloud/deploy/security/real-data-transition-checklist.md` |
| `working/` | Design draft (D1–D35, findings R/G/S), build breakdown, implementation plan | **Absent.** Currently in the parent directory, outside any repository |

> Everything marked absent was described here as existing at a version. It is not in the
> repository, which was initialised fresh on 27 Oct. Until those files are in, a
> reference to one of them is a reference to nothing.

## Rules for this repo

- **Naming.**
  - *CIRCULess core platform* = Cloud + Nodes. This is the subject of this architecture.
  - *CIRCULess waste management platform* = the core plus the services (the "DWMP" of D1.1).
  - Services — Workflows, KB, DPP, LTU quality prediction, NTNU optimiser, BIM visualisation — are **outside** the architecture. They are documented only through integration requirements.
- **Identifiers are stable. Never renumber.** New items take the next free number.

  | Series | What |
  |---|---|
  | D1–D35 | Decisions |
  | R, G, S | Review findings |
  | C, N, X, H, Q | Components |
  | T01–T35 | Test cases (T31 deferred) |
  | F1–F20 | Flows |
  | O-numbers | Open questions |
  | FR/NFR | Requirements |
  | `SR-` | Security requirements |
- **Every file has a version and a status on its first lines.** Bump the version when the content changes. `README.md` is the repository's own guide, not an index of files — the table above is the index.
- **Diagrams as code:** Mermaid, inline. No binary diagrams; the old SVG/PNG in the parent project is stale.
- **The site build fails on a broken link.** `strict: true`, so a dead internal link or a page missing from `nav` stops the build rather than shipping. Run `mkdocs build` before pushing.
- **Never edit a fetched guide in `docs/`.** They come from `circuless-cloud` and `circuless-node`, where they are tested — a CI test there asserts every path, file and service the deployment tutorial names exists. A copy edited here is discarded on the next fetch and loses that guarantee.
- **The directory and the repository are not the same name.** The cloud is `circuless-cloud` on disk and **`circuless-cloud-beta`** on GitHub; `bAvenir/circuless-cloud` is a different, older project.
- **Normative language** in requirements follows RFC 2119: *must*, *should*, *may*.
- **Fixed wordings — quote them exactly:**
  - the in-transit statement: *"Every hop is encrypted: TLS with certificates from a public CA on every publicly reachable endpoint, and WireGuard on the overlay."*;
  - the offline statement in the design draft §3.7.
- **Claim only what is decided.**
  - "Proposed" decisions (D11, D13, D16–D18, D32, D33 at present) are not described as fact in partner-facing files until J agrees them.
  - The DSP claim is *"dataspace-aligned, with a documented DSP mapping"* — never "DSP compliant".
  - M5 is *functional acceptance*. TRL 5 relevant-environment evidence comes only from the partner integration phase (D35).
- **Partner-facing files** — now everything under `docs/`, and in particular the glossary, the security measures and the integration requirements — use plain definitions. Internal names (`decide()`, table names, group paths) appear only where a partner's developer needs them.
- **Style.** Short sentences. Tables for comparisons. Each section says what was decided and why, and nothing else. No marketing language.

## Key facts to keep consistent across files

| Topic | Current fact |
|---|---|
| Hosting | Docker Compose on Hetzner (EU); fresh PostgreSQL; no Kubernetes (D19) |
| Overlay | Isolated CIRCULess network on BVR's NetBird (D34) |
| Identity | Dedicated Keycloak ≥ 26.2; realm `circuless`; orgs as `/orgs/<x>` groups |
| Tokens | 5 minutes; one node audience per token; no name or email in node tokens |
| Anonymous access | None, catalogue included (D21). **One declared exemption**: the node's `/ui` static files, which carry no tenant data and a four-key `config.json`. Say so rather than claiming none |
| MFA | The **decision** is mandatory for platform operators (D23). It is **not enforced yet** — deferred to 4 Nov, in `circuless-cloud/SECURITY-DEFERRALS.md` and in the realm's own `deferred` block. Partner-facing pages must not state it as in place |
| Encryption at rest | Not at TRL 5. BVR stores only non-sensitive partner data; a classification guard enforces it (D22) |
| Service isolation | Private container networks (D20) |
| Plan | M1 Fri 2 Oct · M2 Fri 9 Oct · M3 Fri 16 Oct · M4 Thu 22 Oct · M5 Fri 23 Oct — all past. **Security validation Fri 6 Nov**, which is what the deferrals are due against · then partner integration |
| Effort | 51 d, of which 50 d in October (about 2.5 FTE) |

## Writing backlog, in order

1. The five stubs in `docs/understanding/` — the only part of the site with nothing
   behind it, and the reason a new reader has no front door.
2. `docs/integrating-a-service/integration-requirements.md` — needed before partners are
   contacted. Distinct from the integration *guide*, which teaches: these are the
   obligations a partner is signed off against.
3. Correct the APISIX references in `docs/understanding/security-measures.md`. It is the
   page a partner reads to decide whether to trust the platform, and it currently
   describes an edge that is not deployed.
4. Bring the absent documents in — `working/` first, since the ADRs and arc42 chapters
   are derived from it, and `security_requirements_review.md`, which is already cited
   from the cloud repository.
5. `09_decisions/` — ADRs from D1–D35. Mechanical work; it keeps the IDs.
6. `05_building_blocks.md`, `07_deployment.md`, `06_runtime.md` — from the design draft
   and build breakdown, with Mermaid diagrams.
7. `03_constraints.md`, `04_solution_strategy.md`, `08_crosscutting_concepts.md`,
   `11_risks_and_limitations.md`.
8. `10_security.md` — STRIDE threat model per trust boundary.
9. `02` §10 quality scenarios.
