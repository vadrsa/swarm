# HERDR — what it is, how hard swarm depends on it, and whether that's fatal, fixable, or an asset

**Author:** `vent-herdr`, investigation scout for the venture arm. Local investigation
(machine inspection, source grep, live tests) plus a small web/GitHub check for
publication status. All claims below are tagged with the command or file:line that
backs them.

---

## 1. What herdr is

**Not a local prototype — a real, popular, independent open-source project.**

- **Binary:** `/opt/homebrew/bin/herdr` → `/opt/homebrew/Cellar/herdr/0.7.3/bin/herdr`,
  a Mach-O arm64 executable (`file` output). Installed via Homebrew core, not built
  from a local checkout — there is **no** `~/git/herdr` or any herdr source tree
  anywhere on this machine (`find / -iname "*herdr*"` turned up only the Cellar
  install, config/socket files under `~/.config/herdr`, and the swarm-authored skill
  doc at `~/.claude/skills/herdr/SKILL.md`).
- **Language / size:** Rust, ~30,271 KB repo size, described by its own README as
  "a single Rust binary (~10MB)" (GitHub API + web search corroborate).
- **What it does:** a terminal workspace manager / agent multiplexer — "tmux rebuilt
  from scratch with first-class awareness of AI coding agents." Manages
  workspaces/tabs/panes, detects which coding agent (Claude, Codex, opencode, etc.)
  is running in a pane and its state, persists sessions via a background server, and
  exposes a **local Unix-socket API** so external processes can create tabs, split
  panes, read pane output, and send text/keys — this socket API is exactly what
  `bin/swarm` uses (`herdr pane list`, `herdr tab create`, `herdr pane read`, etc.).
- **Docs/license/publication:** full docs at herdr.dev/docs, source at
  `github.com/ogulcancelik/herdr`, license **AGPL-3.0-or-later** (per `brew info
  herdr`; GitHub's own license field reads "Other/NOASSERTION," i.e. the repo ships
  a non-standard/custom license text — worth a legal look before shipping it
  bundled, not a blocker for the current usage as an external dependency). Published
  on **Homebrew core** (`brew info herdr` → installed from `homebrew-core/Formula/h/herdr.rb`),
  on **GitHub**, and covered by multiple independent tech blogs this month (Tecmint,
  fossengineer, coddykit, pyshine, knightli — all July 2026).
- **Popularity / activity (GitHub API, `gh api repos/ogulcancelik/herdr`):**
  **16,274 stars, 1,105 forks, 72 open issues**, `pushed_at: 2026-07-14T01:18:18Z` —
  **pushed to earlier today**. This is an actively maintained, widely adopted
  project, not an abandoned or private tool.
- **Local install currency:** `brew info herdr` shows 0.7.3 installed, "Analytics:
  install: 10,276 (30 days), 12,802 (90 days)" — i.e. ~10K fresh installs/month via
  brew alone.

**Bottom line on part 1:** herdr is a third party's thriving open-source product
that swarm happens to run inside of. Swarm does not own it, does not vendor it, and
has zero source-level coupling to its internals — only to its CLI/socket contract.

---

## 2. Every touchpoint in swarm's code, and what breaks without it

`grep -c -i herdr bin/swarm` → **41 matches** in a 1,753-line file — all confined to
one clearly labeled section plus `cmd_spawn`/`cmd_close`. Full call sites:

| Function | bin/swarm line(s) | Calls herdr | Failure mode if herdr is gone/unreachable |
|---|---|---|---|
| `herdr_json` | 856-862 | `herdr pane list` / `herdr tab create` (generic JSON wrapper) | `subprocess.run` raises (binary not found) or times out → caught by bare `except Exception` → returns `None`. **Never crashes the caller.** |
| `live_pane_set` | 865-870 | via `herdr_json(["pane","list"])` | Returns `None` ("liveness unknown, never asserted" — comment at :868), not an exception. |
| `pane_prompt_line` / `pane_text` | 873-895 | `herdr pane read` | Wrapped in `try/except` → returns `""` on failure. |
| `read_blocked` | 914-937 | via `pane_text` | Guarded upstream: `cmd_ps` only calls it `if live is not None` (line 1599) — with herdr gone, this is **skipped entirely**, not run-and-failed. |
| `ring_doorbell` / `ring_doorbell_once` | 940-990 | `herdr pane send-text` / `send-keys` | Return `False`/best-effort `True`; `cmd_send` already treats the doorbell as optional (see below). |
| `cmd_spawn` | 1315-1316, 1417-1432 | **hard gate**: `if os.environ.get("HERDR_ENV") != "1": die(...)`, then `herdr tab create` and `herdr pane run` | **This is the one real hard dependency.** Spawning a new agent requires being inside a herdr pane and requires `herdr tab create` to succeed (`die("herdr tab create failed")` at :1430 if the JSON response has no pane id). |
| `cmd_close` | 1642-1662 | `herdr tab close` / `herdr pane close` | Falls back pane→tab, and either way just prints `"{name}: pane already gone"` on failure (:1661) — **never dies**. Files (journal/queue/delivered) are explicitly said to "stay" regardless (:1662). |

### Live test: what actually happens without herdr

Ran directly against this repo (not simulated):

```
$ env -u HERDR_ENV /Users/vadrsa/.local/bin/swarm spawn testxyz "test task" --model sonnet --reason "test"
swarm: not inside herdr (HERDR_ENV != 1); spawn needs herdr as the container
exit code: 1
```
→ **Spawn is the one command that refuses outright.** Confirmed at the exact guard
named above.

```
$ env PATH="/usr/bin:/bin" /Users/vadrsa/.local/bin/swarm ps
```
→ **Exit code 0.** Full tree still rendered (names, parents, queue depths `q=N`,
idle times), every liveness column shows `[?]` instead of `[live]`/`[dead]`, and the
output ends with the literal line `(herdr unreachable — liveness unknown)` — this
is a designed degraded mode, not a crash (`cmd_ps`, bin/swarm:1602-1603, and the
comment at :1596-1598 spells out the intent: *"herdr unreachable (live is None)
means nothing to read; an empty dict is correct, not a degraded one"*).

`cmd_send`'s core path (bin/swarm:1476-1551) — name validation, size limits, the
optional admission middleware, and `queue_put` — **touches herdr nowhere**. The
message is durably written to the filesystem queue regardless. The only herdr
touch is the post-write doorbell (:1556-1563), and that is explicitly best-effort:
on failure it prints `"note: doorbell to {to} skipped (pane unavailable); message
is durably queued"` and returns normally — **no exception, no lost mail, no
non-zero exit**.

### Summary: what's lost without herdr, precisely

- **Lost outright:** spawning new agents (`swarm spawn` hard-refuses), and the
  live-pane views (`ps` liveness column, blocked-agent detection for
  trust/permission/rate-limit dialogs, the wake-up doorbell that speeds up delivery).
- **Not lost:** the entire durable message/journal/queue substrate — `send`,
  `deliver`, `event`, `restore`, the whole named-agent-with-a-journal model, and
  `ps`'s tree/queue/mail-count view (degrades to `[?]`, doesn't disappear).

This matches (and is independently corroborated by) three prior in-repo design
investigations that already asked this exact question — see §4.

---

## 3. Effort to sever vs. effort to ship — the smaller path, honestly

### (a) Sever the dependency — run on plain terminals/tmux

The prior art already scoped this precisely (`docs/design/FLEET.md` §2, table at
line 82-88, and `docs/design/HARNESS.md` §2.1). Findings, re-verified here:

- Every Claude-Code-side hook (`deliver`, `event`, `restore`, doorbell re-ring) is
  `try/except → sys.exit(0)` and **fires through Claude Code's own hook mechanism**,
  not herdr — herdr is only the *container* the pane runs in, invisible to those
  four functions.
- The **irreducible minimum** any harness (herdr, tmux, plain terminal) must supply
  is: a way to create an observable pane/window per agent, a way to know it's alive,
  and a way to type text into it (FLEET.md:90-108). Plain tmux can do the first two
  natively (`tmux new-window`, `tmux list-panes`) and the third via `tmux send-keys`
  — a near-drop-in swap for `herdr tab create` / `herdr pane list` / `herdr pane
  send-text` in the ~7 call sites in the table above.
- **This was tried and explicitly rejected once already**, for a *stronger* reason
  than convenience: **going fully headless (no pane at all) was refused by the
  project's own "graveyard" review** — *"the graveyard explicitly refused headless
  codex agents because 'a headless agent has no pane'"* (FLEET.md:98-100,
  DESIGN §7) — *"Do not run leaves headless — their first-turn failures and model
  refusals are only visible in-pane"* (FLEET.md:100-101). A tmux port keeps the pane
  (satisfies that constraint); dropping the pane entirely does not, and has already
  been tried and killed.
- **Estimated effort:** small. ~7 call sites (`herdr_json`, `live_pane_set`,
  `pane_prompt_line`, `pane_text`, `ring_doorbell*`, `cmd_spawn`'s tab-create, and
  `cmd_close`) behind one thin abstraction, swapped for tmux equivalents; the
  `HERDR_ENV`/`HERDR_WORKSPACE_ID` env-based gating (bin/swarm:1315-1316, 1419) would
  need tmux-native equivalents (`$TMUX`, a pane/window id). Test suite already fakes
  herdr in 42 places (`grep -c herdr tests/test_swarm*.py`), so the seam is already
  test-isolated — this is refactor-shaped work, not a rewrite. Rough size: a few
  days for one engineer, most of it in the pane-liveness and readiness-signal
  parity (herdr's socket API gives structured JSON; tmux gives text to parse).

### (b) Ship herdr as part of the product

- herdr is **already a standalone, independently-installed binary** (Homebrew,
  ~10MB Rust, zero swarm-specific code) — "shipping" it would mean either
  vendoring/bundling the binary with swarm's installer, or (per the AGPL-3.0
  license) depending on it as a hard runtime prerequisite that swarm's own
  `install.sh`/`bootstrap.sh` installs automatically.
- The blocker isn't technical, it's licensing: AGPL-3.0-or-later on herdr means
  bundling it inside a distributed product has real copyleft implications
  (network-use clause) that a plain "swarm depends on brew-installed herdr" posture
  avoids. GitHub's own license field additionally flags herdr's repo as carrying
  non-standard license text ("Other/NOASSERTION") — this needs an actual read of
  herdr's LICENSE file before any bundling decision, not an assumption from the
  brew formula's summary tag.
- **Estimated effort:** small from a packaging-mechanics standpoint (add a
  `brew install herdr` / binary-fetch step to `install.sh`, already how bootstrap
  scripts commonly do it) — but gated on a license review that this investigation
  did not do (out of scope: local + light web only) and that a project lawyer or
  the herdr maintainer should weigh in on before committing.

**Which is smaller, honestly:** **(a), severing the hard-runtime coupling** is the
smaller, lower-risk, more clearly-scoped change — it's pure engineering against an
already-isolated seam with existing test fakes, no license question attached, and a
design doc (FLEET.md) that already did most of the scoping. (b) is not necessarily
*harder* in engineering hours, but it carries an open legal question this
investigation can't close, which makes its true cost unknown rather than merely
larger.

---

## 4. Liability or asset? Evidence, not vibes

**Verdict: a vertically-integrated asset today, with a cheap escape hatch banked
for later — not a liability, and the project has already treated it that way in
writing three separate times.**

Evidence for "asset": the core value swarm claims — *"the observable society is the
product"* (HARNESS.md:106, FLEET.md:459-460) — is a herdr-shaped claim. Swarm's own
design docs, independently, on three separate occasions (`HARNESS.md`, `FLEET.md`,
`OPENCODE-PLUGIN.md`), considered stripping the pane requirement to run agents
headless and **refused every time**, because a paneless agent's first-turn failures
and blocked/trust/permission states become invisible — exactly the failure mode a
multi-agent tool cannot afford to hide. Even the most aggressive alternative-harness
proposal on record (`OPENCODE-PLUGIN.md`, a full design for running opencode instead
of Claude Code as the child harness) keeps `herdr tab create` / pane-per-agent
completely **unchanged** (§3.6, §3.7 scorecard: "spawn / pane ... ✅ unchanged") —
of six harness surfaces redesigned in that document, the pane is the one that never
moved. Evidence for "not a liability": herdr is not a fragile or captive
dependency — it's a 16k-star, actively-pushed-today, independently popular
open-source project with its own docs, its own userbase, and a socket API that was
clearly *designed* for exactly this integration pattern (agent state detection,
orchestration API, explicit support for "claude, codex, copilot ... opencode" in its
own README) — swarm is using it exactly as intended, by a project healthy enough
that dependency risk (abandonment, breaking changes) is low relative to typical
early-stage tooling. And critically, the coupling is **shallow, not deep**: 41 grep
hits confined to one section of a 1,753-line file, every non-spawn touchpoint
already fails soft (tested live above — `ps` degrades to `[?]`, `send`'s core path
never touches herdr at all), and the one hard gate (`spawn` requiring `HERDR_ENV`)
is a deliberate design choice already scoped for a tmux swap, not an accidental
tangle. The honest framing: swarm is *choosing* to be vertically integrated with a
best-in-class terminal multiplexer because that integration is where the product's
observability claim lives — and it kept, in writing, a scoped, small, already-tested
severing path in its back pocket in case that choice ever needs to be undone.

---

## Sources

- [herdr documentation](https://herdr.dev/docs/)
- [herdr.dev — one terminal for the whole herd](https://herdr.dev/)
- [GitHub — ogulcancelik/herdr](https://github.com/ogulcancelik/herdr)
- `gh api repos/ogulcancelik/herdr` (stars/forks/pushed_at, run locally)
- `brew info herdr` (license, install analytics, run locally)
- `bin/swarm` (this repo, lines cited inline)
- `docs/design/FLEET.md`, `docs/design/HARNESS.md`, `docs/design/OPENCODE-PLUGIN.md`
  (this repo — prior internal investigations of this exact question)
- `tests/test_swarm.py`, `tests/test_swarm_process.py` (herdr fakes, this repo)
