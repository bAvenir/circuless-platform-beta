# What it does not do

CIRCULess is at **technology readiness level 5** — demonstrated in a relevant
environment, not a product. Some things a production system would have are deliberately
not built. They are listed here rather than left to be discovered.

Read this before deciding what to put on the platform. It is the chapter that prevents
the expensive misunderstandings.

## The big one: data is not encrypted at rest

**The platform does not encrypt stored data.** Not datasets on a node, not the
catalogue, not the agreement records.

What *is* protected: backups are encrypted, passwords are hashed, credentials your node
holds for your own systems are encrypted, private keys are readable only by the account
that uses them, and databases are not reachable from outside their host.

This was a decision, not an oversight, and it rests on one condition: **Bavenir's
infrastructure holds only non-sensitive data.** Sensitive data stays on your own node,
where protecting the disk is yours to do — and a node Bavenir operates refuses sensitive
data outright.

**It stops being acceptable the moment that condition changes.** If sensitive data, or
personal data beyond user accounts, is to go on Bavenir's infrastructure, encryption at
rest becomes mandatory again, together with a list of other controls. There is a written
gate for exactly that, and it has to be worked through first.

## Classification is self-declared

The platform asks you to mark every dataset as *synthetic*, *non-sensitive* or
*sensitive*, and it enforces where each may live. What it does not do is **check**.
Nothing inspects your files. A dataset marked non-sensitive will be accepted as
non-sensitive, stored unencrypted, and described in the catalogue as non-sensitive.

Three things reduce the risk and none remove it: only your own administrators can
register your data, so the person declaring the class is accountable; new data is private
until you deliberately share it; and every registration is recorded.

**If you are unsure, classify up.** Over-classifying costs you a refused upload.
Under-classifying costs the thing the rule exists to prevent.

## The rest

| | What that means for you |
|---|---|
| **Usage policies are recorded, not enforced** | An agreement can say "for this project only". The platform shows that to both parties and records it. It does not technically prevent other use once data has been read |
| **Identifiers are not permanent** | A dataset's identifier is stable while it exists, but there is no guarantee of a citable, permanently resolvable identifier. Do not use them in publications |
| **Tenants on a shared node are separated logically** | By the software, not by separate machines. Sound, and not the same as physical isolation. An organisation needing that should run its own node |
| **Machine certificates are self-signed** | The certificates nodes and applications use to identify themselves are issued by the platform, not a public authority. Public endpoints use ordinary public certificates |
| **Private-network endpoints rely on the network** | Traffic inside the private network is encrypted by the network itself rather than by a second layer on top |
| **No breached-password check** | Passwords must be at least twelve characters and are locked out after five failed attempts, but are not checked against known-breached lists |
| **No Kubernetes** | So none of the isolation a Kubernetes cluster would give. Services are separated by container networks instead |

## Not finished yet

Distinct from the list above: these are planned and not done, rather than decided
against. All are due before the security validation in November.

| | |
|---|---|
| Two-factor authentication for platform operators | Decided, not yet switched on |
| Administrative access restricted to the private network | Administrative interfaces are reachable from the internet today, behind a login |
| Rate limiting on sign-in | Repeated failed sign-ins lock an account temporarily, which covers attacks on one account. Volume across many accounts is not yet limited |
| A published privacy notice | Not yet written |

[How your data is protected](security-measures.md) carries the full list with dates and
the reasoning for each.

## What this is not a disclaimer about

Everything above is a boundary of the beta. None of it is a gap in the things the
platform exists to do:

- every request for data is decided by the provider's own node, at the moment it is
  made;
- nothing is readable without an agreement, and revoking one stops access within about
  half a minute;
- nothing is reachable without signing in;
- every access and every change to an agreement is recorded, and the records cannot be
  edited or deleted.

Those are tested, not asserted.

---

Next: [how your data is protected](security-measures.md), or the
[glossary](glossary.md).
