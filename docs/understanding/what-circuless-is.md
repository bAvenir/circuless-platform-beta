# What CIRCULess is

A way for organisations to offer each other **tools over an API** — and the data those
tools work on — **without giving up control of them**.

## The problem

In a construction and demolition value chain, the information one organisation needs is
usually already held by another. A recycler knows the composition of a batch. A
contractor knows what went into a building. A manufacturer knows what their material can
tolerate. And researchers and developers can create services and intelligent systems to extract value or recommend actions. 
Putting all of it together can bring a greater reusability and benefits for all.


## Offering a tool, not sending a file

Most of what is worth sharing in this value chain is not a file. It is something that
*does* work: a model that predicts how a reclaimed board will behave, a routine that
grades surface defects, an optimiser that picks a destination for a batch. That capability
lives in an application its owner already runs, and it is not something you can email.

CIRCULess makes it callable. The owner registers the application with their node, and the
node puts an API in front of it. Another organisation calls that API and gets an answer
back. What they never get is the application, the model behind it, or the credential that
opens it — those stay where they were.

The same mechanism carries datasets, which are the other thing a node can offer. The
difference is what the caller ends up holding.

## Granting and withdrawing

Access is an **agreement** between two organisations: what may be used, by whom, for what,
and between which dates. The owner grants it, and the owner ends it. Every call is checked
against it at the moment it is made — not once at the start — by the owner's own node.
Revoking takes effect within about thirty seconds.

**What withdrawal does and does not do.** For a tool, it is complete: the next call is
refused, and the caller never had anything but answers. For a dataset, it stops any
further read — but a file that has already been delivered has been delivered, and no
agreement can reach into someone else's storage and take it back. That is a property of
files, not a limitation of this platform, and it is worth knowing before you choose which
of the two to offer.

## What it is not

| | |
|---|---|
| **Not a marketplace of copies** | What you publish is an endpoint, not a bundle somebody downloads wholesale. The catalogue holds descriptions, never the thing itself |
| **Not a data lake** | Nothing is centralised. Tools and data stay with whoever owns them |
| **Not a broker** | No intermediary holds your data, or runs your application, in order to pass it on |
| **Not a replacement for your systems** | A node sits in front of what you already run. Your application does not change, and needs no CIRCULess-specific code |

## Where the tools and data actually live

On a **node** — a small piece of software that fronts one or more organisations'
applications and datasets, and answers every request for them. The node is the only thing
a caller ever reaches; your application sits behind it and is never exposed.

A node runs either on your own premises, where you control the machine, or on
infrastructure operated by an IT company, for organisations that would rather not run one.

---

Next: [the pieces](the-pieces.md) — what the platform is made of.
