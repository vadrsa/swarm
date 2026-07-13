# Red review — `swarm ps` shows the model

**Reviewer:** `ps-model-red` (adversarial). **Date:** 2026-07-13.
**Under attack:** the design in `.swarm/journal/ps-model.md`, entry *"2026-07-13 — design decided"*.
**Diff under attack:** none. `swarm-dev/ps-model` exists but its tip **is** `main` (`aa6063d`), zero
commits ahead, empty `git diff main...swarm-dev/ps-model`. There is a worktree
(`…/scratchpad/wt-psmodel`) also parked at `aa6063d`. **This review is of the design only**, and I
say so rather than pretend I reviewed code.

## The field, measured (not vibed)

```
ls .swarm/agents/*.json | wc -l        →  150      (design says 143; it grew — same shape)
model values, counted                  →  149 × ''   1 × 'opus'   0 missing-key
the one pin                            →  updater-v2, model "opus", parent operator, currently dead
```

So the ratio is **149:1**, not 142:1. The design's argument is unchanged by that, but its numbers are
stale and the doc should say 149/150.

---

## Attack A — "hiding the default helps" — **WOUNDS**

The design gives two reasons for rendering nothing on inherited agents. Reason (a) survives.
**Reason (b), the one the design calls "the stronger one", is false.** That is the finding.

### A1. Reason (a) — the horizontal-budget argument — **SURVIVES**

> *"a per-line badge that is identical 142 times fights [scannability]"*

I tried to break this with the "absence is ambiguous" steelman: an operator cannot distinguish
*inherited* from *feature-broken/field-missing*. It does not land, for a reason I can measure:

- **There is no missing-key case to confuse it with.** All 150 records carry the `model` key; the
  writer (`bin/swarm:920-922`) writes it unconditionally, so `''` is *always* written, never omitted.
  "The field is missing" is not a state the renderer can be in. The ambiguity the steelman needs
  does not exist in the data.
- **The disambiguator is one line away and already in ps.** If an operator doubts the feature works,
  the *presence* of a `[opus]` badge anywhere in the tree proves it. If no agent is pinned, there is
  nothing for the feature to show and "broken" and "correct" are observationally identical **because
  they produce identical output** — which is not a bug, it is the feature having nothing to say.
- Live-tree budget is real but not tight: the longest living line in the current real tree is **97
  chars** and the tree is **33 rows**. A `[~]` badge on 149 lines would cost ~4 chars × 149 lines of
  pure noise to disambiguate a state that cannot occur. Rejected.

**Verdict: SURVIVES.** A `[~]`/`[inherit]` marker is worse. Do not add it.

### A2. Reason (b) — "we do not know an inherited agent's model" — **WOUNDS (the rationale, not the decision)**

The design writes:

> *"the real model came from the spawner's environment at launch and was never recorded"*

and treats this as an honesty argument: we cannot name the model, so we say nothing.

**The premise is wrong in a way that matters.** I traced it:

- `write_launcher` (`bin/swarm:814-838`): with no `--model`, the launcher execs bare
  `claude --settings … "$PROMPT"` — **no model argument at all**.
- The tab is created (`bin/swarm:906-907`) with `--env SWARM_DIR=…` and `--env SWARM_AGENT_ID=…`
  and **nothing else**. No model, no `ANTHROPIC_MODEL`, no propagation of the parent's pin.

Therefore **"inherited" does not mean "inherits the parent's model."** It means *whatever ambient
default `claude` resolves in herdr's environment*. A child spawned by `updater-v2` (pinned `opus`)
with no `--model` does **not** get opus — it gets the ambient default, same as any other agent.
The word "inherited" in the design is a misnomer that will mislead the next reader of the journal,
and it mislabels a real hazard as a benign one.

**This wounds the rationale but does not kill the decision — it strengthens the decision and changes
what the design must claim.** Rendering `(sonnet)` on an empty field would be a *guess about herdr's
environment*, which is even less defensible than the design thought. The right sentence is not
*"we don't know the inherited model"* but:

> **The empty field means "not pinned." It is a fact about the spawn, not about the model. `ps` can
> honestly report pinned-vs-not; it cannot report which model is running, and must not pretend to.**

### A3. "Misled by silence — the operator scrolls past a pin" — **SURVIVES**

The scenario: operator sees a tree of unmarked lines, assumes uniformity, misses a `[opus]` deep in
a 33-row tree. Real, but it is a **display-length problem, not a marker problem**, and marking the
149 makes it *worse*: a badge on every line is exactly what makes the one different badge hard to
spot. Silence on the common case is what gives the pin its contrast. The current tree is 33 rows —
one screen — and a pin is the only bracket group after `[live]`, so it is the single most salient
token on the line it appears on.

**Verdict on A overall: WOUNDS.** The *decision* (pinned → badge, inherited → nothing) is correct and
survives every attack I could mount. The *stated rationale (b)* is factually wrong about how spawn
works and must be rewritten before it is quoted as precedent. **Required fix: the journal/design
sentence, not the code.**

---

## Attack B — "expanding the dead line breaks R5" — **KILLS the R5 defense**

The design refuses the dead line on R5 grounds:

> *"Attaching per-name payload (`updater-v2(opus)`) to it is exactly the monotonic-growth pressure
> R5 exists to relieve — it makes the one compact line grow in width with history, which is the same
> failure in a different axis."*

I measured that claim against the real 150 records. **It does not survive contact with the data.**

Dead line, all 150 records dead (the worst case R5 is defending against):

| | chars | rows @80 | rows @100 | rows @120 | rows @160 | rows @200 |
|---|---|---|---|---|---|---|
| names only | 1998 | 27 | 21 | 18 | 13 | 11 |
| with `(model)` suffixes | 2004 | **27** | **21** | **18** | **13** | **11** |
| **delta** | **+6 (0.3%)** | **0** | **0** | **0** | **0** | **0** |

**The model suffix costs +6 characters and ZERO wrapped rows at every terminal width I tested.**
It is 0.3% of the dead line. For scale:

- mean agent name = **11.3 chars**; one more dead agent costs **~13.3 chars** on that line.
- **One additional spawn costs 2.2× what the entire model-suffix feature costs — forever, and the
  swarm spawns constantly.** The design is defending a line against a 6-char one-time cost while
  that same line grows by 13 chars every single spawn and R5 accepts that without complaint.

The "same failure in a different axis" framing is where the argument goes wrong. R5's failure mode is
**growth proportional to history**: N dead agents → N names. The model suffix is **not** proportional
to history — it is proportional to *the number of pinned agents*, which is 1 out of 150 and is a rare
deliberate operator act. It is O(pins), not O(history). Calling it "monotonic-growth pressure" is a
category error: it grows with a thing that does not grow.

**Is the fact useful when dead?** Yes, and the design's counter-argument is weak. It says:

> *"a pinned model is a statement about a running agent's cost/capability. For a dead agent it is
> history, and history is one `cat .swarm/agents/<n>.json` away."*

But **post-mortem is the primary use of a pin.** The whole reason you pin a model is that you care
which model did the work; the moment the work is *done* is exactly when "which model produced this
garbage / this gem?" gets asked. And "it's one `cat` away" proves too much — by that argument the
dead line should not exist at all, since the *names* are also one `ls .swarm/agents/` away. R5 kept
the names because a shared line is cheap and the fact is worth a glance. The model suffix is *cheaper
than one more name* and the fact is worth the same glance.

**Verdict: KILLS the refusal's stated justification.** R5 is not threatened — 0 extra rows at every
width, 0.3% width, O(pins) not O(history). If the design still wants to keep the dead line names-only,
it needs a *different* reason than R5, and I do not think one exists. **Recommendation: render the
pin on the dead line too — `dead: a, b, updater-v2(opus), c`.** It costs six characters.

I will steelman the design's last defense: *the dead line is already 1705 chars / 18–22 wrapped rows
in the real tree, so it is already the ugly part of ps and we should not decorate it.* That is a real
observation — **the dead line is 18–22 visual rows vs the living tree's 33, i.e. it already consumes
~40% of the ps screen** and R5's "one line" promise is one *logical* line, not one *visual* one. But
that is an argument for **fixing/pruning the dead line**, not for withholding six characters from it.
It is not an argument the current design makes, and it cuts against R5's own health, not against this
feature.

---

## Attack C — the rest

### C1. `[live] [opus]` — two adjacent bracket groups — **WOUNDS (cosmetic, fixable)**

Proposed: `├─ updater-v2 [live] [opus] q=0 idle 3m`

Every other token on the line is either bracketed-status (`[live]`, `[?]`) or `key=value` (`q=0`) or
prose (`idle 3m`, `(you)`). **`[live] [opus]` puts two visually identical groups side by side that
mean completely different kinds of thing** — one is liveness (a *system* fact, always present), one is
model (an *operator* fact, present 1/150 times). At a glance they read as one two-part status. The
existing line already established a non-bracket convention for "extra fact": `(you)`.

The design's *own journal* writes it as `` (model) `` — *"pinned → ` (model)` suffix on the live
line"* — in the same entry that the parent's brief quotes as `[opus]`. **The design contradicts
itself on the delimiter.** Pick one, and I argue for parens:

```
├─ updater-v2 (opus) [live] q=0 idle 3m      ← paren after name, like (you)
├─ updater-v2 [live] [opus] q=0 idle 3m      ← bracket soup
```

Parens-after-name matches `(you)`, keeps the bracket family meaning "liveness", and puts the model
adjacent to the *thing it is a property of* (the agent) rather than adjacent to the thing it is not
(liveness). **Verdict: WOUNDS.** Trivial to fix; fix it before it ships and before the delimiter
becomes precedent.

### C2. Is `model` a field worth trusting? — **WOUNDS**

`--model` is **completely unvalidated** (`bin/swarm:851-852`): `model, rest = rest[1], rest[2:]` takes
the next argv token verbatim, no regex, no allowlist (contrast `name`, which is regexed against
`NAME_RE`). It is then written verbatim into the record (`:922`) and shell-quoted into the launcher
(`:834`). So `swarm spawn x "t" --model "$(rm -rf ~)"` is *safe* (shlex-quoted, and claude will just
reject it) but the **record now holds an arbitrary string that `ps` will render into the operator's
tree**. It can be 500 chars. It can contain `]`, newlines are impossible via argv but spaces are not.

This is not a security hole — it is a **rendering-robustness hole the new feature opens**. Today the
field is never read by any renderer, so garbage in it is inert. The moment `ps` renders it, a junk
pin becomes a junk *tree*. **The implementation must clamp it** — e.g. render `model[:20]` and strip
whitespace — the same way `last_words` is capped at `LAST_WORDS_CAP` (`:486`). The design says nothing
about this. **Verdict: WOUNDS. Required: cap/sanitize on render.**

### C3. Test fragility — **WOUNDS (pre-existing, now load-bearing)**

`TestPs` (tests/test_swarm.py:326-392) asserts with **exact substrings**: `assertIn("boss [live]")`,
`assertIn("kid (you) [live] q=2")`, `assertIn("lost [parent vanished unknown]")`. Note
`TestPs.AGENTS` fixture records have **no `model` key at all** — so `.get("model")` on them returns
`None`, not `''`. The implementation must use `a.get("model")` truthy-check (both `None` and `''` are
falsy → renders nothing), **not** `"model" in a`. If the implementer writes `if "model" in a:` the
fixture passes and the field breaks; if they write `a["model"]` it **KeyErrors on every existing
test**. That is the single most likely bug in this diff and no existing test guards it.

The tests that would actually catch a regression, and which I will hold the implementer to:
1. a pinned agent renders its model on the live line (positive);
2. an agent with `model: ""` renders **no** model token — assert the *absence* of a delimiter, e.g.
   `assertNotIn("(", line_for_kid)` scoped to that line (negative — this is the one that matters);
3. an agent record with **no `model` key at all** (the current fixture!) renders fine and shows
   nothing — guards the `.get` vs `[]` bug;
4. the dead line: assert exactly what was ruled (whichever way B is resolved);
5. an over-long/garbage model string is clamped (guards C2).

A test suite with only (1) is a happy-path suite and I will call it that. **Verdict: WOUNDS the plan
unless the impl ships the negative tests.**

### C4. Is `ps` the right surface? — **SURVIVES**

I tried to argue for a separate verb (`swarm model`, or `ps --model`). It fails: the pin is a fact
about a *live agent's* cost/capability, `ps` is defined by SELF-AUDIT.md:16 as **"the one view"**, and
a fact that changes how you read the tree belongs *in* the tree. A flag would mean the operator has to
already suspect a pin exists to look for one — which defeats the purpose. `ps` is correct. **SURVIVES.**

### C5. `WORLD.md` untouched — **SURVIVES**

I checked: `WORLD.md` does not mention `--model`. The pin is 1/150 and the contract is read on every
spawn. Adding it taxes every agent to serve a rare operator affordance. The design is right to refuse.
**SURVIVES.**

---

## Summary

| # | Attack | Verdict |
|---|---|---|
| A1 | inherited-marker (`[~]`) is better than silence | **SURVIVES** — no missing-key state exists; badge on 149 lines is pure noise |
| A2 | "we don't know the inherited model" is a rationalization | **WOUNDS** — the premise is *false*; no model is propagated to children at all, so "inherited" is a misnomer. Decision stands; **rationale must be rewritten** |
| A3 | operator misled by silence, scrolls past a pin | **SURVIVES** — silence is what gives the pin contrast |
| B | dead line names-only, on R5 grounds | **KILLS the R5 defense** — +6 chars (0.3%), **0 extra wrapped rows at every width**; one spawn costs 2.2× the whole feature. O(pins), not O(history). **Render the pin on the dead line.** |
| C1 | `[live] [opus]` bracket soup; design self-contradicts on delimiter | **WOUNDS** — use `(opus)` after the name, matching `(you)` |
| C2 | `--model` is unvalidated; ps would render arbitrary strings | **WOUNDS** — must clamp on render, like `LAST_WORDS_CAP` |
| C3 | tests would only assert the happy path; `.get` vs `[]` bug is live | **WOUNDS** — negative + no-key tests are mandatory |
| C4 | `ps` is the wrong surface | **SURVIVES** |
| C5 | `WORLD.md` untouched | **SURVIVES** |

**The core decision — pinned renders, inherited renders nothing — survives everything I threw at it.**
Its *stated reasons* do not: reason (b) is factually wrong, and the R5 defense of the dead line is
refuted by the very data it claims to protect. Two of the design's three answers are right for the
wrong reasons, and one (the dead line) is simply wrong.

**What I would change before this ships:**
1. **Render the pin on the dead line** (`dead: a, updater-v2(opus), b`). R5 is not threatened: 0 rows.
2. **Use `(opus)` after the name**, not `[opus]` after `[live]`. Resolve the design's own contradiction.
3. **Rewrite rationale (b):** the empty field means *not pinned*, not *inherited-and-unknown*. Nothing
   is propagated to children; a pinned agent's child is not pinned.
4. **Clamp the rendered model string** — it is unvalidated argv.
5. **Ship the negative test** (empty `model` → no token) and the **no-key test** (the existing fixture),
   or the diff is a happy-path diff.

**Diff review: not possible.** `swarm-dev/ps-model` == `main`, no commits. I will review it when it exists.

---
---

# Red review, second pass — THE DIFF

**Reviewer:** `ps-model-red`. **Date:** 2026-07-13. **Under attack:**
`swarm-dev/ps-model` @ `d2f8625`, cumulative `main...swarm-dev/ps-model`.
Two commits: `f62a7e0` (original design) + `d2f8625` (the three adopted fixes).
Scope: `bin/swarm` (+27/-2), `tests/test_swarm.py` (+77). Nothing else touched.

**Verdict: SHIP.** No KILLs. Two WOUNDS, both cosmetic-to-moderate, neither
blocking. The clamp holds against every vector I could build; the tests bite on
every mutation I could write. Below is exactly what I tried, so the pass is as
inspectable as a failure would have been.

## 1. Does the clamp hold? — **SURVIVES (26/26 vectors)**

The shipped clamp (`bin/swarm:553-558`):
```python
m = " ".join(str(agents[n].get("model") or "").split())      # collapse ALL whitespace
m = "".join(c for c in m if c.isprintable())[:MODEL_CAP].strip()   # drop control, cap 24
return f" ({m})" if m else ""
```
Three layers, and each earns its place. I ran 26 hostile values through the real
branch renderer (harness: `scratchpad/attack_clamp.py`). **Row count stayed 1 on
every single one. No control character survived into the output on any.**

| vector | result |
|---|---|
| `\n` / `\r` forging a tree row (`opus\n└─ ghost [live] q=0`) | defanged — one row, text inert inside parens |
| U+2028 / U+2029 / U+0085 (the newlines `.split()` catches but `\n`-checks miss) | defanged — `str.split()` splits on all of them |
| vertical tab, form feed | defanged |
| ANSI colour `\x1b[31m…`, cursor-up `\x1b[2A\x1b[K` (scroll damage) | ESC dropped by `isprintable()`; inert literal `[31m` text remains |
| NUL, BEL, zero-width space ×50, RTL-override bidi spoof | stripped by `isprintable()` |
| 500 chars | capped to 24 |
| `├─ fake [live] q=0` (fake branch glyphs) | stays inside parens on its own row |
| non-strings: `int`, `list`, `dict`, `True`, `None` | `str()` coerces; `None`/`""` → renders nothing |
| whitespace-only (`"   "`, `"\t\t"`) | empty after strip → renders nothing (no empty `()`) |

**Why the `.split()` choice is better than it looks:** an author "fixing newlines"
would reach for `.replace("\n", " ")`. That would have **missed U+2028, U+2029 and
U+0085**, all of which some terminals break lines on. `" ".join(s.split())` catches
every Unicode whitespace class at once. This is correct for a reason the comment
doesn't state, and it is the right call.

**Attempts that FAILED to break it, and why:** I could not inject a row (all
line-breaking codepoints die in `.split()`); I could not paint the terminal (all
control chars die in `isprintable()`); I could not blow the line (cap); I could not
produce an empty `()` (`.strip()` then truthy-check); I could not crash it (`str()`
coerces every non-string, `.get(…) or ""` absorbs both `None` and missing-key).

## 2. Do the tests BITE? — **SURVIVES (9/9 mutations)**

I mutated the shipped source nine ways in a scratch clone and re-ran only the three
model tests. **A test that passes on broken code is not a test.** All nine bit with
genuine `failures`/`errors` (harness: `scratchpad/bite.sh`):

| # | mutation | result |
|---|---|---|
| M1 | `model_of` returns `""` always (feature silently off) | **FAILED** (2) |
| M2 | render even when empty (badge on all 149 lines) | **FAILED** (2) |
| M3 | drop the whole clamp (raw verbatim value) | **FAILED** (1) |
| M4 | drop only the `isprintable()` filter (ANSI survives) | **FAILED** (1) |
| M5 | drop only the cap (500-char pin) | **FAILED** (1) |
| M6 | `[opus]` instead of `(opus)` (delimiter regression) | **FAILED** (2) |
| M7 | `agents[n]["model"]` instead of `.get` (the KeyError bug I filed) | **FAILED** (1 error) |
| M8 | render the pin on the **dead line** (breaks R5) | **FAILED** (1) |
| M9 | drop the pin from the **orphan line** | **FAILED** (1) |

Every ruling in this design is now nailed down by a test that fails if the ruling is
reversed — including the two the parent and I *disagreed* about (M8 = R5/dead line,
M6 = delimiter). That is the right way to freeze a contested decision: whoever wants
to reopen it has to delete a named test, in the open. Full suite: **56 tests, OK.**

Test quality note, in the impl's favour: `test_hostile_model_string_cannot_forge_a_row`
asserts `self.assertEqual(len(body), 3)` — **three agents, three rows**. That is a
*structural* property, not a substring, and it is the single assertion that most
directly encodes "the view cannot be corrupted." It also asserts the hostile text is
**defanged, not scrubbed** (`"evil (opus FAKE-LINE: injected) [live] q=0"`), which is
the honest behaviour: the record keeps the truth, the view protects itself.

## 3. Are the 149 unpinned lines byte-identical to `main`? — **SURVIVES**

Checked with `repr()` against `main`'s renderer, not by eye. Six cases — record has
**no `model` key**, `model: ""`, `model: None`, each × `live=set` / `live=None`:

```
no model key at all    live=set    identical=True     model = '' explicit    live=set    identical=True
no model key at all    live=None   identical=True     model = '' explicit    live=None   identical=True
model = None explicit  live=set    identical=True     model = None explicit  live=None   identical=True
```

**Byte-identical on all six.** No trailing space, no double space. The f-string is
built so `model_of()` returns `""` and contributes nothing — `{name}{you}{model_of(name)} [{alive}]`
collapses cleanly. The 149/150 regression risk is closed.

## 4. `(you)` / `(opus)` collision and order — **SURVIVES**

Handled, and tested (`test_you_and_pinned_order`): `kid (you) (opus) [live] q=0`.
Order is `(you)` first. **Defensible, and I'd have chosen the same:** `(you)` is the
more urgent fact (it changes what *you* do next), the pin is a property of the agent.
Both are parens because both are operator-facts about one agent, as against the
`[bracketed]` system-facts about all of them — the comment states this rule explicitly
(`bin/swarm:549-550`), which means the *next* fact has a rule to follow rather than a
precedent to guess at. This is the C1 fix landing properly, not just cosmetically.

## 5. Was the 'inherited' language purged? — **SURVIVES (in the code)**

`grep -in inherit` on the branch: **zero hits in the model code, zero in the tests.**
The two hits in `bin/swarm` (`:359` G17 discipline, `:1042` subprocess env) are
pre-existing and unrelated. The docstring and `model_of` comment now say the true
thing — *"a launcher with no --model execs bare `claude`, and nothing propagates from
the spawner… It is a fact about the spawn, not the model."*

**Minor:** the word survives in the **commit-message body** of `d2f8625` ("an agent
that inherited the spawner's model has an empty 'model' field"), in a paragraph that
is otherwise announcing that this framing was false. Harmless — the shipped artifact
is right — but if the branch is rebased, fix the message.

## 6. Scope creep — **NONE**

`--stat`: `bin/swarm` +27/-2, `tests/test_swarm.py` +77. No other file. `WORLD.md`
untouched (as ruled). No drive-by refactor, no unrelated constant, no reformatting.
`MODEL_CAP = 24` is a new module-level constant sitting with `LAST_WORDS_CAP` — the
right home, and its comment justifies the number (`'claude-opus-4-8' fits`).

## 7. NEW FINDING — semantic forgery inside the line — **WOUNDS**

The clamp stops **structural** injection (a new row). It does **not** stop **semantic**
forgery: a pinned value may contain tokens that mimic *ps's own vocabulary*, inside
the agent's own row. Real output from the shipped code:

```
├─ boss (opus) [live] q=99 idle 0) [live] q=0 idle ?      # --model 'opus) [live] q=99 idle 0s ('
└─ kid [live] q=0 idle ?
```

**`boss`'s true queue depth is 0.** The line displays `q=99`. An operator scanning for
a backed-up queue reads a depth that does not exist. The paren *does* close (`…idle 0)`),
and the real `[live] q=0 idle ?` still follows — so a careful reader sees the doubling —
but at a glance, in a 33-row tree, this is a lie in the one view.

**Severity: low, and I say so plainly.** The threat model is thin: `--model` is typed by
the operator or a parent agent at spawn, not by an outsider — this is not an untrusted
input channel. It is a **foot-gun and a truthfulness bug, not a vulnerability.** But the
design's own standard is *"this swarm judges artifacts, never claims; the renderer must
not manufacture one"* — and here the renderer faithfully prints a manufactured claim.

**Cheapest honest fix (one line, no new concept):** drop `(` `)` `[` `]` in the same
comprehension that already drops non-printables —
```python
m = "".join(c for c in m if c.isprintable() and c not in "()[]")[:MODEL_CAP].strip()
```
A real model id (`opus`, `sonnet`, `claude-opus-4-8`) contains none of these. The one
real id that *does* is `claude-opus-4-8[1m]` — which would render as `claude-opus-4-81m`,
mildly ugly. If that matters, strip only `()` and accept `[]`. Either way the delimiters
of the view stop being forgeable from a record. **Not ship-blocking; file it.**

## 8. NEW FINDING — `MODEL_CAP` counts codepoints, terminals count columns — **WOUNDS**

`[:MODEL_CAP]` bounds **codepoints**, but the tree's real constraint is **display
columns**:

| pin | codepoints | display columns |
|---|---|---|
| `"a"*24` | 24 | **24** |
| `"模"*24` (CJK, East-Asian Wide) | 24 | **48** |
| `"o" + combining accents` | 24 | **1** |

A CJK pin renders **48 columns — 2× the intended bound**. For scale, the longest real
living line in the current tree is 97 columns. The `test_hostile_model_string_cannot_forge_a_row`
assertion `assertLessEqual(len(ln), 80)` measures `len()` — **codepoints** — so it would
**pass** on a 48-column CJK pin that pushes the line well past 80 columns on screen.

**Severity: very low.** No one pins a CJK model id; model ids are ASCII. The tree does
not corrupt — it just gets wider than intended. I raise it because the comment claims
*"cap the length"* and it does not do that for non-ASCII, and because the test that
"guards the width" is guarding the wrong unit. **Not ship-blocking; a comment fix would
honestly close it** (`# cap the codepoints; model ids are ASCII`).

## 9. My dissent on B (the dead line) — **I CONCEDE, partially, and drop it**

The parent rebutted my strongest finding. I said the R5 defense was refuted by
arithmetic (+6 chars, 0 extra rows at every width). The parent granted the arithmetic,
withdrew *"the same failure in a different axis"* as a category error — and then made a
**different** argument I had not attacked:

> *"`dead:` is a list of NAMES — an index into `.swarm/agents/`, deliberately payload-free.
> Give one name a field and the line stops being a name-list and becomes a TABLE with 149
> empty cells, and the NEXT fact (cwd? task? exit code?) has a precedent to point at."*

**This is a better argument than the one I killed, and it beats mine.** My ledger was
*width*; the real ledger is *kind*. A name-list that acquires one optional column is no
longer a name-list, and the cost is not the six characters — it is that the next fact
arrives with a precedent instead of a fight. I measured the wrong thing. I also accept
the parent's answer to my *"the names are one `ls` away too"*: the names **are** the index
you need in order to know what to `cat`, which is precisely why they, and only they,
belong there.

**I do not carry a dissent to the operator on B.** The refusal stands, on the parent's
reasoning, not on the R5 reasoning I refuted — and that distinction is now recorded in
both journals and frozen by mutation M8. My bonus finding (the dead line is never pruned
and already occupies 18–22 visual rows vs the living tree's 33) the parent accepted as a
separate future ruling; I agree it is not this PR's business.

## Second-pass summary

| # | Attack | Verdict |
|---|---|---|
| 1 | defeat the clamp (26 vectors: newlines, U+2028/29/85, ANSI, NUL, bidi, 500-char, fake branches, non-strings) | **SURVIVES** — 1 row every time, no control char out |
| 2 | do the tests bite? (9 mutations incl. R5 and the delimiter) | **SURVIVES** — 9/9 fail on broken code; 56/56 pass clean |
| 3 | unpinned lines byte-identical to `main`? | **SURVIVES** — identical on 6/6 cases by `repr()` |
| 4 | `(you)`/`(opus)` collision + order | **SURVIVES** — tested; order defensible; the paren-vs-bracket *rule* is stated |
| 5 | was 'inherited' purged? | **SURVIVES** in code/tests; survives in one commit-message body (cosmetic) |
| 6 | silent scope creep | **NONE** — 2 files, no drive-bys |
| 7 | **semantic forgery** (`--model 'opus) [live] q=99 idle 0s ('` → a fake `q=99`) | **WOUNDS** — new; one-line fix; not blocking |
| 8 | **`MODEL_CAP` bounds codepoints, not columns** (CJK = 2× the cap) | **WOUNDS** — new; comment/test measure the wrong unit; not blocking |
| 9 | my own finding B (pin on the dead line) | **I CONCEDE** — the parent's name-list-vs-table argument beats my width argument |

**SHIP.** The three adopted fixes landed correctly and are defended by tests that
actually bite. The two new wounds are real but low-severity and can follow. The one
thing I would fix before a human reads the tree is **§7**: a pinned model can print a
`q=` that isn't true, and this project's stated standard is that the renderer never
manufactures a claim.
