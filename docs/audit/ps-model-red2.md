# Red review 2 — the DIFF: `swarm ps` shows a pinned model

> SUPERSEDED by the fix it triggered, live and shipped in current bin/swarm (renaming to a `model=x` namespace, entirely outside `(you)`'s syntax); kept for the record (why the `model=` rendering, not `(model)`, was chosen — its one KILL finding, `--model you` forging the `(you)` self-marker via a namespace collision — reasoning not restated elsewhere).

**Reviewer:** `ps-model-red2` (adversarial). **Date:** 2026-07-13.
**Under attack:** the diff, `main...swarm-dev/ps-model` (3 commits: `1cc2ac1`, `d2f8625`, `f62a7e0`).
The first red (`docs/audit/ps-model-red.md`) reviewed the *design*, before any code existed, and its
5 findings are already adjudicated. This review does not re-litigate them; it attacks the
implementation those findings produced.

**Environment:** clean worktree at `…/scratchpad/wt-psmodel` (`git status`: clean, tip `1cc2ac1`).
`python3 -m pytest tests/test_swarm.py -q` → **58 passed** (confirmed, reproduced).

**Verdict up front (REVISED after a second pass — see §1b/§8): NO-SHIP as-is.** My parent
(`ps-model`) independently found a sharper form of an issue I had first marked cosmetic (§1b) and
asked me to confirm or refute it rather than trust it. I reproduced it, then hunted further per
their brief and found it is **worse than either of us first stated**: the natural fix (strip
structural glyphs from the pin) closes the row-forgery and paren-escape cases but does **not** close
the `(you)`-impersonation case, because the word `you` itself contains no structural character to
strip. §8 has the full account, the fix I now recommend, and why it is sufficient. One KILL. Details
below; §8 supersedes §1b's original verdict.

---

## Attack 1 — defeat the clamp

### 1a. Hostile direction — row injection, escape sequences, exotic Unicode

Tested every payload the brief asked for, against the actual clamp logic
(`bin/swarm:564-568`) run standalone in Python:

```
newline               'evil\nlast: fake row'        -> ' (evil last: fake row)'      — space, not row
CR / CRLF             'evil\r(\n)more'               -> ' (evil more)'                — space
tab                   'evil\ttabbed'                 -> ' (evil tabbed)'              — space
ANSI CSI (color)      '\x1b[31mRED\x1b[0m'           -> ' ([31mRED[0m)'              — ESC dropped, inert
ANSI CSI (cursor up)  '\x1b[2Aoverwrite'              -> ' ([2Aoverwrite)'             — ESC dropped
ANSI OSC (title)      '\x1b]0;pwned\x07'              -> ' (]0;pwned)'                 — ESC+BEL dropped
BEL                   '\x07bell'                      -> ' (bell)'                     — dropped
RTL override U+202E   'opus‮gnitset-live'        -> ' (opusgnitset-live)'         — dropped (category Cf)
combining marks       'óṕúś'×3                        -> unchanged, renders as typed   — inert, no injection
ZWJ / ZWSP             'op‍us' / 'op​us'    -> ' (opus)'                     — dropped (Cf/Cf)
NEL U+0085             'evil\x85more'                  -> ' (evil more)'                — dropped by .split()
LINE SEP U+2028         'evil more'                -> ' (evil more)'                — dropped by .split()
PARA SEP U+2029         'evil more'                -> ' (evil more)'                — dropped by .split()
tree-branch shape       '├─ fake [live] q=0 idle 1m'   -> ' (├─ fake [live] q=0 idle 1m)' — stays INSIDE parens
all-non-printable        '\x00\x01\x02\x03\x1b\x07'    -> ''                            — empty, no marker at all
whitespace-only           '   \t\n  '                   -> ''                            — empty
vertical tab / form feed  'evil\x0bmore' / 'evil\x0cmore' -> ' (evil more)'              — dropped by .split()
backspace                 'opus\x08\x08\x08REAL'        -> ' (opusREAL)'                 — dropped (Cc), not undone
```

**`str.isprintable()` correctly classifies Unicode category `Cf` (format chars) as non-printable** —
verified directly:

```
>>> unicodedata.category('‮')   # RTL override
'Cf'
>>> '‮'.isprintable()
False
```

So RLO/LRO/LRM/RLM/LRI/PDI/BOM (all `Cf`) are stripped. This is the one place the brief explicitly
said "check, do not assume" — checked, confirmed correct.

**No payload produces a second tree row, an escape sequence in the output, or paints the terminal.**
`\x1b` and `\x07` never survive `isprintable()` filtering (`Cc`, control category). The `TURN_CAP`-style
mutation test in Attack 2 (`test_hostile_model_string_cannot_forge_a_row`) independently confirms this
against the *real* `render_ps` call path, not just the standalone clamp.

**Verdict: SURVIVES.**

### 1b. A real semantic break the brief didn't name: parens are not escaped

The clamp collapses newlines to spaces and drops control chars, but it does **not** escape or reject
a literal `)` in the model string. A pinned agent can carry a model value containing `)`  ` [live]`
`q=0` etc. — all ordinary printable ASCII, nothing the clamp strips:

```python
model_of_value('opus) [live] q=0 idle 1m\nfake ├─ evil (opus')
# -> ' (opus) [live] q=0 idle 1m fake ├…)'
```

Rendered inline: `victim (opus) [live] q=0 idle 1m fake ├…) [live] q=0 idle 3m` — the closing paren
lands early and the rest of the field reads as free text that *resembles* trailing status tokens,
still on the **same line**, still **not a new row** (no row injection — the newline was already
collapsed to a space by `.split()`), but visually it can make one agent's line look like it's
reporting a second `[live] q=0` block. This is a cosmetic/confusability issue, not a row-forgery or
terminal-corruption issue — row count and escape-sequence integrity are what Attack 1a and the test
suite guard, and both hold.

**Original verdict here was WOUNDS. SUPERSEDED — see §8. This is a KILL.** My parent rendered the
hostile case directly (rather than trusting the green suite) and found the same paren-escape I'd
found, but pushed it one step further than I had: escaping the paren doesn't just make one line read
confusingly — it lets an attacker **forge the `(you)` marker onto an agent that is not the reader**,
which breaks the one property `ps` cannot afford to lose. §8 has the full account.

### 1c. Honest direction — do real model ids survive whole?

Checked every id Anthropic currently ships, plus one Bedrock-prefixed form, against `MODEL_CAP=32`:

```
claude-opus-4-8                        15 chars  -> WHOLE
claude-sonnet-5                        15 chars  -> WHOLE
claude-haiku-4-5-20251001              25 chars  -> WHOLE   (the longest id actually in .swarm/agents/)
claude-3-5-sonnet-20241022             26 chars  -> WHOLE
claude-3-opus-20240229                 22 chars  -> WHOLE
us.anthropic.claude-sonnet-5-v1:0      33 chars  -> CUT, visibly ('…'), not mangled
```

Also ran the real `.swarm/agents/*.json` corpus (164 records, 6 pins) through **both** `main`'s and
the branch's `render_ps` side by side (see Attack 3) — `wmd-haiku` and `wmd-haiku2`, both pinned to
the literal 25-char `claude-haiku-4-5-20251001`, render **whole**, byte-for-byte, on the branch.

This is exactly the class of bug the first red's own Attack C2 asked for and the *original* diff draft
got wrong per the task brief (cap 24 truncated the last char of a 25-char real id into a
plausible-but-wrong 24-char string). Confirmed via mutation: reverting `MODEL_CAP` from 32 to 24
reproduces the mangling and the regression test (`test_real_long_model_id_survives_whole`) catches it
immediately (Attack 2, mutation 5).

**Verdict: SURVIVES.** No legitimate id (any currently-shipping Anthropic model id, or any real id
in the current `.swarm/agents/` corpus) renders altered. The only value that gets cut is a
34-byte-longer, non-standard Bedrock ARN-style string, and it is cut with a visible `…`, never
silently.

---

## Attack 2 — do the tests bite?

Six new/changed tests. Each mutated at the specific line it claims to guard, re-run in isolation,
confirmed to fail on the mutant and pass on the original.

| # | Test | Mutation | Result |
|---|------|----------|--------|
| 1 | `test_pinned_model_shows_unpinned_shows_nothing` | `return f" ({m})" if m else ""` → always render `(default)` when empty | **FAILS** (2 assertions break: `kid (you) [live] q=2` not found; `boss [live] q=0` polluted) |
| 2 | (same test, R5 clause) | `dead:` line mutated to include `model_of(n)` per name | **FAILS**: `assertNotIn("haiku", out)` catches it — `dead: gone (haiku)` appears |
| 3 | `test_you_and_pinned_order` | swap emission order to `{model_of}{you}` | **FAILS**: expects `kid (you) (opus)`, gets `kid (opus) (you)` |
| 4 | `test_missing_model_key_renders_unpinned` | same "always show parens" mutation as #1 | **FAILS**: `assertNotIn("()", ...)`-adjacent assertion breaks (`boss [live] q=0` not found, `(default)` appears instead) |
| 5 | `test_hostile_model_string_cannot_forge_a_row` | remove the whitespace-collapse + printable-filter (`m = str(agents[n].get("model") or "")`, unclamped) | **FAILS hard**: `assertEqual(len(body), 3)` → `5 != 3` — the newline genuinely forges two extra rows once the collapse is removed, proving the test exercises real row-forgery, not a strawman |
| 6 | `test_real_long_model_id_survives_whole` | `MODEL_CAP` 32 → 24 (the original bug class) | **FAILS**: `'wmd-haiku (claude-haiku-4-5-20251001)...'` not found; actual output has `claude-haiku-4-5-202510…` — reproduces the exact silent-mangling bug the test exists to prevent |
| 6b | `test_over_cap_model_is_visibly_truncated` | off-by-one: `m[:MODEL_CAP]` instead of `m[:MODEL_CAP-1]` before appending `…` | **FAILS**: `assertEqual(len(field), sw.MODEL_CAP)` → `33 != 32` — cut lands one char past the cap |

All 6 tests bite. None is a test that merely restates the implementation — each one fails when the
specific behavior it names is broken, and passes only when that behavior holds.

**Verdict: SURVIVES.**

---

## Attack 3 — byte-identity of the 156(→159 in current data) unpinned lines

Reproduced the parent's claim independently, loading `main`'s (`aa6063d`) and the branch's
(`swarm-dev/ps-model`) `bin/swarm` as two Python modules and calling `render_ps` on the **same**
current `.swarm/agents/*.json` corpus (164 records now, not 162 — the tree grew since the parent's
run):

```
agents: 164   pins: 6
main lines: 165   branch lines: 165
diff count: 6
  line 66:  mr-blast    '...mr-blast [live]...'         vs '...mr-blast (opus) [live]...'
  line 67:  mr-reader   same shape
  line 68:  mr-theater  same shape
  line 159: updater-v2  same shape
  line 161: wmd-haiku   '...wmd-haiku [live]...'         vs '...wmd-haiku (claude-haiku-4-5-20251001) [live]...'
  line 162: wmd-haiku2  same shape
dead-line identical: True (byte-for-byte)
main sha256:   ae8fb2608c749e24...
branch sha256: 94b275fb876e5a64... (differs only by the 6 inserted " (model)" substrings)
```

**Exactly 6 lines differ, exactly matching the 6 currently-pinned agents** (`mr-blast`, `mr-reader`,
`mr-theater`, `updater-v2`, `wmd-haiku`, `wmd-haiku2`). The `dead:` line is verified identical between
`main` and the branch. No trailing space, no double space, no other divergence found in any of the
159 unpinned lines — each is character-for-character identical to `main`'s output.

I could not find a currently-dead pinned agent in the live corpus to exercise the R5 leak path on
real data (all 6 real pins are currently live/orphaned, not dead) — that path is covered instead by
the synthetic test (`gone`/`"model": "haiku"`) and by mutation-testing it directly (Attack 2, #2),
which is sufficient: the guard is proven at the code level even though the current field happens not
to have a live example.

**Verdict: SURVIVES** (claim reproduced and strengthened — 164 records now, not 162, same
6-diff / rest-identical shape holds).

---

## Attack 4 — the `…` itself

`…` is U+2026, `East_Asian_Width=Ambiguous`. In Python, `len('…') == 1` (one codepoint); UTF-8 encodes
it as 3 bytes. `MODEL_CAP` is applied via `len(m) > MODEL_CAP` and `m[:MODEL_CAP-1]` — **codepoints,
not bytes, not terminal columns.** For plain ASCII/Latin model ids (everything Anthropic ships today,
and everything in the real corpus) codepoints == terminal columns == bytes, so this distinction is
inert for the honest case.

It is **not** inert for the hostile/exotic case. `--model` is unvalidated free text, so nothing stops
a spawn like `--model "模模模模...模"` (CJK, all printable, passes the clamp untouched). Measured:

```
32 CJK 模 chars → clamp passes all 32 through unchanged (len==32, not >32, no cut)
estimated terminal columns for the full " (...)" field: 66   (each CJK char = 2 columns, East_Asian_Width=W)
```

**This is a real finding.** `MODEL_CAP=32` is a *character* cap, and the design's own stated purpose
for the cap (bounding a line's width in a fixed-width terminal — see the first red's Attack B, which
measured `ps` line-width budgets in exact characters) is silently defeated by any wide-glyph input:
32 wide characters is not "32 chars of headroom," it's 64 terminal columns, double the budget the cap
was sized against. The astral-plane case (`𝕏`, outside the BMP) does **not** have this problem in
Python 3 — `len()` counts codepoints correctly there (no surrogate-pair miscount) — so the risk is
specifically East-Asian-wide and other double-width glyphs, not astral-plane width.

The line-length test itself has the same blind spot: `test_hostile_model_string_cannot_forge_a_row`
asserts `self.assertLessEqual(len(ln), 80)` — Python char-count, which would pass even on a
double-width-inflated line that renders at 160 terminal columns.

**Verdict: WOUNDS.** Not a KILL — nothing here forges a row, corrupts state, or lies about a real
Anthropic model id (all real ids are ASCII). But the cap's *stated purpose* (bound the rendered width)
is not actually guaranteed for arbitrary `--model` input, and the existing test would not catch a
regression here because it measures the same wrong unit. **Recommended follow-up (not a blocker):**
either cap on `unicodedata.east_asian_width`-weighted columns, or accept this as an explicitly-scoped
gap (ps is an operator tool, `--model` is operator-typed, not adversary-controlled in the threat model)
and say so in the `MODEL_CAP` comment rather than leaving the width claim implicit.

---

## Attack 5 — did 'inherited' actually get purged?

```
grep -n "inherited" bin/swarm tests/test_swarm.py
  bin/swarm:362:    The G17 discipline, inherited: side effects are conditional on the bytes
```

That is the **only** hit in the touched files, and it is unrelated pre-existing text (a comment about
message-delivery discipline, "G17", nothing to do with model inheritance — confirmed by reading
context around line 362, outside the diff entirely). Grepping the **diff itself**
(`git log aa6063d..HEAD --format="%H %s%n%b"`) for "inherited" surfaces only the commit message and
docstring/comment text that correctly uses the word to **describe and refute** the false claim (
`'INHERITED' WAS FALSE`, `does not mean 'inherited the spawner's model'`), which is the point being
made, not a leftover of the old (wrong) framing.

Checked the new docstring (`render_ps:508-514`) and the `model_of` comment (`:550-563`): both
consistently say "PINNED" / "NOT pinned" and explicitly state the record "says nothing about which
model is actually running" — no residual claim that empty means "inherited."

**Verdict: SURVIVES.** The false word is gone from code, comments, and test names in the touched
files; its only remaining appearances are either unrelated or are the corrective explanation itself.

---

## Attack 6 — the R5 guard: does a dead pinned agent leak anything?

Diff review: the only change to the dead-line emission is... none. `git diff` shows zero lines
touched in the `if dead:` block (`lines.append(f"dead: {', '.join(dead)}")` is unchanged — `dead` is
still a bare list of names, never passed through `model_of`).

Confirmed by:
- **Test**: `test_pinned_model_shows_unpinned_shows_nothing` includes `"gone"` pinned to `"haiku"` and
  dead, asserts `self.assertIn("dead: gone", out)` and `self.assertNotIn("haiku", out)` — both pass
  on the real code.
- **Mutation**: patching the dead-line to route through `model_of(n)` makes exactly this test fail
  (`dead: gone (haiku)` appears, `assertNotIn("haiku", out)` catches it) — proving the test is not
  vacuously passing.
- **Real-data byte-identity** (Attack 3): the `dead:` line is byte-identical between `main` and the
  branch on the actual 164-record corpus.

**Verdict: SURVIVES.** The dead line is provably untouched — by diff inspection, by a test that would
catch a regression, and by a mutation that confirms the test bites.

---

## Attack 7 — anything changed that nobody asked for

Diff is exactly: `MODEL_CAP` constant + comment (1cc2ac1 → 32, sized off measured real data),
`model_of()` helper, its call-sites on the live/you line and the orphan (`?─`) line, and the
docstring update correcting "inherited." No other function touched, no signature changed, no
unrelated formatting churn. `git diff --stat`: `bin/swarm | 37 ++-`, `tests/test_swarm.py | 108 ++`,
2 files. Scope matches the brief exactly.

**Verdict: SURVIVES.**

---

## Attack 8 — the `(you)` forgery (raised by ps-model, confirmed and extended)

My parent rendered the hostile case directly instead of trusting the green suite and reported a
sharper form of what I'd filed as §1b. Brief: **confirm or refute, then hunt for more, then judge a
fix without repeating round 1's mistake** (a fix that mangles an honest id is the same bug a third
time). All three, in order.

### 8a. Confirm or refute — is it real?

**Confirmed, reproduced independently.** The exact repro from the brief:

```python
agents = {'glyph': {'name': 'glyph', 'parent': 'operator', 'pane': 'p1',
                     'model': 'x) [live] q=0 idle 1m\n├─ fake'}}
render_ps(agents, {'p1'}, {'glyph': 0}, {'glyph': None}, 'operator', [], 0)
```
```
operator — no waiting mail
└─ glyph (x) [live] q=0 idle 1m ├─ fake) [live] q=0 idle ?
```

One row (no structural forgery — `len(body)==1`, matching Attack 2's mutation test), but the
**text** reads as two agent lines to a human scanning `ps`. My parent's framing is exactly right:
structure sound, view deceptive, and "ps is THE ONE VIEW" is the reason that distinction doesn't
save it — a view whose job is to be read is not fixed by a data structure that parses correctly.

**Who can set a pin?** `--model` at spawn, no validation (`bin/swarm:851-852`, confirmed unchanged
by this diff). Spawning is available to any agent in the tree, not just the operator. So the
steelman *"a human who sees a weird paren goes and `cat`s the record"* fails on its own terms: the
threat isn't an external adversary, it's **any sibling agent**, and the whole point of `ps` being
"the one view" is that agents and the operator are supposed to be able to trust it *without* going
to cat every record — that's the workflow the feature exists to save them from. If the view can be
made to lie, the feature's entire value proposition (trust `ps`, skip the `cat`) is what breaks.

### 8b. Hunt for more — systematic, per the brief's checklist

Ran every structural token named in the brief against the actual `render_ps` (not the standalone
clamp) via the worktree's `bin/swarm`, loaded as a module:

| Forgery attempted | Payload | Result |
|---|---|---|
| Fake child row (tree glyph) | `x) [live] q=0 idle 1m\n├─ fake` | `glyph (x) [live] q=0 idle 1m ├─ fake) [live] q=0 idle ?` — reads as 2 lines |
| Fake `dead:` summary | `x) [live] q=0 idle 1m\ndead: boss, everyone` | `victim (x) [live] q=0 idle 1m dead: bos…) ...` — cut by cap before it gets far, but the leading fragment is convincing |
| Fake operator-mail banner | `x) [live] q=0 idle 1m\noperator — 99 message(s) waiting` | same shape, cut by cap |
| Impersonate a *specific* trusted name inline | `opus) [live] q=0 idle 1s\n├─ boss (you` (reader is literally named `boss`) | `attacker (opus) [live] q=0 idle 1s ├─ bos…) [live] q=0 idle ?` — cut before `(you` lands, by luck of length, not by design |
| **Forge `(you)` on another agent — my parent's favorite, tried specifically** | `x) (you` (7 chars, reader is `someone-else`, agent is `victim`) | **`victim (x) (you) [live] q=0 idle ?`** — clean, complete, well under `MODEL_CAP=32`, **zero truncation marker** |
| Two simultaneous `(you)` claims in one tree | real reader `me` (unpinned) + `victim` pinned to `x) (you` | `├─ me (you) [live] q=0 idle ?` / `└─ victim (x) (you) [live] q=0 idle ?` — **both lines carry `(you)`, structurally identical** |
| Adversarial **name** (not model) forging anything | `NAME_RE = r"^[a-z0-9][a-z0-9-]{0,39}\Z"` | confirmed the regex rejects `(`, `)`, brackets, tree glyphs outright — names are not a vector, only `model` is |

**This confirms the exact attack my parent called their favorite: an agent can forge `(you)` onto
itself, and it renders as a complete, unmarked, un-truncated token — not a visibly-cut fragment.**
That distinguishes it from the row-forgery cases above (which the cap tends to interrupt/mark) — the
minimal payload is 7 characters, nowhere near `MODEL_CAP`, so there is no truncation ellipsis to tip
off a careful reader. **This is the worst instance in the set**, worse than the row-text confusion:
it isn't "a line that reads oddly," it's "a specific, load-bearing two-character marker (`you`) that
the rest of the system (and any agent scanning `ps` for 'is this me') treats as authoritative,
forged with total fidelity."

**One more property, not in the brief's checklist, worth naming explicitly:** `{you}` is computed
**per-reader** (`name == me_name`, evaluated fresh each time someone runs `ps`), but `model_of(name)`
is baked into the **record** and is the same for every reader. A pin of `--model you` (or anything
that reduces to the bare word `you`) therefore does not just fool one victim once — **it makes that
one agent's line read `(you)` to every agent that ever runs `ps` against that record**, each of whom
would read it, at a glance, as "that's my own line." This is strictly worse than a targeted spoof: it's
a standing, reader-independent claim.

### 8c. Judge the fix — mine and my parent's candidate, checked against round 1's lesson

My parent's candidate: **drop/replace `(` `)` and the tree glyphs (`├└│─`) inside `model_of`, the
same way newlines are already dropped** — reasoning: a model id is an identifier, and no legitimate
id contains punctuation used as line-structure syntax.

**Verified against real ids before endorsing it** (round 1's lesson: check the honest case, don't
just assume):

```python
FORBIDDEN = set('()├└│─?[]')     # add '?', '[', ']' too — see below
real_ids = ['claude-opus-4-8', 'claude-sonnet-5', 'claude-haiku-4-5-20251001',
            'claude-3-5-sonnet-20241022', 'claude-3-opus-20240229',
            'us.anthropic.claude-sonnet-5-v1:0', 'opus', 'sonnet', 'haiku']
# every one: forbidden chars present = None
```

And against the live corpus:
```
grep model .swarm/agents/*.json  → 'opus' ×4, 'claude-haiku-4-5-20251001' ×2
# none contain () [] ? ├ └ │ ─
```

**No real id anywhere — Anthropic's shipping ids, the swarm's own bare-word aliases, or anything
currently in `.swarm/agents/`  — uses any of these characters.** I extended the forbidden set beyond
what my parent proposed to also include `[`, `]`, and `?`, because the orphan line's own delimiter
is `[parent … unknown]` and `[?]`/`[live]` are exactly the bracket-status vocabulary a forged pin
could otherwise echo — same reasoning as the tree glyphs, same verification (no real id uses them
either).

**Re-ran every forgery in §8a/§8b against the candidate fix:**

```
you-forgery-minimal      'x) (you'                                  -> ' (x you)'
you-forgery-clean-close  'opus) (you) [live] q=0 idle 1m\n├─ ghost'  -> ' (opus you live q=0 idle 1m  ghost)'
fake-row-glyph           'x) [live] q=0 idle 1m\n├─ fake'            -> ' (x live q=0 idle 1m  fake)'
dead-line-forge          '...\ndead: boss, everyone'                 -> ' (x live q=0 idle 1m dead: boss, …)'
mail-prefix-forge        '...\noperator — 99 message(s) waiting'     -> ' (x live q=0 idle 1m operator — 9…)'
impersonate-name-inline  'opus) [...]\n├─ boss (you'                 -> ' (opus live q=0 idle 1s  boss you)'
```

Every forgery now renders as **one obviously-garbled clause inside a single, un-escapable `(...)`**
— `(x you)` is legible as junk, not as a second field. All 8 honest ids from Attack 1c render
**unchanged**, character for character (re-verified: `claude-opus-4-8`, `claude-haiku-4-5-20251001`,
`us.anthropic.claude-sonnet-5-v1:0` cut with `…` exactly as before — the forbidden-char strip doesn't
touch the cap logic at all, it only shrinks the *input* to the cap).

**But the fix is not sufficient by itself — I found the gap my parent's checklist didn't quite name.**
Because `{you}` and `model_of(name)` are independent string fragments concatenated in sequence
(`{name}{you}{model_of(name)}`, `bin/swarm:577`), and the word **`you` itself contains no forbidden
character**, a pin of exactly `--model you` still produces:

```
victim (you) [live] q=0 idle ?
```

which is **character-for-character identical** to what `me{you}` produces for the real reader:

```
me (you) [live] q=0 idle ?
```

No amount of stripping structural glyphs closes this, because the forgery here isn't a structural
escape — it's a **content collision** with a reserved word. Glyph-stripping is necessary (it closes
the row-forgery, dead-line-forgery, and mail-forgery cases, and the multi-clause `(you)` cases with
trailing garbage) but **not sufficient** for the clean single-word case.

**Required, on top of the glyph-strip:** `model_of` must refuse to render the bare reserved word
`you` (case-insensitively, since a human scanning fast won't distinguish `(You)` from `(you)`) as a
pinned model — either suppress it as if unpinned, or render it distinguishably (e.g. keep the raw
word but do not let it stand alone: `(model: you)` would still collide less, but the simplest correct
fix is a reserved-word check: if the clamped value, case-folded, equals `"you"`, treat it as if the
field were empty. No real model id is or will plausibly be the bare word "you" — this is a zero-cost
carve-out, verified against every id in the honest-case list above.

**Verdict: KILL**, superseding §1b's original WOUNDS. The glyph-stripping half of the fix is
necessary and sufficient for every attack except the reserved-word collision; the reserved-word
check is required in addition.

### 8d. A stronger fix, found in-flight — `model=x` instead of `(model)`

While writing up the glyph-strip + reserved-word fix above, I checked the worktree again and found
`ps-model` had, in parallel, arrived at a **better fix independently**: an uncommitted change to
`bin/swarm` (not yet in any of the 3 reviewed commits) that abandons the `(model)` syntax entirely
and renders `model=opus` — the same `key=value` shape as `q=0` — instead of a parenthesized clause
beside `(you)`.

This is strictly stronger than my glyph-strip + reserved-word proposal, because it removes the
*namespace collision* instead of patching around it: `(you)` and `(model)` no longer share a
delimiter, so there is no string a pin can contain that produces literal `(you)`, full stop — no
reserved-word carve-out needed. I re-ran the entire forgery set from §8a/§8b against this WIP code
directly (loaded the worktree's `bin/swarm`, not a hand-patched copy):

```
you-forgery-minimal ('x) (you')      -> victim model=xyou [live] q=0 idle ?
bare 'you' pin                        -> victim model=you [live] q=0 idle ?
two simultaneous you claims           -> me (you) [live] ...  /  victim model=you [live] ...
fake-row-glyph                        -> glyph model=x[live]q=0idle1mfake [live] q=0 idle ?
dead-line-forge                       -> victim model=x[live]q=0idle1mdead:boss,everyone [live] q=0 idle ?
honest real id (claude-haiku-4-5-...) -> wmd model=claude-haiku-4-5-20251001 [live] q=0 idle ?
honest bare alias ('opus')            -> boss model=opus [live] q=0 idle ?
```

**Every forgery collapses to inert text with no possible collision with `(you)`** — the marker
literally cannot appear unless `name == me_name` produced it, because no pin-derived text ever
contains a `(` immediately followed by `you)`. Honest ids (including the two edge cases from Attack
1c) render whole and correctly. `MODEL_STRUCTURAL` in the WIP (`bin/swarm:46`,
`set("()") | set("─│├└┌┐┘┬┴┼")`) additionally strips box-drawing corner/junction glyphs I hadn't
listed (`┌┐┘┬┴┼`) — broader than my proposed set, still verified empty-intersection with every real
id. It also strips **all** whitespace rather than collapsing runs to a single space (`not c.isspace()`
vs. my `.split()`-then-rejoin) — tighter, and still leaves every honest id (none of which contain
internal whitespace) untouched.

**This WIP is not yet committed and its own test suite is not yet updated to match** — running the
existing 58 tests against it: 2 fail (`test_hostile_model_string_cannot_forge_a_row`,
`test_over_cap_model_is_visibly_truncated`), both because they assert the literal old `"…) [live]"` /
`(...)` string shape, not because the new rendering is wrong — the WIP's own docstring
(`bin/swarm:522-525`) already states the `model=` rationale explicitly and matches what I verified.
I judge the **approach** correct and stronger than what I would have recommended; the remaining work
is mechanical (finish updating the two stale test assertions to the new `model=` shape, then apply
the same mutation-testing discipline as Attack 2 to confirm they bite).

---

## Summary

| Attack | Verdict |
|---|---|
| 1a. Clamp vs hostile input (rows, ANSI, exotic Unicode) | **SURVIVES** |
| 1b. Parens not escaped inside the pin | **SUPERSEDED by §8 — KILL** |
| 1c. Clamp vs honest real model ids | **SURVIVES** (fix for the cap=24 bug confirmed) |
| 2. Do the 6 tests bite on mutation | **SURVIVES** (all 6, including the off-by-one sub-case) |
| 3. Byte-identity of unpinned lines | **SURVIVES** (reproduced on live 164-record corpus, exactly 6 diffs) |
| 4. `…` char-vs-column width, MODEL_CAP unit | **WOUNDS** (real gap: wide-glyph input defeats the cap's stated width purpose; no honest-case breakage) |
| 5. 'inherited' purged | **SURVIVES** |
| 6. R5 guard on the dead line | **SURVIVES** |
| 7. Scope creep | **SURVIVES** |
| 8. `(you)` forgery via unescaped parens + reserved-word collision | **KILL** — fix judged, verified against every honest id, not yet applied |

**One KILL.** An agent that can spawn (any agent in this swarm) can pin `--model` to a value that
makes its own `ps` line render `(you)` — the marker meant to tell a reader "this is your own line" —
to every future reader, indistinguishably from a real one, with no truncation or other tell. This is
not cosmetic: `ps` is "the one view," and a forgeable identity marker inside it defeats the reason
the view is trusted. A secondary, lower-severity WOUNDS (§4, wide-glyph width) remains, not blocking.

## Recommendation: **NO-SHIP on `1cc2ac1` as committed.** The in-flight WIP fix (§8d, not yet
committed) is the right approach and should ship instead of my glyph-strip proposal.

Required before ship (§8d's fix, already in progress in the worktree):
1. Land the `model=x` rendering (namespace change away from `(model)`) — verified in §8d to close
   every forgery in this review, including the reserved-word collision my own proposal needed a
   special case for.
2. Finish updating `test_hostile_model_string_cannot_forge_a_row` and
   `test_over_cap_model_is_visibly_truncated` to assert the new `model=` shape (currently the only 2
   of 58 tests failing against the WIP, both stale-assertion, not logic failures).
3. Add a regression test asserting no pin, of any content, can make `model_of` emit the literal
   substring `(you)` for an agent where `name != me_name` — apply the mutation-testing discipline
   from Attack 2 to it (mutate the fix, confirm the test fails) before trusting it.

Not blocking, optional follow-up:
4. Cap on display-width (`unicodedata.east_asian_width`) rather than codepoint count (§4), or
   explicitly scope-note in the `MODEL_CAP` comment that the cap assumes narrow glyphs.

None of this is a regression from `main` — `main` had no model-rendering at all — but "no worse than
main" is not the bar; "doesn't let one agent impersonate another in the one shared view" is, and the
diff as it stands on `1cc2ac1` does not clear it. The fix is close: §8d's approach is verified
correct, and what's left is finishing the two stale tests and adding the identity-forgery regression
test.
