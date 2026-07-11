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
           if k not in ("SWARM_AGENT_ID", "SWARM_DIR", "HERDR_ENV")}
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
        p = run_swarm(["spawn", "worker", "do the thing"], env, cwd=self.root)
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
        self.assertEqual(run_swarm(["spawn", "worker", "t"], env,
                                   cwd=self.root).returncode, 0)
        p = run_swarm(["spawn", "worker", "t2"], env, cwd=self.root)
        self.assertEqual(p.returncode, 1)
        self.assertIn("already used", p.stderr)

    def test_spawn_confirmed_failure_tears_down_but_keeps_tombstone(self):
        env, log, _ = self.fake_tools(claude=False)   # no claude anywhere on PATH
        p = run_swarm(["spawn", "worker", "t"], env, cwd=self.root)
        self.assertEqual(p.returncode, 1)
        self.assertIn("did not start", p.stderr)
        self.assertIn("claude not found", p.stderr)
        self.assertFalse(os.path.exists(sw.agent_rec_path(self.root, "worker")),
                         "binding must be removed on confirmed failure")
        self.assertTrue(os.path.exists(sw.journal_path(self.root, "worker")),
                        "tombstone must survive the failed spawn")
        with open(log) as f:
            self.assertIn("tab close tab-77", f.read())
        p2 = run_swarm(["spawn", "worker", "t2"], env, cwd=self.root)
        self.assertIn("already used", p2.stderr)   # name burned forever

    def test_spawn_outside_herdr_refused_before_tombstone(self):
        env = {"SWARM_DIR": self.root, "HERDR_ENV": "0"}
        p = run_swarm(["spawn", "worker", "t"], env, cwd=self.root)
        self.assertEqual(p.returncode, 1)
        self.assertIn("not inside herdr", p.stderr)
        self.assertFalse(os.path.exists(sw.journal_path(self.root, "worker")),
                         "refusal before claiming must not burn the name")

    def test_spawn_bad_names_refused(self):
        env, _, _ = self.fake_tools(claude=True)
        for bad in ("Worker", "has space", "-lead", "x" * 41, "operator",
                    "delivered"):
            p = run_swarm(["spawn", bad, "t"], env, cwd=self.root)
            self.assertEqual(p.returncode, 1, f"{bad!r} must be refused")


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


class TestEngineHookSendPath(Base):
    """HOOK-WIRING §3/§4: write-first durability (H-F1) and the fail-open
    branch (H-F2) — hook absent, timing out, or crashing leaves an
    operator-bound send byte-identical to a world with no hook."""

    def _arm(self, script_body):
        d = os.path.join(self.root, "engine")
        os.makedirs(d, exist_ok=True)
        hook = os.path.join(self.bindir, "hookcmd")
        with open(hook, "w") as f:
            f.write("#!/usr/bin/env bash\n" + script_body + "\n")
        os.chmod(hook, 0o755)
        with open(os.path.join(d, "hook"), "w") as f:
            f.write(f"decision-engine\n{hook}\n")
        return hook

    def test_hf1_message_durable_in_queue_before_hook_runs(self):
        witness = os.path.join(self.root, "witness")
        self._arm(f'[ -f "$SWARM_DIR/queue/operator/$1" ] && '
                  f'echo "present as $SWARM_AGENT_ID" > {witness}')
        p = run_swarm(["send", "operator", "--stdin"],
                      {"SWARM_DIR": self.root, "SWARM_AGENT_ID": "kid"},
                      stdin_text="for the human")
        self.assertEqual(p.returncode, 0, p.stderr)
        with open(witness) as f:
            self.assertEqual(f.read().strip(), "present as decision-engine",
                             "file must be durable, and identity injected, "
                             "before the hook sees it")
        self.assertEqual(len(sw.list_waiting(self.root, "operator")), 1)

    def test_hf2_no_marker_is_todays_send_exactly(self):
        p = run_swarm(["send", "operator", "--stdin"],
                      {"SWARM_DIR": self.root, "SWARM_AGENT_ID": "kid"},
                      stdin_text="plain mail")
        self.assertEqual(p.returncode, 0, p.stderr)
        w = sw.list_waiting(self.root, "operator")
        self.assertEqual([r["body"] for _, _, r in w], ["plain mail"])
        self.assertEqual(w[0][2]["from"], "kid")
        self.assertFalse(os.path.isdir(sw.delivered_dir(self.root, "operator")))

    def test_hf2_hook_timeout_leaves_message_and_bounds_the_send(self):
        self._arm("sleep 30")
        t0 = time.time()
        p = run_swarm(["send", "operator", "--stdin"],
                      {"SWARM_DIR": self.root, "SWARM_AGENT_ID": "kid",
                       "SWARM_ENGINE_HOOK_TIMEOUT": "1"},
                      stdin_text="hook will time out")
        elapsed = time.time() - t0
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertLess(elapsed, 20, "send must return at ~T, not the hook's leisure")
        w = sw.list_waiting(self.root, "operator")
        self.assertEqual([r["body"] for _, _, r in w], ["hook will time out"])
        self.assertFalse(os.path.isdir(sw.delivered_dir(self.root, "operator")))

    def test_hf2_hook_crash_leaves_message(self):
        self._arm("exit 1")
        p = run_swarm(["send", "operator", "--stdin"],
                      {"SWARM_DIR": self.root, "SWARM_AGENT_ID": "kid"},
                      stdin_text="hook will crash")
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(len(sw.list_waiting(self.root, "operator")), 1)
        self.assertFalse(os.path.isdir(sw.delivered_dir(self.root, "operator")))

    def test_hf4_guards_no_hook_off_the_operator_path(self):
        witness = os.path.join(self.root, "witness")
        self._arm(f"touch {witness}")
        os.makedirs(os.path.join(self.root, "agents"), exist_ok=True)
        with open(sw.agent_rec_path(self.root, "kid"), "w") as f:
            json.dump({"name": "kid", "parent": "operator", "pane": "nope"}, f)
        # a non-operator send must not invoke the hook...
        run_swarm(["send", "kid", "hello"], {"SWARM_DIR": self.root})
        self.assertFalse(os.path.exists(witness), "hook fired off the operator path")
        # ...and neither must the engine's own operator-bound send (recursion)
        run_swarm(["send", "operator", "--stdin"],
                  {"SWARM_DIR": self.root, "SWARM_AGENT_ID": "decision-engine"},
                  stdin_text="engine escalating")
        self.assertFalse(os.path.exists(witness), "hook fired on the engine's own send")
        self.assertEqual(len(sw.list_waiting(self.root, "operator")), 1)


class TestEngineHookVerb(Base):
    """HOOK-WIRING §7/§11 step 4: the engine-hook verb end to end through a
    real operator-bound send — identity injection (H-F3), pass-is-absence,
    and the H-F7 orphan grep."""

    GRANT = "GRANT: widget schedule questions -> answer 'weekly, Mondays'"

    def _fixture(self, claude_script):
        os.makedirs(os.path.join(self.root, "engine"), exist_ok=True)
        with open(os.path.join(self.root, "engine", "hook"), "w") as f:
            f.write(f"decision-engine\n{SWARM} engine-hook\n")
        jp = sw.journal_path(self.root, "operator")
        os.makedirs(os.path.dirname(jp), exist_ok=True)
        with open(jp, "w") as f:
            f.write(f"# operator ledger\n\n{self.GRANT}\n")
        os.makedirs(os.path.join(self.root, "agents"), exist_ok=True)
        with open(sw.agent_rec_path(self.root, "kid"), "w") as f:
            json.dump({"name": "kid", "parent": "operator", "pane": "nope"}, f)
        with open(os.path.join(self.bindir, "claude"), "w") as f:
            f.write("#!/usr/bin/env bash\n" + claude_script + "\n")
        os.chmod(os.path.join(self.bindir, "claude"), 0o755)
        return {"SWARM_DIR": self.root, "SWARM_AGENT_ID": "kid",
                "PATH": self.bindir + ":/usr/bin:/bin"}

    def _send(self, env, body="when do widget tests run?"):
        return run_swarm(["send", "operator", "--stdin"], env, stdin_text=body)

    def test_hf3_answered_file_claimed_and_reply_is_from_engine(self):
        env = self._fixture(
            "printf 'ANSWER\\nGRANT: widget schedule questions -> answer "
            "'\\''weekly, Mondays'\\''\\nAll clear: weekly, on Mondays.\\n'")
        p = self._send(env)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(sw.list_waiting(self.root, "operator"), [])
        delivered = os.listdir(sw.delivered_dir(self.root, "operator"))
        self.assertEqual(len(delivered), 1)
        with open(sw.journal_path(self.root, "operator")) as f:
            ledger = f.read()
        self.assertIn(f"[hand:decision-engine] CLAIM {delivered[0]}", ledger)
        self.assertIn("weekly, Mondays", ledger)   # the claim line quotes the grant
        w = sw.list_waiting(self.root, "kid")
        self.assertEqual(len(w), 1)
        self.assertEqual(w[0][2]["from"], "decision-engine",
                         "the reply must be from the engine's wire name — "
                         "never OPERATOR, never the asker (H-F3)")
        self.assertIn("AUTO-ANSWER", w[0][2]["body"])
        self.assertIn("the human has NOT read", w[0][2]["body"])

    def test_hf3_pass_is_absence_message_waits_under_true_sender(self):
        env = self._fixture("printf 'PASS\\n'")
        p = self._send(env)
        self.assertEqual(p.returncode, 0, p.stderr)
        w = sw.list_waiting(self.root, "operator")
        self.assertEqual(len(w), 1)
        self.assertEqual(w[0][2]["from"], "kid",
                         "a passed message keeps its true sender (H-F3a)")
        self.assertEqual(sw.list_waiting(self.root, "kid"), [])
        with open(sw.journal_path(self.root, "operator")) as f:
            self.assertNotIn("CLAIM", f.read())

    def test_invented_grant_is_a_pass(self):
        env = self._fixture(
            "printf 'ANSWER\\nGRANT: authority I invented just now\\nsure!\\n'")
        self._send(env)
        self.assertEqual(len(sw.list_waiting(self.root, "operator")), 1)
        self.assertEqual(sw.list_waiting(self.root, "kid"), [])

    def test_no_grants_passes_without_calling_the_model(self):
        witness = os.path.join(self.root, "model-called")
        env = self._fixture(f"touch {witness}; printf 'ANSWER\\noops\\n'")
        with open(sw.journal_path(self.root, "operator"), "w") as f:
            f.write("# operator ledger with no grants\n")
        self._send(env)
        self.assertFalse(os.path.exists(witness),
                         "no grants must mean no model call at all")
        self.assertEqual(len(sw.list_waiting(self.root, "operator")), 1)

    def test_hf7_orphan_in_delivered_is_greppable(self):
        # the redcheck-2 residual: a hook SIGKILLed between its mv and its
        # claim line leaves delivered/<fn> with no ledger line. The collector
        # is a grep of delivered/ filenames against claim lines — prove the
        # orphan surfaces and a proper claim does not.
        env = self._fixture(
            "printf 'ANSWER\\nGRANT: widget schedule questions -> answer "
            "'\\''weekly, Mondays'\\''\\nAll clear.\\n'")
        self._send(env)                       # a properly claimed file
        d = sw.delivered_dir(self.root, "operator")
        with open(os.path.join(d, "999-ghost.json"), "w") as f:
            json.dump({"to": "operator", "from": "ghost", "ts": 999,
                       "body": "claimed then killed"}, f)   # the orphan
        with open(sw.journal_path(self.root, "operator")) as f:
            ledger = f.read()
        orphans = [fn for fn in sorted(os.listdir(d))
                   if f"CLAIM {fn}" not in ledger]
        self.assertEqual(orphans, ["999-ghost.json"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
