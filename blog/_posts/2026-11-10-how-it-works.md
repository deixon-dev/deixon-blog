---
title: "How it works: two checkers and the loop around them"
description: "Specfence's capabilities in one tour: four doors into one workflow, an Alloy model for shapes and a TLA+ model for interleavings, a confirmed-against-the-code-or-it-isn't-a-bug rule, and change guards that put the models to work."
layout: post
series: specfence
part: 2
date: 2026-11-10
---

*Part 2 of 24 in a series on specfence. [Part 1]({% post_url 2026-11-09-what-tests-cannot-see %}) named the gap: tests sample instances, while concurrency and structure bugs hide in interleavings and shapes no test constructs.*

*Level L1 · Needs: part 1 (or nothing, at a skim). The machinery tour.*

## Four doors into one workflow

The tool meets you where you are. There are four ways to start, one question asked once per project ("What are we doing?"), and every door opens onto the same workflow: requirements and specs, a hand-off the coding agent sees, a drift check, resolution with you, and a golden copy of curated properties that guards every later change.

1. **A new system (E1).** You describe what you want in plain prose — five lines is enough to start — and the tool interviews you about what the prose leaves open, then builds the specs. The worked example is [part 3]({% post_url 2026-11-11-greenfield-pool %}): a connection pool specified before a line of it exists.
2. **A change with stated intent (E2).** A bug report, a capability, a feature for an existing codebase. The tool grounds the delta — the report becomes a requirement and a property — then runs the same stages as a new system. [Part 4]({% post_url 2026-11-12-feature-log4j %}) runs a real feature commit through this guard.
3. **Existing code, first use (E0).** You point the tool at a codebase and it hunts latent defects: proposing the riskiest slices, modeling them, and confirming what it finds. [Part 5]({% post_url 2026-11-13-temporal-stomp %}) and [part 6]({% post_url 2026-11-14-structural-kombu %}) are two catches from this door. The confirmed findings bootstrap the first golden copy.
4. **A check-in (E3).** A commit, a PR, a self-check. The tool reviews the diff against the golden copy — on request, or automatically after every commit through an advisory hook. [Part 7]({% post_url 2026-11-15-drift-kombu-hikari %}) shows a guard firing on a real change.

In all four, the specs stay behind the scenes by default and the experience is the same shape. Your goal is the implementation; the Alloy and TLA+ models are guardrails around the coding, reviewable whenever you want — a guided tutorial mode walks through a spec section by section, mapping each variable back to the code it constrains. Every finding names its evidence; every decision that disposes something — accepting a property, waiving one, dropping a recovered requirement — waits for your yes, and an agent's say-so is refused. Nothing lands silently: the hook reports and never gates, and the golden copy updates only through your explicit step. One router picks the door from your goal, one skill set walks the stages, one store holds the goldens: learn one door and you know the moves behind the other three.

## The two checkers

Why two modeling languages? Because they see different things:

- **Alloy sees shapes.** You declare the system's relations — which resources are queued, which are checked out — and assert what must always hold: *a resource is never both queued and checked out*. The solver searches for a snapshot that breaks the claim. When it finds one, the counterexample is a single state you can read at a glance. [Part 6]({% post_url 2026-11-14-structural-kombu %}) is five such snapshots that overfill a pool.
- **TLA+ sees interleavings.** You declare the system's actions — acquire, release, notify, wait — and the checker (TLC) explores every reachable state: every order in which threads can interleave, at small scope. When a property breaks, the counterexample is the exact trace: thread A paused here, thread B ran there, and now the waiter sleeps forever. [Part 5]({% post_url 2026-11-13-temporal-stomp %}) is one of those traces, demonstrated on real code.

The two checkers overlap deliberately. Where both speak about the same defect, they must agree — and their agreement is itself checked. A disagreement between the structural and temporal verdicts would be a finding about the models, not the code.

Small scope deserves a sentence, because it sounds like a cheat. The pool in part 3 is checked with 2 connections and 2 threads, not the real 32 and hundreds. The bet is old and explicit: interleaving bugs are about *shapes of interaction* — two threads racing through one window — and those shapes already appear at the smallest scope that fits them. More threads add states, not shapes.

And size itself is not ignored: the 32-boundary the TLA+ model can't afford is checked at full size in Alloy, where counting is cheap. Each checker carries what it's good at.

## The loop: falsify first

A model-level finding is not a bug on its own. It is a hypothesis, and the tool treats it as one. The loop around the checkers exists to falsify hypotheses:

1. **Propose.** Static analysis ranks slices of the system by risk — shared state, lock shapes, history — and the riskiest get modeled first.
2. **Model.** From code, skeleton generators draft the spec's structure; from prose, the agent writes the spec from the numbered requirements. Either way the judgment — what the operations mean, what must hold — is authored, then checked.
3. **Check.** The solvers run. A violation comes back with its counterexample; a clean comes back with the bound it held under.
4. **Confirm.** The counterexample is checked against the real code statically, without running anything: the checker's trace is walked step by step through the source. Every thread switch must fall where the runtime can actually switch, the locks held must match, and each step's writes must be in the code. A trace the code can't follow stays model-level. Branch conditions are checked along the path each step takes. A step that sits on an `if` test over one field (a yes/no value, or a comparison with a constant) is refuted when that test fails in the state the step starts from. In Node and Go code, a step further inside such a test is marked uncertain; in Python the same check was switched on after a November calibration read every verdict it flipped and found each flip correct, and Java followed in the same release — on by default on both sides since November 20. Tests that call a function are doubted only when the call provably fails in the trace's state — an unmodelled call stays silent rather than guessing. Tests that read several fields or compare against a non-literal are resolved through the names the code actually reads, and a test inside a called function demotes the steps under it when its guard fails. Loop bodies entered with their condition failing or unknown are demoted too — demoted, never refuted, because another thread's timing can always change the answer. Initial-state steps that contradict what the constructors establish are demoted as well. A joint calibration over 1,246 filed confirmations read every one of the twenty-five verdicts the new checks flipped; four were verdicts the old check had gotten wrong. Where the person allows running code, the trace can also be replayed under a deterministic scheduler that forces the exact interleaving, while a *control* interleaving (threads run one after another) must pass.
5. **Record.** A confirmed counterexample is recorded as a bug, with a test outline in the project's own language — the schedule, setup and assertions taken from the trace — marked *not executed*. Running it is the developer's call. Unrefuted properties — claims the checkers couldn't break but nothing demonstrated either — don't ship as bugs.

That fourth step is the one that matters most. Confirmed-against-the-code is what separates this from a linter with opinions. Since 13 November 2026 static confirmation is the bar for a bug: running tests against a complex deployment is outside the tool's scope, and replay stays a local aid. Some findings in this series went further and were demonstrated on running code: [the lost wake-up]({% post_url 2026-11-13-temporal-stomp %}) hung a real sender ten times in three thousand unforced trials.

## The guard: specs that keep working

A spec written once and never re-checked is documentation with delusions. So every model the tool keeps becomes a tripwire:

- **Change review.** Given the trees before and after a change, the tool diffs the specs in plain words ("changed pred Op_release"), re-checks both sides, and reports what the change *restores* (broken before, holds now — the fix, confirmed) and what it *breaks* (held before, fails now — the regression, caught). For each one it adds what it means: the property's claim, the counterexample from the failing side, the code it runs through, and (for temporal properties) a plain-words scenario and a not-executed test outline in the project's language. [Part 7]({% post_url 2026-11-15-drift-kombu-hikari %}) shows the breaks direction firing twice: once temporal, once structural.
- **Golden properties.** Properties that held are pinned. A later change that violates one blocks — the gate's verdict is `BLOCKING`, with the property named. A post-commit hook runs the same guard on the tool's own repository: 598 guarded commits so far, none blocking. Part 7 tells that half honestly.

## The methodology that keeps the tool honest

The examples in this series come from benchmark runs with rules borrowed from experimental science, because the author didn't trust his own tool either:

- **Blinded testers.** The agent modeling a slice works from the code alone: no labels, no fix commits, no hints about where the bug is. What it finds, it finds the way a user would.
- **Preregistration.** Predictions are written down before the checkers run — which properties should fail, which should hold — so a surprising verdict can't be quietly redefined as expected.
- **Frozen verdicts.** Once adjudicated, a verdict doesn't change because a later tool version disagrees. Disagreements become new records, not edits.
- **Adjudication.** An independent pass replays the evidence — re-running confirmations, re-reading the code — and verdicts like *real race, demonstrated* are its words, not the tester's.

Each benchmark run keeps its preregistration, its match table, and its per-claim adjudication files beside each other. The stomp story in part 5 cites all three.

## What it won't do

The boundary from part 1, sharpened: bounded scope, two defect families, a human in the loop. Add one more: the tool needs something to check against. For existing code it needs the code; for a new system it needs your answers — the interview in part 3 is not ceremony, it's where the spec's content comes from. A vague requirement gets a question, not a guess presented as fact. If you opt in, fresh agents that never saw the interview read the requirements too, and a checker shows where their reading differs from the drafting agent's: an idea borrowed from Google's [Elephant-Goldfish Model](https://github.com/google/elephant-goldfish-model), told in [part 8]({% post_url 2026-11-16-landscape %}). (Where the tool does draft a guess, it labels it one and asks for approval.)

Enough machinery. [Part 3]({% post_url 2026-11-11-greenfield-pool %}) starts from five lines of prose and ends with a checked spec.

*Series note (2026-11-19): the opening section above now reads "Four doors into one workflow". As first published it read "Three doors in" (new system, new capability, existing code); the check-in door and the shared-stages framing landed with the single-workflow release, which also records the per-gate person decisions and the advisory-only hook.*

*Series note (2026-11-21): step 4's window check is now on in Java too — on by default on both sides since the November 20 calibration release — and the guard count above is refreshed to 598.*

{% include series.html %}
