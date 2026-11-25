---
title: "Services, examined: the database platform, finally instantiated"
description: "Run 43 sets eight blind testers on two Django services: platform modules meet real code (33 kept specs), 30 of 31 findings adjudicated real — and own-fix recall still 0/8."
layout: post
series: deixon
part: 22
date: 2026-11-19
---

*Part 22 of 24 in a series on deixon. The [previous post]({% post_url 2026-11-20-code-mode-closes %}) closed the gate audit. This one reopens the evidence drawer for the first run on services instead of libraries. Evidence: the run records (kept privately).*

*Level L2 · Needs: comfort reading short Python excerpts. Two projects, file by file.*

Every clean-room target so far was a library, checked under the `library` profile. That left three spec-production paths with nothing behind them: platform modules (0 specs on real code), interfaces with refinement and composition (0 calls), and the Alloy data model (candidate asserts on one project, no kept verdict). Run 43 put services in front of the frozen engine to see whether those paths fire: Saleor, the Django e-commerce app (5 packets, 2016–2023), and Healthchecks, the cron monitor (3 packets, 2022–2023). Eight blinded testers, one tree each, static-only; fifteen blind adjudicators plus an independent label matcher scored the 31 findings. The run was pre-registered (predictions P40–P47 for the service paths); scores froze before analysis.

## The file-to-platform path, working — and its mirror

On Healthchecks the whole chain runs on files. The packet trees carry `docker/docker-compose.yml` with a postgres service, so the deployment model reads postgresql with read-committed isolation; the skeleton instantiates `Db_ReadCommitted` for database-using bundles; testers kept specs calling `DbRead`/`DbWrite`; the confirmed findings rest on those specs. Predictions P40–P42 pass there on file-backed ground.

The mirror is Saleor. Its packet trees carry only a Dockerfile (plus one compose file in a v1 format the inference doesn't read), so no database fact fires — and yet its packets kept the same `INSTANCE Db_ReadCommitted` lines through the skeleton's no-model fallback, which instantiates read-committed for any database-using bundle when isolation is unanswered. Same verdicts, different provenance: 33 platform-`INSTANCE` specs across all 8 packets — 16 file-backed on the 3 Healthchecks packets, 17 fallback-backed on the 5 Saleor ones. The passing predictions can't tell the two apart, and the pre-registration says so in advance. A prediction that passes for the wrong reason is still data, as long as the record names the reason.

Queues and replicas stayed dark: dozens of Celery consumers indexed (69 on the largest trees), replica routers and broker URLs sitting in `settings.py` and the environment where the inference doesn't read — 0 queue or replica modules, exactly as predicted.

## Found four times, independently

The run's headliner is a race four Saleor testers found without knowing about each other, on trees three years apart. Django's sites cache is patched for threads — a lock, a global dict — except the return read sits outside the lock while the clear rebinds the global under it (`saleor/site/patch_sites.py`, 2023 tree):

```python
def new_get_current(self, request=None):
    ...
        if site_id not in THREADED_SITE_CACHE:   # :24, outside the lock
            with lock:
                ...
                THREADED_SITE_CACHE[site_id] = site
        return THREADED_SITE_CACHE[site_id]      # :28, outside the lock

def new_clear_cache(self):                       # :59-62
    global THREADED_SITE_CACHE
    with lock:
        THREADED_SITE_CACHE = {}
```

Thread 1 checks hit, thread 2 clears, thread 1's return raises `KeyError` — against a module docstring claiming a "thread-safe structure". All four verdicts came back real, GIL-reachable (S1.json). The downloads family went six for six the same way (lost increments, `max_downloads` over-served), and the late-binding deferred callbacks twice. The pkt-b excerpt shows one find end to end: violated property, 33-state trace, static confirmation with its assumptions and open sharing question laid out.

## Precise at depth, blank on the labels

Thirty of 31 findings adjudicated real (97%), 29 of them matching no label at all. But own-fix recall is 0/8: the testers found real lost-update races in different code than the eight labelled fixes. Deadlock-by-lock-order, commit-visibility timing, cross-request TOCTOU — the shapes the labels needed had no proposer signal, and the one near-miss (a rank-2 touch on `Check.ping`) became a different real bug on the same target. The run's single recall hit is an *open* partial, and it arrived the honest way: the curator matched nothing, the independent label matcher found the same-region partial, and the curator adopted it over the initial none. Two matchers earn their keep exactly once here.

Two more honest entries. The one wrong-direction verdict (H4.1): a tester confirmed shared `Ping.n` through the refresh race, but ping's UPDATE, re-read and INSERT sit in one `transaction.atomic` block whose row lock serializes the interleaving — the confirmation never carried transaction scope. And the curator's own error: the pre-registration says the packet trees hold zero candidate data-model asserts, read off an output key the tool doesn't emit. The models do carry asserts — 7 of 8 packets violated 3–7 each — computed and discussed in five reports but kept as findings nowhere, so P45a fails on "kept", not on "exist". The frozen scores keep their values; the run's analysis records the correction with the mechanism. The drawer stays open for the curator too.

Interfaces are the standing zero: no publish, no refinement, no composition call in 1,286 tester tool calls (one `--help` read, counted then discarded). The skill gap is now measured on services as well as libraries. What the run moves: platform modules go from 0 specs to 38 kept across 5 run directories, and the spec-production ledger is re-counted to match.

Frozen scores: run43 `b0164b4e…`.

*Series note: this post extends the series past its planned 21 parts. Numbering, the series README, and the index update are the owner's call.*

{% include series.html %}

*Evidence note (2026-11-23): the run records this post cites are kept privately; ask the author for access.*
