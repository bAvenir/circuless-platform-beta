# Security requirements — TRL 5 (mandatory and recommended)

**Source:** `security_requirements.txt` — the TRL 5 adaptation of the T2.7 security requirements.
**Filter:** only items with TRL 5 status **MANDATORY** or **RECOMMENDED** are kept. Deferred and not-applicable items are omitted. Text is as in the source, lightly cleaned; nothing is reworded in substance.
**IDs:** as in the source, prefixed `SR-` so they cannot be confused with WP1's FR/NFR identifiers.
**Review, conflicts and validation plan:** `security_requirements_review.md`.

**58 requirements in TRL 5 scope: 43 mandatory, 15 recommended.**

**No Kubernetes at TRL 5** (J, 24 Sep 2026). The two Kubernetes-specific items, SR-5.1.3 and SR-5.1.4, are moved to §8 *Post-project recommendations*.

**No encryption at rest of non-sensitive data at TRL 5** (J, 24 Sep 2026). SR-2.1.1 and SR-2.1.2 are moved to §9 *Deferred by decision*, with the condition that makes them mandatory again.

---

## 1. Authentication and access control

### 1.1 Authentication

| ID | Requirement | Standard | Risk | Status | Rationale / tool |
|---|---|---|---|---|---|
| SR-1.1.1 | Strong password policy: minimum 12 characters, complexity required. No forced rotation; breached-password check recommended | NIST 800-63B | High | **MANDATORY** | Keycloak policy configuration — trivial to set; protects even trusted-user environments |
| SR-1.1.2 | MFA for all user accounts | GDPR Art. 32 / NIS2 | Critical | RECOMMENDED | Synthetic data and trusted users make this optional at TRL 5, but cheap to enable in Keycloak. Becomes mandatory at TRL 7+ |
| SR-1.1.3 | Account lockout after 5 failed login attempts | OWASP ASVS | High | **MANDATORY** | Single Keycloak setting. Cloud-hosted exposure makes brute force a real risk even for internal tools |
| SR-1.1.4 | OAuth 2.0 / OIDC with authorization code flow; implicit flow disabled | OAuth 2.0 BCP | Critical | **MANDATORY** | Keycloak default. Costs nothing and is foundational for TRL 7+ |
| SR-1.1.5 | Session timeout: 30 min inactivity, 12 h absolute | GDPR Art. 32 | Medium | RECOMMENDED | Relaxed timeout acceptable for trusted consortium users; avoids friction during research sessions |
| SR-1.1.6 | Secure password reset requiring an email token (MFA not required at TRL 5) | OWASP ASVS | Medium | **MANDATORY** | Email-token reset sufficient at this stage |
| SR-1.1.7 | Rate limiting on the login endpoint to prevent automated attacks | OWASP Top 10 | Medium | **MANDATORY** | Cloud exposure makes this non-negotiable. Reverse-proxy rate-limit configuration |

### 1.2 Authorization and access control

| ID | Requirement | Standard | Risk | Status | Rationale / tool |
|---|---|---|---|---|---|
| SR-1.2.1 | Basic RBAC with at least two roles: Admin and User | NIST RBAC | High | **MANDATORY** | Simplified role set appropriate for a consortium research team. Keycloak roles |
| SR-1.2.2 | Principle of least privilege: users access only what their role requires | ISO 27001 | High | **MANDATORY** | Design discipline — enforce from day one to avoid rework at TRL 7+ |
| SR-1.2.3 | API endpoints require a valid authentication token on every request | OWASP API | Critical | **MANDATORY** | No open or unauthenticated endpoints on a cloud-hosted platform, even for synthetic data |
| SR-1.2.4 | Admin functions restricted to the admin role only | CIS Controls | High | **MANDATORY** | Trivial RBAC enforcement; prevents accidental misconfiguration |

---

## 2. Data storage and encryption

### 2.1 Encryption at rest

Deferred by decision for TRL 5 — see §9.

### 2.2 Encryption in transit

| ID | Requirement | Standard | Risk | Status | Rationale / tool |
|---|---|---|---|---|---|
| SR-2.2.1 | TLS 1.2 minimum (TLS 1.3 preferred) for all external-facing endpoints | NIST 800-52 | Critical | **MANDATORY** | Let's Encrypt + cert-manager — automated, zero cost |
| SR-2.2.2 | Weak cipher suites disabled (DES, RC4, MD5, TLS 1.0/1.1) | OWASP TLS | Critical | **MANDATORY** | Mozilla SSL Configuration Generator |
| SR-2.2.3 | HTTPS enforced via HSTS header (max-age ≥ 6 months) | OWASP | High | **MANDATORY** | Single HTTP header. HTTP-only is unacceptable on a cloud host |
| SR-2.2.4 | Valid TLS certificate from a trusted CA — no self-signed certificates on accessible endpoints | CA/Browser Forum | High | **MANDATORY** | Let's Encrypt automates this completely |

### 2.3 Backup and retention

| ID | Requirement | Standard | Risk | Status | Rationale / tool |
|---|---|---|---|---|---|
| SR-2.3.1 | Regular backups of platform state and configuration (weekly minimum) | ISO 27001 | Medium | RECOMMENDED | Restic or provider snapshots — low effort |
| SR-2.3.2 | Backup data encrypted (at minimum via provider volume encryption) | GDPR Art. 32 | Medium | RECOMMENDED | Provider-managed encryption acceptable for TRL 5 backups of synthetic data |

### 2.4 GDPR data subject rights

| ID | Requirement | Standard | Risk | Status | Rationale / tool |
|---|---|---|---|---|---|
| SR-2.4.1 | Right to access, rectification, erasure and portability implemented | GDPR Art. 15–20 | High | **MANDATORY** | For personal data |
| SR-2.4.2 | Cookie consent banner, privacy policy, DPIA | GDPR / ePrivacy | High | RECOMMENDED | Recommended for closed consortium access with no personal data. Required before any public-facing deployment |
| SR-2.4.3 | Data residency: EU/EEA storage for personal data | GDPR Art. 44 | Critical | **MANDATORY** | EU servers will be used |

---

## 3. API functionality and interoperability

### 3.1 API design and documentation

| ID | Requirement | Standard | Risk | Status | Rationale / tool |
|---|---|---|---|---|---|
| SR-3.1.1 | RESTful API following HTTP standards — correct verbs, status codes, no sensitive data in URLs | REST BCP | Medium | **MANDATORY** | Design discipline — costs nothing to do correctly from the start |
| SR-3.1.2 | Basic API documentation (OpenAPI 3.0 / Swagger) for all endpoints | OpenAPI 3.0 | Medium | RECOMMENDED | Essential for partner integration; generated from annotations |
| SR-3.1.3 | API versioning (`/v1/`) in place from the first release | API BCP | Medium | **MANDATORY** | Painful to retrofit; a routing prefix from day one |
| SR-3.1.4 | Error responses use standard codes — no stack traces or internal paths exposed | OWASP API | High | **MANDATORY** | Information-leakage risk; framework-level error handler |

### 3.2 API authentication and security

| ID | Requirement | Standard | Risk | Status | Rationale / tool |
|---|---|---|---|---|---|
| SR-3.2.1 | All API endpoints require a valid JWT / OAuth 2.0 bearer token | OAuth 2.0 / OWASP | Critical | **MANDATORY** | No anonymous endpoints on a cloud-hosted platform, regardless of data type |
| SR-3.2.2 | Bearer tokens expire after at most 8 hours; refresh tokens after at most 7 days | OAuth 2.0 BCP | Medium | **MANDATORY** | Relaxed expiry acceptable for trusted research users; tighten to 1 h / 30 d at TRL 7+ |
| SR-3.2.3 | Input validation on all API parameters — at minimum type checking and length limits | OWASP | Critical | **MANDATORY** | Injection attacks do not care about TRL. Pydantic or equivalent |
| SR-3.2.4 | CORS configured with an explicit origin allowlist — no wildcard in production | OWASP CORS | High | **MANDATORY** | Known set of partner domains |
| SR-3.2.5 | API responses use UUIDs, not sequential integer IDs (prevents BOLA / IDOR) | OWASP API Top 10 | Medium | RECOMMENDED | Cheap now; expensive to change later |
| SR-3.2.6 | Rate limiting on all public-facing API endpoints | API rate limiting | High | **MANDATORY** | Internet-accessible means scraped and probed |

### 3.3 Performance and interoperability

| ID | Requirement | Standard | Risk | Status | Rationale / tool |
|---|---|---|---|---|---|
| SR-3.3.1 | Basic API response-time monitoring — no formal SLA at TRL 5 | DevOps BCP | Low | RECOMMENDED | Prometheus + Grafana |
| SR-3.3.2 | Integration with BIM systems tested with realistic synthetic data | ISO 19650 | High | **MANDATORY** | Core TRL 5 validation objective — must demonstrate relevant-environment integration |
| SR-3.3.3 | DPP API endpoints stubbed or prototyped — operational compliance not required | EU DPP | Medium | RECOMMENDED | Regulation still maturing; prototype the interface |

---

## 4. Cybersecurity measures

### 4.1 Network and perimeter security

| ID | Requirement | Standard | Risk | Status | Rationale / tool |
|---|---|---|---|---|---|
| SR-4.1.1 | Firewall rules: only necessary ports open (443; 22 via VPN only) | CIS Controls | Critical | **MANDATORY** | Provider security groups — minutes to configure |
| SR-4.1.2 | SSH restricted: key-based authentication only, password SSH disabled, port changed or restricted by IP | CIS Controls | Critical | **MANDATORY** | The most common cloud-server compromise vector |
| SR-4.1.3 | VPN or IP allowlist required for administrative / infrastructure access | NIS2 | High | **MANDATORY** | WireGuard; partner IPs as fallback allowlist |
| SR-4.1.5 | DDoS protection service enabled | ENISA | Medium | RECOMMENDED | Free-tier DDoS mitigation available |

### 4.2 Vulnerability management

| ID | Requirement | Standard | Risk | Status | Rationale / tool |
|---|---|---|---|---|---|
| SR-4.2.1 | Dependency scanning in CI/CD — critical CVEs block deployment | OWASP | High | **MANDATORY** | Trivy or Grype |
| SR-4.2.2 | Container image scanning before deployment | CIS Docker | High | **MANDATORY** | Trivy image scan in CI/CD |
| SR-4.2.3 | OS and system packages kept up to date — unattended security upgrades enabled | CIS Controls | High | **MANDATORY** | `unattended-upgrades` |

### 4.3 Secure development lifecycle

| ID | Requirement | Standard | Risk | Status | Rationale / tool |
|---|---|---|---|---|---|
| SR-4.3.1 | No hardcoded secrets in code or configuration — secrets via environment variables or a vault | CIS Controls | Critical | **MANDATORY** | Gitleaks pre-commit hook |
| SR-4.3.2 | Secrets scanning in CI/CD (Gitleaks / TruffleHog) | OWASP DevSecOps | Critical | **MANDATORY** | Free, 15-minute CI integration |
| SR-4.3.3 | SAST in CI/CD (Semgrep / Bandit) | DevSecOps | High | RECOMMENDED | Catches injection and common CWEs early |
| SR-4.3.5 | Protected main branch, required PR reviews, no direct pushes | SLSA Level 2 | Medium | **MANDATORY** | Git branch protection |
| SR-4.3.6 | Dependency version pinning — no floating tags in production | DevSecOps | Medium | **MANDATORY** | Lockfiles, pinned deployment manifests and image tags |

### 4.4 Monitoring and incident response

| ID | Requirement | Standard | Risk | Status | Rationale / tool |
|---|---|---|---|---|---|
| SR-4.4.1 | Basic application and access logging — logs retained at least 90 days | ISO 27001 | High | **MANDATORY** | Structured logging; 90 days sufficient for incident investigation |
| SR-4.4.2 | Alerting on critical events: server down, auth-failure spikes, OOM / disk full | SRE BCP | Medium | RECOMMENDED | Uptime Kuma or native alerts |
| SR-4.4.5 | Documented incident contact list and basic response procedure | NIS2 | Medium | **MANDATORY** | One page: who to call, how to take the server offline, how to notify partners |

---

## 5. Container and infrastructure security

| ID | Requirement | Standard | Risk | Status | Rationale / tool |
|---|---|---|---|---|---|
| SR-5.1.1 | Containers run as non-root users | CIS Docker | High | **MANDATORY** | Dockerfile `USER` directive |
| SR-5.1.2 | Container images scanned for CVEs before deployment (Trivy) | CIS Docker | High | **MANDATORY** | Same tooling as SR-4.2.2 |

---

## 6. Supply chain security

| ID | Requirement | Standard | Risk | Status | Rationale / tool |
|---|---|---|---|---|---|
| SR-6.1.1 | Dependency pinning in all lockfiles and container image tags | DevSecOps | Medium | **MANDATORY** | Same control as SR-4.3.6 |
| SR-6.1.2 | New OSS dependencies require a brief documented rationale before adoption | CIS Controls | Medium | RECOMMENDED | A PR comment or ticket note |
| SR-6.1.3 | SBOM generated per release | NTIA SBOM | Medium | RECOMMENDED | Syft |
| SR-6.1.4 | Build pipeline integrity: signed commits, protected branches, required PR approvals | SLSA Level 2 | High | **MANDATORY** | Same foundation as SR-4.3.5 |

---

## 7. Data platform controls

| ID | Requirement | Standard | Risk | Status | Rationale / tool |
|---|---|---|---|---|---|
| SR-7.1.1 | Formal data classification policy (even if all current data is class *Synthetic*) | ISO 27001 | Medium | **MANDATORY** | One-page policy; states which controls trigger when real data is introduced |
| SR-7.1.2 | Basic database access logging — who connected and when | GDPR Art. 30 | Medium | RECOMMENDED | PostgreSQL `pgaudit` |
| SR-7.1.3 | Dev/test environments confirmed to use only synthetic data — documented and signed off | GDPR Art. 25 | High | **MANDATORY** | Prevents accidental real-data ingestion |
| SR-7.1.5 | Transition checklist: controls required before introducing real personal data | GDPR / NIS2 | Critical | **MANDATORY** | One-page gate listing every deferred and not-applicable item to resolve before real data enters |

---

## 8. Post-project recommendations — not applicable at TRL 5

Nothing is deployed on Kubernetes at TRL 5. These apply if and when the platform moves to Kubernetes after the project. The isolation SR-5.1.3 would give is still required at TRL 5 and is provided by container networks instead (`security_requirements_review.md`, C14).

| ID | Requirement | Standard | Risk | Source status | Rationale / tool |
|---|---|---|---|---|---|
| SR-5.1.3 | Kubernetes NetworkPolicy with default-deny between namespaces | CIS K8s | High | Recommended | Painful to retrofit; 1–2 hours |
| SR-5.1.4 | Kubernetes RBAC hardened — no wildcard ClusterRole permissions | CIS K8s | High | Mandatory | `kube-bench` automates the check |

---

## 9. Deferred by decision — encryption at rest

**Decision (J, 24 Sep 2026):** at TRL 5, BVR infrastructure stores **only non-sensitive partner data**, and data at rest is not encrypted by the platform. Sensitive data stays on the partner's own node, where at-rest protection is the partner's responsibility. Encryption at rest was not a hard requirement of the audit.

**These become mandatory again as soon as** BVR infrastructure stores sensitive partner data, or personal data beyond user accounts and pseudonymous audit identifiers.

**Compensating controls, which remain mandatory:** secrets and upstream credentials encrypted by the platform; backups encrypted (SR-2.3.2); passwords hashed by Keycloak; private keys readable only by their service user; host access over the overlay only; databases not reachable from outside the host; a classification guard on BVR-operated nodes that refuses data classified as sensitive. Rationale and residual risks: `security_requirements_review.md`, C6.

| ID | Requirement | Standard | Risk | Source status | Rationale / tool |
|---|---|---|---|---|---|
| SR-2.1.1 | Cloud provider volume encryption enabled for all storage (provider-managed keys acceptable at TRL 5) | GDPR Art. 32 | High | Mandatory | Encryption is free — no reason to skip |
| SR-2.1.2 | Object / file storage encryption enabled for uploaded documents | ISO 27001 | Medium | Mandatory | MinIO SSE or cloud-provider native encryption |
