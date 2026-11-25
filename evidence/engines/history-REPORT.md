# History-checker bridge spike report (2026-11-21)

## Scores

- P1 (toolchain): **HOLD** — true on H1, false on H2, no tool issues.
- P2 (derivation <= 5 judgments): **HOLD** — 2, both the I/O-boundary gap.
- P3 (bridge verdict): **FEASIBLE pending a small convention (design
  task, not research).** The mechanical part (state, init, mutating
  steps from primed frames) derives cleanly; the single blocker is
  that TLA+ marks neither op boundaries nor I/O roles. A small
  annotation convention (e.g. op tags + read/write roles on actions)
  closes it — the checker, search, and verdict semantics are solved
  by the library. Live-history production (concurrent harness + clock)
  is separate engineering, unspiked and unsurprising.
- P4 (cost <= 2h): **HOLD** (~1h).

## Verdict

The referral stands (Jepsen/Elle/Porcupine judge runs; deixon stays
static), and a TLA+-derived oracle bridge is feasible whenever someone
wants it: define the I/O-boundary convention, generate the model, feed
recorded histories. No build proposed — the demand signal (a Go target
needing both) does not exist yet.

## Walkthrough state after this spike

- CrossHair: shelved, yearly revisit. Alloy 6 temporal: not adopted.
- Apalache: built (second backend, shipped). Tamarin: methods proven.
- History checkers: toolchain proven, bridge feasible-pending-convention.
- Remaining: capacity-in-TLA+ (modeling note), Quint (tabled by owner).
