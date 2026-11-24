# CrossHair spike report (2026-11-21)

Prereg and run log: kept privately (ask the author for access).
Raw outputs: `matcher.out`, `pools.out`, `decorators*.out`, `probe.out` (+`.err`).
Blinded triage: `triage.md` (subagent, no contract-authorship context).

## Scores

- P1a (kombu executability >= 70%): **HOLD** — 14/15 checked (93%).
  One skip: `PoolGroup.create` (always raises; no meaningful contract).
- P1b (healthchecks executability >= 40%): **HOLD, on a technicality** —
  5/5 checked (100%), but the prereged targets are decorator factories
  whose bodies never touch the DB. The real wall was characterized by the
  exploratory probe instead: wrapper logic is symbolically explorable up
  to `Project.objects.get`, where CrossHair's side-effect guard stops
  cleanly with an exact `--unblock` offer. Full DB-path verification
  needs symbolic-DB synthesis (the Nov 2026 study's lesson, confirmed
  in miniature).
- P2 (>= 1 confirmed new-class bug): **HOLD (1, narrow)** — `match()` on
  any registry lacking `glob` raises raw `KeyError` instead of the
  documented `MatcherNotInstalled` (replay-confirmed independently by
  runner and triager). Class: wrong-exception-type / unhandled edge.
  New vs pipeline: run15's kombu verdicts are races and shape bugs;
  no exception-type verdict exists there. Narrow because the public
  module-level path is safe (global registry pre-registers `glob`).
- P3 (<= 30 agent-min per checked function): **HOLD** — ~150 min wall /
  19 checked ~= 8 min (triage separate).

## Precision and reliability notes (all observed, all cautionary)

- Precision 1/12 (8%). Noise modes, characterized: (a) untyped params get
  symbolic `str`, producing `AttributeError`-on-misuse (7 of 8 pools
  hits); (b) icontract `__old__` snapshots can't deepcopy locks (3 hits);
  (c) one self-contradictory call-shape TypeError; (d) one symbolic-object
  leak into C `__repr__`.
- Discovery is nondeterministic: three identical decorators runs gave
  three outcomes (clean / cors TypeError / symbolic-leak artifact).
  Any integration must control for this (repeats, seeds, or verdict
  union rules) before trusting a single run.
- Tool crash (worked around, recorded): CrossHair 0.0.114 `RecursionError`
  on packages that substitute `sys.modules` entries (kombu's lazy root);
  memo doesn't guard re-entry, then importlib needs a spec the substitute
  lacks. Two-line scratch workaround; per-tree env cost on old codebases.
  Upstream-issue-shaped; not filed from this spike.

## Verdict

Bars held, so the prereged follow-up (a second spike, not an integration)
is earned. Recommendation: aim it at precision-on-typed-code first —
re-run the same protocol on fully annotated modern modules to test
whether the 8% is an untyped-code artifact or the tool's baseline —
plus determinism controls (repeat runs, seed behavior). Design the
ranking feed only if precision clears a bar there; feeding 8%-precision
verdicts into priorities would poison the ranking it means to improve.
No engine changes, no filings from this spike (the one real is a narrow
robustness edge on a 2022 tree; re-verify on main before even considering
it).
