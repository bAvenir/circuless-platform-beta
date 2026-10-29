# Integration requirements

What a service has to meet to be integrated into CIRCULess. The
[integration guide](the-guide.md) explains how the platform works and why; this page is
the shorter, flatter list of **obligations**, so that a partner and Bavenir can agree
item by item what is and is not in place.

## How to read it

**must** is required. **should** is recommended: not meeting it is acceptable, and worth
a sentence saying why. The words follow RFC 2119.

Requirements fall into three groups and some apply only in certain cases:

| | |
|---|---|
| **Prerequisites** | True before integration starts — the host, the service, what you deliver |
| **The API contract** | What the service's code does. Organised in **tiers**: tier 0 applies to every service, tier 1 only to services that read the caller's identity, tier 2 throughout as recommendations |
| **Ongoing** | What continues after go-live |

The identifiers — `P1`, `C1`, `O1` — are this page's own, so that a conversation can
name an item. They are not part of the project's requirement numbering.

---

# 1 · Prerequisites

## 1.1 The host that runs the node

Bavenir has a legitimate interest in this host, because the node running on it holds key
material and makes access decisions about other organisations' data.

| | | |
|---|---|---|
| **P1** | The host **must** run Docker Engine and Compose. Linux and macOS are both known to work; nothing in the node depends on a particular operating system | must |
| **P2** | The host **must** need no inbound ports for CIRCULess. The node and the overlay client both connect outwards | must |
| **P3** | A host firewall **must** be enabled | must |
| **P4** | Automatic security updates for the operating system **must** be enabled | must |
| **P5** | Containers **must not** run privileged, and the Docker socket **must not** be mounted into any container | must |
| **P6** | Sizing — CPU, memory and disk — is agreed per deployment and depends on the service alongside the node | *to agree* |
| **P7** | The node image **must** be the one Bavenir publishes, pinned by digest, with its signature verified before it is started | must |
| **P8** | The node's keypair **must** be generated on this host at first start. Only the certificate — the public half — is sent to Bavenir | must |
| **P9** | The private key **must not** leave the host, and the partner **must** back it up separately. It is excluded from every platform backup by design | must |

## 1.2 The service

| | | |
|---|---|---|
| **P10** | The service **must** expose an HTTP API that the node can reach at a stable address | must |
| **P11** | The service **must** have an OpenAPI 3 document that matches what actually runs | must |
| **P12** | The service **should** have a health endpoint and one consistent error format | should |
| **P13** | The service image **should** be signed (Cosign), scanned (Trivy or Grype), and published with an SBOM (Syft) | should |
| **P14** | Every address the service calls outside its host **should** be declared | should |

**P11 is the one that is easy to under-deliver.** A document that once matched is not an
OpenAPI document; it is a description of a previous release. It is what a consumer reads
before deciding to request access, and what the catalogue entry points at.

## 1.3 If the service runs in the node's own Compose stack

These attach to that stack, because it is the stack the node lives in. A service hosted
elsewhere is on the partner's own host, where these become recommendations rather than
requirements.

| | | |
|---|---|---|
| **P15** | The image **must** be pinned by digest, run as a non-root user, and be built for the host's CPU architecture | must *(should, elsewhere)* |
| **P16** | The service **must** declare a healthcheck, CPU and memory limits, and a restart policy | must *(should, elsewhere)* |
| **P17** | Configuration and secrets **must** come from an environment file or Docker secrets — never from the Compose file, and never from git | must *(should, elsewhere)* |
| **P18** | The service **should** log to standard output | should |

## 1.4 Where the service runs is the partner's choice

CIRCULess does not require any particular arrangement. All of these work:

- in the node's Compose stack, on a private network shared with the node;
- on another host the node can reach;
- on the overlay network.

**The only hard requirement is P10** — the node can reach it.

!!! info "Security beyond the node is the partner's"
    CIRCULess governs the path **through the node**: it authenticates the caller, checks
    the agreement, records the call, and attaches your credential. A service may also
    have its own users, its own front door and its own clients, and protecting those is
    the partner's own responsibility. The platform neither requires nor assumes that the
    node is the only way in.

    One obligation follows from that, and it is **C12**.

---

# 2 · The API contract

## 2.1 Tier 0 — every service

| | | |
|---|---|---|
| **C1** | The service **must** validate the node's credential on the path the node uses | must |
| **C2** | The service **must not** treat an unauthenticated caller as a CIRCULess caller | must |
| **C3** | The service **must not** authenticate the end user itself. The platform has already done it, and the service does not have the information to do it correctly | must |
| **C4** | The service **must not** hold any credential for the node | must |
| **C5** | The service **must not** call back into the node to fetch data. The caller sends the bytes in the request body | must |
| **C6** | The service **must** answer within the configured timeout, or return `202` with a `Location` and let the caller poll | must |
| **C7** | The service **must** accept a bounded request body — 10 MiB by default, configurable per service | must |
| **C8** | A `Location` header **must** be a relative path that resolves inside the registered endpoint | must |
| **C9** | The service **must not** log its credential | must |
| **C10** | The service **should** be safe to call again. The node never retries, and forwards `Idempotency-Key` if the caller sends one | should |

**C4 and C5 together are what keep the agreement meaningful.** A service that could fetch
from the node would be reading on its own authority rather than the caller's — and a
caller with no agreement could ask it to fetch something the service happens to be
allowed to see.

**C8 is mandatory rather than advisory** because the node refuses a redirect pointing
outside the registered endpoint: following it would take the caller out from behind the
node, away from the decision and the log. A service that emits `/jobs/7` instead of
`jobs/7` is not merely untidy; it is broken. Registering the endpoint at the root of the
service is the other way to get this right.

## 2.2 Tier 1 — services that read the caller's identity

Only if the service reads the `X-CIRCULess-*` headers. A service that ignores them —
tier 0 — has nothing here to meet.

| | | |
|---|---|---|
| **C11** | The service **must** verify the node's credential before acting on any `X-CIRCULess-*` header | must |
| **C12** | The service **must** be able to tell that a request came from the node, and **must** ignore those headers otherwise | must |
| **C13** | `X-CIRCULess-Subject` **must** be treated as a pseudonymous identifier. The service **must not** attempt to resolve it to a named person | must |

**C12 is the one to design for.** The headers are the node's word about who is calling.
On a request that did not come from the node they mean nothing — and because the node is
not required to be the only way in (§1.4), anyone who can reach the service and holds the
credential could otherwise claim to be anyone.

How the service tells is the partner's choice: a network only the node is on, a distinct
credential on the node's path, client certificates. What matters is that it can tell.

**On C13:** tokens issued for nodes carry no name and no email, so there is nothing for
the node to pass on. A service that needs a display name must obtain it by another
route, with the person's knowledge.

## 2.3 Tier 2 — recommended throughout

| | | |
|---|---|---|
| **C14** | The service **should** log `X-CIRCULess-Request-Id` on every request, so one call can be traced across both logs | should |
| **C15** | The service **should** set `Retry-After` on a `202`. Every poll is a separate authorization decision and a separate log entry | should |
| **C16** | The service **should not** log request bodies that may carry another organisation's data | should |

## 2.4 Streaming

Only if the resource is registered as streaming.

| | | |
|---|---|---|
| **C17** | The service **must** stream without buffering, so the first event reaches the caller before the stream ends | must |
| **C18** | The service **should** honour `Last-Event-ID` so a caller can resume | should |

---

# 3 · Ongoing

| | | |
|---|---|---|
| **O1** | The OpenAPI document **must** continue to match what runs, release to release | must |
| **O2** | The endpoint **must** stay stable, and the partner **must** tell the node operator before changing it | must |
| **O3** | The partner **must** apply node updates. Bavenir announces them; applying them is the partner's | must |
| **O4** | The service **should** be scanned for vulnerabilities before every release, with critical findings fixed first | should |
| **O5** | API changes **should** be announced in advance | should |
| **O6** | The service **should** support rotation of its credential when asked | should |
| **O7** | The service **must not** retain data received from a caller beyond what the call needs | must |
| **O8** | The service **should** declare, at registration, what it stores and for how long | should |
| **O9** | Anything the service writes back to a node **must** be classified correctly | must |

**O7 is the strongest obligation here.** A service receives another organisation's data
in a request body. Keeping it turns a call made under one agreement into a copy that
outlives the agreement — the thing the platform exists to prevent.

**Log retention for the service's own logs is the partner's**, to set and to honour
according to their own policy. CIRCULess does not require a period.

---

## What the node does, so the service does not have to

For completeness, because several requirements above are shaped by it:

| The node | |
|---|---|
| **Strips** | `Authorization`, `Cookie`, `Host`, hop-by-hop headers, and **any inbound `X-CIRCULess-*`** |
| **Forwards** | `Content-Type`, `Accept`, `Content-Length`, `Idempotency-Key`; for streaming also `Mcp-Session-Id`, `Mcp-Protocol-Version`, `Last-Event-ID` |
| **Adds** | The upstream credential, and `X-CIRCULess-Subject`, `-Org`, `-Resource`, `-Request-Id`, `-Actor` |
| **Decides** | The agreement check, on every request, before the service is called at all |
| **Records** | Who called, for which organisation, which resource, the decision and the bytes |

A caller cannot fake an identity header: inbound ones are removed before the service sees
them. That protection applies to requests **through the node** — which is what C12 is
about.
