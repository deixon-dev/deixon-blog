# Apalache spike report (2026-11-21)

Strongest positive result of the improvement walkthrough so far.

## Scores

- P1 (agreement): **HOLD** — C1 identical 3 holds + 1 violation on both
  engines; the violation is the same defect at the same depth (x=Max=3
  after 3 Incs; TLC trace + Apalache State-3 violation agree).
- P2 (depth): **HOLD on the load-bearing clause, with a corrected
  sub-prediction.** C2 (Max=10^9): TLC cannot reach (300 s timeout,
  72M of 10^9+ states, queue growing); Apalache verdicts in 0.9 s.
  The C2' sub-prediction ("both return, Apalache >= 10x") missed as
  specified — TLC already dies at 10^6 (300 s timeout) — and the added
  C2-K gradient point (10^3) reverses the ratio (TLC 0.5 s vs Apalache
  1.7 s; JVM+startup dominates tiny). The true shape is a crossover:
  TLC faster tiny, Apalache reaches orders beyond. The depth gap is
  real and larger than predicted.
- P3 (induction): **HOLD with a characterized limit** — TypeOK base +
  step verified at Max=3 and Max=10^9 (~1 s each, Max-agnostic cost).
  Fully symbolic Max refused (`SubstRule: not assigned`); predicate
  cinit refused (must ASSIGN). So: inductiveness per concrete Max,
  not quantified over Max — each new Max is a ~1 s re-run.
- P4 (annotations <= 10): **HOLD** — 3 `@type` lines + CInit op(s)
  per file (6-7 added lines); block-style placement required (above
  the keyword is not recognized — a real authoring footgun, documented).
- P5 (cost <= 3h): **HOLD** (~2h wall).

## Verdict

Apalache earns the preregistered next step: an integration-design
discussion (second backend for data-heavy slices + the induction flow),
not an integration. Recommended shape, consistent with the earlier
agent-instruction sketch: TLC stays the default; Apalache engages where
TLC demonstrably cannot reach (data fanout, deep thin arithmetic) or
where an inductive proof is wanted; annotation is the known price
(small here, unmeasured on real slice specs — that measurement belongs
to the design spike). Operational notes for that work: `timeout -k`
around TLC (TERM shutdown hangs on large queues); Apalache needs z3 on
PATH and per-config CInit ops.

## Walkthrough state after this spike

- CrossHair: shelved to yearly revisit (2 spikes; 1 real in 14).
- Alloy 6 temporal: not adopted (verdicts work, traces don't — one
  runner feature away).
- Apalache: positive — integration design is the earned next step.
- Remaining queue: Quint (authoring surface), history checkers
  (Elle/Porcupine referral + oracle-bridge question), Cedar pattern,
  Tamarin spike, capacity-in-TLA+.
