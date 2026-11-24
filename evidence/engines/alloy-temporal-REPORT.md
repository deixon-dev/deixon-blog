# Alloy 6 temporal trial report (2026-11-21)

## Scores

- P1 (M1 VIOLATED with readable trace): **FAIL on the trace clause,
  HOLD on the verdict** — the seeded defect is caught (`CountBounded`
  sat, witness SAT), but the engine path returns an initial-state
  snapshot, not the op sequence. Root cause characterized precisely:
  `AlloyRunner.java` uses static `sol.eval` with no temporal support,
  so traces are structurally dropped. Scored as P1 failed: a violation
  whose trace never surfaces does not meet "readable without tooling
  expertise" (the defect here was attributed by reading the 15-line
  model, a crutch real models won't offer).
- P2 (M2 HOLDS): **HOLD** — clean + falsified via Init-drop, with M1
  proving the setup's sensitivity under identical bounds. The seam
  demonstration stands: no threads in, no interleaving-class
  violation out.
- P3 (engine path or quoted gap): **HOLD** — verdicts obtained through
  `gates.check_alloy`; lint accepts temporal syntax (only the standard
  run-command rule applied); falsify works on temporal asserts; the one
  gap (trace rendering) is quoted with file and line.
- P4 (cost <= 2h): **HOLD** — ~40 min.

## Verdict

Temporal Alloy is one runner feature away from usable: verdicts, lint,
and falsification all work; only trace extraction is missing. Until
`AlloyRunner` (or a successor path) surfaces temporal counterexamples
as op sequences, native-temporal specs would produce violations no one
can read — strictly worse than the existing `util/ordering` State-trace
idiom, which renders, confirms, and falsifies end to end today.

Recommendation: do not adopt yet. The earned next step, if this is
wanted, is a scoped build (temporal instance extraction + rendering,
with a readability bar judged on blinded traces), not more trials.
Cheaper alternative that captures most of the value: keep expressing
"shape over time" in the ordering idiom, which this trial re-validated
by contrast. Either way the seam rule stands: no thread vocabulary in
Alloy-temporal, op sequences only, one property one home.
