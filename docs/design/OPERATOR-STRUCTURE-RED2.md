# RED2 — fresh adversarial review of `OPERATOR-STRUCTURE.md`

> SUPERSEDED by OPERATOR-STRUCTURE.md, which folds in and credits its core finding; kept for the record (the review of the now-retracted tool fix — "fixes rendering, not attention — any agent may still mail the human" — that directly caused the pivot to doctrine+middleware).

**Reviewer:** `structure-red2`. I ran none of the original design work — that is my
qualification. Written 2026-07-12 at `main@aa6063d`.

**Method.** Every claim below is checked against a **primary artifact** — the source, the
patch bytes, an executed command with its output pasted — never against the design's
description of itself. Where I could not reach a failure state, I say so and rate the
attack lower, rather than dress up a hit. Two reviews today caught rig-kindness; a red team
that manufactures a finding is worse than useless, and so is one that rubber-stamps.

**Bottom line, in one paragraph.** The central diagnosis is **right, and I confirmed it
independently**: `parent=operator` is the only value a root session can write, and no amount
of prose could ever have fixed that. But **the review was performed against the wrong
artifact.** The patch the brief pointed me at (`git stash@{0}`) is not the code the design's
own child built and tested — it is the **superseded draft that child explicitly rejected as
causing silent, permanent mail loss.** And the corrected code has a defect neither the design
nor any of its three children caught: **after the fix, the human's own messages lose the
OPERATOR sender class.** Zero of seven agents in a realistic tree can hear the human as the
human. That is contract-class, it fires for every human who spawns even once, and it should
block the merge. Separately, the fix **does not do what the design says it does**: it makes
the human's *`ps` view* one node, but "direct load" is `queue/operator/`, and **any agent at
any depth may mail the human, unrestricted, by contract.** The fix solves the rendering of
the attention problem, not the attention problem — which, ironically, is the strongest
argument *for* the doctrine half the author asked me to steel-man deleting.

---

## VERDICTS

| # | Attack | Verdict | Where |
|---|---|---|---|
| **0** | **The reviewed artifact is not the tested artifact** (the stash ≠ the child's diff) | **KILLS the review, not the design** | §0 |
| **A2** | The human loses the OPERATOR sender class after their first spawn — **in the corrected code too** | **KILLS IT** | §1 |
| **F′** | The fix solves the *rendering* of the human's load, not the load — any agent may mail the human | **WOUNDS IT** (and rescues the doctrine) | §2 |
| A | Paneless session claims a new `root-N` on **every** spawn; phantoms render `[live]` forever | **WOUNDS IT** (bounded — unreachable from stock herdr) | §3 |
| B | `is_dead`: a paneless record is now never dead | **WOUNDS IT** — see §3; real interaction with A | §3 |
| C | Hook gates: can `my_name()`'s new directory scan crash a hook? | **SURVIVES** — it cannot. Attack fails | §4 |
| C′ | Hook gates: the `is_agent()` version causes silent mail loss | **KILLS the stash** (child already fixed it) | §0 |
| **E** | `.swarm/` as the file that witnesses "first swarm" | **KILLS IT** — and **I got this wrong first** | §5 |
| **D** | Pane reuse: silent adoption of a predecessor's journal **and children** | **WOUNDS IT** (foundation holds) | §7 |
| **F** | The SPAN override; should the doctrine be deleted? | **SURVIVES** — ship both, on repaired grounds | §8 |
| G | Citations | **SURVIVES**, with one real miss (`settings/root.id`) | §6 |

---

## §0 — THE REVIEWED ARTIFACT IS NOT THE TESTED ARTIFACT

My brief said: *"The working tree's UNCOMMITTED diff: `git diff bin/swarm` — THE FIX IS
IMPLEMENTED AND SITTING THERE."*

**`git diff bin/swarm` is empty.** `bin/swarm:68-69` still reads
`return os.environ.get("SWARM_AGENT_ID") or "operator"`. There is no `root_name`, no
`claim_root_name`, nothing. The fix is in **`git stash@{0}`**.

And the stash is **not** the diff `OPERATOR-STRUCTURE-FIX.md §7g` records as tested:

| | `git stash@{0}` (on disk) | `FIX.md §7g` (the child's tested diff) |
|---|---|---|
| hunks / lines | **9 hunks, +69/−7** | **7 hunks, +66/−8** |
| `is_agent` helper | appears **4×** | appears **0×** — does not exist |
| the three hook gates | `if not is_agent(root_dir(), my_name())` | `if my_name() in ("", "operator")` |
| `cmd_send` sender | `sender = my_name()` | `sender = my_name() or "operator"` |

*(Counts are mechanical: `git stash show -p stash@{0} | grep -c "^@@"` → 9; `grep -c is_agent`
→ 4; the same greps over §7g → 7 and 0.)*

The child did not merely *prefer* its version. **`FIX.md §7d` says the `is_agent()` gate is a
fatal bug it found and removed:**

> **But my proposed gate — `if not is_agent(root, my_name())` — was a real defect, and the
> test suite caught it.** Applying it turned 3 tests into ERRORs… **a live agent whose record
> is missing or momentarily unreadable would have its `deliver` hook silently no-op — and its
> queued mail would never be injected.** That converts a recoverable state into **permanent,
> silent mail loss**, breaking `WORLD.md:51-53`. **It is a worse bug than the one I was fixing.**

`red2-trace` reproduced that rather than trusting it (`docs/audit/red2-trace-2026-07-12.md`,
A4): with the stash's gate, a live agent with mail waiting and a momentarily-missing record
gets `exit=0, empty stdout` — **the mail is not injected**; with the corrected gate the same
mail lands. Same for the anonymous-sender bug (`§7e`): the stash queues `{"from": ""}` from a
normal shell, exit 0, no warning.

And `FIX.md §7i` says the child **left no code behind**: *"`bin/swarm` has been **reverted to
HEAD** (`git status` clean; suite green at HEAD). The verified diff is preserved for whoever
ships it."*

**Consequences, and they are not cosmetic:**

1. **The design's "80 tests, FAILED(failures=1)" cannot have come from the stash.** The stash
   contains a bug the child says produces **3 ERRORs**. So the measurement was taken against
   §7g's code, and the artifact on disk is the pre-fix draft. **The number and the code do not
   belong to each other**, and the brief presented them as if they did.
2. **Attack C, as briefed to me, is an attack on code the author's own child already killed.**
   I ran it anyway (§4) — but the hazard the author most feared was already retired.
3. Whoever ships this must ship **§7g**, not what is on disk. If someone `git stash pop`s and
   commits, they ship the mail-loss bug.

**This kills the review, not the design.** The design's *argument* is unaffected. But a design
doc that says "the fix is implemented and sitting there" while the thing sitting there is the
draft its own child condemned has lost track of its artifact — and the discipline this repo
runs on ("judge artifacts, never claims") is precisely what catches that.

---

## §1 — A2: THE HUMAN LOSES THE OPERATOR SENDER CLASS. **KILLS IT.**

This is the finding that should block the merge. It is **not** in the design, **not** in any
of its three children, and it **survives the child's §7g correction**.

`bin/swarm:158-166` — `relation()` is the only code that can produce the OPERATOR class, and
its only trigger is the literal string `"operator"`:

```python
def relation(sender, recipient, parent_of):
    """...the header names who is speaking and where they stand,
       so a directive can never arrive framed as chatter."""
    if sender == "operator":
        return "the OPERATOR (the human at the root)"
    if parent_of.get(recipient) == sender:  return "your parent"
    ...
    return "another agent"
```

`delivery_head()` (`:221-223`) renders that string **verbatim** into the injected turn:
`[swarm message] from {from} — {rel} — sent {ts}`.

Before the fix, the human's session **is** `operator`, so every message they send — to any
agent at any depth — arrives headed **"the OPERATOR (the human at the root)"**. After the fix,
their session is `root-1`, and `"root-1" != "operator"`.

**I ran `bin/swarm`'s real `relation()` against a realistic tree:**

```
BEFORE (human's session IS "operator"):   human -> w1  'the OPERATOR (the human at the root)'
                                          human -> g1  'the OPERATOR (the human at the root)'
AFTER  (human's session is "root-1"):     human -> w1  'your parent'
                                          human -> g1  'another agent'          <-- !!
```

**`red2-trace` reproduced this end-to-end through the real send/deliver path** and measured
the blast radius on a 7-agent tree:

```
  lead-a -> your parent      w1 -> another agent      w3 -> another agent
  lead-b -> your parent      w2 -> another agent      w4 -> another agent
                                                     deep -> another agent
  sees 'the OPERATOR': 0/7
  DOWNGRADED         : 7/7   (2 as 'your parent', 5 as 'another agent')
```

**Zero of seven.** Everyone below the first tier — most of a real swarm — receives the
human's directive framed as **"another agent"**, the weakest class `relation()` has. The
function's own docstring says the header exists *"so a directive can never arrive framed as
chatter."* After this fix, **it always does.**

**The child's fix does not save it.** `§7e` fixed the anonymous-sender bug with
`sender = my_name() or "operator"`. But that fallback fires **only while `my_name()` is
empty** — and `my_name()` is empty only until the root names itself, which is *the entire
point of the fix*. `red2-trace` proved the disarming inside a single session:

```
PHASE 1 (never spawned):  from operator — the OPERATOR (the human at the root)
PHASE 2: swarm spawn lead   ->  root record {"name": "root-1", ...}
PHASE 3 (same session):   from root-1  — your parent
                          from root-1  — another agent   (to the grandchild)
```

**The fix's success condition disarms its own fallback.** Every human who spawns even once —
i.e. every human who uses swarm at all — permanently loses their voice.

**There is no escape hatch** (`red2-trace` checked all of them): `swarm send --from operator`
→ `unknown flag`; `swarm spawn operator` → `reserved`, so no session ever runs with
`SWARM_AGENT_ID=operator`. The class becomes unreachable by any ordinary path.

**This breaks a contract sentence, not a preference.** `WORLD.md:19` promises the header names
*"the sender and their relation to you (parent / child / sibling / **OPERATOR**)"*. After the
fix, one of the four promised classes can no longer be produced.

**Remedy (one line, untested — the author's call):**

```python
if sender == "operator" or sender.startswith("root-"):
    return "the OPERATOR (the human at the root)"
```

The two goals were never in tension. The patch conflated *"has a name"* with *"is not the
operator."* A root session is the human's session; the records already say
`"parent": "operator"`. Let it be a **node** in the tree and the **OPERATOR** on the wire.

**Not a finding, stated so I don't pad the list:** `relation()` also feeds `send_size_error`
(`:990`), but only through the header's *length* against `TURN_CAP = 8000`. Noise.

---

## §2 — F′: THE FIX SOLVES THE RENDERING, NOT THE ATTENTION. **WOUNDS IT.**

The design's central promise, `§3a` (line 195):

> **`human → flat row of N workers` is not *frowned upon*; it cannot be written.**
> **The human's direct load is one node because that is the only tree the data model admits.**

**"Direct load" is not the `ps` tree. It is `queue/operator/`** — the mail the human has to
read. And `cmd_send` (`:984-992`) places **no restriction of any kind** on who may write
there:

```python
    if to != "operator" and to not in agents:
        die(f"unknown agent: {to}")
    sender = my_name()
    # ... no parent check. no depth check. no throttle. anyone -> operator.
```

There is no restriction *and there cannot be one*, because `WORLD.md:57-59` **promises** it:
*"**nothing ever refuses a message to the operator.**"*

**I found this by reading the source. `red2-doctrine` then ran it** — which is the stronger
evidence, and it arrived at the same place independently (`red2-doctrine-2026-07-12.md` F.3).
Eight spawns from one root session:

```
operator — no waiting mail
└─ root-1 (you) [live] q=0 idle ?
   ├─ w1 [live]  ├─ w2 [live]  ├─ w3 [live]  ├─ w4 [live]
   ├─ w5 [live]  ├─ w6 [live]  ├─ w7 [live]  └─ w8 [live]
```

then three of them report:

```
operator — 3 message(s) waiting for the human (queue/operator/):
    from w1, 0s ago
    from w2, 0s ago
```

**"The flat row is not abolished. It is indented."** Eight agents, eight herdr panes, all
driven by the session the human sits in — which is to say, by the human — and every one of
them can ring the human's mailbox. `ps` draws one node at the top. **The human's day has eight
agents in it.**

And `SPAN.md:140-142` — the sentence this entire doctrine descends from — is about the right
quantity, and it is not nodes:

> The operator's span is theirs to declare and yours to protect: **never let the tree press
> more direct attention on the operator than they asked for.**

**Attention.** Which arrives through `queue/operator/` and through panes to watch — **neither
of which the fix narrows by one byte.**

Two consequences, and the second is the more interesting:

1. **The design overclaims.** The fix guarantees the *shape of `ps`*, not the human's
   attention. §3a's "the only tree the data model admits" is true of `agents/*.json` and false
   of `queue/operator/`. F-DOCTRINE's success criterion (*"the human's direct load is one
   node"*) is therefore **not** established by the fix, and the doc should say so.

2. **This inverts the author's own attack F.** He asked me to steel-man *deleting* the doctrine
   half, on the ground that after the fix the root is a node so the doctrine has nothing left
   to do. **The honest answer is the opposite: the fix is what is incomplete, and the doctrine
   is the only thing left that governs how many agents mail the human.** He asked for the
   argument that would let him delete his own doctrine; the record does not supply it. It
   supplies the reverse. *(The wider doctrine question — is a default coordinator worth its
   bytes at all — is `red2-doctrine`'s, and lands in §7.)*

---

## §3 — A + B: PHANTOM ROOTS, IMMORTAL IN `ps`. **WOUNDS IT** (both versions).

The hunk is byte-identical in the stash and §7g, so this hits whatever ships.

`root_name()` guards `if not pane: return ""` **before** its loop — so a paneless session can
never *find* the `root-N` record it already created. Then
`parent = my_name() or claim_root_name(root)` sees a falsy name and **claims a fresh one, on
every spawn.** `red2-trace`, three spawns, one session (`HERDR_ENV=1`, no `HERDR_PANE_ID`):

```
### ls .swarm/agents/
root-1.json  root-2.json  root-3.json  w1.json  w2.json  w3.json
{"name": "root-1", "parent": "operator", "pane": "", ...}   w1 -> parent root-1
{"name": "root-2", "parent": "operator", "pane": "", ...}   w2 -> parent root-2
{"name": "root-3", "parent": "operator", "pane": "", ...}   w3 -> parent root-3
```

**One human session shattered into three phantom roots.** No crash, no warning, exit 0.

**And attack B is what makes them immortal.** The patched `is_dead` —
`bool(a.get("pane")) and a.get("pane") not in live` — means **a paneless record can never be
dead.** With every real pane killed:

```
operator — no waiting mail
├─ root-1 [live] q=0 idle ?
├─ root-2 [live] q=0 idle ?
└─ root-3 [live] q=0 idle ?
dead: w1, w2, w3
```

Every real agent correctly dead; **three sessions that never existed render `[live]`
forever**, uncleanable except by `swarm close`. The fix exists to prevent
`human → flat row of workers`; in this state it produces a **flat row of fake humans**, each
adopting one worker — the same flatness, now with fabricated nodes and a permanently wrong
liveness column. The two hunks *interact*: `claim_root_name` writes `"pane": ""`, and the new
`is_dead` then guarantees that record outlives everything.

**The honest bound, and why this is WOUNDS and not KILLS.** It needs `HERDR_ENV=1` **and**
`HERDR_PANE_ID` unset. `red2-trace` could not manufacture that from stock herdr — herdr
injects both by the same mechanism, and a session started outside herdr dies cleanly and
earlier (`not inside herdr (HERDR_ENV != 1)`). Reaching it takes something deliberately
clobbering one var and not the other. **I asked for this attack hardest and my child came back
saying it is bounded. I record that rather than inflate it.**

*(A **stale** pane — set but no longer live — is benign: `root_name()` finds no match, returns
`""`, hooks exit 0, `ps` renders fine. The docstring's "a recorded pane can never go stale,
because it is the lookup key" holds. No finding.)*

**Remedy:** make the falsy-pane case explicit — `die()` in `claim_root_name` when
`HERDR_PANE_ID` is empty. A root that cannot be identified cannot be safely named.

---

## §4 — C: THE HOOK GATES. **The attack half-fails — and the half that lands, lands hard.**

The author's stated top worry: `my_name()` *"used to be a pure env read and is now a DIRECTORY
SCAN — that is a real cost and a real risk on EVERY hook invocation."* **I first wrote this off
as SURVIVES. I was wrong, and `red2-mech` proved it by running it.**

**Where the attack fails, and I say so plainly.** The **spawned-agent hot path is genuinely
free.** Every spawned agent has `SWARM_AGENT_ID` set, so `my_name()`'s `or` short-circuits
*before* `root_name()`/`load_agents()` ever runs. Measured, mean ms over 40 runs:

| | PATCHED | CLEAN |
|---|--:|--:|
| **spawned, n=100** | 53.8 | 54.4 |
| **spawned, n=1000** | 100.2 | 100.8 |

**Identical.** The gate costs a spawned agent one `os.path.exists` stat (stash) or nothing
(corrected). **There is no hit here and none was manufactured.** The common, high-frequency case
is fine.

**Where it lands — 1: the root session pays an O(n) scan for nothing.**

| | PATCHED | CLEAN |
|---|--:|--:|
| **root, n=100** | 60.2 | **43.7** |
| **root, n=1000** | **201.0** | **43.8** |

Confirmed O(n): 62 ms @100 → 191 ms @1000 → **530 ms @3000**. CLEAN is flat ~44 ms. This is
**pure dead overhead on the human's own session**, on every prompt/Stop/SessionStart, paid by a
hook that then exits 0 doing nothing. (`cmd_deliver` calls `my_name()` **twice** — a root pays
*two* scans.) **WOUNDS IT.**

**Where it lands — 2: yes, a hook CAN raise. This one is real and it survives §7g.**

`load_agents:150` is `if r and r.get("name")`. `read_json`'s `try/except` is *inside*
`read_json`; the `.get("name")` happens in `load_agents`, **outside any try**. A **truthy
non-dict** record — `[1,2,3]`, `"str"`, `42` — reaches `.get` and raises `AttributeError`. And
the gate's `my_name()` runs **before** the hook body's bulletproof `try`:

```
gate       hook        exit
CLEAN      deliver     0     ← pure env read; load_agents never runs in the gate
STASH      deliver     1     AttributeError: 'list' object has no attribute 'get'
CORRECTED  deliver     1     AttributeError          ← survives §7g
   (same for `event stop` and `restore`, 5/5 stable each)
```

**Caused by the fix, absent on CLEAN, present in *both* versions.** It breaks the documented
contract in `cmd_deliver`'s own docstring: *"Bulletproof: any error → exit 0, no output, turn
intact."* Also confirmed: `chmod 000` on `agents/` → `PermissionError` (root, absent on CLEAN);
a FIFO record → `open()` **hangs forever**. *(Survivors, exit 0 on both: `agents` is a file,
broken symlink, symlink loop, `x.json` is a directory, corrupt/binary/50 MB record, absent
`.swarm`, and a 50k-rename concurrent-writer race — `write_atomic`'s tmp+rename is safe.)*

**And the deeper bug underneath it, which is bigger than the crash and is NOT the fix's fault.**
The same poison record makes `cmd_deliver`'s **body** raise *inside* its `try` — which swallows
it, exits 0, and **never injects the message. The mail stays queued forever.** On **CLEAN too**:

```
spawned agent, one queued message, one poison [1,2,3] record elsewhere in agents/:
  CLEAN      poison=no -> DELIVERED     poison=yes -> LOST
  CORRECTED  poison=no -> DELIVERED     poison=yes -> LOST
```

**Silent permanent mail loss, pre-existing, breaking `WORLD.md`'s *"nothing is ever silently
dropped."*** The fix doesn't cause it — but it makes `load_agents` its `my_name()` hot path,
which is how we found it.

**One token closes both** — `load_agents:150`:

```python
if isinstance(r, dict) and r.get("name"):
```

Root hook: `exit=0` restored. Spawned mail: delivered. Suite: still exactly the one
bug-encoding failure. **This is `red2-mech`'s headline recommendation and I endorse it — it is
orthogonal to every design debate in this review and worth shipping on its own.**

**Where it lands — 3: a TOCTOU race in `claim_root_name`.** 12 concurrent spawns from **one**
pane, 10 rounds → rounds 2, 5, 7, 8, 9 produced **2–4 `root-*` records for the one shared pane**:

```
CAPTURED: 2 root records for pane SHARED-PANE
  root-1 pane='SHARED-PANE' parent=operator
  root-2 pane='SHARED-PANE' parent=operator      ← orphan phantom root
my_name() -> 'root-1'   (sorted-first)
```

`claim_name`'s `O_CREAT|O_EXCL` settles the **name** but not the **pane→name mapping**: two
concurrent spawns both see no root record and both claim different names for the same pane.
**`FIX.md §7c`'s table claims pane-keying kills the concurrent-root case — but it only reasoned
about *different* panes.** Same pane, concurrent spawn, breaks the *"the pane IS identity"*
invariant. Present in **both** versions. Reachable by a script, a `&`-backgrounded pair, or a
fast double-invoke — **more reachable than the empty-pane path.** *(Different panes: 20 panes →
20 distinct names. **SURVIVES.**)*

**Severity ceiling, stated honestly:** the root crash and O(n) cost fire only if a root session's
hook is *actually invoked*, and `FIX.md §7d` argues a root session has no settings file → no
hooks wired. If that holds, both are largely theoretical **for the hook path**. But the
`load_agents` non-dict unsafety is **real on the spawned-agent mail path regardless**, so the
`isinstance` guard stands on its own.

**And the stash's `is_agent` gate: independently confirmed as a real mail-loss defect** (§0) —
`red2-mech` reproduced `structure-mech`'s own §7d bug rather than trusting it:

```
STASH      rec-present -> DELIVERED    rec-absent -> LOST (exit 0, empty stdout, never injected)
CORRECTED  rec-present -> DELIVERED    rec-absent -> DELIVERED
```

---

## §5 — E: DOES A FILE WITNESS "THE FIRST SWARM"? **NO. KILLS IT.**
### (And this is where **I** got caught being kind to the design.)

I have to open this section by convicting myself, because the failure is the one this review
exists to prevent and I committed it.

**My first pass ruled E "SURVIVES — verified by construction."** My evidence:

```
$ git check-ignore -v .swarm     →  .gitignore:7:.swarm/
$ git ls-files .swarm | wc -l    →  0
```

`.swarm/` is gitignored, zero files tracked, therefore *"a repo cloned **with** `.swarm/`
committed"* — the failure mode I most expected to kill it — **cannot happen.** I was pleased
to report the author was right.

**`red2-doctrine` read lines 5-6 of the same file I had just read, and killed it.** The full
`.gitignore`:

```
1  # local backups, never part of the package
2  .backups/
3  *.bak
4
5  # swarm runtime state lives in each project's .swarm/, not here — but ignore any
6  # that ends up in the repo dir just in case
7  .swarm/
```

**The rule says, in the repo's own words, that it is not about user projects.** It exists
because swarm is **self-hosted** — it runs swarms on itself, so its own `.swarm/` lands in its
own checkout. State *"lives in each project's `.swarm/`, **not here**."*

**And the package ships no `.gitignore` to anyone.** Verified:

```
$ git ls-files | grep -i gitignore
.gitignore                          ← exactly one: swarm's OWN

$ tail -2 install.sh
echo "  • The tool writes state into a .swarm/ dir in your project — add it to"
echo "    that project's .gitignore if you don't want it committed."
```

An **instruction**, conditional on the user's preference — *"if you don't want it committed"* —
printed once by an install script. `README.md:67` says the same. **Nothing writes an ignore
rule into a user's project.** A user who doesn't read line 99 of an install script's output, or
who deliberately commits `.swarm/` as the paper trail the README calls it, ships `agents/*.json`
into git.

**So the design's dismissal of this failure mode is wrong twice** (`§4e`, lines 430-434):

> *"A repo commits `.swarm/` anyway (**against the shipped `.gitignore`**) → …
> **This is the only real miss, it requires deliberately un-ignoring runtime state.**"*

There **is no shipped `.gitignore`** — the one it means is swarm's own, which no user inherits.
And it requires **nothing deliberate**: it is the **default** for anyone who took no action.
The failure mode is not perversity; it is **inaction**.

**And the population it hits is exactly the population the pedagogy is for: every teammate who
clones a repo where someone else already swarmed.** On any team that is not an edge case — it
is the *majority* of first-time users.

**What I got wrong, precisely:** I verified the author's claim **against the one repository in
the world where it happens to be true**, and stopped. That is the rig-kindness I was spawned to
catch — a probe that confirms its own hypothesis by testing it where it cannot fail — and I ran
it myself, on the one attack where I was pleased to say "he's right." **A reviewer who cannot
take the hit has no standing to deliver one.** My child caught me; I am recording it rather
than quietly rewriting the section.

**The rest of `red2-doctrine`'s E findings, all executed:**

- **`swarm send operator` creates `.swarm/` with no `agents/` dir at all.** (`ps` and `world`
  create nothing — the laziness claim holds for those.) The design states the predicate **three
  different ways in five lines** — *"`.swarm/` is gitignored"* (:417), *"`.swarm/agents/`
  holding no record"* (:419), *"empty **or absent**"* (:423). **A doctrine a model must execute
  with an `ls` cannot be three predicates.**
- **A *failed* spawn writes `agents/root-1.json`.** With `herdr tab create` forced to fail, the
  spawn dies *after* `claim_root_name()` — so the witness fires when **zero agents ever ran**.
  It records *attempted*, not *ran*.
- **Deletion is the one case the design gets right.** `rm -rf .swarm/` → the confirm fires
  again; cost is one line. Sound.

**The witness, stated exactly:** `.swarm/agents/` witnesses *"someone has spawned in this
working directory, on this machine, since the last `rm -rf`."* That is **neither necessary nor
sufficient** for *"this human has never seen a swarm."* It says nothing about **who**; it fires
on a spawn that **failed**; and it fires per **working directory**, so the same human in a
second checkout gets the lesson twice.

**VERDICT: KILLS IT.** Not the doctrine — the **witness**. And the operator pre-authorized the
answer: *"if genuinely nothing witnesses it, **say so and default to announce-only rather than
build state.**"* **Nothing witnesses it. Default to announce-only.**

*(`red2-doctrine`'s constructive alternative, which I endorse: if the operator wants first-contact
pedagogy, put it where first contact actually happens — `install.sh` already prints a "Done."
block. **The install running IS a fact a file witnesses**, and it costs zero bytes of
always-loaded skill text.)*

---

## §6 — G: THE CITATIONS. **THEY HOLD** — with one real miss.

I checked every load-bearing quote against the file. The author's citation discipline is
genuinely good, and where he is right I say so:

| claim | status |
|---|---|
| `WORLD.md:57` *"The operator is a mailbox, not a node"* | **VERBATIM.** And `WORLD.md:12` *"The human **operator** roots the tree"* — **VERBATIM.** The contradiction he names is **real**. |
| **The central diagnosis**: `parent = my_name()` in `cmd_spawn`; `name in ("operator","delivered")` reserved; no `.swarm/agents/operator.json`; `cmd_spawn` takes only `--model`/`--cwd` | **ALL VERIFIED.** `parent=operator` **is** the only value a root session can write. **The diagnosis is sound and no amount of prose could have fixed it.** |
| `SPAN.md` *"Split under pressure, never in anticipation"* | **VERBATIM** (§3d). |
| `STRUCTURE.md` *"zero for three… never once come from momentary attention pressure"* | **VERBATIM** (§2a). |
| `DECISIONS.md` *"16–17h… **14 seconds**… 3–4s. The tier labels stayed; the attention behind them thinned"* | **VERBATIM** (:118-130). The strongest evidence in the design, and it is real. |
| PHILOSOPHY §9 *"polluted… created the chief-of-staff"* | **VERBATIM** (`docs/PHILOSOPHY.md:272-278`). |
| WATCHLIST #7 | **VERBATIM** (`docs/design/WATCHLIST.md:101`). |
| shipped `SKILL.md` = 122 lines / 7,833 B; the coordinator paragraph | **EXACT**, quoted correctly from `origin/main`. |

**The miss, and it is a real one.** `§3a` says `claim_root_name` *"persists the name to
`settings/root.id` so a restarted session in the same terminal keeps it"*, and `§6`'s cost
table bills **"new state: `settings/root.id` (one file, one line)"**.

**There is no `root.id`.** Not in the stash, not in §7g, nowhere. `FIX.md §7c` — the author's
own child — **deleted it**, titled *"I found the better fix, and it DELETES `settings/root.id`"*,
and explains why: *"`root.id` is itself the mistake… it stores one name per repo — yet identity
belongs to the **session**"*, and two concurrent roots would *"both call themselves `root-1`,
share one identity, and fight over the `pane` field."* Identity is keyed **purely on
`HERDR_PANE_ID`**.

So §3a describes a **superseded design**, and §6 **bills the repo for state the fix
deliberately removed** — while §6a simultaneously argues the fix adds no state. **The cost
table contradicts its own argument.** Fix: `settings/root.id` → **0 new files**, which is
*better* than what the doc claims and strengthens the §6a/WATCHLIST-#7 case.

*(Minor: `PHILOSOPHY.md` and `WATCHLIST.md` are cited as bare filenames; they live at
`docs/` and `docs/design/`. Path shorthand, not fabrication.)*

**One more citation that does not carry its claim** (`red2-doctrine` F.1, and I checked it):
`§4b` grounds the SPAN override partly on *"PHILOSOPHY §9… notes that question **created the
chief-of-staff**. The coordinator layer was never killed. It was **founding**."* But §9 is
titled *"Keep the operator's channel **clean**"*, and the operator's complaint was about **what
the session was doing in the channel** — *"polluted by **you validating work that can be done by
a subagent**"*. Its stated test (`docs/PHILOSOPHY.md:300-302`) is *"anything reaching the
operator must be **readable by someone who has not been in the room**"* — **a test on the
CONTENT of the channel, not on the COUNT of nodes in a tree.** The chief-of-staff was founded to
stop the human's session doing the work (that is doctrine 1, delegate-by-default, and it is not
under review). **§4b must ship on its other ground — the un-flooding asymmetry — alone.**

---

## §7 — D: PANE REUSE. **WOUNDS IT** — but the foundation holds.

**The kill attempt failed, and my child says so plainly.** `red2-doctrine` went after the
foundation, because **herdr's own documentation contradicts the design.**
`~/.claude/skills/herdr/SKILL.md:44`:

> **important: ids can compact when tabs, panes, or workspaces are closed. do not treat them as
> durable ids.**

If pane ids recycle, a new pane inherits a dead one's id, `root_name()` matches someone else's
record, and the seat model has no foundation. So it **tested** rather than asserted:

```
created pane=w4:p93 → closed tab w4:t93 → created NEXT pane=w4:p94
>>> NOT recycled

~/.config/herdr/session.json:  next_public_pane_number: 293   (monotonic, persisted to disk)
```

**The allocation counter is monotonic and persisted**, so it survives a herdr restart. The
design's "stable id" claim is **substantively correct** — asserted without a test, but right.
*(Untested residue the design should own: `herdr session delete` exists, and `session.json` is
the only place the counter lives. Whether deleting a session rewinds the counter to 1 — minting
`w4:p1` into a `.swarm` that still holds a `root-1` claiming `w4:p1` — is one command away from
a real collision. **Ask for a one-line test, not a table row.**)*

**The `cd`-to-another-repo attack — which I briefed as the likely killer — also fails**, and
this is the child running a control rather than banking a hit. Same pane, two repos, no
`SWARM_DIR`: two independent `.swarm/` dirs, each with a well-formed `root-1`, no cross-read
(`root_dir()` resolves `.swarm` per-CWD). With `SWARM_DIR` set, a spawn *does* bleed into the
wrong project's tree — **but the control on unpatched `HEAD` shows the identical bleed.**
Pre-existing property of `root_dir()`, not caused by this fix. **Not a finding against this
design** (though an env var that silently redirects a spawn into another project is worth its
own ticket).

**What is real — D.4, silent adoption.** A new, unrelated session in a reused pane:

```
  new-work   parent=root-1        ← spawned by session TWO
  old-work   parent=root-1        ← spawned by session ONE
  root-1     parent=operator

operator — no waiting mail
└─ root-1 (you) [live]            ← session TWO is marked (you)
   ├─ new-work [live]
   └─ old-work [live]             ← and it now "owns" a child it never spawned
```

Session TWO inherits `root-1`'s name, its journal, **and its predecessor's children**, marked
`(you)`. It did not spawn `old-work`, has no memory of it, and cannot judge its work — but `ps`
tells it that it owns it, and the doctrine tells it to reconcile the tree it owns.

**The design blesses this by analogy to the shipped seat model, and the citation is HONEST.** I
suspected a smuggle — that the "hands come and go, the seat is the standing thing" model was
only ever asserted about *spawned agents* — and **the reverse is true.** `origin/main:skill/SKILL.md:65-71`
asserts the seat model **only** about the human's own root session, never about a spawned agent.
The design is citing it correctly. I record that because I went looking for a smuggle and there
isn't one.

**But the argument still fails, on a distinction the design never draws.** The shipped seat
convention has two safety properties the fix's inheritance does not preserve:

- **Deliberate adoption.** `SKILL.md:73-77`: *"**Take the seat** before acting… Then look before
  touching: `swarm ps`, the operator journal…"* and `:86`: *"open loops belong to the SEAT, and
  any hand **may adopt** them."* The successor **reads, then adopts**. The fix's `root_name()` is
  a **pure lookup**: the successor *is* `root-1` before it has read anything. **Silent.**
- **Project scope.** The seat binds a hand to *the project's* open loops. **The pane binds a
  session to whatever the pane last did — and a terminal pane is not a project.**

And the design's own strongest paragraph is the one that should have caught it (`:147-151`):
*"**The root session is not a durable node.** It is the human's chat window. It compacts. It gets
`/clear`ed. It gets closed when the laptop sleeps."* **Exactly.** And the fix's answer is to make
the **pane** — a thing whose *occupant* changes identity every time the human starts a new
conversation — the sole key of a **durable name and journal**. It binds a durable record to an
ephemeral occupant and calls the binding continuity.

**Cheapest repair (3 lines):** make the inheritance **non-silent**. On a `root_name()` hit,
`claim_root_name` is skipped and nothing is written — so append a *"resumed root-1 in this pane"*
journal line. That restores the seat-take breadcrumb the convention depends on.

**Also real (D.2), and it falsifies the headline in the ordinary case:** two Claude sessions in
two panes on the same project produce `root-1` **and** `root-2` — **the human's `ps` shows two
top-level nodes.** `FIX.md §7c` scores this as a **win** (against the `root.id` alternative,
where both sessions would fight over one identity — and it *is* a win against that). But against
**the design's own promise** — *"the human's direct load is one node"* — it is a miss. It is not
worse than today (today both panes' children write `parent=operator`, so the human sees N workers
flat — two root nodes is strictly better). **The honest sentence is "one node *per session the
human has open*"**, which is a materially weaker claim than §0 and §3a make.

---

## §8 — F: SHOULD THE DOCTRINE BE DELETED? **NO. SHIP BOTH.**

The author asked for the strongest possible case that **the doctrine half is now unnecessary**
and he should ship the 26-line fix alone — and said *deleting my own doctrine would be the best
outcome available*. He asked honestly, so here is the honest answer: **the case is strong, it is
four-grounded, three of the grounds are his own words — and it falls to one executed probe.**

**The steel-man, at full strength:**

1. **The design argues for its own doctrine's deletion**, §3a: *"It deletes doctrine… **Prose that
   a mechanism makes true is prose you can cut.**"*
2. **The default must be skippable** (§4c), so it reduces to *"reflect on your structure."* Is
   that worth **+180 B of always-loaded context** on every swarm, forever?
3. **The design concedes it in advance** — F-DOCTRINE: *"after the fix, **the shape claim is no
   longer a test of the doctrine at all**… **A doctrine whose only remaining job is speech is a
   doctrine you should be willing to cut if it doesn't happen.**"*
4. **It is dead text on 2 of 3 real goals** (§8, MEASURED): the skill never loaded, 2/2, on goals
   meeting every documented trigger.

**And it fails, on ground (i), which is the one carrying the weight.** §2/F.3 above: the flat row
is **not** unrepresentable. It is **indented**. Eight workers under `root-1`, eight panes, and
every one of them can mail the human — **by contract** (`WORLD.md:57-59`: *"nothing ever refuses a
message to the operator"*). The data model makes **one particular parent string** unwritable. It
does not make the *load* unwritable, and load is what the doctrine is for.

Re-read the other three against that:

- **(ii) "it reduces to *think about it*"** — stands, **but that is now the point.** After F.3,
  *"think about your top layer"* is the **only** mechanism in the entire system that bounds the
  human's attention, because **no file format can.** `SPAN.md:43-45` says so outright: *"The
  operator names their own span — this operator says ~3 — and **nothing in the tool today
  respects, records, or even mentions it.**"* **The fix does not change that sentence.**
- **(iii) the concession** — correct, but it **concedes the wrong thing.** F-DOCTRINE should never
  have been narrowed to *"did it announce."*
- **(iv) the skill doesn't fire** — the strongest of the four, and it argues for **fixing the
  trigger**, not deleting the payload. The design says so itself (§8: *"it should probably outrank
  this one"*).

**So: SHIP BOTH.** But the author does not get to read that as vindication, because **two things
he wrote are false as executed and must change:**

1. **The fix's headline claim.** *"`human → flat row of workers` becomes unrepresentable"* (§0) and
   *"the human's direct load is one node because that is the only tree the data model admits"*
   (§3a) are **wrong**. The true claim is narrower and still worth 26 lines:
   > ***`parent=operator` becomes unwritable, so the tree the tool records is the tree that
   > exists — and `ps` stops reattaching a live human's children to a mailbox.***
2. **§4c's comfort must be struck.** *"After the fix, spawning the leaves directly no longer
   produces the flat row"* is exactly the false comfort F.3 refutes. It produces the flat row one
   indent down, with every leaf holding a direct line to the human.

**And §4b, on the SPAN override:** declaring it is honest and I do not score it as dishonesty. But
after dropping the PHILOSOPHY §9 citation (§6), what remains is *one REASONED asymmetry — "you
cannot un-flood a human's window after the fact" — standing against a 3-for-3 MEASURED record that
load never summoned a coordinator.* That is a much weaker thing to write, and **it should be
written as such** rather than as a settled override.

**The doctrine that actually survives is not "default one coordinator."** It is the sentence
`SPAN.md` already wrote and the tool still does not enforce: ***never let the tree press more
direct attention on the operator than they asked for*** — where **attention** means panes to watch
and mail to read, and the count that matters is **agents beneath the human's session**, not nodes
in a `ps` render.

**Replace the F-DOCTRINE falsifier** (`red2-doctrine`'s, and it is better than the shipped one):
after a real multi-part goal in a root session, collect **(a)** `ls .swarm/queue/operator/ | wc -l`
and **(b)** the number of descendants of `root-*`. **FALSIFIED WHEN** either exceeds the operator's
declared span (~3). That tests what the doctrine is actually for — and, unlike the shipped
falsifier, **the fix does not make it un-collectable.**

---

## §9 — WHAT IS ACTUALLY RIGHT, SAID PLAINLY

A hit piece is as useless as a rubber stamp, so: **the core of this design is correct, and I
confirmed it independently rather than relaying it.**

- **The diagnosis is sound and it is the real prize.** `parent = my_name()` in `cmd_spawn`;
  `my_name()` returns `SWARM_AGENT_ID or "operator"`; `operator` is a reserved name that can
  never have a record; `cmd_spawn` takes only `--model` and `--cwd`. **`parent=operator` is the
  only value a root session can write.** No prose could ever have fixed that, and the shipped
  doctrine was therefore **never given a chance to fail** — NOT-ADJUDICATED, exactly as the
  author says. He inherited a "doctrine FIRED" brief, and he **overturned his own premise** and
  led the document with it. That is the behavior this system is supposed to produce.
- **`WORLD.md:57` really is false in the code**, and the contradiction with `WORLD.md:12` is
  real. The contract says mailbox-not-node; the code makes `operator` the identity of a session.
- **The citation discipline is genuinely good.** Every load-bearing quote I checked — SPAN,
  STRUCTURE's 3-for-3, DECISIONS' 16h→14s decay, PHILOSOPHY, WATCHLIST, the shipped SKILL.md
  bytes — is **verbatim and accurate.** Two misses in ~20 (§6), one of which makes the fix look
  *worse* than it is.
- **The §3b catch was the right call and it was load-bearing.** Catching `"pane": ""` — where a
  paneless root renders dead and `eff_parent` reattaches its children back to `operator`,
  restoring the flat row *on the human's screen* — is the difference between a fix that works
  and a fix that only works in the files. That was good adversarial reading of his own child.
- **He escalated the propose-and-confirm lock rather than silently overriding it.** Correct.
- **He named §8 (the skill often doesn't fire) as possibly outranking his own work.** Also
  correct, and rare.

---

## §10 — WHAT I WOULD DO

**Do not ship what is on disk.** `git stash@{0}` is the draft the author's own child condemned:
it silently drops mail for a live agent whose record is momentarily unreadable (§0). If someone
`git stash pop`s and commits, that ships.

**Ship `FIX.md §7g` — plus three lines the review found:**

1. **A2 (blocking).** `relation()` must recognize a root session as the human:
   ```python
   if sender == "operator" or sender.startswith("root-"):
       return "the OPERATOR (the human at the root)"
   ```
   Without this, **zero of seven** agents in a normal tree can hear the human as the human, and
   `WORLD.md:19`'s promised OPERATOR sender class becomes unreachable by any ordinary path. The
   two goals were never in tension: let the root be a **node** in the tree *and* the **OPERATOR**
   on the wire.
2. **Attack A.** `claim_root_name` should `die()` when `HERDR_PANE_ID` is empty, rather than
   silently minting a phantom root per spawn. **A root that cannot be identified cannot be safely
   named.**
3. **D.4.** On a `root_name()` hit, append a *"resumed root-1 in this pane"* journal line — so the
   seat is **taken**, not silently inherited.

**Then fix the document, which currently overclaims in three places:**

- **§0/§3a:** *"`human → flat row of workers` becomes unrepresentable"* / *"the human's direct
  load is one node"* → **false as executed.** Narrow it to what is true and still excellent:
  *`parent=operator` becomes unwritable, so the tree the tool records is the tree that exists.*
- **§4c:** strike *"spawning the leaves directly no longer produces the flat row."*
- **§3a/§6:** delete `settings/root.id` — **it does not exist**, and removing it from the cost
  table makes the fix's WATCHLIST-#7 case *stronger* (0 new files, not 1).

**On the operator's two open questions:**

- **The wait:** the author recommends announce-only, with a fallback of *"confirm on the first
  swarm in a project."* **The fallback is dead** (§5) — nothing witnesses "first swarm," and the
  operator pre-authorized the consequence: *"say so and default to announce-only."* **So: cut the
  wait, keep the announce, and put first-contact pedagogy in `install.sh`, where first contact
  actually happens.**
- **The doctrine:** **keep it.** He asked me to kill it and I could not — not because the
  steel-man is weak (it is strong, and three of its four grounds are his own sentences) but
  because the probe shows the fix does not do the doctrine's job. After the fix, **prose is the
  only mechanism in the system that bounds the human's attention.** `SPAN.md:43-45`: *"nothing in
  the tool today respects, records, or even mentions"* the operator's span. That is still true
  after this fix.

**The single sentence, if only one survives:** *the diagnosis is right and the fix is worth
shipping — but it makes the tree honest, not the human's day quieter, and the code sitting on
disk is not the code that was tested.*

---

## §11 — HOW THIS REVIEW WAS RUN, AND WHERE IT WAS KIND TO ITSELF

The brief asked me to catch rig-kindness. **I committed it, and my own child caught me** (§5): I
verified the `.swarm/`-as-witness claim against the one repository in the world where it is true,
and stopped one line short of the comment that says why. I have left the reversal in the document
rather than quietly rewriting the section, because a reviewer who hides his own miss has no
standing to report anyone else's.

The children were briefed to attack and **three of their most promising attacks failed, and all
three said so:**

- `red2-trace` was pushed hard toward *"the paneless-root bug is the headline"* and came back
  **WOUNDS, not KILLS** — it could not reach `HERDR_ENV=1` without `HERDR_PANE_ID` from stock
  herdr, and refused to inflate it. It also reported **A5 SURVIVES** — the hook gates do **not**
  crash — which was the author's own top-billed worry.
- `red2-doctrine` went after the seat model's foundation with **herdr's own documentation** in
  hand (*"do not treat them as durable ids"*), tested it against the live instance, found the
  counter is monotonic and persisted, and wrote up **its own failure**. It also ran the *control*
  on the `cd`-to-another-repo attack, found the bleed is identical on unpatched `HEAD`, and
  declined the hit.
- `red2-mech` **caught its own rig flattering itself**: its first concurrency run reported
  SURVIVES because a fake launcher was serializing the spawns. It identified that as a rig
  artifact, rebuilt with true overlap, and **flipped its own verdict to WOUNDS** — finding a real
  TOCTOU in `claim_root_name` (12 concurrent same-pane spawns → **2–4 `root-*` records for one
  pane**; `O_CREAT|O_EXCL` serializes *names*, not *panes*, so the "pane IS identity" invariant
  breaks). `FIX.md §7c`'s table claims pane-keying kills the concurrent-root case — but it only
  reasoned about *different* panes.

**What none of us tested:** every scenario ran against a **fake `herdr`** and **fake `claude`** in
a sandbox `SWARM_DIR`. They prove what the *tool* records and renders. **They prove nothing about
what a real model does when handed the doctrine** — that arm still needs the cold root-session
rig, and the design says so itself. The one thing checked against the real herdr is pane-id
durability (§7), and that is live output.
