# Tamarin spike report (2026-11-21)

## Scores

- P1 (authoring): **HOLD with iteration** — theory + 3 lemmas complete
  and parsing after 3 authoring iterations (Eq-idiom rework after a
  wellformedness rejection; secrecy-claim rescoping; agreement-claim
  rescoping). First-try authoring failed twice, both times on
  crypto-modeling judgment (where signatures get checked; who may
  claim secrecy), never on syntax.
- P2 (automaticity): **HOLD** — every verdict from default-heuristic
  runs in seconds; zero manual proof steps, oracles, or GUI.
- P3 (verdicts): **HOLD** — secrecy, injective agreement, and sanity
  all verified. Prereg deviation disclosed: "one modeling fix" became
  two attempts (first misdiagnosed and reverted) plus one
  claim correction that aligned the lemma with the prereged triple.
  No goalpost was moved: the frozen claims are what verified.
- P4 (cost <= 5h): **HOLD** (~2h).

## Verdict

Agent-authoring of Tamarin theories is feasible WITH falsification-
guided iteration, not first-try: each counterexample pointed at the
responsible rule/action, and each fix was minutes once diagnosed —
but both diagnoses needed protocol-domain knowledge (authenticated
vs unauthenticated claims, DH validity subtleties), and headless
attack details are limited to the solve skeleton. No MINA verdicts
were produced or attempted (methods spike, per prereg).

## Walkthrough state after this spike

- CrossHair: shelved, yearly revisit. Alloy 6 temporal: not adopted.
- Apalache: built (second backend, shipped).
- Tamarin: methods proven on SSH KEX core; protocol-slice coverage is
  a discussion, not a build. No engine integration proposed.
- Remaining queue: history checkers (Elle/Porcupine referral + oracle
  bridge), Cedar pattern (referral docs cover it), capacity-in-TLA+,
  Quint (tabled by owner).
