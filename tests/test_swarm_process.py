"""Process-level tests for bin/swarm, ported from the independent review.

Origin: docs/design/REVIEW.md wrote 22 tests against real `swarm` subprocesses
(fixture .swarm/ trees, a fake herdr, a fake claude, a real broken-pipe
stdout). This file ports them to the shipped tree. Runnable as
`python3 -m unittest test_swarm_process -v` from this directory.

Every test here spawns the real process where possible: execute, never infer.
Pure-file logic stays in test_swarm.py; this file covers the verbs end to end.

Ported with adaptations (the code moved under rulings R1-R3 after the review):
  - deliver-on-broken-stdout now expects exit 0, not the 120 the review found
    (ruling R3 fixed it; test_swarm.py holds the twin regression).
Dropped as mooted or already covered, per the dedupe instruction:
  - trailer pessimism at 100 waiting: the queue-depth trailer is deleted
    (ruling R1); whole-delivery at depth is proven by test_swarm.py's
    test_boundary_size_message_delivered_whole_at_depth_150.
  - giant-from silently drops body: behavior redefined by ruling R2
    (build_delivery returns None); covered by test_swarm.py's
    test_undeliverable_returns_none_never_bare_header.
  - corrupt queue file skipped not fatal: covered by test_swarm.py's
    test_corrupt_queue_file_counted_not_hidden.
  - stop re-ring fires when queue non-empty: covered process-level by
    test_swarm.py's test_stop_event_rings_iff_head_deliverable_process_level.
"""
import importlib.machinery
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SWARM = os.path.join(os.path.dirname(HERE), "bin", "swarm")

loader = importlib.machinery.SourceFileLoader("swarmmod", SWARM)
spec = importlib.util.spec_from_loader("swarmmod", loader)
sw = importlib.util.module_from_spec(spec)
loader.exec_module(sw)

FAKE_HERDR = r'''#!/usr/bin/env bash
# fake herdr: logs every call, answers tab create / pane list with JSON
echo "$@" >> "$FAKE_HERDR_LOG"
case "$1 $2" in
  "tab create") echo '{"result":{"root_pane":{"pane_id":"pane-77"},"tab":{"tab_id":"tab-77"}}}' ;;
  "pane list")  echo '{"result":{"panes":[{"pane_id":"pane-77"}]}}' ;;
  "pane run")   shift 3; bash "$@" >/dev/null 2>&1 & ;;   # drop pane-id, run launcher
  "pane read")  echo "" ;;                                 # empty prompt line
  *) : ;;
esac
exit 0
'''

FAKE_CLAUDE = r'''#!/usr/bin/env bash
# fake claude: record argv so the test can see what reached it, then exit 0
printf '%s\n' "$@" > "$FAKE_CLAUDE_ARGS"
exit 0
'''


def run_swarm(args, env_extra, stdin_text="", cwd=None):
    # Clean room: this suite may itself run INSIDE a live swarm, so our own
    # SWARM_AGENT_ID and the real herdr must not leak into the fixture.
    env = {k: v for k, v in os.environ.items()
           if k not in ("SWARM_AGENT_ID", "SWARM_DIR", "HERDR_ENV",
                        "HERDR_WORKSPACE_ID")}
    env["PATH"] = "/usr/bin:/bin"          # no real herdr, no real claude
    env.update(env_extra)
    return subprocess.run([sys.executable, SWARM] + args, input=stdin_text,
                          capture_output=True, text=True, env=env,
                          cwd=cwd or os.getcwd(), timeout=120)


class Base(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="swarm-proc-")
        self.bindir = tempfile.mkdtemp(prefix="swarm-proc-bin-")

    def tearDown(self):
        shutil.rmtree(self.root, ignore_errors=True)
        shutil.rmtree(self.bindir, ignore_errors=True)

    def q(self, to, frm, ts, body):
        d = sw.q_dir(self.root, to)
        os.makedirs(d, exist_ok=True)
        fn = f"{ts}-{frm}.json"
        with open(os.path.join(d, fn), "w") as f:
            json.dump({"to": to, "from": frm, "ts": ts, "body": body}, f)
        return fn

    def fake_tools(self, claude=True):
        log = os.path.join(self.root, "herdr.log")
        argsf = os.path.join(self.root, "claude.args")
        with open(os.path.join(self.bindir, "herdr"), "w") as f:
            f.write(FAKE_HERDR)
        os.chmod(os.path.join(self.bindir, "herdr"), 0o755)
        if claude:
            with open(os.path.join(self.bindir, "claude"), "w") as f:
                f.write(FAKE_CLAUDE)
            os.chmod(os.path.join(self.bindir, "claude"), 0o755)
        env = {"PATH": self.bindir + ":/usr/bin:/bin",
               "SWARM_DIR": self.root, "HERDR_ENV": "1",
               "FAKE_HERDR_LOG": log, "FAKE_CLAUDE_ARGS": argsf,
               "SWARM_READY_TIMEOUT": "10"}
        return env, log, argsf


class TestProcessLevelDeliver(Base):
    """The real `swarm deliver` process — happy path AND real failed write."""

    def test_cli_deliver_moves_file_after_real_drain(self):
        fn = self.q("kid", "boss", 1000, "the real payload")
        p = run_swarm(["deliver"],
                      {"SWARM_DIR": self.root, "SWARM_AGENT_ID": "kid"},
                      stdin_text="{}")
        self.assertEqual(p.returncode, 0)
        out = json.loads(p.stdout)
        ctx = out["hookSpecificOutput"]["additionalContext"]
        self.assertIn("the real payload", ctx)
        self.assertIn("from boss", ctx)
        self.assertFalse(os.path.exists(os.path.join(sw.q_dir(self.root, "kid"), fn)))
        self.assertTrue(os.path.exists(
            os.path.join(sw.delivered_dir(self.root, "kid"), fn)))

    def test_cli_deliver_failed_write_file_does_not_move(self):
        # stdout is a pipe whose read end is already closed -> flush raises
        # EPIPE inside the real process. The file must NOT move, and the exit
        # code must be 0 (the review found 120 here; ruling R3 fixed it).
        fn = self.q("kid", "boss", 1000, "precious")
        r, w = os.pipe()
        os.close(r)
        env = dict(os.environ)
        env.update({"SWARM_DIR": self.root, "SWARM_AGENT_ID": "kid"})
        p = subprocess.Popen([sys.executable, SWARM, "deliver"],
                             stdin=subprocess.PIPE, stdout=w,
                             stderr=subprocess.PIPE, env=env)
        os.close(w)
        p.communicate(input=b"{}", timeout=60)
        self.assertTrue(os.path.exists(os.path.join(sw.q_dir(self.root, "kid"), fn)),
                        "failed drain must leave the message in the queue")
        self.assertFalse(os.path.isdir(sw.delivered_dir(self.root, "kid")))
        self.assertEqual(p.returncode, 0)

    def test_cli_deliver_operator_is_noop(self):
        self.q("operator", "boss", 1000, "mail for the human")
        p = run_swarm(["deliver"], {"SWARM_DIR": self.root}, stdin_text="{}")
        self.assertEqual(p.returncode, 0)
        self.assertEqual(p.stdout, "")
        self.assertEqual(len(sw.list_waiting(self.root, "operator")), 1)


class TestSendCli(Base):
    def _agents(self):
        os.makedirs(os.path.join(self.root, "agents"), exist_ok=True)
        for n, par in (("boss", "operator"), ("kid", "boss")):
            with open(sw.agent_rec_path(self.root, n), "w") as f:
                json.dump({"name": n, "parent": par, "pane": "nope"}, f)

    def test_send_stdin_queues_exact_bytes(self):
        self._agents()
        body = 'tricky $(rm -rf /) `backticks` \'quotes\' 多字节\nsecond line'
        p = run_swarm(["send", "kid", "--stdin"], {"SWARM_DIR": self.root},
                      stdin_text=body)
        self.assertEqual(p.returncode, 0, p.stderr)
        w = sw.list_waiting(self.root, "kid")
        self.assertEqual(len(w), 1)
        self.assertEqual(w[0][2]["body"], body)
        self.assertEqual(w[0][2]["from"], "operator")
        self.assertIn("doorbell to kid skipped", p.stderr)  # no herdr here

    def test_send_oversize_refused_and_nothing_queued(self):
        self._agents()
        p = run_swarm(["send", "kid", "--stdin"], {"SWARM_DIR": self.root},
                      stdin_text="A" * (sw.TURN_CAP + 1))
        self.assertEqual(p.returncode, 1)
        self.assertIn("put it in a file, send the path", p.stderr)
        self.assertEqual(sw.list_waiting(self.root, "kid"), [])

    def test_send_unknown_agent_refused(self):
        p = run_swarm(["send", "ghost", "hello"], {"SWARM_DIR": self.root})
        self.assertEqual(p.returncode, 1)
        self.assertIn("unknown agent", p.stderr)

    def test_send_to_operator_never_refused_no_doorbell(self):
        p = run_swarm(["send", "operator", "--stdin"],
                      {"SWARM_DIR": self.root, "SWARM_AGENT_ID": "kid"},
                      stdin_text="done, please review")
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertNotIn("doorbell", p.stderr)
        self.assertEqual(len(sw.list_waiting(self.root, "operator")), 1)


class TestSpawnEndToEnd(Base):
    def test_spawn_happy_path_with_fake_herdr(self):
        env, log, argsf = self.fake_tools(claude=True)
        p = run_swarm(["spawn", "worker", "do the thing", "--model", "sonnet",
                       "--reason", "this test asserts the exact record fields, "
                       "journal text and argv the spawn must produce — every claim "
                       "it makes is checked mechanically here, so a wrong answer "
                       "cannot survive the assertions"],
                      env, cwd=self.root)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(p.stdout.strip(), "worker")
        with open(sw.agent_rec_path(self.root, "worker")) as f:
            rec = json.load(f)
        self.assertEqual(rec["parent"], "operator")
        self.assertEqual(rec["pane"], "pane-77")
        with open(sw.journal_path(self.root, "worker")) as f:
            j = f.read()
        self.assertIn("do the thing", j)
        with open(os.path.join(self.root, "settings", "worker.task")) as f:
            task = f.read()
        self.assertIn("You are agent worker", task)
        self.assertIn("judged by reading it, never", task)   # duties briefed
        with open(log) as f:
            calls = f.read()
        self.assertIn("tab create", calls)
        self.assertIn("SWARM_AGENT_ID=worker", calls)
        for _ in range(50):                                  # launcher runs async
            if os.path.exists(argsf):
                break
            time.sleep(0.1)
        with open(argsf) as f:
            argv = f.read().splitlines()                     # what claude saw
        self.assertIn("--settings", argv)
        self.assertTrue(any("You are agent worker" in a for a in argv))
        with open(os.path.join(self.root, "settings", "worker.status")) as f:
            st = f.read()
        self.assertTrue(st.startswith("launching"))
        with open(os.path.join(self.root, "settings", "worker.json")) as f:
            settings = json.load(f)
        self.assertEqual(sorted(settings["hooks"]),
                         ["Notification", "SessionStart", "Stop", "UserPromptSubmit"])

    def test_spawn_name_collision_errors(self):
        env, _, _ = self.fake_tools(claude=True)
        # Both spawns carry the flags: the point of this test is that the SECOND one is
        # refused for the NAME, so the first must be a fully valid spawn and the second
        # must fail the tombstone check — not the mandate. A flagless second spawn would
        # still exit 1 and this test would still pass, while testing nothing.
        self.assertEqual(run_swarm(["spawn", "worker", "t", "--model", "sonnet",
                                    "--reason", "checks one string in stderr and one "
                                    "file's existence; the assertion is the whole "
                                    "verification and it is free"],
                                   env, cwd=self.root).returncode, 0)
        p = run_swarm(["spawn", "worker", "t2", "--model", "sonnet",
                       "--reason", "same fixture, second spawn — the refusal it must "
                       "produce is one grep of stderr"],
                      env, cwd=self.root)
        self.assertEqual(p.returncode, 1)
        self.assertIn("already used", p.stderr)

    def test_spawn_confirmed_failure_tears_down_but_keeps_tombstone(self):
        env, log, _ = self.fake_tools(claude=False)   # no claude anywhere on PATH
        # Flags present ON PURPOSE: this test must reach the LAUNCHER and fail there
        # ("did not start"), which it can only do by passing the mandate first. Without
        # them it would exit 1 at the guard, never build a launcher, and still satisfy
        # `returncode == 1` — a green test that had stopped testing the teardown.
        p = run_swarm(["spawn", "worker", "t", "--model", "sonnet",
                       "--reason", "the failure it must produce is a string in stderr "
                       "and two files on disk; both are checked here, so a wrong "
                       "teardown is caught by the next three assertions"],
                      env, cwd=self.root)
        self.assertEqual(p.returncode, 1)
        self.assertIn("did not start", p.stderr)
        self.assertIn("claude not found", p.stderr)
        self.assertFalse(os.path.exists(sw.agent_rec_path(self.root, "worker")),
                         "binding must be removed on confirmed failure")
        self.assertTrue(os.path.exists(sw.journal_path(self.root, "worker")),
                        "tombstone must survive the failed spawn")
        with open(log) as f:
            self.assertIn("tab close tab-77", f.read())
        p2 = run_swarm(["spawn", "worker", "t2", "--model", "sonnet",
                        "--reason", "re-spawn of a burned name; the tombstone refusal "
                        "is one string in stderr"],
                       env, cwd=self.root)
        self.assertIn("already used", p2.stderr)   # name burned forever

    def test_spawn_outside_herdr_refused_before_tombstone(self):
        env = {"SWARM_DIR": self.root, "HERDR_ENV": "0"}
        # No flags, ON PURPOSE — and it must STILL say "not inside herdr", not "spawn
        # needs --model". This pins the mandate guard's PLACEMENT: it sits after the
        # herdr check, so the pre-existing refusals keep their own stderr. Hoisting the
        # guard to the top of cmd_spawn (the naive spot) breaks exactly this assertion.
        p = run_swarm(["spawn", "worker", "t"], env, cwd=self.root)
        self.assertEqual(p.returncode, 1)
        self.assertIn("not inside herdr", p.stderr)
        self.assertFalse(os.path.exists(sw.journal_path(self.root, "worker")),
                         "refusal before claiming must not burn the name")

    def test_spawn_pins_child_to_spawners_workspace(self):
        # without --workspace, herdr places the tab in the FOCUSED workspace,
        # not the spawner's — a child could land in whatever space the human
        # is viewing. The spawner's HERDR_WORKSPACE_ID pins it.
        env, log, _ = self.fake_tools(claude=True)
        env["HERDR_WORKSPACE_ID"] = "w4"
        p = run_swarm(["spawn", "worker", "t", "--model", "sonnet",
                       "--reason", "fixture; the tab-create log line is the whole assertion"],
                      env, cwd=self.root)
        self.assertEqual(p.returncode, 0, p.stderr)
        with open(log) as f:
            create = [l for l in f if l.startswith("tab create")][0]
        self.assertIn("--workspace w4", create)

    def test_spawn_without_workspace_env_falls_back_gracefully(self):
        env, log, _ = self.fake_tools(claude=True)  # no HERDR_WORKSPACE_ID
        p = run_swarm(["spawn", "worker", "t", "--model", "sonnet",
                       "--reason", "fixture; the tab-create log line is the whole assertion"],
                      env, cwd=self.root)
        self.assertEqual(p.returncode, 0, p.stderr)
        with open(log) as f:
            create = [l for l in f if l.startswith("tab create")][0]
        self.assertNotIn("--workspace", create)

    def test_spawn_bad_names_refused(self):
        env, _, _ = self.fake_tools(claude=True)
        # These spawns pass the mandate flags and assert on the SPECIFIC refusal, not
        # merely on `returncode == 1`. Under a required flag, EVERYTHING exits 1 — so a
        # bare returncode assertion here would stay green while silently ceasing to test
        # any of the six name cases. The name check must be what refuses these, and the
        # test now proves it does.
        for bad in ("Worker", "has space", "-lead", "x" * 41):
            p = run_swarm(["spawn", bad, "t", "--model", "sonnet",
                           "--reason", "malformed name; the refusal is one string in "
                           "stderr, checked right here"],
                          env, cwd=self.root)
            self.assertEqual(p.returncode, 1, f"{bad!r} must be refused")
            self.assertIn("bad name", p.stderr, f"{bad!r} must fail the NAME check")
        for reserved in ("operator", "delivered"):
            p = run_swarm(["spawn", reserved, "t", "--model", "sonnet",
                           "--reason", "reserved name; the refusal is one string in "
                           "stderr, checked right here"],
                          env, cwd=self.root)
            self.assertEqual(p.returncode, 1, f"{reserved!r} must be refused")
            self.assertIn("reserved", p.stderr,
                          f"{reserved!r} must fail the RESERVED check")


class TestSpawnMandate(Base):
    """--model and --reason are REQUIRED. The parent chooses the child's model.

    The mandate exists because 142 of 143 spawns silently inherited an ambient default
    that nobody chose. A missing flag must FAIL, and it must fail with an error that
    teaches the question the reason has to answer.
    """

    GOOD = ["--model", "sonnet", "--reason",
            "the child's output here is a file whose contents this test greps; a wrong "
            "answer is caught by the assertion, so it costs nothing"]

    def test_spawn_without_model_fails(self):
        env, _, _ = self.fake_tools(claude=True)
        # A real reason even here, where the spawn is REFUSED and it is never stored: a
        # clause that gets sloppy because "nobody reads this one" is exactly the theater
        # this mandate exists to prevent, and a fixture is where it would start.
        p = run_swarm(["spawn", "worker", "t", "--reason",
                       "the refusal this must produce is one string in stderr, asserted "
                       "on the next line — a wrong answer cannot get past it"],
                      env, cwd=self.root)
        self.assertEqual(p.returncode, 1)
        self.assertIn("--model", p.stderr)
        self.assertFalse(os.path.exists(sw.journal_path(self.root, "worker")),
                         "a refused spawn must not burn the name")

    def test_spawn_without_reason_fails(self):
        env, _, _ = self.fake_tools(claude=True)
        p = run_swarm(["spawn", "worker", "t", "--model", "sonnet"],
                      env, cwd=self.root)
        self.assertEqual(p.returncode, 1)
        self.assertIn("--reason", p.stderr)
        self.assertFalse(os.path.exists(sw.journal_path(self.root, "worker")),
                         "a refused spawn must not burn the name")

    def test_spawn_with_neither_fails(self):
        env, _, _ = self.fake_tools(claude=True)
        p = run_swarm(["spawn", "worker", "t"], env, cwd=self.root)
        self.assertEqual(p.returncode, 1)
        # Pinned to the SPECIFIC refusal, not just to exit 1 — same discipline this change
        # forced on the older tests. Under a required flag everything exits 1, so a bare
        # returncode assertion is a test that can stop testing without ever going red.
        self.assertIn("--model", p.stderr)
        self.assertIn("--reason", p.stderr)
        self.assertFalse(os.path.exists(sw.journal_path(self.root, "worker")))

    def test_blank_reason_is_not_a_reason(self):
        # Whitespace must not satisfy the mandate. A field that a null string satisfies
        # has compelled nothing.
        env, _, _ = self.fake_tools(claude=True)
        p = run_swarm(["spawn", "worker", "t", "--model", "sonnet", "--reason", "   "],
                      env, cwd=self.root)
        self.assertEqual(p.returncode, 1)
        self.assertIn("--reason", p.stderr)

    def test_error_teaches_the_question_not_just_the_flag(self):
        # The error IS the teaching moment — it is the only place most parents will ever
        # meet this idea. It must carry the QUESTION ("can you cheaply tell that this
        # child was wrong?") and the BANNED framing ("why is this model good" launders a
        # guess). An error that merely demands a string would produce "fits the task".
        env, _, _ = self.fake_tools(claude=True)
        err = run_swarm(["spawn", "worker", "t"], env, cwd=self.root).stderr
        self.assertIn("cheaply tell", err)
        self.assertIn("launders a guess", err)
        self.assertIn("opus", err)          # the menu, so the parent can actually choose

    def test_both_present_succeeds_and_record_carries_both(self):
        env, _, _ = self.fake_tools(claude=True)
        p = run_swarm(["spawn", "worker", "t"] + self.GOOD, env, cwd=self.root)
        self.assertEqual(p.returncode, 0, p.stderr)
        with open(sw.agent_rec_path(self.root, "worker")) as f:
            rec = json.load(f)
        self.assertEqual(rec["model"], "sonnet")
        self.assertIn("caught by the assertion", rec["reason"])

    def test_reason_and_model_survive_into_the_journal(self):
        # The journal is the reason's PRIMARY surface: it is where the CHILD reads what
        # it was picked for, and where a later reader finds the decision. A reason that
        # lived only in a JSON the tool reads back would be write-only.
        env, _, _ = self.fake_tools(claude=True)
        run_swarm(["spawn", "worker", "t"] + self.GOOD, env, cwd=self.root)
        with open(sw.journal_path(self.root, "worker")) as f:
            j = f.read()
        self.assertIn("Model: sonnet", j)
        self.assertIn("caught by the assertion", j)

    def test_haiku_is_refused_and_the_refusal_is_honest(self):
        env, _, _ = self.fake_tools(claude=True)
        p = run_swarm(["spawn", "worker", "t", "--model", "haiku",
                       "--reason", "a cheap read whose output would be one file this "
                       "test greps — but the model gate refuses it first, and that "
                       "refusal is a single string in stderr"],
                      env, cwd=self.root)
        self.assertEqual(p.returncode, 1)
        self.assertIn("not agent-capable", p.stderr)
        # The refusal must carry its OWN epistemic status. The measured cause of the wedge
        # is a permission gate swarm hands EVERY child ("Opus would block too"), and the
        # settling probe was never run. A refusal that read as "the Haiku problem is
        # solved" would be the exact harm HARNESS.md §2.4 warns about.
        self.assertIn("settling probe not yet run", p.stderr)
        self.assertFalse(os.path.exists(sw.journal_path(self.root, "worker")),
                         "a refused model must not burn the name")

    def test_unknown_model_is_refused(self):
        env, _, _ = self.fake_tools(claude=True)
        p = run_swarm(["spawn", "worker", "t", "--model", "gpt-9",
                       "--reason", "whatever this child produced would be read back by "
                       "the assertion below; the unknown-model gate refuses it first"],
                      env, cwd=self.root)
        self.assertEqual(p.returncode, 1)
        self.assertIn("unknown model", p.stderr)

    def test_default_is_a_real_choice_recorded_but_not_passed_to_claude(self):
        # `default` means "I looked, and the configured default is right" — a DECISION,
        # and the record keeps it as one. But the LAUNCHER must pass no --model at all,
        # exactly as an unpinned spawn did. Record and launcher diverge here ON PURPOSE:
        # collapsing `default` to "" in the record would erase the very distinction this
        # change exists to capture — a chosen default vs. an inherited one.
        env, _, argsf = self.fake_tools(claude=True)
        p = run_swarm(["spawn", "worker", "t", "--model", "default",
                       "--reason", "the default is right here and its output is one "
                       "file this test greps"], env, cwd=self.root)
        self.assertEqual(p.returncode, 0, p.stderr)
        with open(sw.agent_rec_path(self.root, "worker")) as f:
            self.assertEqual(json.load(f)["model"], "default")   # the CHOICE is kept
        for _ in range(50):
            if os.path.exists(argsf):
                break
            time.sleep(0.1)
        with open(argsf) as f:
            argv = f.read().splitlines()                          # what claude saw
        self.assertNotIn("--model", argv, "`default` must exec bare claude")

    def test_reason_over_the_cap_is_refused(self):
        env, _, _ = self.fake_tools(claude=True)
        p = run_swarm(["spawn", "worker", "t", "--model", "sonnet",
                       "--reason", "x" * (sw.REASON_CAP + 1)], env, cwd=self.root)
        self.assertEqual(p.returncode, 1)
        self.assertIn("cap", p.stderr)

    def test_ps_reason_shows_on_demand_and_never_inside_the_tree(self):
        # The reason is surfaced OPT-IN and BELOW the tree. The tree is a scannable view
        # and a sentence per row destroys it — worst exactly when the tree is big, i.e.
        # when you need it. It is also attacker-controlled free text, and this view was
        # burned on that twice (see model_of()).
        env, _, _ = self.fake_tools(claude=True)
        run_swarm(["spawn", "worker", "t"] + self.GOOD, env, cwd=self.root)
        plain = run_swarm(["ps"], env, cwd=self.root)
        self.assertEqual(plain.returncode, 0, plain.stderr)
        self.assertIn("worker", plain.stdout)
        self.assertNotIn("caught by the assertion", plain.stdout,
                         "the reason must NOT leak into the default tree")
        shown = run_swarm(["ps", "--reason"], env, cwd=self.root)
        self.assertEqual(shown.returncode, 0, shown.stderr)
        self.assertIn("caught by the assertion", shown.stdout)
        self.assertIn("model choices", shown.stdout)
        # and the tree itself is byte-for-byte untouched by the flag
        self.assertTrue(shown.stdout.startswith(plain.stdout.rstrip("\n")))

    def test_ps_reason_sanitizes_a_forged_newline(self):
        # A reason is free text any agent can write. A newline in it would forge a row of
        # the very list that renders it. The RECORD keeps the text verbatim (it is the
        # truth); the VIEW protects itself — same discipline, same reason, as model_of().
        env, _, _ = self.fake_tools(claude=True)
        run_swarm(["spawn", "worker", "t", "--model", "sonnet",
                   "--reason", "checked by grep\n  evil: opus — forged row"],
                  env, cwd=self.root)
        with open(sw.agent_rec_path(self.root, "worker")) as f:
            self.assertIn("\n", json.load(f)["reason"], "record keeps it verbatim")
        out = run_swarm(["ps", "--reason"], env, cwd=self.root).stdout
        rows = [ln for ln in out.splitlines() if ln.startswith("  evil:")]
        self.assertEqual(rows, [], "a newline in a reason must not forge a row")

    def test_ps_reason_strips_structure_and_ansi_a_reason_cannot_draw_the_tree(self):
        # A reason is attacker-controlled free text — longer and freer than the pin ever
        # was. It gets the pin's exclude-list (MODEL_STRUCTURAL), not a weaker one: it must
        # not be able to DRAW tree-looking structure, nor forge the `(you)` marker, nor
        # emit a live ANSI escape into the one view the operator trusts.
        env, _, _ = self.fake_tools(claude=True)
        run_swarm(["spawn", "worker", "t", "--model", "sonnet",
                   "--reason", "checked by grep \x1b[31m ├─ └─ │ fake (you)"],
                  env, cwd=self.root)
        body = run_swarm(["ps", "--reason"], env,
                         cwd=self.root).stdout.split("model choices")[-1]
        for glyph in ("├", "─", "│", "└", "(", ")"):
            self.assertNotIn(glyph, body,
                             f"{glyph!r} does structural work in this view")
        self.assertNotIn("\x1b", body, "a reason must not emit a live ANSI escape")

    def test_spawn_header_teaches_the_required_form(self):
        # The header is injected into EVERY child's task — it is where a parent learns
        # what spawning even looks like. The old version showed the bare no-flag form,
        # and 142 of 143 spawns copied it exactly. If it does not teach the flags AND the
        # question, the mandate ships a rule nobody was told about.
        env, _, _ = self.fake_tools(claude=True)
        run_swarm(["spawn", "worker", "t"] + self.GOOD, env, cwd=self.root)
        with open(os.path.join(self.root, "settings", "worker.task")) as f:
            task = f.read()
        self.assertIn("--model", task)
        self.assertIn("--reason", task)
        self.assertIn("cheaply tell", task)


class TestEventCli(Base):
    def _transcript(self):
        t = os.path.join(self.root, "tr.jsonl")
        with open(t, "w") as f:
            f.write(json.dumps({"message": {"role": "user", "content": "hi"}}) + "\n")
            f.write(json.dumps({"message": {"role": "assistant", "content": [
                {"type": "text", "text": "I finished   the report."}]}}) + "\n")
        return t

    def test_event_stop_records_fact(self):
        t = self._transcript()
        p = run_swarm(["event", "stop"],
                      {"SWARM_DIR": self.root, "SWARM_AGENT_ID": "kid"},
                      stdin_text=json.dumps({"transcript_path": t}))
        self.assertEqual(p.returncode, 0)
        with open(sw.event_path(self.root, "kid")) as f:
            fact = json.load(f)
        self.assertEqual(fact["event"], "stop")
        self.assertEqual(fact["last_words"], "I finished the report.")

    def test_stop_no_ring_when_queue_empty(self):
        env, log, _ = self.fake_tools(claude=True)
        env["SWARM_AGENT_ID"] = "kid"
        os.makedirs(os.path.join(self.root, "agents"), exist_ok=True)
        with open(sw.agent_rec_path(self.root, "kid"), "w") as f:
            json.dump({"name": "kid", "parent": "operator", "pane": "pane-77"}, f)
        run_swarm(["event", "stop"], env, stdin_text="{}")
        calls = ""
        if os.path.exists(log):
            with open(log) as f:
                calls = f.read()
        self.assertNotIn("send-text", calls)


class TestRestoreCli(Base):
    def test_restore_injects_task_and_capped_tail(self):
        os.makedirs(os.path.join(self.root, "settings"), exist_ok=True)
        with open(os.path.join(self.root, "settings", "kid.task"), "w") as f:
            f.write("HEADER...\n--- YOUR TASK ---\nbuild the widget")
        jp = sw.journal_path(self.root, "kid")
        os.makedirs(os.path.dirname(jp), exist_ok=True)
        with open(jp, "w") as f:
            f.write("y" * 9000 + "LAST-ENTRY")
        p = run_swarm(["restore"],
                      {"SWARM_DIR": self.root, "SWARM_AGENT_ID": "kid"},
                      stdin_text=json.dumps({"source": "compact"}))
        ctx = json.loads(p.stdout)["hookSpecificOutput"]["additionalContext"]
        self.assertIn("build the widget", ctx)
        self.assertIn("CONTEXT COMPACTION", ctx)
        self.assertIn("LAST-ENTRY", ctx)
        self.assertIn("journal truncated to its last 4000", ctx)


class TestPsCli(Base):
    def test_ps_no_herdr_liveness_unknown(self):
        os.makedirs(os.path.join(self.root, "agents"), exist_ok=True)
        with open(sw.agent_rec_path(self.root, "boss"), "w") as f:
            json.dump({"name": "boss", "parent": "operator", "pane": "p1"}, f)
        self.q("operator", "boss", 1000, "for the human")
        p = run_swarm(["ps"], {"SWARM_DIR": self.root})
        self.assertEqual(p.returncode, 0, p.stderr)
        first = p.stdout.splitlines()[0]
        self.assertIn("1 message(s) waiting for the human", first)
        self.assertIn("boss [?]", p.stdout)
        self.assertIn("herdr unreachable", p.stdout)
        self.assertNotIn("DEAD", p.stdout)


class TestCloseCli(Base):
    def test_close_subtree_files_stay(self):
        env, log, _ = self.fake_tools(claude=True)
        os.makedirs(os.path.join(self.root, "agents"), exist_ok=True)
        for n, par, tab in (("a", "operator", "t-a"), ("b", "a", "t-b"),
                            ("z", "operator", "t-z")):
            with open(sw.agent_rec_path(self.root, n), "w") as f:
                json.dump({"name": n, "parent": par, "pane": f"p-{n}",
                           "tab": tab}, f)
            os.makedirs(os.path.dirname(sw.journal_path(self.root, n)),
                        exist_ok=True)
            with open(sw.journal_path(self.root, n), "w") as f:
                f.write("j")
        p = run_swarm(["close", "a"], env)
        self.assertEqual(p.returncode, 0, p.stderr)
        with open(log) as f:
            calls = f.read()
        self.assertIn("tab close t-a", calls)
        self.assertIn("tab close t-b", calls)
        self.assertNotIn("tab close t-z", calls)
        for n in ("a", "b", "z"):   # files stay — ALL of them
            self.assertTrue(os.path.exists(sw.journal_path(self.root, n)))
            self.assertTrue(os.path.exists(sw.agent_rec_path(self.root, n)))


class TestEdgesFoundReading(Base):
    def test_missing_ts_message_still_deliverable(self):
        d = sw.q_dir(self.root, "kid")
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "manual.json"), "w") as f:
            json.dump({"from": "human", "body": "hand-dropped"}, f)
        fn, rec, more = sw.select_next(self.root, "kid")
        self.assertEqual(rec["body"], "hand-dropped")


class TestSendMiddleware(Base):
    """The universal send middleware (HOOK-WIRING §13): when configured in
    .swarm/config, EVERY send runs it in the sender's process BEFORE the
    queue write, full envelope on stdin. The verdict is its EXIT CODE alone
    (stdout never parsed): 0 = PASS (queued); 100 = HANDLED (deliberate
    don't-pass, nothing queued); any other exit / timeout / killed / not
    configured fail OPEN (queued unchanged) — 100 sits above the shell's
    reserved and ordinary error codes, so a failure can never be misread as
    a deliberate HANDLED."""

    def _arm(self, script_body, extra=""):
        mw = os.path.join(self.bindir, "mwcmd")
        with open(mw, "w") as f:
            f.write("#!/usr/bin/env bash\n" + script_body + "\n")
        os.chmod(mw, 0o755)
        os.makedirs(self.root, exist_ok=True)
        with open(os.path.join(self.root, "config"), "w") as f:
            f.write(f'[middleware]\ncommand = "{mw}"\n{extra}')
        return mw

    def _kid(self):
        os.makedirs(os.path.join(self.root, "agents"), exist_ok=True)
        with open(sw.agent_rec_path(self.root, "kid"), "w") as f:
            json.dump({"name": "kid", "parent": "operator", "pane": "nope"}, f)

    def test_certainty_message_absent_during_middleware_present_after_pass(self):
        # THE admission-control property: while the middleware runs, the
        # message exists in no queue; after a PASS verdict it is queued.
        # Also pins the identity injection (config identity, default).
        witness = os.path.join(self.root, "witness")
        self._arm(f'c=$(ls "$SWARM_DIR/queue/operator" 2>/dev/null | wc -l); '
                  f'echo "count=$(echo $c) id=$SWARM_AGENT_ID" > {witness}; '
                  f'exit 0')
        p = run_swarm(["send", "operator", "--stdin"],
                      {"SWARM_DIR": self.root, "SWARM_AGENT_ID": "kid"},
                      stdin_text="for the human")
        self.assertEqual(p.returncode, 0, p.stderr)
        with open(witness) as f:
            self.assertEqual(f.read().strip(), "count=0 id=middleware",
                             "queue must be empty while the middleware runs, "
                             "and the default identity injected")
        w = sw.list_waiting(self.root, "operator")
        self.assertEqual([r["body"] for _, _, r in w], ["for the human"])
        self.assertEqual(w[0][2]["from"], "kid")

    def test_every_recipient_is_intercepted_not_just_operator(self):
        witness = os.path.join(self.root, "witness")
        self._arm(f"touch {witness}; exit 0")
        self._kid()
        p = run_swarm(["send", "kid", "--stdin"], {"SWARM_DIR": self.root},
                      stdin_text="agent-to-agent mail")
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertTrue(os.path.exists(witness),
                        "the middleware must run on non-operator sends too")
        self.assertEqual([r["body"] for _, _, r in
                          sw.list_waiting(self.root, "kid")],
                         ["agent-to-agent mail"])

    def test_exit_100_means_handled_nothing_queued(self):
        self._arm("echo 'handled it myself, logging noise'; exit 100")
        p = run_swarm(["send", "operator", "--stdin"],
                      {"SWARM_DIR": self.root, "SWARM_AGENT_ID": "kid"},
                      stdin_text="middleware takes this one")
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(sw.list_waiting(self.root, "operator"), [],
                         "exit 100 = HANDLED = deliberate don't-pass")

    def test_stdout_is_never_parsed(self):
        # exit code is the whole contract: noisy stdout with exit 0 still
        # passes the message through
        self._arm("echo HANDLED; echo garbage; exit 0")
        run_swarm(["send", "operator", "--stdin"],
                  {"SWARM_DIR": self.root, "SWARM_AGENT_ID": "kid"},
                  stdin_text="noisy pass")
        self.assertEqual([r["body"] for _, _, r in
                          sw.list_waiting(self.root, "operator")],
                         ["noisy pass"])

    def test_envelope_on_stdin_carries_from_to_ts_body(self):
        got = os.path.join(self.root, "got")
        self._arm(f"cat > {got}; exit 0")
        run_swarm(["send", "operator", "--stdin"],
                  {"SWARM_DIR": self.root, "SWARM_AGENT_ID": "kid"},
                  stdin_text="payload bytes")
        with open(got) as f:
            rec = json.load(f)
        self.assertEqual(rec["from"], "kid")
        self.assertEqual(rec["to"], "operator")
        self.assertEqual(rec["body"], "payload bytes")
        self.assertIsInstance(rec["ts"], int)

    def test_fail_open_not_configured(self):
        p = run_swarm(["send", "operator", "--stdin"],
                      {"SWARM_DIR": self.root, "SWARM_AGENT_ID": "kid"},
                      stdin_text="plain mail")
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual([r["body"] for _, _, r in
                          sw.list_waiting(self.root, "operator")],
                         ["plain mail"])

    def test_fail_open_timeout_bounds_the_send_and_queues(self):
        # the config's own timeout key bounds the invocation
        self._arm("sleep 30", extra="timeout = 1\n")
        t0 = time.time()
        p = run_swarm(["send", "operator", "--stdin"],
                      {"SWARM_DIR": self.root, "SWARM_AGENT_ID": "kid"},
                      stdin_text="middleware will time out")
        elapsed = time.time() - t0
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertLess(elapsed, 20, "send must return at ~T")
        self.assertEqual([r["body"] for _, _, r in
                          sw.list_waiting(self.root, "operator")],
                         ["middleware will time out"])

    def test_fail_open_nonzero_and_killed(self):
        self._arm("exit 3")              # ordinary error code: fail open
        run_swarm(["send", "operator", "--stdin"],
                  {"SWARM_DIR": self.root, "SWARM_AGENT_ID": "kid"},
                  stdin_text="middleware exits nonzero")
        self._arm("kill -9 $$")          # middleware killed mid-flight
        run_swarm(["send", "operator", "--stdin"],
                  {"SWARM_DIR": self.root, "SWARM_AGENT_ID": "kid"},
                  stdin_text="middleware is killed")
        self.assertEqual([r["body"] for _, _, r in
                          sw.list_waiting(self.root, "operator")],
                         ["middleware exits nonzero", "middleware is killed"])

    def test_recursion_guard_middlewares_own_sends_bypass(self):
        witness = os.path.join(self.root, "witness")
        self._arm(f"touch {witness}; exit 0")
        self._kid()
        run_swarm(["send", "kid", "--stdin"],
                  {"SWARM_DIR": self.root, "SWARM_AGENT_ID": "middleware"},
                  stdin_text="the middleware forwarding")
        self.assertFalse(os.path.exists(witness),
                         "the middleware's own sends must not be re-invoked")
        self.assertEqual([r["body"] for _, _, r in
                          sw.list_waiting(self.root, "kid")],
                         ["the middleware forwarding"])

    def test_sender_death_mid_middleware_nothing_queued_failure_observable(self):
        # Producer-side-interceptor semantics: kill the send while the
        # middleware runs — the message was never accepted (nothing queued),
        # and the sender observes a failed command (nonzero exit), not silence.
        started = os.path.join(self.root, "started")
        self._arm(f"touch {started}; sleep 5")
        env = {k: v for k, v in os.environ.items()
               if k not in ("SWARM_AGENT_ID", "SWARM_DIR", "HERDR_ENV")}
        env.update({"PATH": "/usr/bin:/bin", "SWARM_DIR": self.root,
                    "SWARM_AGENT_ID": "kid"})
        p = subprocess.Popen([sys.executable, SWARM, "send", "operator",
                              "--stdin"], stdin=subprocess.PIPE,
                             stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL, env=env)
        p.stdin.write(b"doomed send")
        p.stdin.close()
        for _ in range(100):
            if os.path.exists(started):
                break
            time.sleep(0.1)
        self.assertTrue(os.path.exists(started), "middleware never started")
        p.kill()
        rc = p.wait(timeout=30)
        self.assertNotEqual(rc, 0, "the sender must observe the failure")
        self.assertEqual(sw.list_waiting(self.root, "operator"), [],
                         "an unaccepted send must leave nothing queued")


if __name__ == "__main__":
    unittest.main(verbosity=2)
