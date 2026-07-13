# CLASSIFICATION RUBRIC — falsifier forms (shared by all falsifier-probe children)

You are auditing swarm journals as READ-ONLY EVIDENCE. Do NOT modify any .swarm/journal/*.md file.
Do NOT design or recommend anything. Your value is a TRUE count, including "zero".

## What counts as a FALSIFIER STATEMENT
A clause where the agent names an observation that WOULD SHOW IT IS OFF TRACK.
Usually "Falsifier: ...", "Falsifier for X: ...", "if <observation> then <I am wrong>".
- EXCLUDE: mentions of the word 'falsifier' that are quoted task text, doctrine
  restatement, a name of a test ("SPAN falsifier 1"), or a report ABOUT someone
  else's falsifier. Those are MENTIONS, not statements. Count them separately as MENTION.
- One journal ENTRY may carry one falsifier statement. Count statements, not lines.

## The three FORM classes (classify each STATEMENT into exactly one)
(a) OBSERVABLE-IN-FILE — the disconfirming observation, IF it occurred, would land in a
    file a later reader can open: this journal, a repo file, an artifact, a swarm record
    (.swarm/agents/, queue/, event/), a git-tracked doc, a test output committed to the repo.
    Test: "Could I, reading only files in this repo, tell whether this fired?" YES -> (a).
    Examples: "if the evidence file's timestamps don't match queue/*/delivered/",
    "if the child's task file lacks the doctrine sentences", "if deliverable mtimes show serial spacing".
(b) OBSERVABLE-ELSEWHERE — it would fire somewhere the repo does NOT record: a live pane, a
    tool result never written down, a model's private judgment, the operator's opinion,
    a process that has since exited, an ephemeral poller log in a session scratchpad.
    Test: firing is real and checkable IN PRINCIPLE, but the witness is not a repo file.
    Examples: "if the probe never reaches idle", "if the operator judges the phrase coaching",
    "if a future harness version co-submits".
(c) UNFALSIFIABLE-AS-WRITTEN — vague, tautological, or with no stated observation:
    "if this turns out wrong", "if I'm off base", "if the design is bad", "if the operator disagrees"
    (with no criterion), circular ones where the falsifier restates the claim.

BORDERLINE RULE: if the observation is file-observable ONLY because the agent itself would have to
choose to write it down (i.e. it fires in the world, and the ONLY record is the agent's own future
journal prose about it), that is still (a) — but flag it `a-self-report`. This distinction matters
enormously to the parent's question, so be strict and honest about it. A TRUE (a) has an
INDEPENDENT witness (mtime, a queue file, a git artifact, a test log, a record the agent
does not author as narrative).
So subdivide (a):
   a-independent = an independent, non-narrative witness exists in the repo
   a-self-report = only witness would be the agent's own later prose

## STEP 2 — the forward hunt (do this ONLY for class (a), both subtypes)
For each (a) statement, READ FORWARD in the same journal (and, if it names one, the artifact).
Determine exactly one outcome:
  FIRED-CHANGED   = the disconfirming observation demonstrably occurred AND the agent changed
                    course. Quote both the firing and the change, with file:line.
  FIRED-IGNORED   = the observation demonstrably occurred AND the agent did NOT change course.
                    THIS IS THE PATHOLOGY. Cite file:line for the firing and show the absence.
  NOT-FIRED       = the journal/artifact affirmatively shows the observation did NOT occur
                    (agent says "falsifier discharged", "checked, not the case", or the
                    artifact shows the healthy value).
  CANNOT-TELL     = the journal simply never returns to it. No later entry references it,
                    and no artifact settles it. BE HONEST — this is expected to be the
                    largest bucket and saying so is the finding, not a failure.

## OUTPUT — write ONE file, exactly this path, nothing else:
<OUTFILE>
Format:
  ## <journal>.md
  ### Statements table
  | # | file:line | exact quoted falsifier text (verbatim, trimmed) | class | subtype | outcome | evidence (file:line of firing/discharge, or "none") |
  ### Counts
  MENTIONS (not statements): N
  STATEMENTS: N   |  (a)-independent: N  (a)-self-report: N  (b): N  (c): N
  OUTCOMES for (a) only: FIRED-CHANGED N | FIRED-IGNORED N | NOT-FIRED N | CANNOT-TELL N
  ### Notable
  - any FIRED-IGNORED in full detail (this is the prize — do NOT manufacture one; zero is a fine answer)
  - any FIRED-CHANGED in full detail
  ### Reconciliation pairing (per journal)
  - Does the journal have entries it calls a reconciliation? How many?
  - Of those, how many name a falsifier IN THE SAME ENTRY? (the doctrine's requirement)
  - Does it name falsifiers but then go idle/never reconcile again? (yes/no + evidence)

MARK EVERY CLAIM: VERIFIED (I read the line) / MEASURED (I counted) / REASONED (I inferred).
Quote verbatim. Never invent a line number — every file:line must be real; I will spot-check.
Report to falsifier-probe when done: `swarm send falsifier-probe --stdin < <OUTFILE>` if short,
else send the path plus your counts.
