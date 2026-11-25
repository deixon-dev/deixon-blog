---
title: "A second engine for the temporal side"
description: "TLC stays the default; Apalache takes the slices TLC cannot reach — symbolic verdicts at Max=10^9 in under a second, an adoption rule that only takes violations, and a trace handoff proven step-for-step. Plus the spikes that did not make it."
layout: post
series: deixon
part: 24
date: 2026-11-22
---

*Part 24 of 24 in a series on deixon. The [previous post]({% post_url 2026-11-20-structural-verdicts %}) closed the Alloy side with measured verdicts. This one opens a second engine on the temporal side: same specs, verdicts where TLC runs out — and the rule that keeps a bounded hold from ever passing as exhaustive. Evidence: [`evidence/engines/`](https://github.com/deixon-dev/deixon-blog/tree/main/evidence/engines).*

## Where TLC runs out

Take a counter with one data-nondeterministic jump (`x'` anywhere in
`0..Max`) and ask whether the type invariant holds. At Max=1,000, TLC
answers in half a second — faster than Apalache's 1.7, most of it JVM
startup. At Max=10^6, TLC dies at the 300-second timeout. At Max=10^9,
it dies having generated 288 million states against a billion reachable,
queue still growing. Apalache answers all three points in about a
second each: symbolic integers do not enumerate. The shape is a
crossover, not a uniform win — TLC faster tiny, Apalache reaching
orders beyond. Induction behaves the same way: the invariant's base
and step check in about a second at Max=3 and at Max=10^9 alike.

## The adoption rule

TLC stays the default everywhere. Apalache engages two ways: automatic
escalation when TLC times out on a spec carrying Snowcat `@type`
annotations, or explicit request (`backend="apalache"` on `module_check`,
with `apalache_length` and `apalache_timeout` budgets). The constant
initializer generates mechanically from the bound configuration; the
annotations are hand-written, 11–21 lines on the measured specs.

One rule governs what comes back: only violations are adopted, with
their traces. Anything else — a bounded hold, a tool error, another
timeout — keeps the original timeout verdict with a note naming what
happened. A hold to depth N is never dressed as exhaustive; it is not
even dressed as a hold.

## The handoff proof

An adopted violation still has to survive confirmation, which walks
TLC-shaped traces. So the adapter converts Apalache's ITF trace to the
same step list the checker consumes: values rendered as TLA literals,
threads attributed by program-counter delta, actions matched against
primed-variable frames expanded through `INSTANCE` calls — and any
ambiguity refuses instead of guessing. On the shop inventory's lost
update, the converted trace matches TLC's step for step: Read(1),
Read(2), Write(1), Write(2), identical changed sets. Both traces are in
the drawer; the compared step lists are in the design report.

## The siblings that did not make it

The walkthrough that produced this backend preregistered every spike
and shelved most of them. CrossHair found 1 real bug in 14
counterexamples across two spikes — contract checking goes to yearly
revisit. Alloy 6 temporal checks run end to end but return
initial-state snapshots instead of traces — verdicts without a story,
one runner feature away from usable. Tamarin proved secrecy and
injective agreement on an SSH key-exchange model the agent authored —
methods only, no verdicts about any real codebase. History checkers
work and a TLA+-derived oracle bridge is feasible pending one
annotation convention. Capacity needs no tool at all: bounded
counters, explicit loss actions, and exact conservation ghosts, all
checked through the standard path. Each verdict below links its report.

## Limits, stated plainly

Induction holds per concrete bound only — fully symbolic constants are
refused upstream, so each new bound is a one-second re-run, not a
re-proof. Temporal properties and deadlock are out of scope for this
path; liveness stays with TLC. Annotations were measured on small
specs; the block-placement footgun (types floating above the keyword
are silently ignored) is documented, linted later. Escalation re-runs
on confirmation, so a deep timeout gets paid twice. And z3 rides along
as a soft dependency — probed at use, never at install.

What changes for users: nothing, unless a slice times out. Then
annotate it and re-run, or ask for the symbolic engine directly. On
unannotated specs the default path behaves exactly as last week —
the second engine only speaks where the first one falls silent.

{% include series.html %}
