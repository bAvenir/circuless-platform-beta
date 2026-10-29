# What CIRCULess is

A way for organisations to share industrial data with each other **without giving up
control of it**.

## The problem

In a construction and demolition value chain, the information one organisation needs is
usually already held by another. A recycler knows the composition of a batch. A
contractor knows what went into a building. A manufacturer knows what their material can
tolerate. Put together, that information makes reuse possible instead of theoretical.

It rarely gets put together. Sharing industrial data normally means sending a copy, and a
copy is a decision you cannot take back:

- you no longer know who has it, or how old their version is;
- you cannot withdraw it when a project ends or a relationship changes;
- commercially sensitive detail sits on somebody else's disk indefinitely;
- so the safe answer is no, and the data stays where it is.

The obstacle is not the file format or the network. It is that *sharing* and *losing
control* have been the same action.

## What CIRCULess does instead

It separates them. Three things move independently:

**A description moves.** You publish what a dataset or service *is* — what it covers, its
licence, where in the value chain it belongs. The description goes into a catalogue
everyone signed in can search. The data itself does not go anywhere.

**A request moves.** Someone finds your description and asks for access, naming what they
want and why.

**A decision moves.** You approve or refuse. If you approve, the agreement says what they
may do, with which resource, and for how long.

Only then is any data read — and it is read **from your system, on your terms, one
request at a time**. Every single request is checked against the agreement at the moment
it is made, by the software holding the data. Not by a central server, and not once at
the start.

The consequence is the point: **withdrawing access is as easy as granting it.** Revoke
the agreement and reads stop, within about half a minute. Nobody has a copy to forget
about, because nobody was given one.

## What it is not

| | |
|---|---|
| **Not a data lake** | Nothing is centralised. The catalogue holds descriptions; the data stays with whoever owns it |
| **Not a broker** | No intermediary holds your data in order to pass it on |
| **Not a file-sharing service** | Access is an agreement that can be revoked, not a link that works until someone remembers to delete it |
| **Not a replacement for your systems** | A node sits in front of what you already have, including existing applications |

## Where the data actually lives

On a **node** — a small piece of software that holds one or more organisations' data and
answers requests for it. A node runs either on your own premises, where you control the
machine, or on infrastructure Bavenir operates for organisations that do not want to run
one.

That choice is yours and it has consequences worth understanding before you make it. See
[who runs what](who-runs-what.md).

## This is a beta

CIRCULess is at **technology readiness level 5**: demonstrated in a relevant environment,
not a product. It works end to end and real organisations can use it, but some controls a
production system would have are deliberately not built yet, and the boundaries are
stated rather than implied.

[What it does not do](what-it-does-not-do.md) is a real chapter, not a disclaimer. Read it
before deciding what to put on the platform.

---

Next: [the pieces](the-pieces.md) — what the platform is made of.
