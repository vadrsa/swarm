# SHARD BRIEF — fp-compliance children (fpc-s0 … fpc-s3)

> SUPERSEDED by nothing (still actively cited by path and byte count in docs/design/ORG-REVIEW.md:468); kept for the record (the Q2i/Q2ii self-labelled-vs-substantive split and the Q6 power-separation design; cited as a VERIFIED exhibit).

READ-ONLY. Never modify any `.swarm/journal/*.md`. You are counting, not designing.
Your value is a TRUE count, including "zero". Do not manufacture findings.

## The doctrine under test
`swarm world`, duty 9: **"a reconciliation is a journal entry that names its falsifier
(the observation that would show you are off track)."**
We are measuring how true that is in practice.

## Definitions you MUST use (from docs/audit/_falsifier-rubric.md)
- **FALSIFIER STATEMENT** — a clause where the agent names an observation that WOULD SHOW
  IT IS OFF TRACK. Usually "Falsifier: ...", "if <observation> then <I am wrong>".
- **MENTION** (NOT a statement) — the word 'falsifier' appearing as: quoted task text,
  doctrine restatement, the *name of a test* ("SPAN falsifier 1"), or a report ABOUT
  someone else's falsifier. These do NOT count as the agent naming its own falsifier.
  This distinction is the whole audit. Be strict.

- **ENTRY** — a `^## ` timestamped heading and its body, up to the next `^## `.
- **RECONCILIATION ENTRY** — the agent is taking stock / re-planning / checking whether it
  is still on track: reviewing progress, re-deciding what to do next, assessing the tree,
  deciding to spawn/close, "where I am / what's left". A pure work-log ("wrote the file",
  "ran the test, it passed") or a pure spawn-notice is NOT a reconciliation. An entry
  written *before going idle* that takes stock IS one.

## Your corpus
A FROZEN snapshot. Read journals ONLY from:
  /private/tmp/claude-501/-Users-vadrsa-git-swarm/46600c76-af7c-494d-8bd3-000e599e5abb/scratchpad/snap/
Do NOT read from `.swarm/journal/` — it is changing under us; the snapshot is the record.
BUT: report `file:line` as **`<name>.md:<line>`** (basename + line number in the snapshot,
which is line-identical to the original at freeze time). Your files are listed in your task.

## What to report — PER JOURNAL, one row each
| journal | total entries | Q2i self-labelled recon | Q2ii substantive recon (REASONED) | Q3 of Q2ii, how many name a falsifier IN THE SAME ENTRY | Q4 named-then-vanished | Q5 never-returns |

- **Q1 total entries** = count of `^## ` headings. MEASURED.
- **Q2i self-labelled** = entries where the agent itself calls it a reconciliation
  (word 'reconcil*' in the heading OR the body plainly self-labels: "reconciling",
  "reconciliation:"). MEASURED — quote the heading.
- **Q2ii substantive** = YOUR JUDGMENT of entries that ARE a reconciliation by the
  definition above, whether or not labelled. This is REASONED — say so. Q2ii should be a
  SUPERSET of Q2i (if not, explain). For each Q2ii entry give `file:line` of its heading.
- **Q3 COMPLIANCE** = of your Q2ii entries, how many contain a FALSIFIER STATEMENT
  (not a mention) *inside that same entry's body*. Give the count and list which ones.
  **This ratio Q3/Q2ii is the compliance rate — the number the whole audit exists for.**
  Also report Q3i = of the Q2i (self-labelled) entries, how many name a falsifier.
- **Q4 named-then-vanished** = journal names >=1 falsifier STATEMENT in its LAST entry and
  never writes another entry after it. (The falsifier can never be honored — the agent
  stopped writing.) yes/no per journal + the file:line of that last falsifier.
- **Q5 never-returns** = journal names >=2 falsifier STATEMENTS across >=2 entries but
  NEVER once re-references an earlier falsifier (never says discharged / fired / didn't
  fire / "my falsifier from the last entry" / restates and settles it). yes/no per journal.

## Q6 — DO NOT judge this, just REPORT candidates to me
Any entry that RE-REFERENCES a falsifier named in an EARLIER entry — anything that looks
like "discharged", "it fired", "did not fire", "that falsifier holds", "my earlier
falsifier", "the falsifier I named". List every candidate `file:line` + the verbatim line.
**I (fp-compliance) verify each one myself by reading — you only surface candidates.
Over-report here rather than under-report. Do not decide; hand me the line.**

## Method
Grep to FIND candidates; then **READ the entry** to judge it. A regex cannot tell you
whether an entry is a reconciliation or whether a 'falsifier' line is a statement or a
mention. Spot-check every count you report. If you are unsure on an entry, put it in a
BORDERLINE list with the quote and let me arbitrate — that is more useful than a confident
wrong bucket.

## Output
Write ONE file: `docs/audit/_fpc-<yourname>.md`. Include:
1. The per-journal table above.
2. Shard totals (all six numbers, exact).
3. The Q6 candidate list, verbatim lines with file:line.
4. A BORDERLINE list of entries you couldn't confidently bucket.
Mark every claim **VERIFIED** (I read the line) / **MEASURED** (I counted) / **REASONED**
(I inferred). Quote verbatim. Never invent a line number — I will spot-check.

When done: `swarm send fp-compliance --stdin < docs/audit/_fpc-<yourname>.md` if short,
else send the path plus your six shard totals.
