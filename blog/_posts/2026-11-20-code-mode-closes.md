---
title: "Eight more gates: what an agent could close alone in the code mode"
description: "The gate audit from part 19, run again on the code mode: eight ways an agent alone could hide a bug, an owed slice or a guard property from the person. Each now waits for the person's yes or says what it holds back. Three cheaper checks of the skill text found two of the problems too."
layout: post
series: deixon
part: 21
date: 2026-11-11
---

*Part 21 of 24 in a series on deixon. [Part 19]({% post_url 2026-11-20-gate-audit %}) audited the requirements mode's gates and closed four routes an agent could take alone. This post asks the same question of the code mode, where the stakes are bugs in someone's existing code. Evidence: the round records linked below, in the deixon repository.*

*Level L2 · Needs: the code mode from [part 2]({% post_url 2026-11-10-how-it-works %}) and the gate audit in [part 19]({% post_url 2026-11-20-gate-audit %}). No formal methods.*

## The question, again

In the code mode, deixon reads existing code, models the risky parts in TLA+, and reports what it finds. The report the person reads has a fixed shape:
- **bugs**, which a checker confirmed;
- **model-level findings**, which it did not;
- **owed slices**, the parts it has not modelled yet;
- **approvals waiting on the person.**

Part 19's lesson was that a rule in the skill text moves an agent less than a gate in the engine does. So the code-mode audit (CM1) asked the same question of every line in that report: can the agent remove it, weaken it, or move it out of sight with only what it writes itself? That means no checker's verdict and no answer from the person.

The audit first listed every place in the code that produces one of those lines, 89 in all. That list was committed before any test asserted a verdict. Then each route got a test that takes only the agent's path and calls the report again. Six seeded engine bugs checked the tests themselves, and all six were caught, with a clean control run first.

## What the audit found

Eight routes worked:
- **Write the answers file.** In the code mode the answers file, meant for clients that cannot show forms, still settled everything: deployment answers, the model's confirmation, which classes are shared, and which modules the deployment never uses. Part 19's freeze covered only the requirements mode. The report never named the file.
- **Withdraw the bug.** Any non-empty reason took a confirmed bug out of section 1. So did replacing it with a model-level finding, which needs no evidence. The report said nothing.
- **Call it a control.** One comment line, `\* @control <reason>`, on the cfg that found a violation moved the violation out of the findings and into a list of expected failures.
- **Write any spec.** A module's owed slice disappeared as soon as a spec existed for it, even one the lint rejected outright. One whose every property could never fail cleared it too, with only a label.
- **Narrow the scan.** `set_scan_policy(screen_slices=0)` turned off the screen that reads each candidate before choosing what to model. Nothing recorded who chose it.
- **Drop the guard's property.** A property the person had accepted for the commit guard could be dropped with one argument, and the store forgot it had ever been there.
- **Accept your own intent item.** The merge gate turned BLOCK into PASS for an item marked "accepted" by any name, "agent" included.

Some routes were the agent's by design, such as its reasons for skipping a candidate. These were kept and labelled, not closed. None of them is silent: each is recorded where the person can find it.

## Three cheaper checks, and what they caught

Part 19 found that checks of the skill text could not have predicted what agents skipped. They were run again, on the two largest code-mode skills, because they cost little:
- **EGM's review** ([Google's Elephant-Goldfish Model](https://github.com/google/elephant-goldfish-model)) ran four times for $5.26. It missed both cases where agents had skipped an instruction in earlier runs. It did find 19 real problems of form, and two real behaviour problems on its own:
  - **the answers-file trust gap,** the same one the audit found;
  - **a contradiction in model-slice:** one sentence said "if every path runs on one thread or loop, the race is not real", while later sections said callbacks on one loop can be real bugs.
- **A load measure:** an agent on the first-look path reads about 24,000 tokens of skill text before its first tool call. Almost half of model-slice belongs to a single tool step.
- **A check for facts in two homes:** 11 passages appear in both a skill and a tool description. One pair disagreed about which proposals may share a spec.

The contradiction and the disagreement were fixed in the text (SR1). Moving step text into tool results would change behaviour, so it waits for its own trial.

## Eight closes, each chosen by the owner

The owner chose each close from two or three options.

| route | the rule now | record |
|---|---|---|
| answers file | counts only if the run began with it, frozen by `begin_run` or the person's own freeze command; the report lists every answer it gave | AF1 |
| withdraw or weaken a bug | asks the person, quoting the bug and the reason; until yes, the bug stays, marked "withdrawal proposed"; every withdrawal is listed | WD1 |
| `@control` | explains a failure only when a real check sits beside it; a lone control stays a finding | CT1 |
| owed slice | stays owed until a check gives a real verdict: a violation, or a property shown able to fail | OW1 |
| scan settings | a setting that reads less than the default counts only with the person's yes | SP1 |
| guard property | dropped only with the person's yes; every drop is logged and listed | GD1 |
| intent item | "accepted" counts only with the person's recorded yes; otherwise the gate blocks | IN1 |

Most closes have the same shape. Where the agent used to decide, the person now answers by elicitation, and their answer is recorded beside the setting it decides. When the person cannot be asked, the stricter state holds, and the question waits. That happens when the client shows no forms, or the run is a headless shell, or a bot drives the run. The bug stays in section 1, the default scan applies, and the property keeps guarding. Each close was checked by its own seeded engine bugs: 7 for AF1, 8 for WD1, 6 for CT1, 6 for OW1, 8 for SP1, 8 for GD1 and 6 for IN1. All were caught, each with a clean control.

## What the fixes found along the way

The test suite and the seeded bugs found five things in the code around the closes:
- **The earlier freeze never froze.** When the person had placed an answers file before the run, `begin_run` decided a run was already under way and returned before freezing anything. Part 19's tests had frozen the file by hand, so they never saw it.
- **The shell lost a tool.** Making `withdraw_finding` ask the person made it async, and the shell runner refused every async tool. So shell users could no longer withdraw even a finding that needed no question. The runner learned to run the tools that ask only sometimes; shells with a terminal have since gained prompts on `/dev/tty`, so the person can answer there too.
- **One seeded bug was caught only by the site count.** No fixture had a spec shared by two modules. An existing test file had one, once its stand-in checker learned the new field.
- **One seeded bug survived.** The person backs a value, the agent moves it to the default, then puts the old value back on its own. The old yes would back it. A test for that sequence was added, and the second run caught it.
- **Three tests passed by luck.** They called the now-async guard tool without awaiting it, so the call never ran, and their assertions happened to hold anyway.

## What this does not show

The closes are tested by seeded bugs, not by agents. No trial has shown agents taking these routes less, or the person catching more. The state files the engine writes, such as the findings log or the freeze record, can still be hand-edited. Like part 19, the audit set that aside as forgery, which the signed driver envelope from [part 13]({% post_url 2026-11-20-how-to-talk %}) guards against. In a bot-driven run, a bug cannot be withdrawn and a guard property cannot be dropped at all, because the envelope has no place for those answers yet. That fails safe, but it is a gap.

And the closing point of part 19 still holds. More of these gates now hold until the person says yes. Each question quotes what the person is agreeing to: the bug and the reason, the property's claim, the narrower scan. Reading it is still the person's job.

*Series note: the series has since continued with [Part 22]({% post_url 2026-11-20-services-first-run %}), which reopens the evidence drawer for services, and [Part 23]({% post_url 2026-11-20-structural-verdicts %}), which closes the Alloy side.*

*Series note (2026-11-21): "the run is a shell" above now reads "headless shell" — shells with a terminal prompt on `/dev/tty` since the November 20 release.*

{% include series.html %}

*Evidence note (2026-11-23): the run records this post cites are kept privately; ask the author for access.*
