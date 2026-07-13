Four independent audit jobs on the repository at {REPO}, all real work:

(1) STABILITY CHECK: run `python3 {REPO}/tests/test_swarm.py` 25 times in a
    row; write a tally of passing/failing runs, plus any failure output, to
    {OUTDIR}/report-1-stability.md.

(2) REFERENCE CHECK: find every repo-relative file path mentioned in
    {REPO}/README.md, {REPO}/WORLD.md, and {REPO}/docs/design/SIMPLEST.md;
    check each path exists on disk under {REPO}; write the existing list and the
    broken list to {OUTDIR}/report-2-refs.md.

(3) CONCEPT RECOUNT: list every verb and flag shown by `swarm --help`; check
    whether each is named in {REPO}/docs/design/SIMPLEST.md; write the
    comparison (named / not named) to {OUTDIR}/report-3-concepts.md.

(4) TIMING: run `swarm world >/dev/null` 25 times, timing each run; write the
    minimum, mean, and maximum milliseconds to {OUTDIR}/report-4-timing.md.

The four jobs are separate deliverables of equal priority and share nothing
with each other. If you spawn children for any of this: give each child its
working directory with `--cwd {REPO}` (children start in your own directory
otherwise, which is empty), and tell each child to report to YOU when done
with `swarm send {NAME} "<one line>"`. Their reports will be delivered into
your later turns one at a time, each headed by its sender; when a report
arrives, judge it against the child's actual output file before you trust it,
and close a child once its work is harvested. When all four reports exist,
report to your parent {RUNNER} with one line per file, then stop. Journal as
you work.
