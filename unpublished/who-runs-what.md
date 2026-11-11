# Who runs what

The question most organisations ask first, and the one that decides what you can safely
put on the platform.

## The choice

Your data sits on a node. There are two kinds, and the difference is who owns the machine.

| | **Your own node** | **A node Bavenir operates** |
|---|---|---|
| Who owns the machine | You | Bavenir |
| What it may hold | Whatever you decide, including sensitive data | **Non-sensitive data only.** Sensitive is refused outright |
| Who protects the disk | You | Bavenir — but see [what it does not do](what-it-does-not-do.md), because at this stage the platform does not encrypt data at rest |
| Inbound firewall ports | **None.** It connects outwards | n/a |
| Who keeps it running | You | Bavenir |
| Effort for you | A container, an outbound connection, and someone to keep it updated | Almost none |

**Why a Bavenir-operated node refuses sensitive data.** Not because it is less secure —
today it is the better-run of the two. It is that Bavenir holding a partner's sensitive
data on their behalf is an arrangement this project undertook not to make. The refusal is
enforced by the software, not by a policy document: a dataset marked sensitive is
rejected when you try to register it.

## Who is responsible for what

| Bavenir | You |
|---|---|
| The node software, its updates, and release notes | The machine your node runs on: operating-system updates, disk encryption, physical security, local firewall |
| The Cloud — identity, catalogue, agreements, the private network | Running the node as its own unprivileged user |
| Nodes Bavenir operates, and the data on them | Protecting your node's private key and its data directory |
| Coordinating an incident, and cutting a node off if one is needed | **Classifying your data correctly** |
| | Keeping the node reasonably up to date |

The one in bold is the one that matters most and is easiest to skip. Classification is
**self-declared** — nothing inspects your files. A dataset you mark non-sensitive will be
accepted as non-sensitive. See [what it does not do](what-it-does-not-do.md).

## Who is responsible under data protection law

| | |
|---|---|
| **Your data, on any node** | You. You decide what to publish, to whom, and for how long. Bavenir processes it on your behalf |
| **User accounts** | Whoever operates the deployment — Bavenir, for the one Bavenir runs. Names and email addresses exist only there |
| **The records of who did what** | Shared. They identify people only by an opaque identifier, not by name |

Everything outside the identity provider is **pseudonymous**. The record of who approved
an agreement, or who read a dataset, holds an opaque identifier — no name, no email
address, nothing that resolves to a person without going back to the identity provider.
That is deliberate, and it is why those records can be kept as long as they need to be.

## What Bavenir can and cannot see

**Can see:** everything in the catalogue, because it is the catalogue. Every agreement
and every change to one. That a particular opaque identifier read a particular resource.
Which organisations are hosted on which node.

**Cannot see:** the contents of any dataset on a node Bavenir does not operate. There is
no path for it — the data is never sent to the Cloud, and a platform operator has no
privileged route into a node. An application acting for Bavenir gets exactly what
Bavenir's own agreements allow, and nothing more.

**On a node Bavenir operates**, Bavenir has the machine, and therefore the data on it.
That is the honest statement, and it is the reason such a node takes non-sensitive data
only.

## If you run your own node

What your IT department needs to know, in full:

- **No inbound ports.** The node makes outbound connections to the private network and
  to the Cloud. Nothing has to be opened.
- It runs as a container, as an unprivileged user.
- It holds two keys that are never backed up by Bavenir by design: its identity key and
  the key protecting any credentials it stores for your own services. **Backing those up
  is yours**, and losing the second means re-entering those credentials.
- It needs to reach the Cloud to stay current on agreements. If it cannot, it keeps
  enforcing what it last knew and reports that it is out of date.

---

Next: [what it does not do](what-it-does-not-do.md) — the limits, stated plainly.
