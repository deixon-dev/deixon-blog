# Evidence: the second engine (part 24)

Primary sources for the second-engine post. Every spike below was
preregistered before running; preregs, run logs, and raw tool outputs
are kept privately (ask the author for access). What is vendored here is what the post's claims rest on.

`depth-REPORT.md` — the Apalache depth spike: agreement with TLC on
small specs, the CounterJump gradient (TLC 0.5 s at Max=10^3, dead at
10^6 and 10^9; Apalache ~1 s at all three points), per-concrete-Max
induction. `design-REPORT.md` — the design spike: annotation burden
measured on real slice specs (11–21 lines), the ITF-to-confirmation
handoff, and the integration design that shipped.

`inventory-tlc-trace.json` and `inventory-apalache-trace.itf.json` —
the two traces the handoff claim compares: TLC's 5-line lost update
against Apalache's 5-state ITF counter-example on the same shop
inventory spec. Both attribute Read(1), Read(2), Write(1), Write(2)
with identical changed sets through the real confirmation consumer.

The siblings, one report each: `crosshair-spike1-REPORT.md` and
`crosshair-spike2-REPORT.md` (1 real in 14 counterexamples; shelved
to yearly revisit), `alloy-temporal-REPORT.md` (verdicts work, traces
do not), `tamarin-REPORT.md` (SSH key-exchange secrecy and agreement
verified; methods only, no verdicts about any real codebase),
`history-REPORT.md` (Porcupine bridge feasible pending one annotation
convention), `capacity-REPORT.md` (the queue pattern, verified).
