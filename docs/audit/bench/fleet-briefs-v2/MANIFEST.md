# fleet-briefs-v2 — MANIFEST (frozen)

Frozen at repo main@aa6063d, installed bin/swarm md5 9b976cef8ab903366274a3a1ff2552da, opencode v1.17.13.
Editing any brief means a new fleet-briefs-v3/ dir; cross-version rows compare only where the md5 is unchanged.
Placeholders the runner substitutes: {NAME}=probe agent name, {RUNNER}=parent/runner name, {OUTDIR}=fresh per-probe artifact dir inside the sandbox, {REPO}=absolute path to the read-only repo checkout.

**v2 delta from v1 (rig-bug fix, fleet-eval 2026-07-11):** run-cell.sh drives
`opencode run --dir $SANDBOX`, so the model's cwd is the sandbox, NOT the repo.
v1's d1-duties and d2-cheap referenced repo files by BARE path (`README.md`), which
resolved to nothing in the sandbox cwd — every model correctly reported "no README"
(a FALSE [M] failure). VERIFIED: a model with `--dir $SANDBOX` and `--auto` CAN read
an absolute `{REPO}/…` path outside cwd. Fix: d1-duties + d2-cheap now use the
`{REPO}/` prefix (d2-heavy already did). Only those two files' md5s changed; all others
are byte-identical to v1, so v1↔v2 rows compare directly for every unchanged brief.

| file | md5 | role |
|---|---|---|
| 00-duties-preamble.md | 89aee8ba7db13a31034af47cbf590937 | prepended to every dimension brief; the swarm-duties the model sees in place of SKILL.md |
| d1-duties.md | b8df09d200e2b3c34aaea98d4ca09d16 | D1 spawn brief (appended after preamble) — **v2: {REPO}/ prefix** |
| d2-cheap.md | badca7e470801128705e0d868c449573 | D2 cheap delegation brief (appended after preamble) — **v2: {REPO}/ prefix** |
| d2-heavy.md | babe164b49196bd4d21cd5bfce7b619d | D2 heavy delegation brief (appended after preamble); real spawn available |
| d3a-exact-paths.md | ba6d40fd31e038a5d859d438b462c88b | D3 exact-paths/exact-counts brief (from R2 D4) |
| d3b-swarm-cli.md | db7da7d1bce55bca86d7e888da9f8640 | D3 swarm-CLI syntax probe brief (NEW) |
| d3c-standby.md | 24a76c039d5a7364c893e5a70d3bcc86 | D3 message-delivery standby brief (turn-1 setup) |
| d3-M1-nearcap.txt | 2b1d86a19da51cbe13a88b4f048d50c7 | D3 message 1 — near-cap whole-delivery probe (amber..harbor, 7437 chars) |
| d3-M2-relation.txt | 99209cbf9f4001e6079781ca30febcc0 | D3 message 2 — relation-header echo probe |
| d3-M3-plain.txt | 88aa463d8ee4369162864b77dc3fb609 | D3 message 3 — plain task probe |
| d4-turn1.md | 46ceab5fb5534ed7743b4a4650603ee9 | D4 turn-1 brief — plan + Shelf 1 |
| d4-turn2-distractor.md | 43e6db6c6dccf4d8291421cdbfaa5b3d | D4 turn-2 message — distractor + Shelf 2 |
| d4-turn3-restart.md | 9c2f877f99f0cdd1f663231d6d62071f | D4 turn-3 message — simulated restart, re-read journal + Shelf 3 |
