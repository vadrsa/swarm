# Structure mechanics probe — 2026-07-12

Agent: structure-mech. For: operator-structure-scout.
Scope: facts only, quoted from `bin/swarm` (1150 lines) and the live `.swarm/` tree. No design opinions.

**Headline (the load-bearing one):** VERIFIED — a root session that spawns ONE coordinator, which then spawns workers, leaves the human with **exactly one direct child** in the files. Parent is recorded from `SWARM_AGENT_ID` at the spawning process, so the coordinator's spawns get `parent: coordinator`, and `ps` renders only `kids["operator"]` as roots. See Q3.

---

## Q1 — What determines an agent's NAME and PARENT? What is a ROOT session's identity?

**VERIFIED.**

NAME: chosen by the spawner, first positional arg to `spawn`; validated, never derived.

```python
# bin/swarm:844
    name, task = argv[0], argv[1]
# bin/swarm:854-857
    if not _re.match(NAME_RE, name):
        die(f"bad name '{name}': lowercase letters, digits, hyphens (max 40). "
            f"The name is chosen, not derived — pick one that names the work.")
# bin/swarm:29 (the regex)
NAME_RE = r"^[a-z0-9][a-z0-9-]{0,39}\Z"
```

PARENT: **not a flag, not an argument.** It is the spawning process's own identity, read from the environment at spawn time:

```python
# bin/swarm:868-869
    root = root_dir()
    parent = my_name()
```

And `my_name()` is the whole of identity in this tool:

```python
# bin/swarm:63-64
def my_name():
    return os.environ.get("SWARM_AGENT_ID") or "operator"
```

**A ROOT session (no `SWARM_AGENT_ID`) is therefore named `operator`.** There is no other identity mechanism — no config file, no argument, no ledger. `SWARM_AGENT_ID` unset ⇒ you are `operator`, full stop.

The reserved-name guard makes the collision explicit and total: nobody can *spawn* an agent called `operator`, so the name is available to exactly one thing — an unset env var:

```python
# bin/swarm:861-862
    if name in ("operator", "delivered"):
        die(f"'{name}' is reserved")
```

Parent fallback on read is also `operator` (a missing/blank `parent` field reads as operator):

```python
# bin/swarm:132-133
def parents_of(agents):
    return {n: (a.get("parent") or "operator") for n, a in agents.items()}
```

## Q2 — Root session runs `swarm spawn foo "task"`: what parent lands in `.swarm/agents/foo.json`? Any way to make it NOT `operator`?

**VERIFIED — parent recorded is `operator`.** The code path, in order:

1. `parent = my_name()` → `os.environ.get("SWARM_AGENT_ID") or "operator"` → `"operator"` (bin/swarm:869, 64).
2. Written verbatim into the agent record:

```python
# bin/swarm:920-922
    write_atomic(agent_rec_path(root, name), json.dumps(
        {"name": name, "parent": parent, "pane": pane, "tab": tab,
         "model": model, "cwd": cwd, "task": task, "ts": now_ms()}))
```

with `agent_rec_path` = `.swarm/agents/<name>.json` (bin/swarm:79-80).

3. The same `parent` string is also baked into the child's spawn header (bin/swarm:896: `write_atomic(taskfile, spawn_header(name, parent) + task)`).

**Is there ANY way for a root session to spawn a child whose parent is NOT `operator`?**

- **No `--parent` flag.** `spawn`'s flag parser accepts exactly two flags and dies on anything else:

```python
# bin/swarm:845-853
    rest, model, cwd = argv[2:], "", os.getcwd()
    while rest:
        if rest[0] == "--model" and len(rest) > 1:
            model, rest = rest[1], rest[2:]
        elif rest[0] == "--cwd" and len(rest) > 1:
            cwd, rest = rest[1], rest[2:]
        else:
            die(f"spawn: unknown flag {rest[0]}")
```

- **`SWARM_AGENT_ID` CAN be set, and it works.** `my_name()` is a plain `os.environ.get`; nothing validates it against the agents dir, nothing checks that the pane matches, nothing guards it. So `SWARM_AGENT_ID=coordinator swarm spawn worker "task"` from the root session's shell would write `{"parent": "coordinator", ...}` into `.swarm/agents/worker.json`. **This is an env-var override, not a supported flag** — it is exactly the mechanism spawn itself uses to give the child its identity (bin/swarm:906-907, below). Nothing in the code prevents a human or a root session from setting it by hand. **UNKNOWN:** whether any doctrine/skill text tells anyone to do this; I found no such instruction in `bin/swarm` (it contains zero occurrences of "skill", see Q6).

The forward direction — how a *spawned* child gets a non-operator identity — is the herdr tab env:

```python
# bin/swarm:906-907
    d = herdr_json(["tab", "create", "--cwd", cwd, "--no-focus", "--label", name,
                    "--env", f"SWARM_DIR={root}", "--env", f"SWARM_AGENT_ID={name}"])
```

So: **the pane's env is the sole carrier of identity.** A spawned child's tab has `SWARM_AGENT_ID=<its own name>`; the root session's terminal does not have the var at all, which is precisely why it is `operator`.

## Q3 — Root spawns `coordinator`; `coordinator` spawns workers. What parent do the workers get? Does the human's node have exactly 1 direct child?

**VERIFIED — workers get `parent: coordinator`, and the human's node has exactly 1 direct child, in the files and in `ps`.**

Chain of code facts:

1. Root spawns `coordinator` → `.swarm/agents/coordinator.json` has `"parent": "operator"` (Q2).
2. The coordinator's pane was created with `--env SWARM_AGENT_ID=coordinator` (bin/swarm:907).
3. When the coordinator runs `swarm spawn worker-a`, that process's `my_name()` returns `"coordinator"` (bin/swarm:64 — env var is set), so `parent = my_name()` = `"coordinator"` (bin/swarm:869), written as `{"parent": "coordinator"}` (bin/swarm:921).
4. `ps` builds the tree from those recorded edges and renders **only** the children of `operator` as roots:

```python
# bin/swarm:519-531 (eff_parent + kids)
    def eff_parent(n):
        p = agents[n].get("parent") or "operator"
        ...
    kids = {}
    for n in shown_set:
        kids.setdefault(eff_parent(n), []).append(n)
# bin/swarm:553
    roots = kids.get("operator", [])
```

So `kids["operator"] == ["coordinator"]` — one root line — and the workers render nested underneath it via `walk()`'s recursion (bin/swarm:544-551).

**Load-bearing conclusion: yes.** "The human's direct children" is a well-defined, file-witnessed set: `{n : agents[n].parent == "operator"}`. It is exactly the set of agents spawned by a session with no `SWARM_AGENT_ID`. One coordinator spawned from root ⇒ that set has size 1, regardless of how many workers the coordinator spawns.

**Corroborating live evidence** — the current `.swarm/agents/` (90 records) already shows deep trees working exactly this way. Parent distribution:

```
23 operator          16 field-tester      8 fleet-eval        4 onboarding-scout
 4 deleg-heavy-after-1  3 decision-wiring  3 v3-red           3 graveyard-check
 3 wiring-surfaces   3 decision-scout     3 harness-scout     3 grave-notlist
 3 hook-scout        3 operator-structure-scout  2 pipeline-scout  2 proxy-scout
 1 warm-coord-1      1 wiring-drafter     1 pipeline-drafter  1 eval-red
```

Non-`operator` parents are recorded and honored (e.g. `field-tester` has 16 direct children). The mechanism is proven in the field; the failure is 23 records carrying `parent: operator`, i.e. 23 agents spawned directly from root sessions.

One caveat on the `dead:` reattach rule, in case it matters to the design: `eff_parent` **skips dead ancestors**. If the coordinator's pane dies, its live workers reattach to the nearest living ancestor — which is `operator` — and would then render as direct children of the human in `ps`:

```python
# bin/swarm:519-526
    def eff_parent(n):
        # nearest non-dead ancestor; ...
        p = agents[n].get("parent") or "operator"
        seen = set()
        while p in agents and p not in shown_set and p not in seen:
            seen.add(p)
            p = agents[p].get("parent") or "operator"
        return p
```

**The files never change** (`agents/worker-a.json` still says `parent: coordinator`); this is a *view* rule only. So the answer differs by which you mean: **in the files — always exactly 1. In `swarm ps` — 1 while the coordinator is live; N if the coordinator's pane dies with workers still running.**

## Q4 — What does `swarm ps` show, what is the operator mailbox path, who can `send` to whom?

**VERIFIED.**

`cmd_ps` (bin/swarm:1049-1065) loads every agent record, herdr's live pane set, per-agent queue depth, junk count, and the last event fact, plus operator mail, and hands them to the pure renderer:

```python
# bin/swarm:1057-1060
    op_mail = [(r.get("from", "?"), int(r.get("ts") or 0))
               for _, _, r in list_waiting(root, "operator")]
    out = render_ps(agents, live, queues, events, my_name(), op_mail, now_ms(),
                    junk)
```

The rendered output, in order (bin/swarm:493-575):

1. **Operator mail on top** — either the count plus a `from <name>, <age> ago` line per waiting message, or "no waiting mail":

```python
# bin/swarm:505-512
    if op_mail:
        lines.append(f"operator — {len(op_mail)} message(s) waiting for the human "
                     f"(queue/operator/):")
        for frm, ts in op_mail:
            lines.append(f"    from {frm}, {fmt_age(now - ts)} ago")
    else:
        lines.append("operator — no waiting mail")
```

2. **The tree**, rooted at `kids["operator"]`, one line per live agent: name, `(you)` if it's the caller, `[live]`, `q=<depth>`, `idle <age>`, and an indented `last: "<80 chars>"` line if there's a last-words fact:

```python
# bin/swarm:539-545
        lines.append(f"{prefix}{branch}{name}{you} [{alive}] {q_of(name)} {idle}")
        if ev and ev.get("last_words"):
            cont = "   " if is_last else "│  "
            lines.append(f'{prefix}{cont}   last: "{ev["last_words"][:80]}"')
```

3. Orphan lines (`?─ <name> [parent <p> unknown]`) for live agents whose parent chain leaves the records (bin/swarm:569-572).
4. **`dead: <comma-separated names>`** — one shared line, names only (bin/swarm:573-574).

Note the operator is **not** a node in this tree. It is a header line. The human's own name never appears with a `[live]`/`q=`/`idle` line.

**Operator mailbox path:** `.swarm/queue/operator/` — from the generic `q_dir(root, name)`:

```python
# bin/swarm:67-68
def q_dir(root, name):
    return os.path.join(root, "queue", name)
```

and `delivered_dir` = `.swarm/queue/operator/delivered/` (bin/swarm:71-72). Confirmed on disk: `.swarm/queue/operator/` exists, currently holds **0** waiting `.json` files and a `delivered/` directory with ~60 records (e.g. `1783622829437-hardener.json`).

**Who can send to whom: anyone to anyone.** `cmd_send` has exactly one recipient check — the name must be a known agent, or the literal string `operator`:

```python
# bin/swarm:985-987
    if to != "operator" and to not in agents:
        die(f"unknown agent: {to}")
```

There is **no parent/child restriction on send.** Any agent may send to any other agent, to `operator`, and (nothing forbids it) to itself. The tree relation is used only to *label* the message for the recipient, via `relation()`:

```python
# bin/swarm:158-174
def relation(sender, recipient, parent_of):
    if sender == "operator":
        return "the OPERATOR (the human at the root)"
    if parent_of.get(recipient) == sender:
        return "your parent"
    if parent_of.get(sender) == recipient:
        return "your child"
    sp = parent_of.get(sender)
    if sp and sp == parent_of.get(recipient):
        return "your sibling"
    return "another agent"
```

Two asymmetries between `operator` and every real agent:

- **No doorbell for operator.** Sending to a real agent rings its pane; sending to `operator` rings nothing, because there is no pane:

```python
# bin/swarm:1036-1039
    # Doorbell, best-effort, only for mail that was actually queued. The
    # operator is a mailbox, not a node: no pane, no doorbell, no warning —
    # the human sees the mail at the top of `ps`.
    if proceed and to != "operator":
```

- **Nothing auto-drains operator mail.** The `deliver` hook — the thing that moves a queue file to `delivered/` — hard-exits for operator (see Q7). Per `skill/SKILL.md:69-70`, the drain is a *human/hand convention*: "A hand claims an operator-mail file by moving it to `queue/operator/delivered/` AND writing a hand-tagged claim line in the operator journal". The 60 files in `delivered/` were moved there by hand, not by code.

## Q5 — Is `operator` a real node with a file, or a synthetic parent string?

**VERIFIED — synthetic. It is a string, not a node.**

Filesystem, checked directly:

```
$ ls .swarm/agents/operator.json
ls: .swarm/agents/operator.json: No such file or directory
```

90 records exist in `.swarm/agents/`; none is `operator.json`, and none can ever be, because spawn refuses the name (bin/swarm:861-862, quoted in Q1). `load_agents` only reads that directory (bin/swarm:125-131), so `"operator" not in agents` is invariant.

The string is manufactured in three places, all defaults:

- `my_name()`: `os.environ.get("SWARM_AGENT_ID") or "operator"` (bin/swarm:64)
- `parents_of()`: `a.get("parent") or "operator"` (bin/swarm:133)
- `render_ps`: `roots = kids.get("operator", [])` (bin/swarm:553)

The tool's own comment says it outright:

```python
# bin/swarm:1037-1038
    # operator is a mailbox, not a node: no pane, no doorbell, no warning —
    # the human sees the mail at the top of `ps`.
```

What `operator` *does* have on disk, despite having no agent record:

- **a queue**: `.swarm/queue/operator/` + `delivered/` (exists; `send` writes it like any other)
- **a journal**: `.swarm/journal/operator.md` (exists, 55,353 bytes, mtime today 19:59)

But **no** `agents/operator.json`, **no** `event/operator.json`, **no** `settings/operator.*`, **no** pane, **no** hooks. (`settings/` does contain `operator-structure-scout.*` and `red-operator.*` — those are ordinary agents whose *names begin with* "operator"/"red-operator", not the operator seat.)

So `operator` is precisely: **a name that is one env-var-absence, one queue directory, and one journal file — and nothing else.** That is the collision your audit named: the human's root session and the string used as "no parent" are the same identifier, and any session with `SWARM_AGENT_ID` unset silently *is* the operator.

## Q6 — `spawn_header()`: full text. Does a spawned child ever see `skill/SKILL.md`?

**VERIFIED. Does the child see SKILL.md: NO — `grep -i skill bin/swarm` returns ZERO hits.**

The child's prompt is exactly `spawn_header(name, parent) + task`, written to `.swarm/settings/<name>.task` (bin/swarm:896) and `cat`'d into `claude "$PROMPT"` by the launcher (bin/swarm:833-835). The header, verbatim, with `{name}`/`{parent_desc}` substituted:

> You are agent **{name}** in a swarm — a tree of Claude agents. Your parent, who judges and approves your work: **{parent_desc}**.
> You have the `swarm` CLI: `swarm spawn <name> "<task>"` to delegate, `swarm send <name>` to message (a message is a claim on one turn), `swarm ps` to see the whole tree, `swarm world` for the full contract — read it before coordinating others.
>
> Your duties (briefed, not enforced): keep your journal at `.swarm/journal/{name}.md` — append timestamped entries in your own words as you work, and always before going idle; a reconciliation entry names its falsifier (the observation that would show you are off track). Report to your parent when done or stuck. Produce concrete, inspectable artifacts — all work, including yours, is judged by reading it, never by claims.
>
> Delegate by default: keep judgment, verification, and glue; spawn children for the work itself — doing parallelizable work serially yourself is off-track. Each reconciliation, ask whether the tree still matches the remaining work and whether your span still matches your attention: spawn what is missing, close harvested children whose workstream is done, split what you cannot attend, absorb what no longer earns its layer — keep a child only if you can name its next task. When you dispatch to a name you have dispatched to before, say what recurred, in the same entry — this is how repeated shapes of work become visible to anyone reading your journal. You are over span when you can no longer name each child's state and the next artifact you expect from it without re-reading. If a spawn would take you past that, spawn a coordinator and split the stream instead; when a coordinator's stream shrinks to what you can hold directly, absorb it — harvest, close, take the survivors. The operator's span is theirs to declare and yours to protect: never let the tree press more direct attention on the operator than they asked for. When you judge a child's work, judge its delegation too. Closing a subtree to re-form a better shape is normal and encouraged — harvest its journal and artifacts first, journal the reason; files survive close, and burned names are the record working as designed.
>
> `--- YOUR TASK ---`

`{parent_desc}` is computed at bin/swarm:772-773 and is the ONLY place the header varies by tree position:

```python
# bin/swarm:771-773
def spawn_header(name, parent):
    parent_desc = ("the human operator" if parent == "operator"
                   else f"agent `{parent}`")
```

So a child spawned by a root session is told *"Your parent, who judges and approves your work: **the human operator**."* — and a child spawned by an agent is told *"...: **agent `<parent>`**."*

The same header is re-injected on every SessionStart/compaction, via `cmd_restore` reading `settings/<name>.task` (bin/swarm:739-757).

**SKILL.md reach: the tool has none.** Zero occurrences of "skill" (case-insensitive) in all 1150 lines of `bin/swarm`. The only pointer the child gets to any further doctrine is the string `swarm world` in the header, which prints `WORLD.md` from the repo root:

```python
# bin/swarm:1090-1096
def cmd_world():
    # WORLD.md sits at the repo root, one level above bin/ ...
    doc = os.path.join(
        os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "WORLD.md")
```

`skill/SKILL.md` — which contains the operator-seat doctrine, the ~3 span default, and the review-desk pattern (SKILL.md:40-75) — is loaded by the Claude Code skill mechanism into a session that *invokes* the skill. A spawned child's session is started by `claude --settings <file> "$PROMPT"` (bin/swarm:834-835) and **is never told the skill exists**. That is a code fact, not an inference: the string does not appear in the file.

## Q7 — Operator journal path; does the root session write to it?

**VERIFIED — path exists and is written; the writing is convention, not code.**

Path: `.swarm/journal/operator.md`, by the generic rule:

```python
# bin/swarm:75-76
def journal_path(root, name):
    return os.path.join(root, "journal", f"{name}.md")
```

On disk: `.swarm/journal/operator.md`, 55,353 bytes, mtime 2026-07-12 19:59. So **yes, something is writing it, and recently.**

But **`bin/swarm` never writes it.** The tool writes a journal in exactly one place — `claim_name`/`cmd_spawn`, creating the *child's* journal as its tombstone (bin/swarm:764-767, 876-880) — and `operator` can never be spawned (bin/swarm:861). Every hook entrypoint that could touch operator state hard-exits first:

```python
# bin/swarm:686-687   (deliver)
    if my_name() == "operator":
        sys.exit(0)
# bin/swarm:703-705   (event: stop/notification)
    if my_name() == "operator":
        sys.exit(0)
# bin/swarm:738-740   (restore)
    if my_name() == "operator":
        sys.exit(0)
```

So a root session gets **no** delivery hook, **no** event fact, **no** restore injection, and **no** automatic journal entry. The 55KB file is written **by the root session's own hands, as a doctrinal convention**, described in `skill/SKILL.md:53-75`: "The seat is the standing thing: one journal (`.swarm/journal/operator.md`), one mailbox, one set of open loops... everything below is **convention in that journal, not tool state**."

That is the whole asymmetry in one line: **every spawned agent's journal, mailbox, delivery, restore, and event fact are enforced by code; the operator's are enforced by nothing.**

---

## Summary table

| # | Question | Verdict |
|---|---|---|
| 1 | Name / parent source | VERIFIED — name = positional arg (chosen); parent = `my_name()` = `$SWARM_AGENT_ID or "operator"` (bin/swarm:64, 869). Root session **is** `operator`. |
| 2 | Root spawn → parent recorded | VERIFIED — `"parent": "operator"` (bin/swarm:921). No `--parent` flag (bin/swarm:845-853). `SWARM_AGENT_ID` **can** be set by hand and would change it — plain `os.environ.get`, unvalidated. |
| 3 | Coordinator's workers | VERIFIED — workers get `parent: coordinator`; **in the files the human has exactly 1 direct child.** In `ps`, still 1 while the coordinator is live; its death reattaches live workers to `operator` in the *view* only (bin/swarm:519-526). |
| 4 | `ps` output / mailbox / send | VERIFIED — operator mail header, then tree from `kids["operator"]`, then orphans, then `dead:`. Mailbox `.swarm/queue/operator/`. **Anyone may send to anyone**; the only check is that the recipient exists (bin/swarm:986). |
| 5 | Is `operator` a node? | VERIFIED — **synthetic string.** No `agents/operator.json` (spawn reserves the name, bin/swarm:861). Has a queue and a journal; no record, no pane, no hooks. |
| 6 | `spawn_header()` text / SKILL.md | VERIFIED — full text quoted above; the only tree-dependent phrase is "the human operator" vs "agent \`X\`". **`grep -i skill bin/swarm` → 0 hits.** A spawned child never sees `skill/SKILL.md`. |
| 7 | Operator journal | VERIFIED — `.swarm/journal/operator.md`, 55KB, live. **Written by convention only**; `bin/swarm` never writes it, and all three hooks `sys.exit(0)` when `my_name() == "operator"` (bin/swarm:687, 705, 740). |

No UNKNOWNs except one, flagged in Q2: whether any doctrine text anywhere instructs a session to set `SWARM_AGENT_ID` by hand — out of scope for a `bin/swarm` read.
