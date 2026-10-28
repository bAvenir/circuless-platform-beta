# Compliance against the TRL 5 security requirements

**Assessed:** 26 October 2026, against `security_requirements.md` (58 requirements in TRL 5
scope: 43 mandatory, 15 recommended).
**Scope:** `circuless-cloud`, `circuless-node`, `circuless-management-ui-beta`, at the
commits on `main` on that date.

**Updated the same day.** Four of the gaps this review found were written up within
hours of it — the rows concerned are marked *pending sign-off* and name the document.
They are drafts on `feature/security-audit-prep`, not yet merged and not yet signed, so
they are **not** counted as met in the summary below. That count is the position as
found.

| | Mandatory | Recommended | Total |
|---|---|---|---|
| **Met** | 28 | 8 | **36** |
| **Partial** — the control exists but does not cover everything the requirement asks | 5 | 4 | **9** |
| **Not met** | 10 | 3 | **13** |

The ten unmet mandatory requirements divide three ways, and the division matters more
than the number:

- **four are in the project's own deferral register**, with reasoning and a due date of
  4 November (SR-4.1.1, SR-4.1.3, SR-4.3.5, SR-6.1.4);
- **one is a recorded deviation** that time will not fix (SR-1.1.7);
- **five were not recorded anywhere** (SR-2.4.1, SR-3.3.2, SR-4.4.5, SR-7.1.1, SR-7.1.5).
  Those five were the real finding of this review. **Four have since been written**
  (26 Oct) and await sign-off; **SR-3.3.2 was closed as out of scope** the same day —
  other consortium partners integrate BIM, so its evidence comes from them.

## How this was assessed, and what it cannot tell you

Evidence is the repositories: configuration, code, tests and the deployment documents.
That is the right source for config-as-code, and it has one blind spot worth stating
plainly.

**The running deployment was not inspected.** Docker was not running on this machine, so
the test Keycloak that normally allows claims to be checked end to end was unavailable,
and the deployed host is not reachable from here. Where a requirement is satisfied by a
*setting in git* this review can confirm it; where it depends on a command having been
run on a server — `unattended-upgrades`, the Hetzner firewall, the SSH configuration —
this review confirms only that the procedure is written down. Those rows are marked
**partial — procedure documented, application unverified** rather than met.

**Two things were tested live** because a documented claim was load-bearing and cheap to
check: Trivy's handling of the expiry on a suppressed finding (§3.1), and whether the
`platform-admin` realm role survives the console's token narrowing (it does).

---

## 1. What needs attention, in order

### 1.1 Five mandatory requirements were not met and not recorded

The project keeps a careful deferral register — `circuless-cloud/SECURITY-DEFERRALS.md`
and a `deferred` block inside `realm-config.json`, both printed by CI. It is unusually
good. These five were outside it, which meant nobody had accepted them in writing and
the 4 November validation had no entry to close.

> **Four were written on 26 October**, after this review and in response to it:
> `real-data-transition-checklist.md`, `data-classification-policy.md`,
> `incident-response.md` and `data-subject-rights.md`, all in
> `circuless-cloud/deploy/security/`. They are drafts awaiting sign-off. The
> descriptions below are the state this review found, kept as written because that is
> what the review is a record of.

| ID | Requirement | State |
|---|---|---|
| **SR-7.1.1** | Formal data classification policy | The **mechanism** exists and is enforced — every dataset carries `classification ∈ {synthetic, non-sensitive, sensitive}` and a BVR-operated node refuses `sensitive` (D22, node invariant 13). The **one-page policy** the requirement asks for, stating which controls trigger when real data arrives, does not exist |
| **SR-7.1.5** | Transition checklist before real personal data | Nothing. This is the gate that makes §9's deferral of encryption at rest safe — the deferral says these controls "become mandatory again as soon as" real data arrives, and no document lists what must then be done |
| **SR-4.4.5** | Documented incident contact list and response procedure | Nothing. One page: who to call, how to take the host offline, how to notify partners |
| **SR-2.4.1** | GDPR access, rectification, erasure, portability | Nothing. See below — this one needs a decision before it needs an implementation |
| **SR-3.3.2** | BIM integration tested with realistic synthetic data | **Out of scope for the core platform — decided (J, 26 Oct 2026).** *BIM visualisation* is one of the **services**, which `circuless-architecture/CLAUDE.md` places outside the architecture, and the integration is done by **other consortium partners**, not by BVR. The requirement remains mandatory for the project and its evidence comes from those partners. Listed here only so it is not assumed covered by the platform |

**SR-7.1.5 is the one I would do first.** It costs an hour, and it is what an auditor
will ask for the moment they read §9. The deferral of encryption at rest is reasonable
and well argued; it is only safe if the trigger is written down somewhere other than the
paragraph that deferred it.

**SR-2.4.1 needs a decision, not code.** The platform does hold personal data: Keycloak
user accounts carry name and email, required by the realm's User Profile. Everything
*else* is deliberately pseudonymous — tokens, the audit log and the node's access log
carry a subject identifier and nothing else (D31), which is a genuinely strong position
and worth stating as such. So the realistic answer is probably "rights are exercised
against Keycloak by the platform operator, and here is the procedure", not an API. But
that is a paragraph somebody has to write and sign.

### 1.2 Four mandatory requirements are deferred with reasoning

Already recorded, due 4 November, no action needed beyond closing them on time.

| ID | Requirement | Register entry |
|---|---|---|
| SR-4.3.5 | Protected main branch, required PR reviews | "There is one developer. A required review would block every merge, and self-approval through a second account is theatre" |
| SR-6.1.4 | Build pipeline integrity: signed commits | "No signing key is configured and the whole history is unsigned" — the register also writes out exactly how to close it |
| SR-4.1.1 | Firewall: only necessary ports (22 via VPN only) | Port 22 reachable from the internet; waits on the overlay (C12). SSH itself already refuses passwords |
| SR-4.1.3 | VPN or allowlist for administrative access | Keycloak's admin console is on the public internet behind a login form |

SR-4.1.3 is the one to prioritise among these. The register says it itself: *"an admin
console on the public internet is the first thing an auditor looks for."*

### 1.3 One mandatory requirement cannot be met in the current topology

> **Unblocked 26 Oct 2026.** The precondition — that nothing authenticating to that
> Keycloak presents a client certificate at the TLS layer — has been settled by J:
> nothing does. The route can terminate at Traefik, which makes both this and SR-4.1.3
> ordinary work. Procedure: `circuless-cloud/deploy/security/keycloak-tls-termination.md`.
> Not yet performed, so the verdict below stands until it is.


**SR-1.1.7 — rate limiting on the login endpoint.** Recorded as a deviation rather than
a deferral, correctly, because time will not fix it. Keycloak sits behind a Traefik TCP
router with `tls.passthrough=true`, so Traefik never sees HTTP and `rateLimit` is an HTTP
middleware. The analysis in the register is sound, the compensating control (brute-force
lockout, five attempts, temporary) is real and verified, and three remedies are written
out with the preferred one's configuration already drafted.

What remains genuinely uncovered is volumetric abuse of the token endpoint spread across
many accounts. **The Cloud API itself is rate-limited** (60/min, burst 120) — the
deviation is narrower than it first appears and the register says so.

---

## 2. Where the platform is notably strong

Worth recording, because an audit report that lists only gaps misrepresents the posture.

- **SR-1.2.3 / SR-3.2.1, no anonymous endpoints.** Enforced by a test that enumerates
  everything the application serves — routes *and* mounted static trees — and asserts
  401 without a token, so new routes are covered automatically rather than by review.
  The node's single exemption, `/ui`, is declared in `ANONYMOUS_PREFIXES`, asserted
  there, and constrained: a `config.json` of four keys, with a fifth failing both a test
  and the node's own startup check.
- **SR-1.2.2, least privilege.** The authorization decision is one pure function with an
  exhaustive table test, and a node principal is refused on every endpoint it has no
  business calling. Identity comes from the token and never from the request body.
- **SR-3.2.3, input validation.** Pydantic throughout, plus path confinement on the
  node's data and invoke routes.
- **SR-4.3.1 / SR-4.3.2, secrets.** Beyond the gate: when four secret files *were*
  committed, the incident was found, resolved, and — most of the point — the detection
  gap was analysed and closed with a rule keyed on **location rather than shape**, since
  a bare base64 blob matches no secret pattern. The commit is allowlisted by SHA so a
  secret committed tomorrow still fails. That is better practice than the requirement
  asks for.
- **SR-6.1.1 / SR-4.3.6, pinning.** Lockfiles committed, images pinned by digest, and
  `cosign verify` before deployment.

---

## 3. Two findings about the controls themselves

These are not requirement rows. They are ways the compliance machinery reports better
than it performs, which matters more to an audit than any single gap.

### 3.1 A time-boxed security exception never expires

> **Decided (J, 26 Oct 2026): no automated check will be built.** Deferral dates are
> tracked by the technical lead outside the repository. The finding below stands as a
> description of what the files do and do not enforce — a date written in
> `.trivyignore.yaml`, `SECURITY-DEFERRALS.md` or `realm-config.json` is a note to a
> person, not a control.


`circuless-cloud/.trivyignore.yaml` suppresses `AVD-DS-0002` (no `USER` directive) on the
Postgres Dockerfile, carrying `expiredAt: 2026-10-23` so that the exception would lapse
and the finding reappear. **It does not.** Tested on 26 October against Trivy 0.74:

| | Result |
|---|---|
| Scan with no ignore file | finding **reported** |
| Committed ignore file, `expiredAt: 2026-10-23` (3 days past) | **suppressed** |
| Identical file, only the date changed to `2026-11-30` | **suppressed** |
| Identical file, full RFC3339 timestamp `2026-10-23T00:00:00Z` | **suppressed** |

Only the date differs between rows two and three, and the outcome is the same, so the
expiry is not being evaluated for misconfiguration entries in this version.

The suppression itself is correct — the official Postgres entrypoint needs root to fix
ownership and run `initdb` before dropping to `postgres` via gosu, and adding the
directive breaks a fresh volume. The property the rule defends holds by the entrypoint.
**The finding is that the expiry is decorative.** Any exception given a date in this file
will outlive it silently, and the deferral process depends on those dates meaning
something. The remedy is a calendar reminder or a CI check that reads the dates itself,
not a configuration change.

*This also corrects a prediction made in this project on 22 October, that the gate would
turn red when the date passed. It did not, and the gate was green on 26 October.*

### 3.2 One of three repositories has no server-side CI

> **Addressed 26 Oct 2026** on `feature/console-ci-workflow`:
> `.github/workflows/ci.yml` in the console repository, mirroring the node's two-job
> shape. See the note at the end of this section.


`circuless-management-ui-beta` has no `.github/workflows`. Its gates run only through
`bvr-ci` on a developer's machine.

This is **less serious than it sounds**: `bvr-ci patch` runs gitleaks and Trivy before it
will cut a release, verified on 26 October, and Trivy does scan `package-lock.json` and
the Dockerfile. So SR-4.2.1, SR-4.3.2 and SR-5.1.2 are enforced before anything ships.

But the enforcement is local and bypassable, where the other two repositories have the
same gates running server-side on every push. If an auditor reads "dependency scanning in
CI/CD — critical CVEs block deployment" strictly, the console does not have CI. Copying
the node's workflow across is an hour.

**What adding it immediately found.** The console's suite was failing one test on `main`
— `nodeDownload.test.ts`, "is the bytes the node sent" — and nobody knew, because
nothing had run it since 22 October. The cause was not a code change: under vitest's
jsdom environment, whether the global `Blob` is Node's or jsdom's depends on the Node
version, and only Node's has `.text()`. A Node upgrade on a developer machine broke an
assertion that had passed for weeks. Fixed by reading the blob with `FileReader`, which
jsdom always supports. That is the argument for this item in one example: an untested
`main` is not a passing `main`.

### 3.3 SAST does not cover the Cloud API

Noted here rather than in the table because the row still passes. Bandit and Semgrep run
in the node's CI over `src` and `tests`. In the Cloud's CI they run over
`deploy/keycloak/scripts` **only** — `api/src`, the Cloud API itself, is not scanned.
SR-4.3.3 is recommended rather than mandatory, and the scope looks like an oversight
rather than a decision. Widening it is a one-line change.

---

### 3.4 A documented file permission that nothing establishes

`BACKUP-AND-RESTORE.md` sets the three Restic secrets to `0444` — deliberately, since a
non-root container user must read them — and describes them as "0444 inside a `0700`
directory like the others". Nothing sets that directory to `0700`:
`gen-dev-secrets.sh` does `mkdir -p` with no `chmod`, so the mode is the operator's
umask, typically `0755`.

If the deployed host has `0755`, the Restic repository password and the object-storage
credentials are readable by any local user — and that password is what stands between a
copy of the backups and their contents. The host could not be inspected from here, so
this is a **check, not yet a finding**: `stat -c '%a %n'` on the directory settles it.
The fix either way is a `chmod 0700` in the generator and a correction to the sentence
in `BACKUP-AND-RESTORE.md`, which currently asserts a property nothing creates.

Does not change the verdict on SR-4.3.1, which is about secrets in code and
configuration. It does bear on the §9 compensating control "private keys readable only
by their service user".

## 4. Every requirement

Legend: **✅ met** · **◐ partial** · **❌ not met** · *(M)* mandatory · *(R)* recommended

### §1.1 Authentication

| ID | | Evidence |
|---|---|---|
| SR-1.1.1 *(M)* | ✅ | `realmSettings.passwordPolicy`: `length(12)`, upper, lower, digit, special, `notUsername`, `hashAlgorithm(argon2)`. No forced rotation |
| SR-1.1.2 *(R)* | ❌ | MFA not enforced. **In the register**, due 4 Nov. Recommended at TRL 5 |
| SR-1.1.3 *(M)* | ✅ | `bruteForceProtected: true`, `failureFactor: 5`, `permanentLockout: false` — temporary by design, so guessing a known username cannot deny service to that person |
| SR-1.1.4 *(M)* | ✅ | Every shipped client: `implicitFlowEnabled: false`, `directAccessGrantsEnabled: false`. The register's entry concerns `dev-cli` and a spike script, which are development tooling and not in the realm file |
| SR-1.1.5 *(R)* | ✅ | `ssoSessionIdleTimeout: 1800` (30 min), `ssoSessionMaxLifespan: 43200` (12 h) — exactly as specified |
| SR-1.1.6 *(M)* | ◐ | `resetPasswordAllowed` and `verifyEmail` are on, and SMTP is fully overridable from the environment. The committed value is `mailpit`, a local catcher: a deployment that has not set the override has no working reset |
| SR-1.1.7 *(M)* | ❌ *(unblocked)* | Was "not possible in the current topology". The precondition for changing the topology was settled 26 Oct; scheduled via `keycloak-tls-termination.md`. Still unmet until performed |

### §1.2 Authorization

| ID | | Evidence |
|---|---|---|
| SR-1.2.1 *(M)* | ✅ | Three levels, not two: `platform-admin` realm role, org admins via `/orgs/<x>/admins`, members via `/orgs/<x>` |
| SR-1.2.2 *(M)* | ✅ | One pure `decide()` with exhaustive table tests; node principals refused on every endpoint not explicitly opted in; identity from the token, never the body |
| SR-1.2.3 *(M)* | ✅ | CI test enumerates every route and mounted static tree and asserts 401 |
| SR-1.2.4 *(M)* | ✅ | Registries are `platform-admin` only; verified in practice this week when an org admin correctly could not see the node registry |

### §2.2 Encryption in transit

| ID | | Evidence |
|---|---|---|
| SR-2.2.1 *(M)* | ✅ | TLS ≥ 1.2, 1.0 and 1.1 refused. Measured 2 Oct, transcript in `deploy/security/evidence/` |
| SR-2.2.2 *(M)* | ✅ | Mozilla intermediate profile applied 2 Oct |
| SR-2.2.3 *(M)* | ✅ | `stsSeconds=15768000` — six months exactly, the floor the requirement sets |
| SR-2.2.4 *(M)* | ✅ | ACME via the host's Traefik resolver; no self-signed certificate on a public endpoint. Node and service certificates are self-signed but are `private_key_jwt` credentials, not TLS server certificates, and are not on accessible endpoints |

### §2.3 Backup

| ID | | Evidence |
|---|---|---|
| SR-2.3.1 *(R)* | ✅ | Restic, nightly databases and weekly configuration, off-host. Exceeds the weekly minimum |
| SR-2.3.2 *(R)* | ✅ | Restic encrypts with a password held on the host and in Passbolt. The nightly job reads the snapshot back and deletes it if it does not verify |

### §2.4 GDPR

| ID | | Evidence |
|---|---|---|
| SR-2.4.1 *(M)* | ✅ *(pending sign-off)* | `deploy/security/data-subject-rights.md`, 26 Oct. A documented procedure rather than endpoints, on the finding that no table outside Keycloak holds a name or an email — the audit and access logs carry a pseudonymous subject only. Erasure of the residual identifier rests on two independent grounds, anonymisation and Art. 17(3). Needs §1 and §7 completed by the operator |
| SR-2.4.2 *(R)* | ❌ | No privacy policy, cookie notice or DPIA. The console sets no cookies and uses `sessionStorage`, which reduces the ePrivacy question but does not answer the others |
| SR-2.4.3 *(M)* | ✅ | Hetzner `fsn1` (Falkenstein, Germany) for the host and for backup object storage; "EU locations only" is a stated host requirement |

### §3.1 API design

| ID | | Evidence |
|---|---|---|
| SR-3.1.1 *(M)* | ✅ | Correct verbs and codes; identifiers in paths are UUIDs and slugs, no tokens or personal data in URLs |
| SR-3.1.2 *(R)* | ◐ | OpenAPI is generated and committed, and the console's client is generated from it. It is deliberately **not served** — `openapi_url=None`, since an unauthenticated index of every route is worth a lot to a scanner. Partner-facing documentation therefore means handing over the file |
| SR-3.1.3 *(M)* | ✅ | `/v1` on every route, asserted by test on both cloud and node |
| SR-3.1.4 *(M)* | ✅ | Reason codes from one enum; no stack traces, internal paths or versions |

### §3.2 API security

| ID | | Evidence |
|---|---|---|
| SR-3.2.1 *(M)* | ✅ | As SR-1.2.3. The node's `/ui` exemption is static sign-in code carrying four OAuth-public values |
| SR-3.2.2 *(M)* | ✅ | Access tokens 300 s; refresh bounded by a 12 h session maximum. Far inside 8 h / 7 days |
| SR-3.2.3 *(M)* | ✅ | Pydantic models with length and pattern limits; path confinement on `/data` and `/invoke` |
| SR-3.2.4 *(M)* | ✅ | Explicit origin allowlist; a validator rejects `*` at startup rather than at review |
| SR-3.2.5 *(R)* | ✅ | UUIDs throughout; "never sequential integers in anything external" is an invariant with a test |
| SR-3.2.6 *(M)* | ◐ | Cloud API rate-limited at 60/min, burst 120. The node's own API, reached through the gateway, carries no rate limit |

### §3.3 Performance and interoperability

| ID | | Evidence |
|---|---|---|
| SR-3.3.1 *(R)* | ◐ | Uptime Kuma polls a health endpoint and records response time. There is no per-endpoint API latency monitoring, which is what the row describes — adequate at TRL 5 |
| SR-3.3.2 *(M)* | — *(out of scope)* | Owned by **other consortium partners**, who integrate BIM; decided J, 26 Oct 2026. `circuless-architecture/CLAUDE.md` names *BIM visualisation* as a **service**, "outside the architecture … documented only through integration requirements". Mandatory for the project, evidenced by the partners doing it, not by this platform |
| SR-3.3.3 *(R)* | ❌ *(out of scope here)* | No DPP endpoints in these repositories. As with BIM, *DPP* is a named service and therefore outside the core platform's architecture. Owned by the service work |

### §4.1 Network

| ID | | Evidence |
|---|---|---|
| SR-4.1.1 *(M)* | ❌ | Port 22 open to the internet. **In the register**, due 4 Nov. Declared port list is otherwise correct and verified by full 65535-port scans, retained as evidence |
| SR-4.1.2 *(M)* | ◐ | SSH offers `publickey` only — confirmed. Port unchanged and not IP-restricted; the requirement asks for key-only **and** restriction |
| SR-4.1.3 *(M)* | ❌ *(route decided)* | Keycloak admin console publicly reachable; Traefik's dashboard already returns 404. In the register, due 4 Nov, and now with a procedure: `ipAllowList` on `PathPrefix(/admin)` once the edge route is HTTP. Note there is no variant that avoids terminating TLS — a passthrough route cannot match a path |
| SR-4.1.5 *(R)* | ✅ | Hetzner's network-level DDoS mitigation, included by default |

### §4.2 Vulnerability management

| ID | | Evidence |
|---|---|---|
| SR-4.2.1 *(M)* | ✅ | Trivy on lockfiles, HIGH and CRITICAL fail the gate. Demonstrated this month: a CRITICAL `certifi` advisory was caught, analysed and fixed in both Python repositories, with the reasoning written up |
| SR-4.2.2 *(M)* | ✅ | Trivy covers Dockerfiles; `cosign verify` before `compose up` |
| SR-4.2.3 *(M)* | ◐ | `unattended-upgrades` documented with install and verification commands. Whether it is enabled on the host could not be confirmed from here |

### §4.3 Secure development

| ID | | Evidence |
|---|---|---|
| SR-4.3.1 *(M)* | ✅ | Docker secrets and environment variables; `.gitignore` plus a location-keyed gitleaks rule; a test asserts git tracks nothing in `secrets/` but the `.gitignore` |
| SR-4.3.2 *(M)* | ✅ | Gitleaks over full history on every run. See §2 for the incident and the rule that closed it |
| SR-4.3.3 *(R)* | ◐ | Bandit and Semgrep in both Python repositories, but the Cloud's run covers `deploy/keycloak/scripts` only — see §3.3 |
| SR-4.3.5 *(M)* | ❌ | No branch protection, no required review. **In the register**, due 4 Nov |
| SR-4.3.6 *(M)* | ✅ | `uv.lock` and `package-lock.json` committed; images pinned by digest everywhere, including base images |

### §4.4 Monitoring

| ID | | Evidence |
|---|---|---|
| SR-4.4.1 *(M)* | ✅ | Keycloak events on, `eventsExpiration: 7776000` (90 days) with admin events and details; append-only audit log in the Cloud; append-only access log on the node; `pgaudit` on the database |
| SR-4.4.2 *(R)* | ✅ | Uptime Kuma, running off the Cloud host so it survives that host |
| SR-4.4.5 *(M)* | ✅ *(pending sign-off)* | `deploy/security/incident-response.md`, 26 Oct. A template: the procedure and commands are concrete, the contacts are blanks the operator fills. Needs §1 completed |

### 5. Containers

| ID | | Evidence |
|---|---|---|
| SR-5.1.1 *(M)* | ✅ | `USER` in the Cloud API, backup, node and console images; the console's base runs as uid 101 with no root stage. Postgres is the one exception, documented with its reason, and the property holds via the entrypoint's `gosu` drop |
| SR-5.1.2 *(M)* | ✅ | As SR-4.2.2 |

### 6. Supply chain

| ID | | Evidence |
|---|---|---|
| SR-6.1.1 *(M)* | ✅ | As SR-4.3.6 |
| SR-6.1.2 *(R)* | ◐ | The rule exists and is honoured in the Python repositories. The console's own plan records that it "does not survive contact with npm and needs rewording" — an honest note rather than a silent lapse |
| SR-6.1.3 *(R)* | ✅ | Syft generates a CycloneDX SBOM in both Python repositories' CI, retained as an artifact. Attached to CI runs rather than to releases |
| SR-6.1.4 *(M)* | ❌ | Commits unsigned. **In the register**, due 4 Nov |

### 7. Data platform

| ID | | Evidence |
|---|---|---|
| SR-7.1.1 *(M)* | ✅ *(pending sign-off)* | `deploy/security/data-classification-policy.md`, 26 Oct. Three classes, the placement rule, and an explicit statement that the class is self-declared and unverified. Needs the `non-sensitive` definition confirmed and §8 signed |
| SR-7.1.2 *(R)* | ✅ | `pgaudit` in `shared_preload_libraries`, extension created in each database, settings on the Postgres command line |
| SR-7.1.3 *(M)* | ✅ *(pending sign-off)* | The statement is §6 of the classification policy, naming each environment rather than claiming generally. Needs signing |
| SR-7.1.5 *(M)* | ✅ *(pending sign-off)* | `deploy/security/real-data-transition-checklist.md`, 26 Oct. Trigger, the §9 compensating controls as a verify-list, the deferred items that block, and what becomes mandatory at the gate |

---

## 5. Suggested order of work

1. **SR-7.1.5**, the transition checklist. An hour, and it is what makes §9's deferral
   defensible.
2. **SR-7.1.1** and **SR-7.1.3**, which are largely the same document — the classification
   policy already has its mechanism, and the synthetic-data statement is a paragraph in it.
3. **SR-4.4.5**, the incident page.
4. **SR-4.1.3 and SR-1.1.7 together** — one change closes both, now that terminating TLS
   at Traefik is available. The register names the admin console as the first thing an
   auditor looks for, and SR-1.1.7 is the only requirement here ever classified as
   impossible. `keycloak-tls-termination.md` is the procedure; the risk to manage is the
   issuer claim, not the mTLS removal.
5. **SR-2.4.1**, a decision and a paragraph on data subject rights.
6. ~~SR-3.3.2, BIM integration~~ — **closed as out of scope (J, 26 Oct)**: other
   consortium partners integrate BIM, and the evidence comes from them.
7. ~~§3.1, a check that reads the expiry dates~~ — **declined (J, 26 Oct)**: deferral
   dates are tracked by the technical lead, not by CI.
8. ~~§3.2, a CI workflow for the console~~ — **done (26 Oct)**, and it found a failing
   test on `main` on its first run.

Items 1–3 and 5 are documents, total perhaps half a day. They move four mandatory
requirements from unrecorded to met, and close the partial on SR-7.1.3 along the way.
