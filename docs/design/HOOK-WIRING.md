# HOOK-WIRING — a cold, per-message, timeout-bounded engine hook on the operator send path

**Author:** `hook-drafter`, for `hook-scout`. Written at `main@834fec4`,
2026-07-11; revised same day after two adversarial reviews — `hook-red`
(`.swarm/research/hook-red-review.md`) and the independent `hook-redcheck`
(`.swarm/research/hook-redcheck-review.md`) — consolidated **3 KILL / 7 WOUND,
all repaired in place, none changing the recommendation** (races-allowed for v1,
which the KILLs *strengthen* — the "structural certainty" the alternative was
sold on turned out not to be real). Repaired sites say what changed and which
finding forced it. Fourth iteration of the decision-engine wiring, and the first
to **edit `bin/swarm`**. The three prior docs — `DECISION-WIRING.md` (`DW §n`),
`PIPELINE-WIRING.md` (`PIPE §n`), `PROXY-WIRING.md` (`PROXY §n`) — treated the
tool as off-limits and built additive file-conventions; PIPE §5b concluded a
*hard* engine-first guarantee is "unbuildable on this substrate" — and, as the
KILLs below confirm, PIPE was **right**: this document does not overturn that,
it finds a *smaller* thing (a T-bounded narrowing of the same races-allowed
tendency) that the send path can carry. The operator overruled the framing, and
then — after an initial custody framing — corrected the *shape* of the overrule
to its final form, in their own words:

> *"The engine is cold on each message that lands in this intermediary mailbox.
> The HOOK — the hook, not the engine — is called with the message, with a
> timeout. If it times out, we send the message to the operator. If it doesn't
> time out and returns an answer, we go based off the answer."*

This is decisive and it simplifies the design radically. There is **no standing
engine, no custody queue, no reclaim sweep, no mid-flight-death problem, no
wedged-alive problem.** The engine is a **cold, per-message, timeout-bounded
hook invocation** on the operator-bound send path — the tool's *own idiom*
(`cmd_deliver`, `cmd_event` are cold binaries invoked per event via settings
hooks, bin/swarm:804-817). Timeout **or** crash **or** unconfigured ⇒ the
message proceeds to `queue/operator/` as-is, **in code** — a fail-open branch,
not a rule a human remembers. This document designs that hook honestly, solves
the three problems the cold shape *does* raise (durability ordering, sync vs
detached, cold-start economics), and recommends for or against building it
against PIPE's races-allowed baseline.

**Evidence discipline:** every load-bearing claim cites `DW §n`, `PIPE §n`,
`PROXY §n`, a `WORLD.md` line (`W:n`), or a `bin/swarm:line` at `main@834fec4` —
re-derived against that commit. Grants, the auto-answer ritual, override, kill,
training, and the four interruption states are **inherited whole from DW and
re-used, not re-derived**; this document touches only what the cold hook
changes.

---

## The recommendation in one paragraph

**Buildable, and recommended AGAINST for v1 — and the reviews make the case
*against* stronger, not weaker.** The cold-hook shape is mechanically clean: a
branch in `cmd_send` that, when an engine hook is configured and
`to=="operator"`, writes the message to `queue/operator/` **first** (durable,
never dropped — the design's soundest part, confirmed by both reviews) and
*then* invokes `swarm engine-hook <file>` with a timeout — a cold
`subprocess.run(..., timeout=T)`, exactly how the tool already runs its hooks.
If the hook returns an answer within `T`, the hook performs DW's claim ritual
(move the file to `delivered/`, hand-tagged claim line, reply to the original
asker **in the engine's own wire name** — which requires the tool to *inject*
that identity into the cold invocation, §7/§3: the correction hook-redcheck
forced). If it times out, crashes, or is not configured, the message is
**already sitting in `queue/operator/`** — today's behavior, exactly, with zero
recovery machinery (§4). Write-then-invoke is load-bearing: a pre-write hold
would let a killed send process **silently drop** operator mail (W:51-53
forbids); writing first makes durability independent of the hook (§4, CONFIRMED
by both reviews).

**What the reviews killed, and what survives.** The first draft claimed
synchronous invocation "delivers strict engine-first ordering" and therefore
"structural certainty that the operator's queue is hook-passed." **That is
false, and it is now removed** *(KILL-1/KILL-2)*: `subprocess.run` blocks the
*sender's* process; the human reads `queue/operator/` via a **separate** `swarm
ps` on their own schedule (bin/swarm:933-943), consulting no shared state the
block touches — so **nothing on this substrate orders the human relative to the
hook.** PIPE §5b said exactly this and said it at the *invariant* level ("it
stands even if someone later added an operator-delivery path to bin/swarm",
PIPE:346-347); the send-path branch is a **new instance of the family PIPE
already swept** (its mechanism-#1, "tool code on the path"), not an escape from
it. The cold hook survives PIPE's barrier-kill *only because* sync does **not**
make the human wait — and precisely because it is not a barrier, it does **not**
deliver the certainty a barrier would. What sync actually buys is a **T-bounded
narrowing of the same races-allowed tendency PIPE §5c already describes**, made
safe by mv-and-abort (DW §1c) — reliable engine-first *reading*, never provable
engine-first *ordering*.

**The three real problems the cold shape raises** are unaffected by the KILLs:
**(1) durability ordering** — write-first, §4 (CONFIRMED); **(2) sync vs
detached** — **synchronous**, because detached degrades even the T-bounded
tendency into plain races-allowed, and the sender-latency is affordable at the
measured operator-mail volume (PROXY §2a: ~37 lifetime operator-bound messages,
a handful/day — the branch is scoped to `to=="operator"` so the hot plane never
blocks, §5); **(3) cold-start economics** — a cold model invocation per message
is realistically **tens of seconds, not single-digit**, so `ENGINE_HOOK_TIMEOUT`
is a tens-of-seconds block and **timeouts are a modal outcome, not a tail risk**
(§6, R4): most items would pass *by timeout*, not by decision, which further
guts the certainty case. Registration is *"the hook is configured or not"* — a
marker file `.swarm/engine/hook` carrying **two lines: the engine's wire name
and the command** (the name is mandatory — §7 — so the tool can inject the
identity), world-readable, deletable = disable (§2). Identity: the answer goes
out in the engine's own name **only if the tool injects `SWARM_AGENT_ID` into
the cold invocation** — a bare `subprocess.run` inherits the *sender's* env and
would launder the reply under the OPERATOR header (KILL-3, §7); the fix is an
explicit `env=`. Pass = *absence of a claim* (the message already waits under
its true sender), so pass never launders (§7, CONFIRMED). **Net cost, priced
honestly:** **~60 new bin/swarm lines** (the `cmd_send` branch + helper ≈ 20,
*plus* the ~40-line `swarm engine-hook` verb the first draft omitted from the
headline — R8) + a new verb + a marker file + a timeout constant + **one
CONTRACT-CLASS amendment that, for the first time in this lineage, puts
tool-invoked code on the operator path** (§8, R7). **Against races-allowed's
zero machinery and zero contract touch**, the hook buys only a T-bounded
tendency-narrowing — not certainty — and the record shows no harm even that
would have prevented. **Recommend races-allowed for v1.** The pilot condition
that would once have flipped the choice — "the operator names structural
certainty a hard requirement" — is now **void**: no operator sentence can make
the substrate carry a guarantee it structurally cannot (§12). The hook wins only
in the narrower case §12 states.

---

## 1. What the correction changed, and the insight that survives

**The custody framing is dead.** An earlier version of this design routed
operator mail into a standing engine's *custody queue* and needed a coded
reclaim sweep to rescue mail when the engine died or wedged. The operator's
correction dissolves all of it: there is no standing engine to die, no custody
to strand, no reclaim to witness. **Cut entirely:** standing-engine spawn,
custody queue, reclaim-on-`cmd_deliver`, the idle-tree tail, and the
wedged-but-alive analysis. Those were problems of a *persistent* engine holding
mail; a *cold per-message hook* holds nothing between messages.

**Where this sits relative to PIPE — stated honestly** *(rewritten after
hook-red R2 KILL: the first draft claimed "PIPE §5b missed the send path," which
is a strawman).* PIPE §5b did **not** miss the send path. Its argument is at the
*invariant* level, not the code level: "This reason is about the invariant, not
the code: **it stands even if someone later added an operator-delivery path to
bin/swarm**" (PIPE:346-347). PIPE enumerated **six** mechanisms for ordering two
hands and killed all six; **mechanism #1 is "tool code on the delivery path"**
and #2–#5 are the shared-consulted-state forms (PIPE:362-404). A send-path
branch in `cmd_send` is a **new instance of that same family — not an escape
from PIPE's sweep.** PIPE killed the family *as a barrier*: any component the
human must wait on before reading is a single point of failure the moment it can
block the human. **The cold hook survives that kill only because it is not a
barrier** — sync blocks the *sender*, never the human (the KILL-1 fact, §5), so
the human is never made to wait on it. And that is precisely why the hook cannot
deliver the certainty a barrier would: a mechanism that does not order the human
cannot *guarantee* the human sees only hook-passed mail. Both KILLs point the
same way — the send path is real code on a real path, but on *this* substrate it
can only narrow a tendency, not enforce an order. What the correction *does*
keep is the **shape**: the decision happens at send time, in `cmd_send`, via a
cold sub-invocation — precisely the idiom of `cmd_deliver`/`cmd_event`, cold
`swarm` sub-invocations wired as command hooks (bin/swarm:804-817:
`{self_path} deliver` etc.). The engine is not an agent with a pane and a queue;
it is a **binary the tool calls with the message and a timeout.** That native
idiom is why the two hardest problems of the custody design (mid-flight death,
wedged-alive) do not exist here: a cold invocation that times out or crashes
leaves the message already durable in `queue/operator/` from before the
invocation began (§4).

---

## 2. Registration: "the hook is configured or not," a marker file

The send-path branch must fire **only when an engine hook is configured**, and
be a pure fail-open otherwise (§3). The tool already has an idiom for "a hook is
wired": per-agent settings JSON mapping events to `swarm` sub-commands
(bin/swarm:810-817). The engine hook is the same shape — a command the tool
invokes — but it is invoked from *inside* `cmd_send`, not from a Claude session's
event loop, so it cannot live in a session's settings file. It lives in a
**marker file the send path reads**:

```
.swarm/engine/hook          # TWO lines:
decision-engine             #   line 1: the engine's WIRE NAME (mandatory)
/abs/path/to/swarm engine-hook   # line 2: the command to invoke
```

**The name is mandatory, not decorative** *(added after hook-redcheck finding 1
KILL — see §7).* Because the hook is a *cold subprocess with no pane*, the tool
must **inject** the engine's `SWARM_AGENT_ID` into the invocation (§3, §7); the
name in line 1 is the identity the tool injects. Without it the reply launders
under the OPERATOR header — the exact DW/PROXY kill. So registration witnesses
*two* facts: that a hook is configured (the file exists) and *what wire identity
it speaks as* (line 1).

- **Existence is registration; line 1 is the identity, line 2 is the command.**
  `registered_hook(root)` is a `try/open/read/splitlines` returning `(name,
  command)` or `None` on any error (the bulletproof discipline of `cmd_deliver`,
  bin/swarm:609). Absent file ⇒ `None` ⇒ fail-open branch (§3). `engine_name` is
  defined precisely as **line 1 of this marker** — the referent the §3 recursion
  guard needs.
- **World-readable** (W:28 discipline; any hand can `cat` it to see whether the
  send path is armed) and **deletable = disable:** `rm .swarm/engine/hook`
  disarms the branch instantly, tool-wide, with no cooperation — the tool reads
  the file's absence on the next send. This is the hardest kill layer (§9), and
  it is *stronger* than DW's soft kill (DW §7, which rides the engine's briefed
  re-read) because the **tool** reads this file, not the engine.
- **Not tool state in the DECISIONS sense.** One line of world-readable text
  under `.swarm/`, the same shape as DW's grant ledger (DW §3a). It stores one
  fact — "operator-bound sends should invoke this command" — which a file can
  witness (W:3-5).

**Why a marker file and not a settings entry:** the settings files
(bin/swarm:810-817) wire hooks into *Claude sessions'* event loops
(`UserPromptSubmit` → `swarm deliver`). The engine hook fires from `cmd_send`,
which is not a session event — it is the tool relaying a message. So the tool
needs to read the hook command at send time, from a place `cmd_send` looks. A
marker file is that place; a session settings file is the wrong layer. (The
marker could later be promoted into a top-level `.swarm/config.json` if the tool
grows one, but a single-purpose marker is the minimal honest shape today.)

---

## 3. The send-path branch: invoke-then-decide, fail-open by construction

The branch sits in `cmd_send` after the durable write (§4 argues the ordering).
The current send block is **bin/swarm:912-919** (record → `send_size_error` →
`queue_put`), and the doorbell special-case is **bin/swarm:921-930** *(cite
ranges corrected after hook-redcheck finding 5 — the first draft wrote
"912-923"/"921-923").* Diff shape:

**Current (bin/swarm:912-919):**
```python
    rec = {"to": to, "from": sender, "ts": now_ms(), "body": body}
    err = send_size_error(rec, relation(sender, to, parents_of(agents)))
    if err:
        die(err)
    try:
        queue_put(root, rec)
    except OSError as e:
        die(f"could not queue message: {e}")

    # Doorbell, best-effort (bin/swarm:921-930). ...
    if to != "operator":
        ...
```

**Proposed** *(the `env=` injection and the marker-derived name are the
hook-redcheck-finding-1 KILL fix; `from_stdin_reply` is deleted per hook-red R3
— the `to=="operator"` + `sender != eng_name` guards suffice, argued below):*
```python
    rec = {"to": to, "from": sender, "ts": now_ms(), "body": body}
    err = send_size_error(rec, relation(sender, to, parents_of(agents)))
    if err:
        die(err)
    try:
        fn = queue_put(root, rec)          # (1) DURABLE FIRST — never dropped (§4)
    except OSError as e:
        die(f"could not queue message: {e}")

    # Engine hook. FAIL-OPEN: only for operator-bound mail, only if configured,
    # and NEVER for the engine answering (the eng_name guard). The message is
    # ALREADY durable in queue/operator/ above; the hook can only MOVE it (claim)
    # or leave it (pass). Timeout/crash/absent => it stays in queue/operator/ = today.
    reg = registered_hook(root)            # (eng_name, command) or None if absent
    if to == "operator" and reg and sender != reg[0]:
        eng_name, command = reg
        # Inject the swarm env contract — WITHOUT this the cold child inherits the
        # SENDER's env and my_name() resolves to the asker, or "operator" when unset,
        # laundering the reply under the OPERATOR header (bin/swarm:52-53, 830; §7).
        env = {**os.environ, "SWARM_AGENT_ID": eng_name, "SWARM_DIR": root}
        try:
            subprocess.run(command.split() + [fn], env=env,
                           timeout=ENGINE_HOOK_TIMEOUT, capture_output=True)
        except Exception:
            pass                            # timeout OR crash => leave it in queue/operator/
        # Whatever the hook did (claimed & answered as eng_name, or nothing), we're
        # done: claimed => file in queue/operator/delivered/, asker answered as the
        # engine; not claimed => file waits for the human. Never dropped either way.

    # Doorbell unchanged (bin/swarm:921-930): operator is a mailbox, no doorbell.
    if to != "operator":
        ...today's logic...
```

Five properties, each a code fact not a remembered rule:

1. **Fail-open is `reg is None` OR the `subprocess` raising `TimeoutExpired`/any
   exception.** In every one of those cases the message is *already* in
   `queue/operator/` from the durable write above, untouched — byte-identical to
   `main@834fec4` **on these non-claiming branches** *(scoped after hook-red R11 /
   hook-redcheck 4: the claimed-then-crashed branch is NOT byte-identical — it is
   DW state-3, §9).* The operator's "if it times out, we send the message to the
   operator" and "unconfigured ⇒ as-is" are the *same* branch: do nothing more,
   the file is already there. **The engine-absent and engine-timeout-without-claim
   send paths are byte-identical to today** (H-F2).
2. **The hook can only claim-or-pass; it cannot drop.** Because the write
   preceded the invocation, the hook operates on an *already-durable* file. If it
   answers, it moves the file to `delivered/` (DW §3b claim). If it does nothing
   (timed out, or chose to pass), the file stays in `queue/operator/`. **There is
   no interleaving where the message leaves the filesystem** (CONFIRMED by both
   reviews — the design's soundest claim). One honest caveat the reviews forced:
   if the timeout SIGKILLs the child *after* its claim `mv` but *before* the
   claim line, the file lands in `delivered/` **mis-recorded, not lost** — the
   bytes survive, the record can be corrupt (§9, hook-redcheck 2/4).
3. **Identity must be injected, or the reply launders** *(rewritten after
   hook-redcheck finding 1 KILL).* The `env={..., "SWARM_AGENT_ID": eng_name,
   "SWARM_DIR": root}` on the invocation is **not optional plumbing** — it is the
   only thing that makes "the engine answers in its own name" true. A bare
   `subprocess.run` inherits the sender's env, so inside the hook `my_name()`
   (bin/swarm:52-53) would resolve to the *asker* (answering itself) or to
   `operator` when unset — the OPERATOR-header laundering DW/PROXY killed. The
   tool injects `eng_name` (marker line 1, §2) exactly as `cmd_spawn` injects it
   into a pane (`--env SWARM_AGENT_ID={name}`, bin/swarm:830). §7 is the full
   argument; the `env=` here is its mechanism.
4. **The `sender != reg[0]` guard prevents recursion, and it is sufficient
   without `from_stdin_reply`** *(deleted per hook-red R3 — it was an undefined
   symbol in the safety predicate).* `reg[0]` is `eng_name`, the marker's line 1
   (§2) — a real, known referent. Two facts make the single guard enough: **(a)**
   the branch is `to=="operator"`-gated, and the engine's *answers* go to the
   *asker* (`to==<asker>`, DW §3b), never to `operator`, so a reply never enters
   the branch at all; **(b)** the one case where an engine action *does* send to
   `operator` (e.g. the engine escalating something itself) is caught by `sender
   != eng_name` — the engine's own env carries `SWARM_AGENT_ID=eng_name`, so its
   operator-bound send skips the hook and lands directly, no self-invocation.
   No third guard is needed.
5. **`ENGINE_HOOK_TIMEOUT` is the one new constant** (§6 prices it — realistically
   tens of seconds, not ~10s). It is the maximum latency a sender pays on an
   operator-bound send (§5, sync).

**Size, honestly** *(corrected after hook-red R8 — the first draft's "~20 lines"
omitted the verb).* The `cmd_send` branch + `registered_hook` helper is **~20
lines**; the `swarm engine-hook` **verb is a further ~40 lines** of new
bin/swarm code (§11) — it runs the DW decision and, on an answer, the claim
ritual with the injected identity. **True new-bin/swarm cost: ~60 lines + a new
verb**, and §12 weighs *that* number against races-allowed's zero, not the ~20.

---

## 4. Problem (1) — durability ordering: write first, then invoke

**The operator named this as the design's substance, and the ordering is not
optional.** Two orderings are possible; only one is safe.

**Write-first (recommended):** `queue_put` the message into `queue/operator/`
*before* invoking the hook. Consequences:

- The message is **durable the instant `cmd_send` commits it** — the same O_EXCL,
  never-overwrite, never-drop guarantee `queue_put` gives every message today
  (bin/swarm:252-275). The hook's existence, success, timeout, or crash cannot
  un-write it.
- **On a returned answer,** the hook performs the claim ritual: it moves the file
  from `queue/operator/` to `queue/operator/delivered/` (the DW §3b claim move,
  `mv`, with a hand-tagged claim line) and replies to the original sender in the
  engine's own wire name. The `delivered/` record then honestly witnesses "an
  engine hand claimed and answered this" — DW's exact semantics.
- **On timeout or crash,** the message is *already* in `queue/operator/`. Nothing
  to recover. The human drains it exactly as today (SEAT §3). This is why the
  cold shape has no mid-flight-death problem: the failure mode of the custody
  design (mail stranded where the human can't see it) is *structurally absent* —
  the mail is in `queue/operator/` from the first microsecond, and the hook only
  ever *removes* it (by claiming) or *leaves* it.

**Invoke-first / pre-write hold (rejected):** hold the message in the send
process, invoke the hook, and write to `queue/operator/` only if the hook passes.
This is **forbidden**, mechanically: if the send process is killed (SIGKILL, pane
closed, machine dies) *during* the hook invocation — a multi-second window (§6) —
the message was never written anywhere and is **silently dropped.** That is
exactly what W:51-53 forbids ("Nothing is ever silently dropped") and what
`queue_put`'s entire O_EXCL design exists to prevent (bin/swarm:252-261: "the
drop WORLD.md forbids"). A pre-write hold trades the never-drop guarantee for a
seconds-wide drop window on every operator message. **Rejected without
exception.**

**The subtle objection, answered: doesn't write-first mean the human could drain
the item before the hook claims it?** Yes — for the duration of the hook
invocation, the item is in `queue/operator/` and a human *could* grab it. This is
the write→claim race, and it is real. **But it is bounded to `ENGINE_HOOK_TIMEOUT`
and it fails safe both ways:**

- If the hook claims first (moves to `delivered/`), a human `mv` of the same file
  fails (POSIX rename exclusivity — DW §1c's claim-race convention, inherited):
  the file is already gone from `queue/operator/`. The human sees it in
  `delivered/` with the engine's claim line and the AUTO-ANSWER reply — no double
  action (DW W-F8).
- If the human claims first, the hook's `mv` fails and the hook aborts its claim
  (DW §1c mv-and-abort). The human handles the item themselves; the engine
  answered nothing. **This is exactly today's races-allowed outcome** (PIPE §5c) —
  the human won the race.

So write-first does *not* give a "hook always claims before the human can touch
it" ordering — **and neither does synchronous invocation** *(rewritten after
hook-red R1 KILL: the first draft claimed sync "guarantees the ordering," which
is false).* Write-first guarantees *durability* — a real, structural guarantee
(the bytes cannot be lost). Sync (§5) guarantees only that the hook's decision
happens before the *sender's* `swarm send` returns — it does **not** order the
*human*, who reads `queue/operator/` via a separate `swarm ps` on their own
schedule (bin/swarm:933-943), consulting nothing the sender's block touches. So
the design has **one guarantee (durability, from write-first) plus one
tendency-narrowing (sync, which shrinks the write→claim window to `T` and leans
on mv-and-abort to make the residual safe)** — not two guarantees. §5 states
this plainly rather than overselling it.

---

## 5. Problem (2) — sync vs detached: recommend synchronous

The operator described a **synchronous** hook: the send blocks up to the timeout.
The alternative is **detached**: write, fire the hook in the background, return
instantly. They differ on exactly the write→claim race §4 raised.

**What sync does and does not buy** *(this bullet rewritten after hook-red R1
KILL — the first draft titled it "delivers strict engine-first ordering," which
is mechanically false).* **On this substrate, nothing orders the human relative
to the hook.** The human reads `queue/operator/` through an independent `swarm
ps` (bin/swarm:933-943) on their own schedule; `subprocess.run(timeout=T)` blocks
the *sender's* process and touches no lock, no flag, no shared state the human's
read consults. So "engine reads first" is a **tendency, not an order** — the same
kind of tendency PIPE §5c's races-allowed already gives, and for the same reason
(the always-awake / just-invoked reader usually gets there first). What sync adds
over plain races-allowed is **narrowing**: the hook's claim-or-pass decision
completes before the sender's `swarm send` *returns*, so the write→claim window
in which a human could grab an item the hook was about to answer is bounded to
`T` (one hook invocation) instead of open-ended. Inside that window the race is
made safe by mv-and-abort (DW §1c, DW W-F8): whoever's `mv` lands first wins, the
loser aborts, no double action. **Sync buys a T-bounded, mv-safe narrowing of the
races-allowed tendency — not an ordering guarantee over the human.** (The first
draft's own next sentence already conceded sync "does not *eliminate*" the race
and "nothing can, on this substrate" — the KILL removed the contradicting claim
above it.)

- **The cost is sender latency:** the sending agent's `swarm send operator` call
  blocks up to `T` (§6: realistically **tens of seconds** for a cold model
  invocation, R4) inside its own turn.

**Detached (rejected for v1):** write, fire the hook with no wait, return
immediately. Zero sender latency — but the write→claim window is now **open-ended,
not `T`-bounded**: `cmd_send` returns, the sender's turn ends, and the hook is
still deciding. A human glancing at `ps` and draining wins the race routinely,
not rarely. mv-and-abort keeps it *safe* (no double action) but detached gives up
even the narrowing — it *is* plain races-allowed (PIPE §5c) with an extra code
branch that buys nothing. So the only reason to prefer the hook at all (the
`T`-bounded narrowing) requires sync; detached collapses the hook into the
baseline it is supposed to improve on.

**Pricing sync's latency against measured volume.** Borrowing PROXY §2a's
measured numbers: **~37 lifetime operator-bound messages** over the whole
recorded history (PROXY §2c / LM §1), against ~127 plane messages/day of which
only ~21/day are operator-authored dispatches and the rest agent-to-agent
(PROXY §2a). Operator-bound mail is **rare** — a handful per day at most. The
send-path branch fires *only* on `to=="operator"` (§3), so:

- **The blocking cost lands on ~a-handful-of-sends-per-day, not the plane.** The
  hot path — agent-to-agent traffic, ~112/day — never enters the branch (it is
  `to != "operator"`, guarded at §3). The sync latency is paid only by the rare
  operator-bound send.
- Each such send pays up to `T` seconds *once*, inside a turn that is already
  seconds-to-minutes long (a Claude turn). A block of even tens of seconds (§6,
  R4) on a once-in-a-while operator send is negligible against turn duration —
  the affordability comes from the *rarity* of operator mail, not from `T` being
  small. This is
  **not** PROXY's interposed-proxy disaster (which serialized the *whole plane*
  through one queue, PROXY §2a) — the branch touches only operator mail, so there
  is no serialization of parallel conversations.

**Verdict: synchronous.** The latency is affordable because operator mail is rare
and the branch is scoped to it; detached buys back that latency at the cost of
dissolving the T-bounded narrowing into plain races-allowed, which defeats the
only reason to build the hook. **The condition under which detached wins:** if
operator-bound volume ever rises to where a per-send tens-of-seconds block is a
real drag (a tree sending operator mail on a hot loop — itself a design smell,
PHIL §9), *or* if the timeout budget `T`
proves to need tens of seconds (§6) making the block painful, then detached +
races-allowed (i.e., just PIPE) is the honest fallback — but that is the
recommendation of §12 anyway.

---

## 6. Problem (3) — cold-start economics: the true recurring price

**Every operator-bound send that enters the branch pays a full cold hook
invocation.** The hook is a fresh process: it must load its grants (the STANDING
GOALS entry, DW §3a), load whatever context the assumed engine needs to judge
the message (its model, its training artifact — the black box the brief assumes,
DW preamble), run the decision, and — on an answer — perform the claim ritual.
Nothing is warm; there is no standing process holding loaded state (that was the
custody design, cut).

**What this sets the timeout budget to — priced at the cold-model reality**
*(rewritten after hook-red R4: the first draft's "~10s" was optimistic to the
point of being the wrong default, which made H-F6 read as a tail risk when it is
modal).* The dominant cost is the engine's decision, which for the assumed black
box is a **cold model invocation per message**: fresh process spawn + model
cold-start + a real completion over grants + whatever context the engine needs.
For any real model that is commonly **tens of seconds, not single-digit.** So:

- **`ENGINE_HOOK_TIMEOUT` is realistically a tens-of-seconds budget** — there is
  no honest single-digit default for a cold model completion. Set it long enough
  that a legitimate decision usually finishes (or the hook times out on most
  messages and the whole exercise degrades to a slow pass-through), and it is
  *by construction* a tens-of-seconds block on the sender's turn.
- **Therefore H-F6 (timeouts dominate) is a MODAL outcome, not a tail risk.** If
  cold invocations routinely brush or exceed `T`, a large fraction of operator
  items pass **by timeout, not by decision** — the hook did not judge them, it
  ran out of time — and the "structural certainty" the hook was supposed to buy
  degrades to "the queue holds items the hook judged *or gave up on*," **at full
  price** (a tens-of-seconds block bought on every operator send to deliver a
  timeout-pass). This is not hidden in a falsifier footnote; it is the expected
  operating point of a cold model-backed hook, and §12's math weighs it as such.
- **This is the hook's true recurring price** — per operator-message, cold, every
  time. Unlike the custody design's one warm pane amortizing load (DW §9 #6), the
  cold hook pays the full load on *every* invocation.

**Why the cold cost is survivable here at all (and was not for the plane).** PROXY
killed the interposed plane proxy partly on turn economics — doubling ~127
messages/day and serializing them (PROXY §2a). The cold hook fires
~a-handful-of-times/day (operator mail only), so the *aggregate* cost that would
be ruinous at plane volume is small at operator-mail volume. But "survivable in
aggregate" is not "cheap per-message": each operator send still eats a
tens-of-seconds block, and a meaningful share of them buy only a timeout-pass.
This is the price §12 weighs against races-allowed's **zero** — and R4 is why
that comparison is less favorable to the hook than the first draft implied.

---

## 7. The identity rule: answer-in-engine's-name is legitimate; write-first makes forwarding unnecessary

**The hook's answer is DW attribution — but ONLY if the tool injects the
engine's identity; a bare invocation launders it** *(this section rewritten
after hook-redcheck finding 1 KILL — the first draft copied DW's phrase "from
the engine's own environment" onto a substrate that had thrown that environment
away).* DW's engine spoke as itself because DW's engine was a **spawned agent
with `SWARM_AGENT_ID=decision-engine` in its pane env** (bin/swarm:830). The cold
hook has **no pane and no env** unless the tool provides one. A bare
`subprocess.run(command + [fn])` inherits the *sender's* environment, so inside
`swarm engine-hook` `my_name()` (bin/swarm:52-53) resolves to:

- **the asker's name** — when an agent ran `swarm send operator` (its
  `SWARM_AGENT_ID` is inherited), so the engine's reply and claim line go out
  `from: <the asker itself>` — the asker is answered *by itself*, relation
  resolves wrong; or
- **`operator`** — when the send came from an env with no `SWARM_AGENT_ID` (the
  human's own shell, the seat), so `my_name()` returns `"operator"` and the reply
  goes out under **`the OPERATOR (the human at the root)`** (bin/swarm:154-155)
  while its body says "the human has NOT read your message." **That is the exact
  OPERATOR-header laundering DW:315-317 ("never the OPERATOR header") and PROXY
  §2c both killed.**

**The fix, load-bearing not incidental:** the tool must invoke the hook with
`env={**os.environ, "SWARM_AGENT_ID": eng_name, "SWARM_DIR": root}`, where
`eng_name` is **line 1 of the marker file** (§2) — exactly as `cmd_spawn` injects
identity into a pane (`--env SWARM_AGENT_ID={name}`, bin/swarm:830). `SWARM_DIR`
is injected for the same reason: the cold child must find its root the way every
other swarm self-invocation does, not by hoping the sender's `cwd` happens to
resolve (hook-redcheck finding 3 — same root cause). **With the injection**, the
hook's `swarm send <asker>` reply carries `from: decision-engine` and the
AUTO-ANSWER marker — the engine speaking as itself (DW §1a.2, the *stronger*
attribution), no laundering. **Without it, §7 is a laundering machine.** The
recursion guard `sender != eng_name` (§3) is coherent only because `eng_name` now
has this real referent (the marker's line 1); the first draft's guard had no
defined name to compare against (hook-red R3). All three of hook-redcheck's
findings share this one root cause — *the design was invoking a swarm identity
without the swarm env contract* — and the `env=` injection closes all three.

**The forward case dissolves under write-first — and this is cleaner than the
custody design.** In the custody framing, "pass" meant the engine had to *forward*
the held message onward to `queue/operator/`, which required preserving the
original `rec["from"]` and thus a new `swarm forward` primitive (the custody
design's §7). **Write-first removes the need entirely:** the message is *already*
in `queue/operator/` under its true sender from the durable write (§4). "Pass"
is simply the hook **doing nothing** — not claiming, not moving. The file stays
where `queue_put` put it, `from: <original sender>`, and `relation` resolves
truthfully from the original sender (bin/swarm:147-163) when the human's side
reads it. **There is no re-send, so there is no `from` to launder.** The
identity-preservation problem the custody design had to solve with a new verb is
*structurally absent* in the write-first cold-hook shape.

- **Answer path:** engine replies as itself (`from: decision-engine`) — legitimate
  (DW §3b).
- **Pass path:** engine does nothing; the message waits under its original sender
  (already written, §4) — no laundering possible, because no message is authored.

The one residual: if a *future* variant wanted the hook to forward with
enrichment (attach a trace to the passed message), that would reintroduce the
forward-and-preserve-`from` problem. This design does **not** do that — pass is
absence (DW §4, DW §8 I3 for the pass subset), and the falsifier H-F3 fires if
any passed operator message shows `from: decision-engine`.

---

## 8. Contract exposure — every touched WORLD.md sentence, one pass

**The novelty, named honestly up front** *(added after hook-red R7 — the first
draft called this "the cleanest of any design," which inverts the truth).* This
is the **first design in the lineage to put TOOL-INVOKED code on the operator
send path.** DW/PIPE/PROXY all left `bin/swarm` untouched and layered convention
on top; their contract touches were about *who may read a queue*. This design has
the *tool itself* invoke a mover on operator-bound mail. That is **heavier**
contract exposure than any predecessor, not lighter — "lighter than the custody
design" (true) does not make it light. The amendment below must carry that
weight, and the `(including this hook)` parenthetical is where it lands (flagged
in (3)).

**(1) "Nothing ever refuses a message to the operator" (W:59).** *Does the hook
refuse?* **No — this half is genuinely sound.** The message is `queue_put` into
`queue/operator/` *first*, always, with the full never-drop guarantee (§4). The
hook runs *after* the message is already the operator's. On timeout, the
operator's instruction is literally "we send the message to the operator" — which
requires no action, because it is *already there*. The hook can only
*claim-and-answer* (a legitimate hand claim, DW §3b) or *leave it*. **There is no
code path where an operator message is refused or dropped** — write-first
guarantees it (CONFIRMED by both reviews). **Not a violation, and never-drop is
independent of the hook** — but this soundness is about *refusal*, not about the
novelty above; the hook still adds tool-invoked machinery to the path even though
that machinery cannot refuse.

**(2) "Delivered means delivered" (W:51) / what `delivered/` witnesses.** When the
hook answers, it moves the file to `queue/operator/delivered/` with a hand-tagged
claim line — exactly DW's engine-hand claim (DW §3b step 1). The `delivered/`
record honestly means "a hand (the engine) claimed this and consumed the turn of
answering it." This is the *same* semantics DW already established and DW's
mailbox amendment (DW §9) already covers ("a hand they have seated in writing
moves the mail to `delivered/`"). **No new strain beyond DW's inherited
amendment** — because, unlike the custody design, mail never transits a second
queue; it is written to `queue/operator/` and either claimed there or left there.
The one-message-one-turn model (W:17-19) holds: an answered message consumes one
turn (the engine's claim-and-answer), a passed message consumes one turn (the
human's eventual drain). No split-across-queues record.

**(3) "Messages to operator wait until the human looks" (W:57).** DW already
amended this to "wait until the human's side looks — the human, or a hand they
have seated in writing" (DW §9). *Does the cold hook need more?* **Marginally —
and less than the custody design did.** DW's amendment covers a *hand that reads
`queue/operator/`*. The cold hook *is* such a hand (it reads and claims from
`queue/operator/`), invoked by the tool rather than running as a session — so
DW's "a hand seated in writing" *nearly* covers it, but "seated" connotes a
standing agent, whereas this is a per-message tool invocation. The honest
amendment names the invocation shape:

**The recommended amendment (mailbox paragraph W:57-61), superseding DW's**
*(wording demoted from "guarantee"-shaped to "tendency"-shaped after hook-red
R6/R7 — the first draft's "within the timeout the hook may claim … or leave it"
read as though the hook reliably gets first look, which KILL-1 disproved):*

> "Messages to `operator` are queued in `queue/operator/` and never refused or
> dropped. When an **engine hook is configured** (`.swarm/engine/hook`), the tool
> invokes it — cold, per message, with a timeout — *after* the message is durably
> queued, in its own wire name from the marker. The hook may, within the timeout,
> claim a grant-covered message (moving it to `delivered/` with a hand-tagged
> claim line and answering the asker in the engine's own name) — but it holds no
> priority over the human: an operator-bound message is ordinary waiting mail
> from the instant it is queued, and whichever hand's `mv` lands first wins. On
> timeout, crash, or with no hook configured, the message simply waits, exactly
> as before. **The human's side — the human, or a hand seated in writing —
> moves the mail to `delivered/` and journals the claim before acting on it; this
> tool-invoked hook counts as such a hand, and is the first tool-invoked mover of
> operator mail the contract admits.**"

**The `(including this hook)` parenthetical was the real contract cost, now made
explicit** *(hook-red R7).* DW's amendment let "the human's side" include a *hand
seated in writing* — a human decision to seat an agent. This amendment stretches
"the human's side" to include a **cold process the tool spawns per message**.
That is the load-bearing move, and the last sentence names it outright rather
than gloss it: for the first time, a tool-invoked mover touches operator mail.
The clause "the operator queue **alone** is drained by its reader: the tool never
delivers there" (W:59-61) is *strained* by this — the tool still does not
*deliver* to the queue (write-first uses `queue_put`, not a delivery path), but it
now *invokes a mover* on it, which the old sentence did not contemplate.

**CONTRACT-CLASS bill: one amended paragraph (W:57-61), and it is the heaviest
contract touch in the lineage** — the first to admit tool-invoked code onto the
operator path. Lighter than the *custody* design's (no custody location, no
reclaim guarantee, no transit-turn) but heavier than DW's/PIPE's/PROXY's, all of
which touched no tool code at all. **Ships with the code**, because the moment the
branch merges the tool behaves this way and a contract that doesn't match the tool
is the off-books failure DECISIONS §1c names (W:66: "this page is the whole
contract").

---

## 9. What is inherited whole, and kill/override

**Inherited from DW, NOT re-derived** (stated once): the grant ledger and
provenance rule (DW §3a), the confidence/threshold composition (DW §2c — grants
gate, score only shrinks within), the auto-answer ritual and body template (DW
§3b), the override ritual and grant-freeze (DW §6), the training feed and
self-training exclusion (DW §5), the claim-race convention (mv-and-abort, DW §1c),
and falsifiers DEC F1–F7 / DW W-F1–W-F8. **The decision logic is inherited whole**
— the hook does not change how the engine decides, answers, learns, or is
overridden. **But one thing does NOT inherit, and the first draft wrongly said
it did** *(hook-redcheck finding 2 WOUND):* DW's *recovery machinery for a
half-completed claim* was a property of a **standing agent** — a live engine with
a journal, a pane, and a seat reconciling its open loops. The cold hook has none
of those. So the recovery *rule* transfers; the *hand that runs it* does not.

**The interruption states, re-graded honestly.** The cold hook holds nothing
across turns — it is a single `subprocess.run`. But `subprocess.run(timeout=T)`
on `TimeoutExpired` sends an **uncatchable SIGKILL to the child**, and the DW
claim ritual is strictly ordered (move → claim-line → answer → record, DW §3b).
So:
- **Timed out / crashed before the claim `mv`** ⇒ message waits in
  `queue/operator/` = DW state 1 (file untouched); the human drains it.
  **Byte-identical to today, and truly no recovery needed** — this is the cold
  shape's genuine gift, and it covers the common case (a hook that times out
  *while deciding* has not touched the file).
- **SIGKILLed *after* the `mv` but *before* the claim line** ⇒ the file is in
  `queue/operator/delivered/` **with no claim line and no answer** — DW state 2/3.
  **This is unrecoverable-but-not-lost, not "inherited verbatim."** The bytes
  survive (hook-redcheck 4 CONFIRM — the message never leaves the filesystem),
  but **no standing hand reconciles it:** there is no engine journal to show an
  open loop, no seat watching the engine's claims, no C16 alarm owner. The orphan
  sits in `delivered/` mis-recorded. **Who would catch it:** the next human (or
  seated hand) draining `queue/operator/delivered/` — a `delivered/` entry with no
  matching claim line in the operator ledger is a visible anomaly on a `grep`, and
  H-F7 (below) is its collector. **Bound on the harm:** the window is one
  `subprocess.run`, *far* rarer than a standing engine's whole-turn crash window
  (DW's baseline) — but rarer is not absent, and the design owns it as a real
  residual rather than inheriting a recovery hand that does not exist.
- **SIGKILLed after answering, before the record** ⇒ DW state 4; the reply is in
  the asker's `delivered/`, so the anomaly is still discoverable — but again by a
  *draining human*, not a standing seat reconcile.

**Kill — three layers, the hardest tool-enforced:**
- **Disarm (hardest):** `rm .swarm/engine/hook`. The send branch (§3) reads the
  absence on the next send and stops invoking — tool-read, no cooperation. Any
  in-flight message is already in `queue/operator/` (write-first), so nothing is
  stranded.
- **Soft kill (freeze grants):** inherited DW §7 — the hook still runs but
  answers nothing (grants frozen), leaving every message for the human.
- **Hard kill:** there is no standing pane to close; disarm *is* the hard kill.
  This is simpler than DW/custody (no `swarm close` needed — nothing persistent
  exists).

---

## 10. Falsifiers — each with a named collector

Inherited: DEC F1–F7 and DW W-F1–W-F8 remain in force for the engine's decision
behavior. The hook adds:

1. **H-F1 — an operator message dropped.** Any operator-bound send that reaches
   neither `queue/operator/` nor `queue/operator/delivered/`. **Collector:** a
   test on the send path (pure file logic, exercisable without a pane — the
   `queue_put`/`relation` test discipline). This is the write-first guarantee
   (§4); if it ever fires, the ordering was inverted to a pre-write hold — the one
   forbidden design. **Highest severity: the never-drop contract is void.**
2. **H-F2 — the fail-open is not byte-identical.** With `.swarm/engine/hook`
   absent, or on a hook timeout/crash, an operator-bound send differs by any byte
   from `main@834fec4`'s `queue/operator/` result. **Collector:** a test comparing
   the send path with the hook absent, timing-out, and crashing, against the
   baseline. This is the operator's "as-is" guarantee.
3. **H-F3 — a reply or claim mis-attributed (the identity KILL's collector).**
   Two shapes: **(a)** a *passed* operator message headed `from decision-engine`
   (the hook re-authored a pass — §7 makes this structurally impossible, pass = do
   nothing); **(b)** an *answer or claim line* headed `from: <asker>` or under the
   **OPERATOR header** instead of the engine's name — the exact laundering
   hook-redcheck finding 1 identified when the `env=` injection (§3/§7) is missing.
   **Collector:** the asker reading its own `delivered/` (a reply "from itself" or
   "from the OPERATOR" carrying an AUTO-ANSWER "the human has NOT read this" body
   is a glaring contradiction); the seat diffing a reply's `from` against
   `eng_name`. One instance of (b) ⇒ the invocation dropped the `SWARM_AGENT_ID`
   injection — a spine break, the reply is laundering.
4. **H-F4 — the branch fires off the operator path.** A non-operator send, or the
   engine's own reply, invokes the hook (the §3 guards failed). **Collector:**
   grep/trace for hook invocations on `to != "operator"` sends. Recursion/scope
   hazard.
5. **H-F5 — the send path acquired an unbounded block.** A hook invocation with
   no timeout, or a timeout so long it stalls the sender's turn beyond
   `ENGINE_HOOK_TIMEOUT`. **Collector:** code review of the diff; a timing test on
   an operator-bound send with a hung hook — it must return within `T`. The whole
   sync argument (§5) rests on the block being bounded.
6. **H-F6 — timeouts dominate (expected MODAL, per R4, not a tail).** The hook
   times out on a large fraction of operator messages, so the value §12 weighs is
   illusory — most items pass by timeout, not by decision, at full block cost.
   Given a cold model invocation is realistically tens of seconds (§6), this is
   the *expected* operating point, not a rare failure. **Collector:** the pilot's
   hook-latency log (§11 step 8) and the seat's per-stint count of timeout-passes
   vs decided-passes. Fires ⇒ raise `T` (paying more sync latency, §5) or accept
   the engine is too slow to earn the branch (→ races-allowed, §12).
7. **H-F7 — an orphan in `delivered/` with no claim line (the redcheck-2
   residual's collector).** A file in `queue/operator/delivered/` with no matching
   `[hand:engine]` claim line in the operator ledger — the signature of a hook
   SIGKILLed between its `mv` and its claim line (§9), which no standing hand
   reconciles because the cold hook has no journal/seat. **Collector:** the next
   human or seated hand draining `delivered/` — a `grep` of `delivered/` filenames
   against claim lines in `.swarm/journal/operator.md` surfaces it. Not
   auto-recovered (there is no standing engine to adopt the loop); it is *found*
   on the next drain and the finder writes the missing record or re-handles the
   item. Bound: the window is one `subprocess.run`, rarer than DW's standing-engine
   crash window, but real — this falsifier exists precisely because the design
   does not pretend the recovery hand inherits.

---

## 11. Priced implementation sketch — the edit that touches bin/swarm

Unlike DW/PIPE/PROXY (zero bin/swarm lines), this design edits the tool. Sized,
ordered, each step with its verification. **RESEARCH ONLY — no edits are applied
by this document.**

| # | actor | step | size | verify |
|---|---|---|---|---|
| 1 | **[human]** | STANDING GOALS grants + threshold + enable (DW §9 #1, inherited) | ~12 lines text | provenance quoted (DEC F7, once). **Blocking.** |
| 2 | **[builder]** | `registered_hook(root)` helper — read `.swarm/engine/hook`, return **`(eng_name, command)`** from its two lines, `None` on any error; `ENGINE_HOOK_TIMEOUT` constant | ~8 lines, `bin/swarm` | unit: absent → `None`; two-line marker → `(name, command)` tuple |
| 3 | **[builder]** | The `cmd_send` branch (§3) — write-first, then bounded `subprocess.run(timeout=T, env={..., SWARM_AGENT_ID: eng_name, SWARM_DIR: root})`, fail-open, operator-only + `sender != eng_name` guard | ~18 lines, `cmd_send` | **H-F1/H-F2 tests:** message always in `queue/operator/` first; hook absent/timeout/crash → byte-identical to `main` on non-claiming branches |
| 4 | **[builder]** | `swarm engine-hook <file>` verb — cold: read the queued record, run the DW decision (grants), on answer do the claim ritual (mv to `delivered/` + claim line + reply **as `my_name()`, which the injected `SWARM_AGENT_ID` makes = eng_name**), on pass exit 0 doing nothing | ~40 lines, new verb | **H-F3 tests:** a passed file stays in `queue/operator/` under original `from`; an answered file → `delivered/` + asker got `from: <eng_name>` (NOT the asker's own name, NOT OPERATOR — the env-injection check) |
| 5 | **[human]** | WORLD.md mailbox amendment (§8) — **ships with the code**; heaviest contract touch in the lineage | ~10 lines | paragraph matches merged behavior; `swarm world` prints it |
| 6 | **[human/seat]** | Write `.swarm/engine/hook` marker (**line 1 = engine wire name, line 2 = command**) + `.swarm/briefs/decision-engine-hook.md` (DW §9 #3 inherited, adapted: cold per-invocation, no standing pane, claim ritual runs as the injected identity, kill = rm marker) | ~120 lines brief + 1 two-line marker | marker's line 1 is the name the injection uses; brief's claim ritual + fail-open verbatim |
| 7 | **[seat]** | Shadow: point the marker at a hook that only *logs* what it would answer, claims nothing | drill | operator sends land in `queue/operator/`; hook log shows would-answers; zero moves |
| 8 | **[seat]** | First live answer: hook claims one granted item within `T` | drill | DW chain check; **reply's `from` == eng_name (the env-injection works, H-F3)**; hook latency logged (feeds H-F6); item in `delivered/` |
| 9 | **[seat]** | **Timeout drill (§4/§5/§6):** point the marker at a hook that sleeps past `T`; send an operator item | drill | send returns within `T`; message waits in `queue/operator/`; human drains as today (H-F2). **Note the modal case:** with a real cold model this is the *common* outcome (H-F6), not just a drill |
| 10 | **[seat]** | **Partial-claim drill (§9, redcheck-2):** SIGKILL the hook between its `mv` and its claim line | drill | file in `delivered/` with NO claim line; verify H-F7's grep surfaces the orphan; confirm **no standing hand auto-recovers** — the next drain finds it |
| 11 | **[seat]** | Kill drills: `rm .swarm/engine/hook` (branch stops next send); soft freeze (hook answers nothing) | drills | §9 observations; fail-open holds after disarm (H-F2) |
| 12 | **[adopt gate]** | After the pilot (DW §5.4): human reads §10 collectors + H-F6 timeout rate, adopts / narrows / kills. **On kill:** `rm` marker, delete grants, **revert the bin/swarm edit** — dead weight without a hook | — | tool reverts to `main@834fec4` send path |

**Size totaled** *(corrected after hook-red R8 — the first draft headlined "~20"
by omitting the verb):* ~20 lines of `cmd_send` branch + helper, **plus a
~40-line `swarm engine-hook` verb** = **~60 lines of new bin/swarm code**, + one
two-line marker + one constant + one CONTRACT-CLASS WORLD.md paragraph (the
lineage's heaviest). Smaller than the custody design (~50 lines across four
functions *plus* a reclaim sweep on three call-sites, i.e. more total), but the
honest number to weigh against races-allowed is **~60 lines + a verb**, not ~20.
Compare DW/PIPE/PROXY: **zero** bin/swarm lines.

---

## 12. The comparison — HOOK-ROUTED vs RACES-ALLOWED — and the recommendation

Everything except one axis is **identical by inheritance**: both use DW's grants,
auto-answer ritual, ledger audit, override, kill-by-freeze, and training. An
asking agent sees the identical AUTO-ANSWER message under either. The engine's
*decision behavior* is DW verbatim in both. **The one axis that differs is what
the hook buys over races-allowed — and the two KILLs shrank it dramatically**
*(this whole section rewritten after hook-red R1/R2: the first draft's "structural
certainty" column was false).* It is **not** "the operator's queue is *guaranteed*
hook-passed" — nothing on this substrate orders the human relative to the hook
(§5). It is only "the engine's cold read is *attempted in-band, synchronously,
before the send returns*, so it reaches the mechanical share slightly more
reliably than an always-awake standing hand would."

| axis | RACES-ALLOWED (PIPE's recommendation) | HOOK-ROUTED (this document) |
|---|---|---|
| **engine-first reading** | *tendency.* The standing hand reads first because it never sleeps (PIPE §5c); a human can drain first. | *tendency, T-bounded.* The cold hook is invoked synchronously on the send, so its read is attempted before the send returns and the write→claim window is bounded to `T`. **Still a tendency — the human is not ordered (§5, KILL-1).** Marginally more reliable in-band reading; **no** provable certainty. |
| **provable certainty** | none, and none claimed. | **none either** — the first draft claimed it; KILL-1/KILL-2 removed it. The substrate cannot carry "prove every item was hook-passed." |
| **new machinery** | **none.** Zero bin/swarm lines (PIPE §4). | **~60 bin/swarm lines** (branch+helper ~20 *plus* the ~40-line verb, R8) + a new verb + a two-line marker + a timeout constant. |
| **contract touch** | DW's one inherited amendment, **unchanged** (PIPE §8). | DW's amendment **rewritten** to name the invocation + timeout — the **lineage's heaviest**, first tool-invoked code on the operator path (§8, R7). Ships with the code. |
| **fail-open** | trivial — no rule to suspend; engine-down = today (PIPE §5d). | a **code branch** (§3) — byte-identical when the marker is absent or the hook times out **without claiming** (H-F2); the SIGKILL-mid-claim branch is an unrecovered orphan (§9, H-F7). Clean on the common path, a real residual on the rare one. |
| **failure surface** | the engine can only ever *subtract* itself (DW §8 I3 whole). | **subtract-only for the bytes** (write-first, CONFIRMED) — no new lose-mail class. But it adds a *record*-corruption residual (orphan in `delivered/`, §9) that races-allowed's standing engine reconciles and the cold hook cannot. |
| **cost per operator send** | zero added (PIPE §5). | up to `ENGINE_HOOK_TIMEOUT` — **tens of seconds** for a cold model (§6, R4) — blocking on operator-bound sends only (~a-handful/day). Aggregate small; per-message real; and a **modal fraction are timeout-passes** buying nothing (H-F6). |

**The honest trade, restated:** the cold hook buys a **T-bounded narrowing of the
engine-first *tendency*** — the engine's cold read attempted synchronously in-band
— and pays **~60 bin/swarm lines, a new verb, the lineage's heaviest contract
touch, a tens-of-seconds block on every operator send, and a record-corruption
residual on SIGKILL-mid-claim.** It does **not** buy provable certainty (KILL-1);
that column is empty for both designs now. It **does** keep the bytes safe
(write-first, CONFIRMED) — no new lose-mail class — a real
improvement over custody, and the reason this design is worth writing down even
while recommending against it.

**Recommendation: RACES-ALLOWED for v1 — and the KILLs strengthen it.** The
record does not show the hook's value is *needed*: PIPE §12 cited "zero
misorderings, zero backlogs in the entire operator corpus." The operator has
never been harmed by seeing an item before the engine considered it, because that
harm requires the human to *act wrongly* on an unconsidered item, and the human
acting on operator mail *is* the safety layer (DEC §7, "the only #62 detector").
Races-allowed already delivers the value — the engine reads the mechanical share
first, reliably, because it never sleeps — at zero machinery, zero contract touch,
zero send-path latency. The cold hook offers only a *T-bounded narrowing* of that
same tendency (KILL-1), and pays ~60 bin/swarm lines + a verb + the lineage's
heaviest contract touch + a tens-of-seconds block on every operator send for it —
with a modal fraction of those blocks buying only a timeout-pass (H-F6, R4).

**The consequence of the two KILLs the operator most needs to hear — CONDITION 1
IS VOID.** The first draft said "flip to HOOK-ROUTED if the operator names
structural certainty a hard requirement." **No operator sentence can flip it**,
because the substrate cannot carry structural certainty over the human: sync
blocks the sender, not the human, who reads `queue/operator/` through an
independent `swarm ps` (bin/swarm:933-943, KILL-1). The hook delivers a T-bounded
tendency, never a guarantee — so "I must be able to *prove* every item was
hook-passed" is a want **this design cannot satisfy** regardless of how badly the
operator wants it. That framing is deleted from the fork, not softened. This is
the same answer PIPE §12/§5e reached; the send-path license did not change it,
because the license moved code onto the send path but code there still cannot
order the human (KILL-2).

**The exact conditions under which HOOK-ROUTED still wins** (a much narrower door
than the void condition 1):

1. **The operator wants the synchronous-invocation *property itself*, for a
   reason OTHER than provable certainty** — e.g. "I want the engine's cold read
   *attempted in-band* on every operator send, so the mechanical share is more
   reliably handled the instant mail is sent, not whenever a standing hand next
   wakes." That is a real, buildable property (the T-bounded narrowing) — just not
   *certainty*. If the operator names *this*, the hook delivers it and
   races-allowed does not (races-allowed reads first only when the standing hand
   happens to be awake and gets there first).
2. **AND cold-start is fast enough that the property is real** — H-F6 clean: the
   engine decides within `T` on the large majority of items (not timing out), so
   the in-band read actually happens rather than degrading to a timeout-pass. If
   the cold model is slow (the expected case, R4), even this narrower value
   evaporates and the hook is strictly worse than races-allowed (full cost, mostly
   timeout-passes).

If **both** hold, **switch to HOOK-ROUTED** — the ~60-line edit and the contract
amendment are the honest price of the in-band-read property, and §3–§7 (with the
`env=` identity injection) are the build. If either fails — and condition 1's old
certainty framing is *void*, not merely unmet — races-allowed is not a compromise
but the right design. The fork is real but small; my lean is races-allowed; and
the one thing the operator must not be told is that any sentence buys certainty,
because none does.

---

## Summary for hook-scout

*(This summary rewritten in the repair pass — the first draft's spine claims
were the two KILLs.)* The operator's corrected shape is the engine as a **cold,
per-message, timeout-bounded hook** on the operator send path — the tool's own
idiom (`cmd_deliver`/`cmd_event` are cold `swarm` sub-invocations wired as hooks,
bin/swarm:804-817). This **dissolves the custody design entirely** — no standing
engine, no custody queue, no reclaim, no mid-flight-death, no wedged-alive (cut).
**Where it sits relative to PIPE, corrected (hook-red R2 KILL):** PIPE §5b did
**not** miss the send path — its kill is *invariant-level* ("stands even if
someone added an operator-delivery path", PIPE:346-347) and its six-mechanism
sweep already covers tool-code-on-a-path. The send-path branch is a *new instance
of that family*, and it survives PIPE's barrier-kill only because sync does not
make the human wait — which is exactly why it also cannot deliver certainty. The
branch: on `to=="operator"` with a configured hook, **`queue_put` first (durable,
never dropped — W:51-53), then invoke `swarm engine-hook <file>` with a timeout**
(send block bin/swarm:912-919, doorbell 921-930). **(1) Durability ordering** —
write-first is mandatory: a pre-write hold would silently drop mail on a killed
send (forbidden); write-first makes durability hook-independent, so
timeout/crash/absent leave the message in `queue/operator/` = today (§4, CONFIRMED
by both reviews). **(2) Sync vs detached** — **synchronous**, blocking `T` on
operator-bound sends *only* (~a-handful/day, PROXY §2a), buying a **T-bounded
narrowing of the races-allowed tendency — NOT an ordering guarantee** (hook-red R1
KILL: nothing orders the human, who reads via a separate `swarm ps`,
bin/swarm:933-943); detached collapses even the narrowing into plain
races-allowed (§5). **(3) Cold-start** — a cold model invocation is realistically
**tens of seconds** (R4), so `ENGINE_HOOK_TIMEOUT` is a tens-of-seconds block and
**timeouts are MODAL** — a large fraction of items pass by timeout, not decision
(§6, H-F6). **Identity (hook-redcheck finding 1 KILL):** the answer is DW
attribution *only if the tool injects* `env={..., SWARM_AGENT_ID: eng_name,
SWARM_DIR: root}` into the cold invocation (`eng_name` = marker line 1) — a bare
`subprocess.run` inherits the sender's env and launders the reply under the
asker's name or the **OPERATOR header** (the DW/PROXY kill); pass = do nothing, so
pass never launders (§7). **Registration** = a **two-line marker**
`.swarm/engine/hook` (name + command), `rm` = disable (§2). **Contract:** the
mailbox paragraph (W:57-61) rewritten to name the cold invocation + timeout —
**the lineage's heaviest touch, the first tool-invoked code on the operator
path** (§8, R7). **Recovery residual (hook-redcheck 2):** a hook SIGKILLed
between `mv` and claim line leaves an orphan in `delivered/` that **no standing
hand reconciles** (the cold hook has no journal/seat) — bytes safe, record
corruptible, found on the next drain (H-F7). **The heart (§12):** the cold hook
buys **a T-bounded tendency-narrowing, NOT provable certainty** (the certainty
column is empty for both designs after the KILLs), and **restores the
subtract-only failure surface for the bytes** (write-first, no new lose-mail
class), at **~60 bin/swarm lines** (branch+helper ~20 *plus* the ~40-line verb,
R8) + a verb + the heaviest contract + a tens-of-seconds block per operator send.
**Recommendation: races-allowed for v1** — the record shows no harm even the
tendency-narrowing prevents, and the value is delivered at zero machinery.
**Condition 1 is VOID:** no operator sentence can flip to HOOK-ROUTED for
*certainty*, because the substrate cannot carry certainty over the human (KILL-1).
The hook wins only in the narrower case: the operator wants the **in-band
synchronous-read property itself** (not certainty) **AND** cold-start is fast
enough that it isn't a timeout-pass (H-F6). Two adversarial reviews (`hook-red`,
`hook-redcheck`), 3 KILL / 7 WOUND, all repaired in place, recommendation
unchanged and strengthened.

---

## 13. ADOPTED — the universal send middleware (supersedes the operator-only shape, and §4's pre-write kill)

*Written by the builder at adoption, 2026-07-11, recording the operator's
corrections of this document plainly. Where earlier sections conflict with
this one, this one wins; they remain above as the design record that led
here. Terminology: the adopted thing is a MIDDLEWARE — "hook" survives only
in this document's filename and its historical sections.*

**The adopted form.** A **generic send middleware**, configured in
`.swarm/config` (TOML, world-readable, one `[middleware]` section only — a
chain belongs inside the middleware, not the tool):

    [middleware]
    command  = "python3 /path/to/mw.py"  # required; a resolvable command
                                         # string, args allowed (the git
                                         # core.editor / Procfile pattern)
    identity = "middleware"              # optional; default "middleware"
    timeout  = 60                        # optional; seconds

When configured, **every** `swarm send` — all recipients, not just the
operator — runs the command in the sender's process, BEFORE the queue write,
with the full envelope (`from`, `to`, `ts`, `body`) as JSON on stdin, bounded
by the configured timeout (default `MIDDLEWARE_TIMEOUT`, env
`SWARM_MIDDLEWARE_TIMEOUT`, 60s), with `SWARM_AGENT_ID = <identity>` and
`SWARM_DIR` injected — so anything the middleware itself sends is attributed
to IT, never to the original sender. No `[middleware]` section, no `command`
key, or an unreadable file = no middleware: `cmd_send` is byte-identical to
today. The verdict is the middleware's EXIT CODE alone — stdout is never
parsed:

- **exit 0** → PASS: the tool queues the message for its recipient, unchanged.
  This is next() — the common case, success = continue.
- **exit 100** (`MIDDLEWARE_HANDLED_EXIT`) → HANDLED: deliberate don't-pass —
  the middleware owned the message (answered, dropped, or forwarded via its
  own `swarm send`, in its own wire name); the tool queues nothing. 100 sits
  above the shell's reserved codes (126–128, 130) and the ordinary error
  codes (1–2), so an incidental failure can never be misread as a deliberate
  HANDLED.
- **any other exit, a timeout, a kill, or no configuration** → FAIL-OPEN: the
  tool queues the message unchanged — crash, `set -e`, and command-not-found
  all pass through safely, and a broken middleware degrades to no middleware
  in code.

The only guard that remains is recursion: a send whose sender IS the
configured identity is not re-intercepted.

**§4's pre-write kill is superseded, and it was wrong.** §4 rejected any
pre-write hold in one sentence — a killed send "silently drops" mail — but
that scenario ignored sender-observed failure semantics: if the sender's
process dies while the middleware runs, the send never returned, so the
message was never ACCEPTED; the sender is watching its own command fail, and
retries per its briefing. That is producer-side interception — the normal
middleware contract everywhere — not a silent drop: "nothing is ever silently
dropped" governs accepted messages, and an unaccepted send has the sender as
its observer. Likewise, the lineage's "certainty is unbuildable" findings
(KILL-1/KILL-2, PIPE §5b) governed mechanisms that try to order READERS of a
queue AFTER a message is admitted — they stand, for that problem, and are
irrelevant to this one: admission control decides BEFORE the queue write, and
nobody can read what was never queued.

**The decision engine is demoted to what it always should have been.** The
operator-mail decision engine of DW/PIPE/PROXY and §2–§12 above is now merely
THE FIRST MIDDLEWARE ONE MAY WRITE — an executable outside the tool,
configured via `.swarm/config`, carrying its own grants, model, prompt, and
ledger. `bin/swarm` carries ZERO of it: no grants, no model call, no decision
prompt, no recipient special-casing, and no engine.
