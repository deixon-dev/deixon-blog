# Apalache design spike report (2026-11-21)

## Scores

- P1 (burden <= 40 lines and <= 120 min/unit): **HOLD** — A: 21 lines /
  ~50 min; B: 11 lines / ~20 min. Leaves-only annotations sufficed
  (no operator annotations); INSTANCE/Cadrinality transparent.
- P2 (agreement): **HOLD** — A: violation + hold match TLC (same defect,
  verified trace-to-trace); B: 3/3 holds match.
- P3 (handoff): **HOLD, strongly** — ITF→TraceState adapter (kept as
  `itf_adapter.py`) feeds the REAL `schedule_of` with zero engine edits;
  step lists identical to TLC's (thread/action/changed, 4/4). One
  inference required: action identity is absent from Apalache output,
  attributed here by pc-delta (spec-scoped table; general rule below).
- P4 (design written): this document.
- P5 (cost <= 4h): **HOLD** (~3.5h).

## Integration design (recommended: proceed to build proposal)

1. **Trigger rule.** TLC stays the default everywhere. Apalache engages
   when (a) TLC demonstrably cannot reach in budget (timeout/OOM —
   automatic escalation, never silent substitution on a green verdict),
   (b) the slice is data-fanout shaped (agent flag first; auto-heuristic
   later), or (c) an inductive proof is requested. Bounded lengths are
   disclosed per verdict in the existing bounds field.
2. **Annotation pipeline.** Snowcat block annotations + CInit live next
   to the spec in `.specverify/` (versioned with it, validated by an
   `apalache parse` gate). CInit is MECHANICAL from cfg CONSTANT lines
   (generate, don't hand-write); `@type` lines are hand-written at
   ~10-20/spec (measured 11-21). Lint the known footgun: annotations
   outside the declaration block are silently ignored.
3. **Verdict reconciliation.** Both-engines protocol: run the trigger
   engine, keep TLC's verdict beside Apalache's; agreement strengthens,
   disagreement becomes a record (new model-level note, never a silent
   override). Apalache-found violations enter confirmation through the
   ITF adapter (proven at the seam) and face the SAME bar (static
   confirmation or replay) before any bug status. Length bounds travel
   with the verdict so "holds to depth N" is never misread as "holds".
4. **Backend plumbing.** `fetch.py` pin (release asset + sha256, exactly
   like the jars) + z3 prerequisite probe (like the Java prereq check,
   with version floor); `checker/apalache.py` wrapper mirroring
   `checker/tlc.py` (`run_apalache` -> run record with ITF + MC-format
   trace); CLI surface for length/per-condition budgets. Constants stay
   concrete (symbolic Max refused upstream — retest yearly).
5. **Cost model.** First-annotation ~30-60 min/spec (measured 20-50),
   near-zero marginal per re-check; adapter ~80 lines kept and proven;
   confirmation unchanged downstream of `schedule_of`; CInit generation
   is a day's work; the general action-attribution matcher (delta-match
   against primed-variable frames, reusing the frame machinery
   confirmation already has) is the one genuinely new piece, estimated
   days not weeks. Suggested phasing: plumbing + adapter, then trigger
   rule, then annotation assistance.

## Walkthrough state after this spike

- CrossHair: shelved, yearly revisit (2 spikes; 1 real in 14).
- Alloy 6 temporal: not adopted (verdicts work, traces don't).
- Apalache depth: positive (verdicts beyond TLC's reach).
- Apalache integration design: COMPLETE (this document) — build
  proposal is the earned next step, on the owner's word.
- Remaining queue: Quint (tabled by owner), history checkers
  (Elle/Porcupine referral + oracle bridge), Cedar pattern, Tamarin
  spike, capacity-in-TLA+.
