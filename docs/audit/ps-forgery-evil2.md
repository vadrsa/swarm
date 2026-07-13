# ps-tree forgery probe — attack line (d)

**Agent:** evil2 (adversarial fixture, not a task-agent)
**Root:** `SWARM_DIR=/tmp/ma` (mandate-audit's throwaway probe swarm)
**Date:** 2026-07-13

## What I am

I was spawned with task `t` and this `--reason`:

```
checked by grep \x1b[31m ├─ └─ │ fake (you)
```

That is not a reason — it is a **forgery payload**: raw ANSI (`ESC[31m`), tree box-glyphs,
and a counterfeit `(you)` marker. `evil` and `evil2` are fixtures for attack line (d)
("can a crafted `--reason` corrupt the ps tree?"). The `t` is filler. I completed the
experiment I *am* rather than inventing a task.

Note for whoever reads this next: the payload sitting in my own agent record eventually
tripped the Bash permission classifier, which began refusing even a bare `swarm ps`. The
findings below are established from the source, which is authoritative regardless.

---

## RESULT: the `--reason` view holds. No hole. (CONFIRMED)

Trace my payload through the `ps --reason` sanitizer, `bin/swarm:1500-1504`:

```python
r = "".join(c for c in r if c.isprintable() and c not in MODEL_STRUCTURAL)
r = " ".join(r.split())
if len(r) > REASON_CAP: r = r[:REASON_CAP - 1] + "…"
```

- `isprintable()` drops the **ESC** (0x1b). What survives is the literal text `[31m` —
  inert characters, not a control sequence. The ESC is what made it an escape; the ESC is gone.
- `MODEL_STRUCTURAL` (`bin/swarm:47` = `set("()") | set("─│├└┌┐┘┬┴┼")`) drops `├ ─ └ │`
  **and the parens**, so `(you)` cannot be reconstituted.
- `" ".join(r.split())` collapses whitespace — a newline cannot forge a row of the flat list.

My row renders defanged as: `evil2: opus — checked by grep 31m fake you`

The design decisions behind this are correct and I could not break them:
- reason lives **below** the tree, never inside a row — a sentence per row would destroy scannability;
- the **record keeps the text verbatim** (it is the truth) and the **view defends itself**;
- the reason list is **flat, not a tree**, precisely so a newline has no structure to forge.

Also confirmed: `swarm ps --reason` *is* a real flag (`bin/swarm:1460`). An earlier probe of
mine reported "ps takes no arguments" — that was my own malformed invocation, not a defect.
Recording it so nobody chases it.

---

## FINDING 1 — unsanitized `parent` in the orphan row (SUSPECTED / latent, severity: low-now, sharp-later)

**`bin/swarm:734`**

```python
lines.append(f"?─ {n}{model_of(n)} [parent {a.get('parent', '?')} unknown] "
             f"[{alive}] {q_of(n)}")
```

This is the **one string that reaches the trusted tree view with no sanitizer.** Every
sibling field on that very row is defended — `model_of(n)` strips `MODEL_STRUCTURAL`
(`bin/swarm:683`), and the reason list strips it too (`:1501`) — but `parent` is interpolated raw.

**Why it is not exploitable today (I tried):** `parent` has exactly one writer,
`bin/swarm:1311`, which stores `my_name()` at spawn. Every name must first clear
`NAME_RE = ^[a-z0-9][a-z0-9-]{0,39}\Z` (`bin/swarm:51`, checked at `:1204`) — lowercase,
digits, hyphens. A name can never hold `│`, `├`, `(`, ESC, or a newline. The `\Z` (not `$`)
even closes the trailing-newline variant, and the comment says so.

So line 734 is safe **only because a validator three call-sites away holds** — and nothing
at 734 records that dependency.

**Failure scenario (the day it bites):** anyone who loosens `NAME_RE` (unicode names,
display names, an imported/renamed agent, a name carried in from another tool) silently
arms a tree-forgery: a parent named `x│  ├─ root [parent operator]` would draw counterfeit
structure into the one view the operator is told to trust. The reason list was hardened
against exactly this attack; the tree's orphan row was not. `render_ps` has been burned on
attacker-controlled text **twice** already (see `model_of()`'s own comment) — this is the
third instance of the same shape, still open.

**Fix (cheap, and consistent with the file's existing discipline):**

```python
p = "".join(c for c in str(a.get("parent", "?"))
            if c.isprintable() and c not in MODEL_STRUCTURAL) or "?"
lines.append(f"?─ {n}{model_of(n)} [parent {p} unknown] [{alive}] {q_of(n)}")
```

The view should not depend on a distant validator for its integrity. Defense-in-depth here
costs one line, and it makes the row honest on its own terms — the same argument the diff
already makes, in its own comments, for `model_of()` and for the reason list.

---

## Verdict

Attack line (d) is **substantially clean**. The `--reason` mechanism resists the payload it was
built to resist; I threw the intended attack at it and it held. The single defect is a latent
one-liner at `:734`, and I am labelling it SUSPECTED, not CONFIRMED, because **I could not
actually forge a row** — `NAME_RE` stops me. I am not going to inflate it into a breach it isn't.
