# CrossHair spike 2 report (2026-11-21)

Prereg: `runs/2026-11-21b/PREREGISTRATION.md`. Run log: `RUNLOG.md`.
Raw outputs: `fn-*.out/.err` (per-function x3), `cfg-r*.out/.err`
(module runs, crashed). Blinded triage: `triage.md`.

Corpus: own typed engine code (`tla/cfg.py`, `forge/questions.py`),
11 targets, budgets pinned (`--per_condition_timeout 60
--max_uninteresting_iterations 20`, `PYTHONHASHSEED=0`).

## Scores

- P1 (precision >= 50%): **FAIL** — 0 REAL / 2 distinct counterexamples.
  Both triaged noise with caller evidence: (1) render round-trip breaks
  only on `''` fields, which the format cannot serialize, `read_cfg`
  never produces, and no caller constructs (universal postcondition was
  over-strong, not the code); (2) `cfg_owner('', 0)` passes an int where
  the docstring and every caller use a collection (input-synthesis noise
  on the corpus's one unannotated parameter).
- P2 (stability >= 80%): **HOLD** — 11/11 byte-identical across 3 repeats.
  Pinned budgets + hash seed stabilized discovery; spike-1 flakiness did
  not reproduce under controls (different corpus — suggestive, and the
  controls are now the required protocol if this is ever revisited).
- P3 (executability >= 70%): **HOLD** — 9/11 checked (82%). Two skips,
  both deterministic tool crashes on `pathlib` overload handling
  (`load_cfg`, `cfg_spec_marker`; `intersect_signatures` ValueError).
- P4 (cost <= 30/function): **HOLD** — ~11 min/function (triage separate).

## Reliability findings (beyond the bars)

- Recall gap: `spec_syntax('a >> b == c')` violates its postcondition
  (icontract raises concretely), yet CrossHair reported CONFIRMED 3x —
  symbolic strings realized too short to discriminate (`realize_text_2len`
  in verbose). Clean != verified on string-heavy code; CONFIRMED is
  budget-relative and the bound bit on a 4-character input. (Behavioral
  consequence nil — order affects only which mark an error message quotes.)
- No crash isolation: one crashing target kills a whole-module run (the
  module runs died on the `pathlib` crash); per-function targeting is
  mandatory, tripling run count.
- Absolute noise fell sharply vs spike 1 (2 counterexamples on typed code
  vs 12 on untyped), but with zero confirmed the precision question is
  answered against: typedness removes the str-substitution noise and
  leaves contract-domain overreach plus recall gaps.

## Verdict

P1 fails, so no ranking-feed design spike. Combined record across both
spikes: 1 real in 14 counterexamples (7%), two tool-crash classes
(`sys.modules` substitution, `pathlib` overloads), no crash isolation,
budget-relative CONFIRMED with a demonstrated miss. CrossHair goes to
yearly revisit — the tool is pre-1.0 and moving, but nothing here earns
integration work. The agent time is better spent on the Alloy 6 temporal
trial (nearly free, same jar) next in the walkthrough queue.
