# Bot teams: a driver bot decides, dev bots build

Most runs have a person answering specfence's questions: by MCP elicitation, or through the headless
answers file (`.specfence/answers.yaml`). Some teams have no person in the loop. A **driver bot**
supplies the requirements and makes the decisions, and **dev bots** do the building, all under a
framework loop. In that setup the usual rule "the agent MUST NOT answer for the person" is not
enough, because a dev bot can write any file the driver can, the answers file included.

So driver inputs come in a **signed envelope**, `.specfence/driver.json`. The engine checks the
signature against a public key you configure before it reads anything in the envelope. The agent
skill is `src/specfence_engine/skills/bot-team.md`.

## What it guarantees, and what it does not

- **Key pinned in the server's environment: anti-forgery ("pinned driver mode").** If
  `SPECFENCE_DRIVER_PUBKEY` is set in an environment no dev bot controls, such as an
  orchestrator-hosted server, a dev bot cannot get a decision counted that the driver did not
  sign. That holds for decisions passed through a tool and for records written straight into
  `.specfence/`. In this mode:
  - **Records must be backed.** Every verified envelope is archived at
    `.specfence/driver-envelopes/<digest>.json`. A stored decision counts only if it cites an
    archived envelope that still verifies under the pinned key and says the same thing. This
    covers scenario acceptances, forge answers, typed and sharing answers, deployment answers and
    confirmation, and the evidence policy. Anything else is ignored by every gate and listed under
    `unbacked` by `driver_envelope_info`.
  - **`answers.yaml` is not read, and nothing elicits.** All questions go to the driver.
  - **Decisions come only from the envelope.** A relayed golden `accept` or issue `approve`/`file`
    is refused even where the envelope says nothing. Filing needs the envelope's approval as well
    as its filing entry. `golden_approve` and `golden_run` refuse a store holding a property no
    envelope accepted.

  Two limits remain. A dev bot can delete records or archived envelopes, which stalls the run
  but forges nothing. It can also remove a property from the golden store; nothing detects that,
  because the store keeps no signed list of what it must hold.
- **Key in a workspace file (`.specfence/driver.pub`) or an agent-spawned server:
  tamper-evidence only.** A dev bot can replace the key, or point its own server at its own key.
  Stored records are not re-checked, so a hand-written record counts. Every applied input still
  records its key id, so the audit trail shows which key decided, but that is evidence, not proof.
- **No envelope and no pinned key: nothing changes.** Elicitation and the answers file work exactly
  as before.

## Setting it up

1. **Make keys on the host, next to the driver:**

   ```bash
   python -m specfence_engine.driver keygen --out ~/driver-keys --key-id requirements-bot
   ```

   This writes `driver.key` (mode 0600) and `driver.pub`. The private key MUST NOT enter the
   workspace.

2. **Configure the public key.** Either set `SPECFENCE_DRIVER_PUBKEY=requirements-bot:<hex>` in the
   server's environment, or copy `driver.pub` to `<root>/.specfence/driver.pub`. If both are set,
   the environment wins. Exposing the public key is safe.

3. **Each round, sign what the driver has said so far:**

   ```bash
   python -m specfence_engine.driver sign --key ~/driver-keys/driver.key --payload payload.json --out driver.json
   ```

   ```bash
   python -m specfence_engine.driver verify --pub ~/driver-keys/driver.pub --envelope driver.json
   ```

   Then place `driver.json` in `<root>/.specfence/`.

## The payload

Every section is optional except `driver`:

```json
{"driver":    {"id": "requirements-bot"},
 "answers":   {"deployment": {}, "evidence": {}, "options": {"_unlisted": "default"}},
 "free":      {"<question-id>": "<free-text answer to an ask_user question>"},
 "scenarios": {"accepted": ["<scenario digest>"]},
 "golden":    {"accept": [{"spec": "Pool.tla", "cfg": "Pool.cfg", "lang": "tla"}]},
 "issues":    {"<bundle-id>": "approve"},
 "filing":    {"<bundle-id>": {"title": "", "repo": "", "body_extra": ""}}}
```

`answers` takes the same sections as `answers.yaml`. Envelope answers and answers-file answers are
merged. If the two give **different** answers for the same subject, both are refused until one of
them changes, so neither source wins silently. Deployment answers must name a single profile. In
pinned driver mode `answers.yaml` is not read at all.

## The loop

1. A dev bot runs headless. When a tool returns open questions instead of asking them, the
   framework (never the dev bot) reads `open_questions(root)` and `driver_envelope_info(root)` and
   passes the questions to the driver.
2. The framework signs the driver's answers into a fresh `driver.json`. The dev bot then calls the
   same tool again, and the engine verifies the envelope before reading it. A recorded answer shows
   `via: driver-envelope`, the key id, and the digest of the envelope it came from.
3. **Decisions use `decision="driver"`:** `golden_review(..., decision="driver")` applies the
   envelope's golden acceptances, `review_issue_bundle(bundle, decision="driver")` applies its issue
   approvals, and `file_issue(bundle, ..., decision="driver")` files with the envelope's repo, title
   and body. If the envelope covers a decision, a relayed `accept`, `approve` or `file` from the
   agent is refused. In pinned driver mode it is refused even when the envelope does not cover it.
4. **Re-sign every round.** An envelope holds only what the driver had said when it was signed, so
   a stale envelope answers stale questions. In pinned driver mode, records from earlier rounds keep
   counting through the archived copies of their envelopes.

## When it refuses

If an envelope is present but bad (malformed JSON, no public key configured, a key-id mismatch, a
schema error, or a signature that does not verify), every tool that would read it refuses. It is
never silently ignored. To diagnose without refusing, call `driver_envelope_info(root)`: it reports
whether an envelope is present, whether it verifies, and which sections it covers. It also reports
whether the key is pinned, and lists the `unbacked` records: stored decisions that pinned mode
ignores, with the store and the reason for each. In a pinned run this list should be empty. An
entry means something wrote to `.specfence/` outside the driver's channel. When the envelope carries deployment
answers, a `deployment` block names their profile and the stored models they reach (`reaches`). A
proposal under another profile counts as reached when the envelope corrects its profile. If models
are stored and none is reached, a `note` says so: the answers fill nothing until the profiles line up.
