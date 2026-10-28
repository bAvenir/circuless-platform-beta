# CIRCULess architecture

The authoritative architecture of the **CIRCULess core platform** — the CIRCULess Cloud and the CIRCULess Nodes. The two code repositories include this repo as a submodule at `docs/architecture/`.

Owner: J (Bavenir, architect / technical lead). Changes to decisions and requirements need J's approval. Documentation changes do not.

## Layout

| Path | What | Status |
|---|---|---|
| `README.md` | Index of every file, with version and status | Keep current |
| `01_scope_and_context.md` … `11_risks_and_limitations.md` | arc42 chapters. 01 and 02 exist; 03–11 are to write | See README |
| `09_decisions/` | ADRs in MADR format, one per decision, `ADR-0NN` ↔ `DNN` | To write, from the decision log |
| `12_glossary.md` | **Partner-facing** terms | v1.0 |
| `WP1_requirements.md` | Verbatim baseline from D1.1 §3 | **Never edit** |
| `02_requirements_and_quality.md` | Assessment of every WP1 requirement, with the decisions | v1.0 |
| `D2.1_requirements.md` | **The authoritative beta requirement set** | v1.0 |
| `security_requirements.txt` / `.md` | T2.7 security requirements: source, and the cleaned TRL 5 set | Baseline |
| `security_requirements_review.md` | Conflicts, decisions, coverage, validation plan | v0.4 |
| `security_measures.md` | **Partner-facing**, technical audience | v1.0 |
| `service_integration_requirements.md` | The contract a service must meet to integrate | To write |
| `working/` | The working documents: design draft (decisions D1–D35, review findings R/G/S), build breakdown, implementation plan | Decision history. Superseded chapter by chapter as 03–11 and the ADRs are written |

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
- **Every file has a version and a status on its first lines.** Bump the version when the content changes, and update `README.md`.
- **Diagrams as code:** Mermaid, inline. No binary diagrams; the old SVG/PNG in the parent project is stale.
- **Normative language** in requirements follows RFC 2119: *must*, *should*, *may*.
- **Fixed wordings — quote them exactly:**
  - the in-transit statement: *"Every hop is encrypted: TLS with certificates from a public CA on every publicly reachable endpoint, and WireGuard on the overlay."*;
  - the offline statement in the design draft §3.7.
- **Claim only what is decided.**
  - "Proposed" decisions (D11, D13, D16–D18, D32, D33 at present) are not described as fact in partner-facing files until J agrees them.
  - The DSP claim is *"dataspace-aligned, with a documented DSP mapping"* — never "DSP compliant".
  - M5 is *functional acceptance*. TRL 5 relevant-environment evidence comes only from the partner integration phase (D35).
- **Partner-facing files** (`12_glossary.md`, `security_measures.md`, and later `service_integration_requirements.md`) use plain definitions. Internal names (`decide()`, table names, group paths) appear only where a partner's developer needs them.
- **Style.** Short sentences. Tables for comparisons. Each section says what was decided and why, and nothing else. No marketing language.

## Key facts to keep consistent across files

| Topic | Current fact |
|---|---|
| Hosting | Docker Compose on Hetzner (EU); fresh PostgreSQL; no Kubernetes (D19) |
| Overlay | Isolated CIRCULess network on BVR's NetBird (D34) |
| Identity | Dedicated Keycloak ≥ 26.2; realm `circuless`; orgs as `/orgs/<x>` groups |
| Tokens | 5 minutes; one node audience per token; no name or email in node tokens |
| Anonymous access | None, catalogue included (D21) |
| MFA | Mandatory for platform operators only (D23) |
| Encryption at rest | Not at TRL 5. BVR stores only non-sensitive partner data; a classification guard enforces it (D22) |
| Service isolation | Private container networks (D20) |
| Plan | M1 Fri 2 Oct · M2 Fri 9 Oct · M3 Fri 16 Oct · M4 Thu 22 Oct · M5 Fri 23 Oct · validation report Fri 6 Nov · then partner integration |
| Effort | 51 d, of which 50 d in October (about 2.5 FTE) |

## Writing backlog, in order

1. `service_integration_requirements.md` — needed before partners are contacted (suggested: after M3, 16 Oct).
2. Partner IT prerequisites, one page — for the partner integration phase.
3. `09_decisions/` — ADRs from D1–D35. Mechanical work; it keeps the IDs.
4. `05_building_blocks.md`, `07_deployment.md`, `06_runtime.md` — derived from the design draft and build breakdown, with Mermaid diagrams.
5. `03_constraints.md`, `04_solution_strategy.md`, `08_crosscutting_concepts.md`, `11_risks_and_limitations.md`.
6. `10_security.md` — STRIDE threat model per trust boundary.
7. `02` §10 quality scenarios.
