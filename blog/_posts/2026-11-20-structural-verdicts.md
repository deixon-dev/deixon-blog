---
title: "Structural verdicts: the Alloy track, measured end to end"
description: "Six rounds take structural verification from model-level advisories to confirmed defects: a static confirmation ladder, a calibration that fires its own stop rule at 2/21, fences, verified extraction — and the honest misses."
layout: post
series: specfence
part: 23
date: 2026-11-20
---

*Part 23 of 24 in a series on specfence. The [previous post]({% post_url 2026-11-20-services-first-run %}) ran the first service eval. This one closes the Alloy side: every structural verdict can now travel from proposal to a confirmed defect — and every step was measured first. Evidence: the ST1–ST6 preregs and results, and the frozen labels and scores, are kept privately.*

*Level L2 · Needs: comfort reading short Alloy and Python excerpts. Six rounds, file by file.*

## The ladder: a counterexample becomes a verdict

A temporal counterexample gets confirmed against the code — threads, locks, switch points — before anyone calls it a bug. A structural one used to stop at "model-level finding": no machinery related an Alloy instance back to the code, so no structural verdict could ever become more than an advisory.

`confirm_alloy_instance` is that machinery, static throughout: every atom and field in the violating instance must resolve through the model's `-- @code` tags to index symbols; every trace step must fit exactly one `Op_` frame, whose method must exist, write the fields the step changes, and be invocable; a violation needing a write nothing performs, or a state a coded guard forbids, is *refuted*. Six fixtures carried preregistered verdicts — confirmed, two uncertains, two refutes, one refusal — and all six held on first run. A confirmed result files under a new terminal status, `structural defect`, with the same evidence bar as its temporal siblings.

## Calibration fires its own stop rule

The ranking was a principled guess, so the next round labeled a case set: 21 top-ranked structural proposals across six trees, read by hand, reasons frozen before any ranking run. Two were real — an RPC `unregister` that leaks its route when `cancel` throws mid-way, and a datastore `remove_schedules` that forgets one of its three indexes. Precision 2/21 sits below the preregistered 0.15 stop line, so the ranking work stopped as designed: no tuning on noise.

The same round evaluated the ladder's gate: six hand models over the two reals plus four injected mutants. Four confirmed, all four true on hand-reading; one fence case (a sin of omission, no attributable step) and one false refute — the last traced to a genuine engine bug the measurement itself surfaced: mutator calls on subscript receivers (`self.d[k].add(v)`) recorded reads but no write. The gate held at 4/6 with 100% confirmed-precision, and the index bug went on the fix list instead of into the verdicts.

## Fences, extraction, and the honest miss

With labels frozen, three generation fences shipped against them: merged-only groups, single-writer pairs, and doc/shape claims with no co-write evidence now score quarter. Both reals stayed eligible; precision moved 2/19 to 2/10 — every preregistered target hit exactly.

Then the miss, reported as data: mechanical extraction of `Op_` bodies from method code is verified-correct (every mismatch demotes to a hand stub, never a wrong op) but covers ~3% of methods on real trees and 0% on the triage classes — real methods call helpers, loop, and await. Hand model-writing stays the bottleneck; no unsound widening was attempted to chase the coverage number. Mechanical extraction has since extended to Java, Go, and JS/TS through pinned tree-sitter grammars — verified-correct, coverage unchanged — so the bottleneck stands.

## Corners, a blind run, and the scale verdict

The remaining rounds filled the corners: SQLAlchemy schemas and `.one()` drift asserts, review-time flags for stale `@code` cites, Go parity (the F1 fixture confirms with zero mechanism changes), the subscript-write fix, subclass-writer attribution, throw-path assumptions made explicit — and a blind eval on three unseen trees: 0/15 real — then a second round on four more trees: 1/13 real (C1, a stale `_partition_set` in kazoo), three positives total (T5, T11, C1), re-ablation still deferred.

The measured economics: ~7 agent-minutes per triage read, ~30–40 per hand model, roughly one agent-hour per confirmed structural defect end to end. Depth-2 stands — at 0.20 fenced precision, deeper budgets buy mostly noise. The lever is generation precision, and now there is a labeled oracle to measure it against.

*Series note (2026-11-21): the blind-eval totals above now include round 2 (1/13, C1 kazoo), and the extraction paragraph notes the Java/Go/JS-TS tree-sitter extension.*

{% include series.html %}

*Evidence note (2026-11-23): the run records this post cites are kept privately; ask the author for access.*
