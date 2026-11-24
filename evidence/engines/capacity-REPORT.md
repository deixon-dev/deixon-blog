# Capacity-in-TLA+ report (2026-11-21)

## Scores

- P1 (BP clean): **HOLD with correction** — clean on all checkable
  invariants, all falsified; NoDrop removed after the vacuity lint
  correctly refused it (no Drop action exists to violate it).
- P2 (drop design clean): **HOLD** — Bounded + DropsCounted hold and
  are falsified; NoDrop knowingly unchecked (dropping is the design).
- P3 (mutant caught): **HOLD** — the uncounted Drop violates
  DropsCounted.

## Verdict

Capacity reasoning needs no new tool: bounded counters, explicit loss
actions, and exact conservation ghosts express it in current TLA+,
checked through the standard path with the standard lints (which
actively helped: orphan, unbounded, and frozen findings each improved
the models). Recommendation: use this pattern on service models where
queue/depth/drop logic is load-bearing; keep rates in measurement.
Nothing to build, nothing to refer — close the NFR walkthrough item.

## Walkthrough: complete

- CrossHair: shelved, yearly revisit. Alloy 6 temporal: not adopted.
- Apalache: built (second backend, shipped). Tamarin: methods proven.
- History checkers: toolchain proven, bridge feasible-pending-convention.
- Capacity: pattern proven (this note). Quint: tabled by owner.
- Referrals documented in the field guide.
