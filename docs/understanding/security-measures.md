# How your data is protected

CIRCULess lets organisations offer each other tools and data without handing over control
of them. This page explains, in ordinary language, how that control is kept.

## The short version

**Nothing is pooled.** There is no central store holding everyone's material. Each
organisation keeps its own and answers requests about it.

**The owner decides, every time.** When someone asks to use your tool or your data, the
answer comes from *your* node, checking *your* agreement, at the moment of the request —
not from a central server, not from the network, and not once at the start of a
relationship.

**Permission is something you can end.** Access is an agreement between two
organisations, with dates on it. You grant it and you end it. Withdrawal reaches your
node in about half a minute.

**Nobody is anonymous.** Every request, including a search of the catalogue, comes from
an identified person or application belonging to a known organisation.

**Everything is written down.** Every use, allowed or refused, is recorded: who, when,
and what. The records cannot be edited or deleted afterwards by anyone, which is what
makes them worth having.

**The most sensitive material never leaves home.** Shared infrastructure holds only
material its owner has marked non-sensitive. Anything marked sensitive stays on the
owner's own machine, and nodes on shared infrastructure refuse it outright.

## What this means in practice

| If you are wondering | What actually happens |
|---|---|
| *Will my data end up in a database I do not control?* | No. What is published centrally is a **description** — what something is, its licence, who to ask. The thing itself stays with you |
| *Can a competitor see what I have?* | Only if you choose to make it discoverable. Seeing that something exists is not permission to use it, and anything new is private until you deliberately change that |
| *What if I change my mind?* | End the agreement; the next request is refused. For a tool this is complete, because the caller only ever received answers. For a file, see the note below |
| *Who can see my model, or my method?* | Nobody. A caller sends a question and receives an answer. They never receive the application itself, nor the credential that opens it |
| *What if the platform operator goes rogue?* | They cannot grant access to your material. That decision is made by your node, from agreements you approved |
| *What if the central service goes down?* | Your node carries on from the agreements it already holds, and carries on refusing what it should refuse |

## One thing to be clear about

**Ending an agreement stops future access. It does not retrieve a file somebody has
already downloaded.**

That is a property of files rather than a shortcoming of this platform: once bytes have
been delivered they are in someone else's hands, and no system can reach in and remove
them. It is the main reason offering a **tool** is usually stronger than offering a file
— a caller who asks a question and receives an answer holds nothing once the agreement
ends.

We would rather state this plainly than have it discovered later.

## The protections behind it

The same measures, without the technical detail:

| | |
|---|---|
| **Identity** | One sign-in service for the whole platform. Machines prove who they are with a private key that never leaves their own hardware, so there are no shared passwords to leak |
| **Permission to act** | Short-lived passes — five minutes, and valid for one destination only. A pass issued for one organisation's node is refused everywhere else |
| **Separation** | Several organisations can share a node and still not see one another. Their data, credentials and records are kept apart centrally, rather than relying on each piece of software to remember |
| **In transit** | Every connection is encrypted. Partner machines reach the platform by connecting outwards, so nothing at a partner's site has to be exposed to the internet |
| **Records** | Append-only, enforced by the database itself rather than by policy — the software cannot alter or delete an entry even by mistake |
| **Supply chain** | Software is built automatically and checked on every change for known vulnerabilities and for credentials accidentally left in the code |
| **Backups** | Encrypted, taken nightly, kept away from the machine they came from, and restored as a test rather than assumed to work |

## Who is responsible for what

| | |
|---|---|
| **The platform operator** | The software, the shared infrastructure, and any node run on your behalf |
| **Your organisation** | If you run your own node, the machine it sits on: operating-system updates, disk protection, physical security, local firewall. And in every case, what you choose to publish, to whom, and how you classify it |

## What is not in place yet

This is a beta — **validated in a relevant environment, not a finished product**. Some
controls are deliberately deferred. Each is recorded in a register that the build process
prints on every run, so none of them can quietly disappear.

**Due before the platform is validated**

| | Why it is not done yet |
|---|---|
| A second factor at sign-in for platform operators | It starts to matter with the first person holding that role |
| Named contacts for an incident | The procedure is written; for CIRCULess project the technical partners are clear within the consortium |
| Privacy notice and data-protection screening | A closed consortium, with no personal data beyond user accounts |

**Accepted for this stage, with a path to the final version**

| | |
|---|---|
| Material stored on shared infrastructure is not encrypted on disk | Only non-sensitive material is held there, and sensitive material is refused. This becomes required the moment that stops being true |
| Machine certificates are self-signed | Issued by a certificate authority in the final version |
| Organisations sharing a node are separated by software, not by hardware | A dedicated node per organisation wherever that is required |
| Obligations attached to an agreement are recorded and shown, not automatically enforced | To be assessed for the final version |

---

Next: [the glossary](glossary.md) — the terms used across this documentation.
