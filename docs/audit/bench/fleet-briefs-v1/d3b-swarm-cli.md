> SUPERSEDED by fleet-briefs-v3/d3b-swarm-cli.md; kept for the record (doubly stale — superseded generation, and predates v3's later `--model`/`--reason` edit).

This task exercises the `swarm` command-line tool directly. Do each step with
the real command; do not describe it, run it.

(1) Create one child agent named `helper-note` with the task text
    "Write the single word amber to {OUTDIR}/child-out.md, then stop."
    Use `swarm spawn` to do this.

(2) Send your parent {RUNNER} a message whose only content is the single line
    `spawn-done`. Use `swarm send`.

(3) Run `swarm ps` and save its full output to {OUTDIR}/ps-snapshot.md.

(4) Write to {OUTDIR}/cli-report.md three lines: on line 1 the exact `swarm
    spawn` command you ran; on line 2 the exact `swarm send` command you ran; on
    line 3 the word `done`.

When all of the above is finished, report to your parent {RUNNER} with one line,
then stop. Journal as you work.
