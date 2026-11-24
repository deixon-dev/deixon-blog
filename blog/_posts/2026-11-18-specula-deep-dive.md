---
title: "Specula vs specfence: the same loop, different answers to its critics"
description: "A deep comparison with the closest neighbor: shared TLA+ core, different bars for what counts as a bug, and how each side handles circularity, composition, and what happens after the bug."
layout: post
series: specfence
part: 10
date: 2026-11-11
---

*Part 10 of 24 in a series on specfence. The [landscape]({% post_url 2026-11-16-landscape %}) named Specula the closest neighbor. This post earns that claim line by line.*

*Level L2 · Needs: part 8 or 9. The closest-neighbor comparison.*

## What Specula is

[Specula](https://www.aiinsiders.net/article/speculas-bug-hunting-agent-impresses-a-reviewer-but-not) ([paper](https://arxiv.org/abs/2607.25333), August 2026) is an agentic system for one job: find concurrency bugs in existing code. It writes a TLA+ specification from the code, validates the spec against observed traces, model-checks it, and reproduces every confirmed bug as a timed integration test. Across 48 concurrent and distributed systems in seven languages it surfaced 249 bugs, 207 previously unknown, at a median cost of $57 in tokens per system. Two opposing checks drive it: trace validation pulls the spec toward the code, model checking pushes back when the spec gets too permissive to catch anything.

## Capability overlap

- **Same checker, same exhaustiveness.** Both bet that interleaving bugs live in state spaces small enough to exhaust, and both use TLA+/TLC to do it.
- **Same rule that a trace must fit the code.** A counterexample the real code can't follow doesn't ship, in either tool.
- **Same feedback insight.** The reported gap — 62 bugs for the full loop, versus 2 for an unassisted frontier model and 3 for the model armed with only the standard TLA+ toolchain — matches specfence's founding bet: the advantage is the loop, not the model or the tool access.
- **Same cost profile.** Tens of dollars in tokens per system, hours end to end. Both are cheap enough to run routinely, expensive enough to aim carefully (hence slicing).

## Differences

- **Where specs come from.** Specula derives specs from the code it checks — 87% of its invariants come from implementation and comments, per reviewer [Murat Demirbas](https://muratbuffalo.blogspot.com/2026/08/specula-scaling-formal-specifications.html). Specfence's greenfield door derives specs from prose plus interview, independent of any code. Its from-code door derives the same way Specula does, but adds falsification controls (mutants that must violate, controls that must pass) so a vacuous model can't survive.
- **Composition.** Specula models one module at a time and mocks the interactions — Demirbas's sharpest objection, unanswered in the paper. Specfence composes through published, version-pinned interfaces with client re-checks when an interface changes.
- **The second checker.** Specula is TLA+ only. Specfence pairs every temporal verdict with an Alloy structural model, and treats disagreement between the two as a finding about the models.
- **The bar for a bug.** Specula ships a bug only with a timed integration test that reproduces it. Specfence ships one once the trace is confirmed statically against the code, with a test outline marked *not executed*; running it is the developer's call. Specula's bar is higher per bug; specfence's reaches code it cannot run, such as a complex deployment.
- **After the bug.** Specula ends at the reproduced test. Specfence pins the restored property as a golden and guards every later change against it — the bug becomes a tripwire, not just a ticket.

## How to use each

- *Specula:* point it at a codebase (a research system; follow its repo's setup), get back reproduced concurrency bugs as timed tests. Best for: auditing unfamiliar concurrent code fast.
- *specfence:* install the wheel, open an agent session with the server enabled, and start from prose (new system), a feature description, or a codebase. Best for in a pilot: building with guardrails from day one, or auditing with the verdicts pinned afterwards.

Use both when auditing: Specula's breadth for the first sweep, specfence's depth — composition, goldens, structural cross-check — for what matters.

## Contrasting example: the loosened guard

Specula's own paper supplies the exhibit both sides share (§3.3.1, Figure 6). On a Kudu-Raft implementation, the agent quietly loosened a safety guard just to make a log replay pass — trace validation rewarding a spec edit that made the code look right. Model checking caught it in a single step. That's the loop working: the permissiveness check firing against the conformance check.

Specfence's mirror image is the kombu control: the race verdict stands because the atomic-acquire control is TLC-clean *and* a defect-injected variant violates in two steps. Same moral from the other side — a clean means nothing without the demonstration that the check can fail. Both systems learned, independently, that a verifier needs an adversary, and both built the adversary in: Specula as opposing checks, specfence as falsification-first gates. The difference is what happens next — Specula files the test; specfence also pins the property, so the guard can't be quietly loosened without failing the gate.

Next: [Imandra vs specfence]({% post_url 2026-11-19-imandra-deep-dive %}) — ask the logician, or set the tripwire.

{% include series.html %}
