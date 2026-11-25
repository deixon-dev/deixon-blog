---
title: "bull, examined: a shared timer name matched to its fix, and the same wait-gap found three times"
description: "Eight blind first-looks at the bull job queue in Node.js: a shared lock-renewal timer matched exactly to its own upstream fix, a count-then-listen wait gap found independently on three trees, two fixes that live in Lua where no JS tool can see them — and the misses."
layout: post
series: deixon
part: 20
date: 2026-11-11
---

*Part 20 of 24 in a series on deixon. [Part 14]({% post_url 2026-11-20-evidence-overview %}) opened the file drawer. This post reads the Node drawer all the way through: the first project in a fourth language. Evidence: the run records (kept privately).*

*Level L2 · Needs: comfort reading short JavaScript excerpts. One project, file by file.*

{% include series.html %}

bull is a Node.js job queue over Redis: producers add jobs, workers process them with concurrency, locks, retries, delays and priorities. The tool looked at it eight times. Runs 38 and 41 are cleanroom experiments that set blinded testers on unlabelled code trees — four bull packets per run (plus four on socket.io, then bull again with async and ava); each tester session gets one tree, the engine, and the brief. Each blinded, each on a tree fixed before any tester ran, each working static-only — reading code, never running it. That last clause first, because it bounds everything below: bull verdicts are statically confirmed plus blind-adjudicated, never demonstrated on running code, and the deployment models are unconfirmed guesses at how the code is called, so caller threading is assumed where the verdicts say so. With that stated: the eight testers filed 25 findings (2 withdrawn as superseded), clustered into 15 claim groups, every live subclaim judged real by a fresh blind adjudicator — 23 for 23 — with two exact own-fix matches and one exact open-fix match.

## The exact match: the timer name every job shared

One packet (run38 pkt-c, August 2015) filed four model-level findings and matched its own fix exactly. Its first, in short: concurrent jobs share one lock-renewal timer name, so one job's completion cancels another's renewal, and a finished job's renewer is left running.

Every processed job arms a lock-renewal timer under the same hardcoded name (`lib/queue.js:516-518`), and every completion clears that name (`lib/queue.js:556-558`):

```js
var lockRenewer = function(){
  job.renewLock(_this.token);
  _this.timers.set('lockRenewer', _this.LOCK_RENEW_TIME / 2, lockRenewer);
};
// ...
.finally(function(){
  _this.timers.clear('lockRenewer');
});
```

With concurrency 2, job B's `set` lands while job A's renewer is armed — and `TimerManager.set` overwrites the stored handle without clearing the old one (`lib/timer-manager.js:47-48`):

```js
TimerManager.prototype.set = function(name, delay, fn){
  this.timers[name] = setTimeout(fn, delay);
  this.idle = false;
};
```

So B's arm orphans A's live timer (which keeps renewing a finished job's lock), and A's completion clears the name out from under B (whose lock then expires mid-processing and whose job gets reprocessed). The blind matcher — shown the finding and the upstream fix, never the tree — ruled it **exact** on [`8212cdde5f`](https://github.com/OptimalBits/bull/commit/8212cdde5fb6899215dbb21dcb9590fd196a9da0) ("Fix failing tests", August 2015): the fix replaces the single-name manager with uuid-identified timers, exactly the collision the finding names. The adjudicator judged both subclaims real (verdict). The packet's engine proposed nothing — zero slices on every track — so the tester read `lib/` by hand, wrote three TLA+ specs with controls, and filed from those. The full report is kept privately.

## The thrice-found wait gap

The run's most instructive cluster is one the labels never named. `whenCurrentJobsFinished` reads the active-job count over an async Redis round trip, then attaches `_.after(count)` completion listeners (`lib/queue.js:937-955`):

```js
Queue.prototype.whenCurrentJobsFinished = function(){
  var _this = this;
  var resolver;
  return new Promise(function(resolve, reject) {
    _this.getActiveCount().then(function(count) {
      if(count === 0){
        resolve();
      }else{
        resolver = _.after(count, function(){
          // ... remove listeners, resolve
        });
        _this.on('stalled', resolver);
        _this.on('completed', resolver);
        _this.on('failed', resolver);
```

A job completing inside the count-then-listen gap emits before the listeners attach, so the count is never reached and `pause(true)`/`close()` hang. Three packets on three trees (December 2016, November 2016, February 2017) filed it independently — all adjudicated real (verdict) — and none of the three trees' labels is this defect. It is the strongest signal in the Node runs that tester-authored slices converge on real defects without proposer guidance: same mechanism, three blind sessions, zero proposals to point at it.

## The boundary the tool cannot cross

Two of run38's four bull fixes live where no JavaScript tool can see them. `c8e8ceeef0` ("atomically remove a job") adds a lock-ownership check inside the `moveToCompleted` *Lua script*, and `456b13d1b9` (double-processing) adds an `ensureActive` guard inside the `takeLock` *Lua script* — both defects and both fixes in Lua string literals executed by Redis. The JS wrappers the extractor reads are unchanged in the relevant sense. These packets are unfindable-by-construction for a JS-static tool, and the run counts them as misses honestly rather than excluding them.

What the testers found instead, on those same trees, verified too. pkt-a's NOSCRIPT retry re-sends the caught error as the script arguments (`scripts.js:32-36`), breaking recovery after any Redis flush — filed twice, on two packets, both real (verdict). pkt-b's `PriorityQueue.run` inverts priority order every other pass by reversing the queue list in place — real, deterministic (verdict). And run41's pkt-a matched its own fix exactly: a stale worker's lockless failure path corrupting a finished job, the defect [`d42e60c9bc`](https://github.com/OptimalBits/bull/commit/d42e60c9bc7e5f5717046c17a86e374ce0a7adf9) ("check for lock before marking complete/failed") fixes by re-obtaining the lock first.

## The misses

Five bull packets missed their labels, all the same way: the tester filed real bugs that are not the fix. The redlock-adoption refactor (run41 pkt-b) is too diffuse for one slice — its tester instead matched a *later* fix exactly (the renewal re-arm, as an open match). The one-line `stopTimer` reorder (run41 pkt-d), the `close()` hang (run38 pkt-b) and the Lua takeLock guard (run38 pkt-d) each sat beside louder defects the testers chose instead. With zero proposals on every bull tree, every choice was the tester's own reading — and every choice verified. That is the run pair's shape in one line: recall 3 of 8 packets matched (2 own, 1 open), precision 23 of 23.

## Numbers

Eight packets, 25 findings filed (2 withdrawn), 23 live subclaims in 15 groups, 23 judged real — 14 races, 9 deterministic. Three label matches (2 own exact, 1 open exact), all blind-matcher verdicts (MATCHES). Zero wrong-direction verdicts, zero isolation violations. Wall time 0.22–0.39 h per packet. Frozen scores: run38 `9388ddbb…`, run41 `44b16beb…`.

*Evidence note (2026-11-23): the run records this post cites are kept privately; ask the author for access.*
