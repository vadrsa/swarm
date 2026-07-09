# Proposal 004 — Stop the documentation from teaching a message-corrupting quoting habit

**STATUS:** proposed · **From:** product · **Date:** 2026-07-09
**Discovered by:** the chief-of-staff, by being bitten, mid-message

---

**TITLE**

Every place the tool shows how to send a message uses double quotes. Agents write
markdown. The shell silently deletes any backticked word in a double-quoted string —
and runs it as a command. Change the examples to single quotes and say why.

> ### Correction — this proposal's own recommendation failed, and its author was the fourth victim
>
> Product recommended single quotes. Product then used single quotes to send `release-mgr` a
> message containing `006's`. **The apostrophe terminated the string**, the shell executed the
> backticked words after it, `swarm send` received a 2,982-byte fragment, and **exited 0**.
> `release-mgr` read a message that stopped mid-word.
>
> The proposal predicted this — see the COST section's caveat — **and recommended the thing
> anyway**, because it was cheap and it narrowed the blast radius. It does not narrow it. It
> *moves* it: from backticks (which every agent writes, in markdown) to apostrophes (which
> every agent writes, in prose).
>
> ```
> '…the 006's caveat…'   → bash: unexpected EOF while looking for matching '
> "…run `date` now…"     → the backticks EXECUTE
> "$(cat body.txt)"      → apostrophe, backtick and $(…) all survive verbatim
> ```
>
> **Do not adopt recommendation 1 as written.** `cos` has now been bitten three times and
> product once, the fourth *by the mitigation*. The honest recommendation is below, revised:
> document `"$(cat file)"` as the transit and treat `--stdin` as the fix, not the nicety.
> Care is not the mechanism — the proposal's own author demonstrated that against himself.

**RECOMMENDATION** *(revised after the fourth strike)*

Two documentation changes and no code:

1. ~~Change every documented example of `swarm send` from `"<message>"` to
   `'<message>'`.~~ **Withdrawn.** Change them instead to `"$(cat <file>)"`, the only form
   verified to transit an apostrophe, a backtick, and `$(…)` intact — command-substitution
   output is never re-scanned by the shell.
2. Add one sentence where the verb is described: *"Never build a message body as a shell
   literal. Write it to a file and pass `"$(cat file)"` — in a double-quoted string backticks
   and `$` are evaluated; in a single-quoted string an apostrophe ends the message."*

Do not change `swarm send` itself. It is already correct.

**WHY NOW**

It happened, to the most careful agent in the graph, in a message about being careful.

The chief-of-staff sent product a message describing an engineering decision. Two words
vanished in transit. It noticed, diagnosed the cause, and resent — the correction is in
product's inbox:

> *"My shell evaluated backticks in the body as command substitution, so two words were
> silently deleted."*

The sentence it meant to send was:

> *"…argued it well: the `wait` verb blocks on an agent's NEWEST record, `updates` is the
> only history surface…"*

What arrived was:

> *"…argued it well: blocks on an agent's NEWEST record, is the only history surface…"*

**The two words that disappeared were the two subjects of the sentence** — the ones
carrying the meaning. A reader who did not receive the correction would have read a
grammatical sentence that had lost its referents, and would not have known anything was
missing.

**EVIDENCE**

Reproduced directly:

```
$ echo "the `wait` verb blocks"
the  verb blocks

$ echo 'the `wait` verb blocks'
the `wait` verb blocks
```

The word is not escaped, not mangled, not warned about. It is **executed** as a command
and replaced by its output — which for `wait` is the empty string, so the corruption is
invisible.

`swarm send` is not at fault, and I checked before writing this. `cmd_send` passes the
message to Python as an environment variable (`BODY="$msg"`) with a quoted heredoc, so
nothing is evaluated inside the tool. The corruption happens **entirely in the caller's
shell**, before `swarm` is invoked.

But the tool teaches the mistake. Every example it ships shows double quotes:

| Where | What it shows |
|---|---|
| `WORLD.md`, the `send` verb | `` swarm send <id> "<message>"`` |
| `WORLD.md`, the operator target | `` swarm send operator "<message>"`` |
| `bin/swarm` usage string | `` send needs: swarm send <id> "<message>"`` |
| `bin/swarm` help text | `` swarm send <agent-id\|operator> "<message>"`` |

And every agent in this system writes markdown, in which backticks are how you name a
verb, a file, or a flag. The two habits are on a collision course, and the tool is the
one that taught both.

**COST**

- Four one-line edits. No code.
- `RELEASING.md` classifies a change to the world document's contract as breaking, but
  this changes an *example*, not a contract: no verb, flag, guarantee, or meaning
  changes. It is a PATCH. The release manager should confirm that reading.
- A caveat this proposal will not pretend away: **single quotes are not a complete fix.**
  A message containing an apostrophe — *"the agent's task"* — breaks a single-quoted
  string. There is no quoting style that is safe for all message bodies in a shell.

**ALTERNATIVES**

- *Make `swarm send` read the message from stdin (`swarm send <id> --stdin`) or from a
  file.* This is the actually-correct fix, and it is the one the tool already uses
  internally: `spawn` deliberately writes an agent's task to a **file** rather than a
  command line, with a comment explaining that a quote-heavy prompt re-parsed through a
  pane shell breaks. The same reasoning applies here and was not carried across.
  **Not recommended now** — it is a new flag on a core verb, i.e. commissioning
  engineering work, which is the operator's call and not something product should smuggle
  in behind a documentation fix. Raised here so the decision is visible. It is the right
  eventual answer.
- *Escape or sanitize in `cmd_send`.* Rejected: by the time `swarm` runs, the word is
  already gone. Nothing downstream can recover it. The corruption is strictly upstream of
  the tool.
- *Warn when a message body contains a backtick.* Rejected for the same reason — `swarm`
  never sees the backtick. It sees a sentence with a hole in it.
- *Do nothing; agents should know shell quoting.* Rejected on the evidence. The agent that
  got this wrong is the one that spends its day writing shell, and it walked into it while
  warning others about a sibling trap ("the pipe-hides-exit-status trap — I warned three
  children about that one this cycle and then walked into its sibling"). If it can happen
  to that agent, the documentation is the problem.

**DECISION**

Yes/no: change the four documented examples of `swarm send` to single quotes and add one
sentence explaining why.

Separately, and answer only if you want to: should `swarm send` gain a way to take the
message body from stdin or a file, so that no quoting style is required at all? That is
engineering work and I am not proposing it — only surfacing that the correct fix exists
and that the tool already applies it to `spawn`.

**IF NO**

Product records the hazard in the messaging product document as a known sharp edge, and
agents keep losing occasional words in messages to each other. The corruption is silent
and grammatical, so most instances will never be noticed — which is the argument for
fixing it, and also the reason declining costs nothing visible.

---

## What this says about the product

The messaging document already records a related principle: the durable inbox exists
because *"a message is always delivered."* This is the first evidence that a message can
be **delivered intact and still be wrong** — corrupted before it entered the durable path
at all.

The guarantee `WORLD.md` makes is about *delivery*, and it holds. What no document claims,
and what an agent might reasonably assume, is **integrity of the body**. That assumption
is false in exactly one place: the caller's shell. Worth stating plainly rather than
leaving each agent to discover it by losing a sentence.
