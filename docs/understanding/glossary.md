# CIRCULess core platform — Glossary

**Version:** 1.0 · 24 Sep 2026 · **Audience:** CIRCULess partners
Terms as used in the CIRCULess core platform documentation, user interfaces and APIs. A term in *italics* inside a definition is itself defined in this glossary. Acronyms are listed at the end.

---

## 1. The platform

**CIRCULess core platform**
The *CIRCULess Cloud* and the *CIRCULess Nodes* together. It lets organisations publish data and services, find one another's, agree access, and exchange them, with every access decided by the provider's own node and recorded. Built and operated by Bavenir (BVR) in WP2.

**CIRCULess waste management platform**
The *core platform* together with every *service* integrated into it. Called "CIRCULess DWMP" in D1.1.

**CIRCULess Cloud**
The central part of the core platform, operated by BVR: the *identity provider*, the *catalogue*, *agreements*, the organisation and node registries, the *public gateway*, and control of the *overlay network*. It holds identities, metadata and agreements — not the data being exchanged.

**CIRCULess Node** (node)
A small application that holds an organisation's *datasets*, fronts its *services*, and makes the *access decision* for every request to them, locally. A node can run in the Cloud or on an organisation's own premises, and can host several *tenants*.

**BVR-operated node**
A node run by BVR on its own infrastructure. It stores only *non-sensitive* data and refuses data *classified* as *sensitive*.

**Partner-operated node** (on-premises node)
A node run by an organisation on its own premises. The organisation is responsible for the host it runs on — see *shared responsibility*.

**Tenant**
An organisation's own space on a node: its assets, service credentials and audit log, kept separate from the other tenants on the same node.

**Cloud API**
The API of the CIRCULess Cloud: catalogue search, access requests and agreements, and the organisation and node registries.

**Catalogue**
The searchable collection of *metadata records* of the assets published by all nodes. It holds descriptions, never the data itself. Signing in is required.

**Public gateway**
The entry point for users whose computer is not on the *overlay network* — typically someone using a browser. It forwards requests to the right node unchanged and never makes access decisions.

**Overlay network**
A private, encrypted network connecting the nodes and the Cloud, based on WireGuard and managed with NetBird. A node joins it by connecting outwards, so no inbound firewall ports need to be opened at a partner's site.

**Cloud admin UI**
The web interface for searching the catalogue, requesting access, approving requests and downloading data.

**Node admin UI**
The web interface for managing a node and the assets of its tenants.

**Platform operator**
A BVR staff member who administers the core platform. Platform operators must use *MFA*.

---

## 2. Organisations, users and identity

**Organisation**
A participating partner — a company, research institute or public body. An organisation owns its *assets* and is a party to *agreements*.

**Organisation admin**
A member authorised to act for their organisation: approving *access requests* to its assets, registering assets and managing *service credentials*. Admin rights apply only to one's own organisation.

**Member**
A user belonging to an organisation. A user can belong to more than one.

**User**
A person with an account on the platform.

**Principal**
Anything that can authenticate to the platform: a *user*, a *service client* or a *node*.

**Service client** (machine client)
The identity that an organisation's automated pipeline or service uses to call the platform. It belongs to exactly one organisation.

**Node identity**
The identity a node uses to talk to the Cloud — to publish its metadata and receive agreements. A node identity can never be used to access data or services.

**Identity provider**
The system that authenticates principals and issues their tokens: a dedicated Keycloak instance for CIRCULess.

**Access token**
A short-lived, signed token (JWT) presented with every request. It is valid for five minutes and for one node only — see *audience*.

**Audience**
The single node, or the Cloud API, that an access token is valid for. A token issued for one node is refused by every other.

**Acting on behalf of a user**
A service such as Workflows exchanges a user's token for one valid at a node, so the access is recorded as the user's own, with the service as the *actor*. Also called token exchange.

**Actor**
The service that made a request on a user's behalf. Recorded in the *audit log* next to the user.

**Acting organisation**
The organisation on whose behalf a request is made. It matters when a user belongs to several organisations, and is recorded in the audit log.

**MFA** (multi-factor authentication)
A second factor at sign-in, such as a one-time code. Mandatory for platform operators; available for any organisation's users on request.

**Signed client assertion**
How service clients and nodes authenticate: they sign with a private key that never leaves their machine, and the platform holds only the matching public key, as an X.509 certificate. No shared passwords or secrets are exchanged. Technical name: `private_key_jwt`.

---

## 3. Assets and data

**Asset** (resource)
Anything an organisation publishes on a node: a *dataset* or a *service*.

**Dataset**
Data offered as a single file, or as a *bucket* of files.

**Bucket**
A dataset made of several files, such as a batch. It comes with a *manifest*.

**Manifest**
The list of the files in a bucket, with their sizes, checksums and types.

**Metadata record**
The description of an asset — title, description, publisher, format, licence, value-chain phase and more — in the DCAT-AP standard. It is what the catalogue shows.

**Asset identifier**
A globally unique identifier (UUID) given to every asset. Persistent identifiers that survive moving an asset to another node follow in the final version.

**Value-chain phase**
The category an asset belongs to: *material characterisation*, *processing*, *product development* or *value chain*. The catalogue can be filtered by it.

**Licence**
The terms under which an asset may be used, chosen from a controlled list. Required before an asset can be published to the catalogue.

**Discoverability**
Who can see an asset's metadata:

| Level | Who sees the metadata |
|---|---|
| hidden | the owning organisation only |
| catalogue | any signed-in user or service |

A level visible without signing in is reserved for later; in the beta, all catalogue access requires signing in. New assets start as *hidden*.

**Visibility**
Who can read an asset's data or call its service:

| Level | Who can use it |
|---|---|
| private | the owning organisation's admins |
| org | any member or service client of the owning organisation |
| agreement | the owning organisation, plus organisations with an accepted *agreement* |
| public | any signed-in user or service |

New assets start as *org*.

**Classification**
The owner's statement of how sensitive a dataset is: *synthetic*, *non-sensitive* or *sensitive*. Set at registration.

**Sensitive data**
Confidential business data, or personal data inside an asset. It stays on the owner's own node; BVR-operated nodes refuse it.

**Upload** (ingestion)
Putting data into a dataset through the node's API — by a person, an organisation's pipeline or an adapter service.

**Two-stage deletion**
Deleting an asset or an account: it is withdrawn at once — no longer visible, no longer usable — and purged after the *retention period*. Audit records are kept.

**Retention period**
How long deleted items and audit records are kept before they are purged: at least 90 days.

---

## 4. Access and agreements

**Access request**
A request by one organisation to use an asset of another.

**Agreement**
The recorded permission for a *consumer organisation* to use one or more assets of a *provider organisation*, for given *actions*, within a time window. Its status is one of: requested, offered, accepted, rejected, revoked, expired.

**Provider organisation**
The organisation that owns the asset. Its admins approve or reject access requests.

**Consumer organisation**
The organisation that uses the asset under an agreement.

**Offer**
An agreement proposed by the provider organisation, which the consumer organisation's admin accepts.

**Revocation**
Ending an agreement before it expires. It takes effect within about 30 seconds, plus at most the five-minute lifetime of tokens already issued.

**Action**
What an agreement permits: *read* (download data) or *invoke* (call a service).

**Usage policy**
The rules attached to an agreement, expressed in a CIRCULess profile of ODRL 2.2. Permissions and time limits are enforced by the node; duties are recorded and shown to both parties.

**Access decision**
The yes-or-no decision on a request. Made by the node that holds the asset, for every request, locally, without contacting the Cloud.

**Audit log**
An append-only record of every access and management decision, allowed or denied. Each node keeps one per tenant; the Cloud API and the identity provider keep their own.

---

## 5. Integrating services

**Service** (CIRCULess service)
An external application, owned by an organisation, that offers functionality through an API — for example Workflows, the Knowledge Base, the Digital Product Passport, quality prediction, the logistics optimiser or BIM visualisation. Services are integrated into the platform; they are not part of the core platform.

**Provider face**
How a service offers its functionality: registered as an asset in its owner's tenant on a node, and reachable only through that node.

**Consumer face**
How a service uses the platform: as a *service client* of its organisation, needing agreements like any organisation — or *acting on behalf of a user*.

**Invocation**
Calling a service through a node. The node checks access, adds the *service credential*, forwards the request to the *upstream service* and returns the response.

**Upstream service**
The service's own API, behind the node.

**Service credential**
The secret — for example an API key — that a node uses to call an upstream service for a tenant. Stored encrypted on the node and never visible to callers.

**Invoke policy**
The service owner's declaration of how the service should be called: timeouts, synchronous or submit-and-poll, streaming, which methods may be retried, maximum request size.

**Service contract**
What a service must provide to be integrated: an HTTP API, an OpenAPI description, a credential the node can hold, an invoke policy, and accepting traffic only from its node. No CIRCULess-specific code is needed on the service side.

**OpenAPI description**
A machine-readable description of an API. Required for every service, and published with its metadata record.

---

## 6. Security and operations

**Every hop encrypted**
The platform's statement on encryption in transit: TLS with certificates from a public certificate authority on every publicly reachable endpoint, and WireGuard on the overlay network.

**Shared responsibility**
BVR is responsible for the platform software, the Cloud and BVR-operated nodes. An organisation running its own node is responsible for the host it runs on — operating system updates, disk protection, physical security and local firewall.

**Degraded mode**
When the Cloud is unreachable, nodes keep deciding access from their cached agreements. New tokens cannot be issued while the identity provider is down, so after at most five minutes new requests stop until it recovers.

**Node kill switch**
Cutting a node off the platform by disabling its node identity and removing it from the overlay network.

**Security validation**
The verification of the security requirements after the core platform is implemented, before the T2.7 audit.

**TRL 5**
Technology Readiness Level 5: technology validated in a relevant environment. The level the beta platform is validated at.

---

## 7. Acronyms

| Acronym | Meaning |
|---|---|
| API | Application Programming Interface |
| BIM | Building Information Modelling |
| BVR | Bavenir |
| DCAT-AP | Data Catalogue Vocabulary — Application Profile for data portals in Europe |
| DoA | Description of the Action |
| DPP | Digital Product Passport |
| DSP | Dataspace Protocol |
| DWMP | Digital Waste Management Platform (D1.1's name for the CIRCULess waste management platform) |
| GDPR | General Data Protection Regulation |
| IFC | Industry Foundation Classes (OpenBIM data model) |
| JWT | JSON Web Token |
| KB | Knowledge Base |
| MCP | Model Context Protocol |
| MFA | Multi-factor authentication |
| mTLS | Mutual TLS |
| ODRL | Open Digital Rights Language |
| OIDC | OpenID Connect |
| PKCE | Proof Key for Code Exchange |
| RBAC | Role-based access control |
| SSE | Server-Sent Events |
| TLS | Transport Layer Security |
| TRL | Technology Readiness Level |
| UUID | Universally Unique Identifier |
| WP | Work Package |
