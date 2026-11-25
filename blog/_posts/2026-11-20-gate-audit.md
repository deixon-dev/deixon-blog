---
title: "Gates, not words: what stopped an agent skipping a step"
description: "Four agent runs read an instruction and skipped it. Three cheap checks of the text could not have warned us; a gate that holds 'done' changed what agents did. So we audited every gate for what the agent alone can do to open it, and found four ways."
layout: post
series: deixon
part: 19
date: 2026-11-11
---

*Part 19 of 24 in a series on deixon. [Part 13]({% post_url 2026-11-20-how-to-talk %}) showed the conversation that produces a verdict. This post asks what happens when the agent in that conversation skips a step, and what can stop it. Evidence: the round records linked below, in the deixon repository.*

*Level L2 · Needs: the requirements mode from [part 3]({% post_url 2026-11-11-greenfield-pool %}). No formal methods.*

## Four runs read it and did nothing

deixon's requirements mode has a step for outside inputs. While the agent writes the TLA+ spec, it tags every step that depends on something outside the system, such as a database connection or a payment, and deixon then asks the person what should happen when that thing fails. The instruction is one paragraph in the skill the agent follows.

We gave the step to agents in a blinded trial: two runs on a connection pool and two on expense approvals, eight outside inputs between them, with a bot playing the person (results). Every run read the paragraph. No run tagged a single input, and no run mentioned outside inputs at all. All four finished with `done: true`, because nothing in the gate depended on the tag. The gate could not see a judgement the agent never made.

The next version added a gate: until the spec tags an input or declares `@inputs none: <why>`, `forge_done` refuses. The pool runs now tagged the database (results). Two of three expenses runs took the cheaper way out and wrote a "none" for a system that pays people. The version after that made the person confirm the claim. The confirmation reached the bot playing the person, and it confirmed both wrong "none"s (results).

So the text was not enough, the gate moved behaviour, and the person's yes is a gate only as good as the person reading it. Hold that last point; it comes back at the end.

## Three cheap checks that would not have warned us

Each agent trial costs about thirty agent sessions. A cheaper check that caught a bad instruction before the trial would pay for itself. We tried three, each pre-registered against the defects the trials had already found.

**A reviewer that never saw the conversation.** Google's [Elephant-Goldfish Model](https://github.com/google/elephant-goldfish-model) (EGM) reviews a document with fresh agents, its "Goldfish". We ran EGM's own review on the exact skill text each trial used, for about $3.40 (EG2). It found real problems of form: undefined terms, limits that contradict each other, detail at the wrong altitude. It did not say the tagging could be skipped. It named the "none" weakness once, then advised recording it as a known limit rather than fixing it. Scored later against the third trial, its prediction had no hits and two misses. That fits what EGM is for: it reviews designs, and our defect was about what an agent does.

**A lint.** Every must-do in a skill should say what checks it, `**checked**` or `**no check**`, and a lint can list those that say neither (SL1). It flagged the skipped sentence. But it caught only 12 of 20 seeded mutants and 2 of 4 earlier cases where agents had skipped an instruction. deixon's skills state rules as commands, as statements ("one input carries the same name on each step"), and as asides ("is yours to get right"), and no sentence pattern sees all of them. About half of what it flags is real. It is kept as a reading list, not a check.

**A rehearsal.** Give one fresh agent the skill and the same prose, with no engine and no person, and see what it writes (RH1, results). This one failed most usefully. Both rehearsals of the first version tagged the database, where every trial run had tagged nothing. Two even tagged the approver's role, which no trial ever reached. Eight runs, about $6.40, and one of four cells agreed with the trials.

The rehearsal shows why all three failed. A fresh agent with nothing else to do follows the paragraph. The trial agents read the same paragraph in the middle of hours of engine output and questions, and passed over it. The failure was load, not wording, and no check of the wording can reproduce load.

## Auditing the gates instead

If gates are what move behaviour, the gates are what to check. For every reason `forge_done` or `done_check` gives, the audit asked one question: can the agent make it go away with only what it writes itself, with no checker's verdict and no person's answer (EH1)? Each reason got a test that raises it, takes only the agent's route, and calls the gate again. A completeness test counts every place in the code that can produce a reason, so a new one fails until it is audited.

Forged state files were set aside: an agent that hand-writes the engine's question log is lying, and the signed driver envelope from [part 13]({% post_url 2026-11-20-how-to-talk %}) is the guard against that. The audit looked for routes that need no lie. It found four:

- **Delete the requirement.** The requirements document is the agent's own file. Remove R1, and "R1 is carried by nothing" goes away with it.
- **Write the answers file.** Clients without forms accept scenarios through `.deixon/answers.yaml`, and the skill tells the agent to transcribe the person's approvals into it. The same file settled every open deployment assumption, whoever wrote it.
- **Restate your own model as a fresh reading.** The fresh readers borrowed from EGM catch a reader that copied the drafting conversation. They did not catch a drafting agent that wrote "a reading" itself.
- **Untag the step.** Unstated guards were checked only on steps tagged `@req`. Remove the tag, and the question about the guard goes.

Each audit verdict was itself tested: four engine mutants, all caught. The first run of that check reported 0 of 4, because the tests were importing the unmutated checkout. A check that cannot fail would have passed everything; this one now runs a control first.

## Four fixes, each chosen by the owner

- **A removed requirement needs a yes** (RL1). The gates remember every requirement they have read. One that disappears becomes a question that quotes it: "R1 was in the requirements and has been taken out: 'Every expense has one owner.' Should it go?" Done waits for "Yes, remove it".
- **The answers file is frozen for deployment answers** (RF1). The run records the file's hash when it begins, and only that file counts. Scenario acceptance through the file still works, for clients without forms, but the done report lists every one and flags a file that changed mid-run. The first build of this fix also dropped the signed envelope's answers. The full test suite caught it before the commit.
- **Guards are checked on any step that writes what a tagged property reads** (GU1), so removing a tag, or never writing one, no longer hides the question.
- **deixon can run the fresh readers itself** (FR3). The person names a reader command in the server's settings, such as `claude -p`, `codex exec` or `gemini -p`, where the agent cannot change it. Each reader then starts in an empty folder with only its instructions, and only those readings count. Without a command, readings still count, labelled "recorded, not proven fresh".

Each fix has its own mutation check: 7 of 7, 9 of 9, 4 of 4 and 7 of 7 caught, each with a clean control.

Then a real reader run. The example from [part 8]({% post_url 2026-11-16-landscape %}): "The approver of an expense is not its owner", with a drafted model that said `e.approver != e.owner`. That compares the whole set of approvers with the owner, so an owner may approve their own expense if someone else approves it too. Two `claude -p` readers, started by deixon with no tools, each wrote "no approver is the owner", and Alloy reported the difference on R2 for each. The whole thing took 22 seconds.

## What this does not show

The fixes are tested by mutation, not by agents. No trial has yet shown that agents behave differently because a removed requirement now asks, or because the answers file is frozen. The fresh readers are not measured on seeded defects; the 22-second run is one example with a defect we planted. Each claim in this post links to its record, and those records say the same.

[Part 21]({% post_url 2026-11-20-code-mode-closes %}) runs the same audit on the code mode, and closes eight more routes.

And one hole stays open, by design: the gate that needs the person. In the third outside-input trial, a bot played the person, and twice it confirmed a claim it should have caught. deixon now quotes the claim in every such question, so the person reads exactly what they are agreeing to. Reading it is still the person's job. Every other gate holds until a checker agrees or the person does. That one holds until the person reads.

{% include series.html %}

*Evidence note (2026-11-23): the run records this post cites are kept privately; ask the author for access.*
