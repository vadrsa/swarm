# Field evidence — workspace-placement bug (spawn omits --workspace) — 2026-07-12

**Author:** `field-tester`. Reported bug: spawned tabs open in the wrong herdr
workspace when multiple spaces exist. Root cause (operator-confirmed): `cmd_spawn`'s
`herdr tab create` passes no `--workspace`, so the child lands in herdr's *focused*
space, not the parent's.

## BASELINE — installed tool (delegation v2, `~/.local/bin/swarm`)

**Repro protocol** (SWARM_DIR sandbox `/tmp/swarm-sandbox-ws`; live `.swarm/`
untouched; focus manipulated for ~2.4 s and restored):

1. State: one workspace `w4` (label "swarm", focused) — every live agent including me
   (the spawner) lives in `w4`. Created workspace `w9` (label `ws-probe-b`) with
   `--no-focus`.
2. `herdr workspace focus w9` → verified `focused: ['w9']`.
3. With `w9` focused, spawned `ws-probe-1` from my session (my pane is in `w4`):
   `SWARM_DIR=/tmp/swarm-sandbox-ws swarm spawn ws-probe-1 "…placement probe…"`.
4. Read placement, restored focus to `w4`.

**Result (VERIFIED, exact outputs):**

```
child agent record:  pane: w9:p2   tab: w9:t2      <- FOCUSED space, not parent's
herdr tab list --workspace w4 : (…existing tabs…)   no ws-probe-1
herdr tab list --workspace w9 : w9:t1 1
                                w9:t2 ws-probe-1    <- the bug, precisely
```

Timeline: focus moved 01:51:41.4Z, spawn returned and placement captured, focus
restored 01:51:43.7Z.

**Verdict: BASELINE BUG REPRODUCED.** The child of a `w4` parent opened in `w9`
purely because `w9` held focus at spawn time. With a human working in another space,
every spawn in flight lands on the human's current screen and detaches from its
parent's workspace.

## AFTER — hardener's workspace-pin branch

**Binary:** `/Users/vadrsa/git/swarm-wspin/bin/swarm`, md5
`f0a5273235ecc1c7dfd6c49455106ec2`. Diff vs installed: one site — `cmd_spawn` inserts
`--workspace $HERDR_WORKSPACE_ID` into `herdr tab create` (env set by herdr in every
pane; verified present in mine: `w4`), with unset falling back to today's behavior.

Fresh workspaces for the after-runs: `wA` (ws-after-b), `wB` (ws-after-c); probes
spawned into the same sandbox.

### Test A — identical repro (PASS, VERIFIED)

`wA` focused (verified `['wA']`) → branch spawn of `ws-probe-2` from my `w4` session:

```
ws-probe-2 record:  pane: w4:p50  tab: w4:t50        <- PARENT's space
tab list wA:  wA:t1 1                                 <- only its default tab
tab list w4 (tail):  … w4:t50 ws-probe-2
```

### Test B — third space focused MID-spawn (PASS, MEASURED)

Spawn of `ws-probe-3` started 01:54:41.058Z; focus moved to `wB` at +343 ms (before
the tab create inside spawn):

```
ws-probe-3 record:  pane: w4:p61  tab: w4:t61        <- PARENT's space
tab list wB:  wB:t1 1        tab list wA:  wA:t1 1   <- both empty of probes
```

### Test C — grandchild from the child (PASS, VERIFIED)

With `wA` focused for the whole window (verified at capture time), `ws-probe-2`
(pane in `w4`) ran the branch binary to spawn `ws-probe-g1`:

```
ws-probe-g1 record:  pane: w4:p62  tab: w4:t62  parent: ws-probe-2   <- CHILD's space
focus during grandchild spawn: ['wA']
tab list w4 (tail): w4:t50 ws-probe-2 / w4:t61 ws-probe-3 / w4:t62 ws-probe-g1
```

### Verdict

**BASELINE BUG REPRODUCED; FIX VERIFIED LIVE in all three cases.** Children and
grandchildren now open in their spawner's workspace regardless of which space holds
focus — including focus stolen mid-spawn. This is the placement proof the fake-herdr
unit tests cannot give.

Cleanup: probe tabs (`w4:t50/t61/t62`) and workspaces `wA`, `wB`, and baseline's `w9`
closed; `w4` left focused; sandbox records remain at `/tmp/swarm-sandbox-ws`.
