# Audit: functionality and security

What the CIRCULess core platform does, and what it has to satisfy — in one place, for
the security validation.

Every row carries **how to demonstrate it**, phrased so that somebody who did not build
the platform can follow it. Where a control cannot be shown — because it is a document
awaiting signature, or a setting on a host nobody has checked — the row says so rather
than offering a command that would pass regardless.

## How to read it

**Part A — functionality** is written from a **user's** point of view: a thing a person
or an application can do, not a unit of code. The *Case* column cites the acceptance
cases in `circuless-cloud/deploy/acceptance/RUN-SHEET.md`, which are the stable
identifiers for these (T01–T35). An **S** case is security-critical and may never be
skipped.

**Part B — security requirements** is every requirement in TRL 5 scope from
`security_requirements.md`, with the verdict from `compliance-assessment.md`.

| | |
|---|---|
| ✅ | met |
| ◐ | partial — the control exists but does not cover everything the requirement asks |
| ❌ | not met |
| — | out of scope for the core platform |

---

# Part A · Functionality

> **Verification status is deliberately blank.** Blocks 1–3 were run locally and
> recorded; the rest were run by hand over the acceptance days. J confirms what was
> actually witnessed before that column is added, because a list that says "verified"
> on somebody's recollection is worse than one that says nothing.

Throughout: `GT` is `circuless-cloud/deploy/keycloak/scripts/get-token.py`, which drives
a real browser sign-in and prints a token; `ACT` is
`circuless-node/examples/acting-for-a-user/act.py`. The run sheet has the full
step-by-step for every T-case.

## A1. Identity and sign-in

| # | A user or application can… | Case | How to validate |
|---|---|---|---|
| A1.1 | Sign in through the identity provider and reach the console | T01 | Open `/console`, sign in. The bar shows a principal type and a truncated subject — and **no name or email**, which is the point (D31) |
| A1.2 | Obtain a token scoped to exactly one system | T01 | `GT --scope "openid node:alpha-onprem"`. Decode it: `aud` is that node alone. Ask for two audiences and Keycloak refuses |
| A1.3 | Authenticate an application with its own key, no shared secret | T22, T23 | `ACT keypair` then `ACT as-itself`. A token arrives with no secret anywhere in the exchange; the client proves itself by signing |
| A1.4 | Be refused when presenting a token for a different node | T03 **S** | Take a `node:bvr-cloud` token to `alpha-onprem`. Expect **401**, audience mismatch |
| A1.5 | Be refused when presenting a node's token to read data | T02 **S** | Present a node's own token to `GET /v1/t/alpha/resources/<id>/data`. Expect **403 `node_principal_not_permitted`** (D14) |
| A1.6 | Not edit their own authorisation attributes | T04 **S** | In Keycloak's account console, try to set `org_id` on your own user. Refused — admin-editable only. `kc.py verify` performs the same attack and asserts it did not land |
| A1.7 | Delete their own account | T29 | Delete a test user. They cannot sign in immediately; the audit trail keeps the pseudonymous `sub`, which is the documented position (`data-subject-rights.md` §4) |

## A2. Organisations, nodes and tenants — the platform operator

| # | The operator can… | Case | How to validate |
|---|---|---|---|
| A2.1 | Register an organisation | — | TUTORIAL Part 3: `POST /v1/orgs`, then confirm it appears in `GET /v1/orgs`. **Both halves**: the `/orgs/<slug>` groups must also exist in the realm, or nobody can act as it |
| A2.2 | Register a node and give it a gateway address | — | TUTORIAL Part 4: `POST /v1/nodes`, then `circuless-cloud-routes` generates the gateway route. Confirm the node answers through `<node>.nodes.circuless.bavenir.eu/v1` |
| A2.3 | Say which organisations a node hosts | — | Console → **Nodes** → *Change hosted organisations*. The screen states what will be added and removed before saving, because the API replaces the whole set |
| A2.4 | See whether a node is usable — tenants, audience scope, route, certificate, heartbeat | — | Console → **Nodes**. Each node shows five checks. A node hosting nobody, or whose realm scope is missing, is marked rather than left looking healthy |
| A2.5 | Retire a node or an organisation without deleting its history | — | `PUT /v1/nodes/<uuid>` with `{"status":"suspended"}`. The row stays, the audit entries that name it still resolve, and `GET /v1/audit` shows the change with before and after |
| A2.6 | Register a service client for an organisation | — | TUTORIAL Part 7, end to end: add the client, apply, register its certificate, obtain a token. `kc.py verify` reports its `principal_type` and `org_id` |

## A3. Publishing a resource

| # | An organisation can… | Case | How to validate |
|---|---|---|---|
| A3.1 | Register a dataset with a licence and upload its file | T05 | As `svc-alpha-pipeline`, register and upload. Within 30 s the Cloud catalogue shows a `dcat:Dataset` carrying its licence |
| A3.2 | Upload a dataset as a set of objects rather than one file | T05 | Upload five bucket objects; the manifest lists five |
| A3.3 | Register a service resource, with its endpoint kept private | T06 | Catalogue shows `dcat:DataService` with an endpoint *description*. Confirm `endpoint_url` appears **only** to someone who may manage the resource — a consumer who had it could bypass the node |
| A3.4 | Rely on new resources being invisible until deliberately shared | T34 **S** | Register with no sharing settings. Result is `hidden` / `org`, and Beta cannot see it. Defaults closed (NFR4) |
| A3.5 | Change a resource's discoverability and see the catalogue follow | T10 | Mark it `hidden`; it disappears from Beta's catalogue within the sync interval |
| A3.6 | Be refused when publishing into another organisation's tenant | T07 **S** | As `beta-user`, register in tenant `alpha`. Expect **403** |
| A3.7 | Have upstream credentials settable by admins only, and never readable | T08 **S** | As a service principal, try to rotate a `ServiceCredential` — **403**, admins only. Then confirm no API or screen ever returns one |
| A3.8 | Withdraw a resource, with access denied at once and data purged later | T32 **S** | Delete it. The catalogue record is withdrawn and reads are refused **immediately**; the access log entries remain; data goes at `purge_after` |

## A4. Discovery

| # | A consumer can… | Case | How to validate |
|---|---|---|---|
| A4.1 | Search the catalogue across organisations and nodes | T09 | Console → **Catalogue**, or `GET /v1/catalogue?q=PET`. Records from more than one node appear |
| A4.2 | See a record's licence, theme, and where to fetch it | T09 | Open a record. **Check the `accessURL` exists** — a node with no gateway address publishes a record with no distribution at all: discoverable and unfetchable, silently |
| A4.3 | Not see what has not been shared with them | T10, T34 **S** | As a member of another organisation, search for the hidden resource. Absent — filtered by discoverability, never by visibility |

## A5. Agreements

| # | A party can… | Case | How to validate |
|---|---|---|---|
| A5.1 | Request access to a resource they found | T09 | Console → catalogue record → *Request access*. It appears in both parties' **Agreements** as `requested` |
| A5.2 | Have their organisation taken from their token, not from what they send | T11 **S** | Post a request with `consumer_org=alpha` in the body while signed in as Beta. The agreement records **beta** — the body is ignored (R3) |
| A5.3 | Approve or reject a request, as the provider's admin | T12, T13 **S** | As `alpha-admin`, approve. Status becomes `accepted`, and the Cloud audit log records actor, time, before and after |
| A5.4 | Offer access without waiting to be asked | — | Console → **Agreements** → *Offer access*. Only an admin sees the form. Choosing "everything we publish" is a deliberate selection, never a blank field |
| A5.5 | Accept an offer, as the consumer's admin | — | As the consumer's admin, accept. A member who is not an admin sees the row and no button |
| A5.6 | Revoke access already granted | T33 | Revoke. Both the approval and the revocation are in `GET /v1/audit` with actor and time |
| A5.7 | See a decision take effect platform-wide within a bounded time | T12, T26 | Revoke, then retry every 5 s and **record the number**. Expect refusal within the 30 s sync plus the residual token lifetime. "It seemed quick" is not evidence |
| A5.8 | Be refused when deciding on another organisation's resource | T13 **S** | As `beta-admin`, approve a request against Alpha's resource. Expect **403** |

## A6. Reading data

| # | A consumer can… | Case | How to validate |
|---|---|---|---|
| A6.1 | Download a dataset once an agreement permits it | T12 | After approval, `GET …/data` returns 200 within 30 s. The node's access log shows Beta's pseudonymous subject, acting org `beta`, and a byte count |
| A6.2 | Be refused before one does, with a reason that says why | T09 | Before approval, the same call returns **403 `no_agreement`** — a reason code, not a bare refusal |
| A6.3 | List a bucket, fetch one object, and resume a partial download | T14 | Manifest lists five; one object returns 200; a `Range` request returns **206** |
| A6.4 | Read as an application rather than a person, under the same agreement | T15 | As `svc-beta-pipeline`, read the same dataset. 200, logged as `principal_type=service` |
| A6.5 | Belong to two organisations and act as one of them, explicitly | T16 | As `consultant`, read Alpha's dataset. Allowed as an Alpha member and logged with acting org `alpha`. Where two organisations could authorise, the request must name one |
| A6.6 | Download in a browser, from a machine with no VPN | T24 | From a machine with **no NetBird client**, download through the console via `alpha-onprem.nodes.…`. 200 with CORS accepted. **Screenshot it** |

## A7. Calling a service

| # | A consumer can… | Case | How to validate |
|---|---|---|---|
| A7.1 | Invoke a provider's service through the node, under an agreement | T17, T18 | Invoke before approval — 403; after — 200. T18 does the same across the overlay to a partner node |
| A7.2 | Have the provider's credential attached without ever seeing it | T17 **S** | Read the **service's own log**: it shows `X-CIRCULess-Org` and the injected upstream credential, and **no caller `Authorization`** |
| A7.3 | Not reach the provider's service directly, bypassing the decision | T17 **S** | Confirm a forged inbound `X-CIRCULess-Subject` never arrives at the service — every inbound `X-CIRCULess-*` is stripped |
| A7.4 | Receive a streamed response as it is produced | T20 | Call an SSE endpoint. The **first event must arrive before the stream completes**. A buffered stream looks like a slow one, so watch the timing, not the result |
| A7.5 | Get a clear failure when a service is too slow | T21 | Make the service exceed `timeout_s`. Expect **504** with a reason code, and an entry in the access log |
| A7.6 | Be protected from a service redirecting them off the platform | T19 **S** | Service redirects to itself → rewritten to the node's `/invoke`. Service redirects to an external host → **refused**. A followed external redirect looks like success |

## A8. Acting on someone's behalf

| # | An application can… | Case | How to validate |
|---|---|---|---|
| A8.1 | Act for a signed-in user, with the node seeing that user | T22 | `ACT for-user --user-token <beta-user>`. The node's log shows the **user** as subject, the service as `azp`, acting org `beta`. The user's token must carry `svc:…` in its `aud` or Keycloak refuses the exchange |
| A8.2 | Act as itself, and get nothing its organisation has no agreement for | T23 **S** | `ACT as-itself` against the same resource — **403**. There is no privileged platform path |

## A9. Audit and transparency

| # | A party can… | Case | How to validate |
|---|---|---|---|
| A9.1 | Read every access decision about their own resources | T28 **S** | As `alpha-admin`, read Alpha's access log. Every allow and deny from the run is there, with pseudonymous subjects |
| A9.2 | Not read another organisation's log | T28 **S** | As `beta-admin`, try — **403**. On a shared node, a Beta admin cannot see tenant `bvr` |
| A9.3 | See who changed an agreement, when, and what it was before | T33 | `GET /v1/audit` after an approve and a revoke: actor, acting org, time, before and after |
| A9.4 | Read the audit trail in the console, with subjects pseudonymous | — | Console → **Audit**. An org admin sees their own organisation; the platform operator sees everything. Subjects are truncated and there is no name or email anywhere |
| A9.5 | Rely on those records being append-only | T32, T33 | Withdraw a resource and confirm its log entries survive. No update or delete path exists in the code for either log — the absence is the control |

## A10. Running it

| # | The platform can… | Case | How to validate |
|---|---|---|---|
| A10.1 | Keep enforcing agreements while the Cloud API is down | T27 | Stop the Cloud API, then keep requesting against a node. Decisions stay correct from the cache; recovery needs no restart |
| A10.2 | Report its own staleness while disconnected | T27 | During the outage, the node's `/healthz` and `/metrics` report a stale sync |
| A10.3 | Record an outage in monitoring | T27 | Uptime Kuma must be **watching before you stop anything** — the outage only appears in its history if it was already checking |
| A10.4 | Keep internal endpoints unreachable from the internet | T25 **S** | Four `curl`s through the gateway: `/internal/authz`, `/metrics`, `/healthz`, `/.well-known/…`. All refused at the edge, because the route matches `/v1` alone |
| A10.5 | Be restored into a clean environment within the recovery target | T35 | Restore and **record the elapsed time against the 4 h target**. Run against the provider's machine image, which also carries Keycloak's database |

## Not demonstrated, and why

| # | | |
|---|---|---|
| T30 | Member list | C19 does not exist — no `/members` endpoint. Integration flow F1 stays half-tested |
| T31 | Persistent identifiers | Deferred with FR3, for the final version |
| — | BIM integration | A service, integrated by other consortium partners — outside the core platform |

---

# Part B · Security requirements

58 in TRL 5 scope: 43 mandatory, 15 recommended. Verdicts and the reasoning behind each
are in `compliance-assessment.md`; this column says how to see it for yourself.

Recurring commands: `KC` is `circuless-cloud/deploy/keycloak/scripts/kc.py`, `CI` is
`bvr-ci run-tests` in each repository. Measured transcripts are in
`circuless-cloud/deploy/security/evidence/`.

## B1. Authentication

| ID | | Requirement | How to validate |
|---|---|---|---|
| SR-1.1.1 | ✅ | Strong password policy, ≥ 12 characters | `realmSettings.passwordPolicy` in `realm-config.json`, asserted by `KC verify`. Names `argon2` explicitly rather than inheriting it. Try setting an 8-character password |
| SR-1.1.2 | ❌ | MFA for all user accounts *(recommended)* | Not enforced. In the deferral register and in the realm's own `deferred` block, due 4 Nov |
| SR-1.1.3 | ✅ | Lockout after 5 failed attempts | `bruteForceProtected`, `failureFactor: 5`, `permanentLockout: false`. Fail five sign-ins and watch the account lock **temporarily** — permanent lockout would turn guessing into denial of service |
| SR-1.1.4 | ✅ | Authorization code flow; implicit disabled | Every shipped client has `implicitFlowEnabled: false` and `directAccessGrantsEnabled: false`. There is no password grant to try |
| SR-1.1.5 | ✅ | Session timeout 30 min / 12 h *(recommended)* | `ssoSessionIdleTimeout: 1800`, `ssoSessionMaxLifespan: 43200` |
| SR-1.1.6 | ◐ | Password reset by email token | `resetPasswordAllowed` and `verifyEmail` are on. **The committed SMTP host is `mailpit`**, a local catcher — confirm the deployment overrode it, or reset silently does nothing |
| SR-1.1.7 | ❌ | Rate limiting on the login endpoint | Not present: Keycloak is behind a TLS-passthrough TCP router, where HTTP middleware cannot apply. Compensated by brute-force lockout. **Unblocked** — `deploy/security/keycloak-tls-termination.md` |

## B2. Authorization

| ID | | Requirement | How to validate |
|---|---|---|---|
| SR-1.2.1 | ✅ | RBAC with at least two roles | Three levels: the `platform-admin` realm role, org admins via `/orgs/<x>/admins`, members via `/orgs/<x>`. `GET /v1/whoami` returns which you hold |
| SR-1.2.2 | ✅ | Least privilege | One pure `decide()` with exhaustive table tests. Behaviourally: A1.5, A3.6, A5.8, A8.2 are all "the obvious shortcut is refused" |
| SR-1.2.3 | ✅ | Every API endpoint requires a token | A CI test enumerates every route **and mounted static tree** and asserts 401 without a token, so new routes are covered automatically. One declared exemption: the node's `/ui`, static sign-in code |
| SR-1.2.4 | ✅ | Admin functions restricted to admins | Registries are `platform-admin` only. Sign in as an org admin: the console's **Nodes** section is not offered, and `GET /v1/nodes` returns 403 |

## B3. Encryption in transit

| ID | | Requirement | How to validate |
|---|---|---|---|
| SR-2.2.1 | ✅ | TLS 1.2 minimum | `nmap --script ssl-enum-ciphers -p443 <host>`, or the transcript in `evidence/h4-edge-2026-10-02.txt`. 1.0 and 1.1 refused |
| SR-2.2.2 | ✅ | Weak ciphers disabled | Same transcript; Mozilla intermediate profile, applied 2 Oct |
| SR-2.2.3 | ✅ | HSTS ≥ 6 months | `curl -sI https://api.circuless.bavenir.eu/v1/whoami \| grep -i strict`. `max-age=15768000` — six months exactly, the floor |
| SR-2.2.4 | ✅ | Certificate from a trusted CA | Open it in a browser. Node and service certificates are self-signed, but they are `private_key_jwt` credentials, not TLS server certificates, and are on no accessible endpoint |

## B4. Backup

| ID | | Requirement | How to validate |
|---|---|---|---|
| SR-2.3.1 | ✅ | Regular backups, weekly minimum *(recommended)* | `docker compose … run --rm backup snapshots` lists nightly database and weekly configuration snapshots. The cron entries are in `BACKUP-AND-RESTORE.md` |
| SR-2.3.2 | ✅ | Backups encrypted *(recommended)* | Restic encrypts with a password held on the host and in Passbolt. `run --rm backup check` verifies. The nightly job **reads the snapshot back** and deletes it if it does not verify |

## B5. GDPR

| ID | | Requirement | How to validate |
|---|---|---|---|
| SR-2.4.1 | ✅ | Access, rectification, erasure, portability | `deploy/security/data-subject-rights.md`. Rectification is self-service in Keycloak's account console; the rest is an operator procedure. **Pending sign-off**: §1 and §7 |
| SR-2.4.2 | ❌ | Cookie consent, privacy policy, DPIA *(recommended)* | None published. The console sets no cookies and uses `sessionStorage`, which narrows the ePrivacy question without answering the others |
| SR-2.4.3 | ✅ | EU/EEA data residency | Hetzner `fsn1`, Falkenstein, for the host and the backup bucket |

## B6. API design

| ID | | Requirement | How to validate |
|---|---|---|---|
| SR-3.1.1 | ✅ | RESTful, no sensitive data in URLs | Read `openapi.json`: path parameters are UUIDs and slugs. No token, email or name appears in any path |
| SR-3.1.2 | ◐ | OpenAPI documentation *(recommended)* | `api/openapi.json` is generated from the routes and committed. **Deliberately not served** — an unauthenticated index of every route is worth a lot to a scanner — so partner documentation means handing over the file |
| SR-3.1.3 | ✅ | `/v1` versioning | Every route is under `/v1`, asserted by test on both Cloud and node. The gateway rule matches `PathPrefix(/v1)` and nothing else |
| SR-3.1.4 | ✅ | Standard error codes, no stack traces | Provoke a 403 and a 422. Each returns a reason code from one enum; no stack trace, internal path or version appears |

## B7. API security

| ID | | Requirement | How to validate |
|---|---|---|---|
| SR-3.2.1 | ✅ | Every endpoint requires a bearer token | As SR-1.2.3 |
| SR-3.2.2 | ✅ | Token expiry within bounds | `accessTokenLifespan: 300` — five minutes, against a limit of eight hours. Refresh is bounded by the 12 h session maximum, against seven days |
| SR-3.2.3 | ✅ | Input validation on all parameters | Pydantic models with length and pattern limits. Behaviourally: post an over-long slug, and a `../` path to `/data` — both refused, the second by path confinement |
| SR-3.2.4 | ✅ | CORS allowlist, no wildcard | A validator refuses `*` at **startup**, not at review. Set it and the node will not boot |
| SR-3.2.5 | ✅ | UUIDs, not sequential ids *(recommended)* | Every external identifier in `openapi.json` is a UUID or a slug |
| SR-3.2.6 | ◐ | Rate limiting on public endpoints | The Cloud API carries `rateLimit` at 60/min, burst 120 — `evidence/` has a `429`. **The node's API, reached through the gateway, carries none** |

## B8. Performance and interoperability

| ID | | Requirement | How to validate |
|---|---|---|---|
| SR-3.3.1 | ◐ | API response-time monitoring *(recommended)* | Uptime Kuma polls a health endpoint and records response time. There is no per-endpoint latency monitoring, which is what the row describes |
| SR-3.3.2 | — | BIM integration | Owned by **other consortium partners**; evidence comes from them. Not evidenceable from this platform |
| SR-3.3.3 | ❌ | DPP endpoints stubbed *(recommended)* | None. DPP is a service, outside the core platform's architecture |

## B9. Network

| ID | | Requirement | How to validate |
|---|---|---|---|
| SR-4.1.1 | ❌ | Only necessary ports open; 22 via VPN | Port scan — `evidence/port-scan-2026-10-19.txt`, all 65535 ports, not a sample. 443, 80 and **22** are open; 22 should be overlay-only. In the register, due 4 Nov |
| SR-4.1.2 | ◐ | SSH key-only and restricted | `ssh -o PreferredAuthentications=password` is refused — the server offers `publickey` only. The port is unchanged and not IP-restricted, which is the other half of the requirement |
| SR-4.1.3 | ❌ | VPN or allowlist for administrative access | `curl https://auth.circuless.bavenir.eu/admin/` from anywhere reaches a login page. Traefik's own dashboard already returns 404. Route decided — `keycloak-tls-termination.md` step 3 |
| SR-4.1.5 | ✅ | DDoS protection *(recommended)* | Hetzner's network-level mitigation, on by default |

## B10. Vulnerability management

| ID | | Requirement | How to validate |
|---|---|---|---|
| SR-4.2.1 | ✅ | Dependency scanning in CI; critical CVEs block | `CI` in each repository, or any CI run. Demonstrated in October: a CRITICAL `certifi` advisory was caught, analysed and fixed in both Python repositories — `deploy/security/dependency-advisories.md` |
| SR-4.2.2 | ✅ | Container image scanning before deployment | Trivy covers the Dockerfiles in the same run; `cosign verify` precedes `compose up` |
| SR-4.2.3 | ◐ | Unattended security upgrades | `systemctl is-enabled unattended-upgrades` **on the host**. Documented with install and verification commands in `H5-host-hardening.md`; application not verified from a development machine |

## B11. Secure development

| ID | | Requirement | How to validate |
|---|---|---|---|
| SR-4.3.1 | ✅ | No hardcoded secrets | Docker secrets and environment variables; `git ls-files deploy/compose/secrets/` returns only the `.gitignore`, asserted by test |
| SR-4.3.2 | ✅ | Secrets scanning in CI | Gitleaks over **full history** on every run. When four secret files were once committed, the incident, the blast radius and the **detection gap** were all written up, and the gap closed with a rule keyed on location rather than shape |
| SR-4.3.3 | ◐ | SAST in CI *(recommended)* | Bandit and Semgrep run in both Python repositories. **The Cloud's run covers `deploy/keycloak/scripts` only — `api/src` is not scanned.** The console has no SAST |
| SR-4.3.5 | ❌ | Protected main branch, required reviews | Not configured; one developer, and self-approval through a second account would be theatre. In the register, due 4 Nov |
| SR-4.3.6 | ✅ | Dependency pinning, no floating tags | `uv.lock` and `package-lock.json` committed; every `FROM` carries a digest, asserted by a CI check in each repository |

## B12. Monitoring and incident response

| ID | | Requirement | How to validate |
|---|---|---|---|
| SR-4.4.1 | ✅ | Application and access logging, ≥ 90 days | `eventsExpiration: 7776000` with admin events and details; append-only audit log in the Cloud; append-only access log on each node; `pgaudit` on the database |
| SR-4.4.2 | ✅ | Alerting on critical events *(recommended)* | Uptime Kuma, deliberately run **off** the Cloud host so it survives that host. T27 exercises it |
| SR-4.4.5 | ✅ | Incident contacts and procedure | `deploy/security/incident-response.md`. **Pending**: §1 is a blank contacts table, and an incomplete §1 means there is no procedure. Walk §4 and §5 once on a test deployment before the validation |

## B13. Containers

| ID | | Requirement | How to validate |
|---|---|---|---|
| SR-5.1.1 | ✅ | Containers run as non-root | `docker compose exec <service> id` for each. Postgres is the one documented exception — its entrypoint needs root for `initdb` and drops to `postgres` via gosu, so check the **running process**, not the Dockerfile |
| SR-5.1.2 | ✅ | Images scanned for CVEs before deployment | As SR-4.2.2 |

## B14. Supply chain

| ID | | Requirement | How to validate |
|---|---|---|---|
| SR-6.1.1 | ✅ | Pinning in lockfiles and image tags | As SR-4.3.6 |
| SR-6.1.2 | ◐ | Documented rationale for new dependencies *(recommended)* | Honoured in the Python repositories. The console's own plan records that the rule "does not survive contact with npm and needs rewording" — an honest note rather than a silent lapse |
| SR-6.1.3 | ✅ | SBOM per release *(recommended)* | Syft produces a CycloneDX SBOM in both Python repositories' CI, retained 90 days. Attached to CI runs rather than to releases |
| SR-6.1.4 | ❌ | Signed commits, protected branches | `git log --show-signature` — history is unsigned. No signing key is configured. In the register, due 4 Nov, with the exact steps to close it |

## B15. Data platform

| ID | | Requirement | How to validate |
|---|---|---|---|
| SR-7.1.1 | ✅ | Data classification policy | `deploy/security/data-classification-policy.md`. The **mechanism** is enforceable: register a `sensitive` resource on a BVR node and it is refused, `422 classification_not_permitted`. **Pending sign-off** |
| SR-7.1.2 | ✅ | Database access logging *(recommended)* | `pgaudit` in `shared_preload_libraries`, extension created per database. Note `pgaudit.log_parameter` is **off**, because parameters can carry secrets |
| SR-7.1.3 | ✅ | Dev/test use synthetic data only | §6 of the classification policy names each environment rather than claiming generally. **Pending signature** |
| SR-7.1.5 | ✅ | Transition checklist before real personal data | `deploy/security/real-data-transition-checklist.md`. **Pending sign-off**, and note it records that one control §9 relies on — host access over the overlay only — is itself still deferred |

---

## Where the detail lives

| | |
|---|---|
| The requirements themselves | `security_requirements.md` |
| Evidence and reasoning per requirement | `compliance-assessment.md` |
| The acceptance cases, step by step | `circuless-cloud/deploy/acceptance/RUN-SHEET.md` |
| Deferrals, with dates and accepted reasoning | `circuless-cloud/SECURITY-DEFERRALS.md` |
| Policies written for the audit | `circuless-cloud/deploy/security/` |
| Symptom-first troubleshooting | `circuless-cloud/deploy/TROUBLESHOOTING.md` |
