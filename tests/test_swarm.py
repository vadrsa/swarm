"""Tests for bin/swarm — every pure-file behavior.

Runnable as `python3 -m unittest test_swarm -v` or `python3 -m pytest test_swarm.py`.
Live-pane behaviors (doorbell, stop re-ring) are exempt per the brief; their
decision logic (select_next on a non-empty queue) is covered here.
"""
import importlib.machinery
import importlib.util
import json
import os
import shutil
import subprocess
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SWARM = os.path.join(os.path.dirname(HERE), "bin", "swarm")

loader = importlib.machinery.SourceFileLoader("swarmmod", SWARM)
spec = importlib.util.spec_from_loader("swarmmod", loader)
sw = importlib.util.module_from_spec(spec)
loader.exec_module(sw)


def msg(root, to, frm, ts, body):
    d = sw.q_dir(root, to)
    os.makedirs(d, exist_ok=True)
    fn = f"{ts}-{frm}.json"
    with open(os.path.join(d, fn), "w") as f:
        json.dump({"to": to, "from": frm, "ts": ts, "body": body}, f)
    return fn


class Base(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="swarm-test-")

    def tearDown(self):
        shutil.rmtree(self.root, ignore_errors=True)


class TestSelection(Base):
    def test_oldest_first(self):
        msg(self.root, "a", "x", 3000, "third")
        msg(self.root, "a", "y", 1000, "first")
        msg(self.root, "a", "z", 2000, "second")
        fn, rec, more = sw.select_next(self.root, "a")
        self.assertEqual(rec["body"], "first")
        self.assertEqual(more, 2)

    def test_ts_tie_breaks_on_filename(self):
        msg(self.root, "a", "bbb", 1000, "from bbb")
        msg(self.root, "a", "aaa", 1000, "from aaa")
        fn, rec, _ = sw.select_next(self.root, "a")
        self.assertEqual(rec["from"], "aaa")

    def test_empty_queue(self):
        self.assertIsNone(sw.select_next(self.root, "a"))

    def test_delivered_dir_and_junk_ignored(self):
        os.makedirs(sw.delivered_dir(self.root, "a"), exist_ok=True)
        msg(self.root, "a", "x", 5000, "old-but-delivered")
        # move it into delivered/, leaving one real waiting message
        os.replace(os.path.join(sw.q_dir(self.root, "a"), "5000-x.json"),
                   os.path.join(sw.delivered_dir(self.root, "a"), "5000-x.json"))
        with open(os.path.join(sw.q_dir(self.root, "a"), "notes.txt"), "w") as f:
            f.write("not a message")
        msg(self.root, "a", "y", 9000, "real")
        fn, rec, more = sw.select_next(self.root, "a")
        self.assertEqual(rec["body"], "real")
        self.assertEqual(more, 0)


class TestDeliverOnce(Base):
    """One message per turn; the delivered/ move happens ONLY after the emit
    reports the bytes drained (the G17 discipline)."""

    def test_exactly_one_per_turn_oldest_first(self):
        msg(self.root, "a", "p", 1000, "one")
        msg(self.root, "a", "p", 2000, "two")
        seen = []
        emit = lambda o: (seen.append(o), True)[1]
        self.assertTrue(sw.deliver_once(self.root, "a", {}, emit))
        self.assertEqual(len(seen), 1)
        ctx = seen[0]["hookSpecificOutput"]["additionalContext"]
        self.assertIn("one", ctx)
        self.assertNotIn("two", ctx)
        waiting = sw.list_waiting(self.root, "a")
        self.assertEqual([r["body"] for _, _, r in waiting], ["two"])
        delivered = os.listdir(sw.delivered_dir(self.root, "a"))
        self.assertEqual(delivered, ["1000-p.json"])

    def test_failed_drain_leaves_message_in_queue(self):
        fn = msg(self.root, "a", "p", 1000, "precious")
        self.assertFalse(sw.deliver_once(self.root, "a", {}, lambda o: False))
        self.assertTrue(os.path.exists(os.path.join(sw.q_dir(self.root, "a"), fn)))
        self.assertFalse(os.path.isdir(sw.delivered_dir(self.root, "a")))
        # next turn it is offered whole again
        got = []
        self.assertTrue(sw.deliver_once(self.root, "a", {},
                                        lambda o: (got.append(o), True)[1]))
        self.assertIn("precious",
                      got[0]["hookSpecificOutput"]["additionalContext"])

    def test_empty_queue_emits_nothing(self):
        self.assertFalse(sw.deliver_once(self.root, "a", {},
                                         lambda o: self.fail("must not emit")))


class TestRulingRegressions(Base):
    """Regressions for the review's findings, one per ruling."""

    def test_no_queue_depth_trailer_ever(self):
        # finding 1 (ruling R1): the trailer is deleted — a delivery with a
        # deep backlog carries head + body and nothing else
        for i in range(5):
            msg(self.root, "a", "p", 1000 + i, f"m{i}")
        got = []
        sw.deliver_once(self.root, "a", {}, lambda o: (got.append(o), True)[1])
        ctx = got[0]["hookSpecificOutput"]["additionalContext"]
        self.assertNotIn("more waiting", ctx)
        self.assertTrue(ctx.endswith("m0"))  # nothing after the body

    def test_boundary_size_message_delivered_whole_at_depth_150(self):
        # finding 2 (ruling R1 moots it; this proves the moot): a message that
        # send accepts at the exact cap boundary is delivered WHOLE even with
        # 150 messages queued behind it
        rec = {"to": "a", "from": "boss", "ts": 1000, "body": ""}
        head = sw.delivery_head(rec, sw.relation("boss", "a", {"a": "boss"}))
        rec["body"] = "B" * (sw.TURN_CAP - len(head))
        self.assertIsNone(sw.send_size_error(rec, "your parent"))  # accepted
        d = sw.q_dir(self.root, "a")
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "1000-boss.json"), "w") as f:
            json.dump(rec, f)
        for i in range(150):
            msg(self.root, "a", "p", 2000 + i, f"filler {i}")
        got = []
        sw.deliver_once(self.root, "a", {"a": "boss"},
                        lambda o: (got.append(o), True)[1])
        ctx = got[0]["hookSpecificOutput"]["additionalContext"]
        self.assertEqual(len(ctx), sw.TURN_CAP)
        self.assertNotIn("[truncated", ctx)
        self.assertTrue(ctx.endswith("B"))  # the whole body, to its last char

    def test_undeliverable_file_stays_queued_and_emits_nothing(self):
        # finding 3 (ruling R2): a hand-crafted record whose head alone blows
        # the cap is NOT delivered, NOT moved, and NOT emitted as bare header —
        # never delivered is honest; delivered-without-its-body is a lie
        d = sw.q_dir(self.root, "a")
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "1000-evil.json"), "w") as f:
            json.dump({"to": "a", "from": "F" * 9000, "ts": 1000,
                       "body": "the body"}, f)
        self.assertFalse(sw.deliver_once(self.root, "a", {},
                                         lambda o: self.fail("must not emit")))
        self.assertTrue(os.path.exists(os.path.join(d, "1000-evil.json")))
        self.assertFalse(os.path.isdir(sw.delivered_dir(self.root, "a")))
        # and it is not invisible: it counts as a waiting message
        self.assertEqual(len(sw.list_waiting(self.root, "a")), 1)

    def test_deliver_exits_zero_on_broken_stdout(self):
        # finding 6 (ruling R3): a real `swarm deliver` process whose stdout
        # reader is gone must still exit 0 — and the message must stay queued
        fn = msg(self.root, "kid", "boss", 1000, "precious")
        env = dict(os.environ, SWARM_DIR=self.root, SWARM_AGENT_ID="kid")
        p = subprocess.Popen([SWARM, "deliver"], env=env,
                             stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                             stderr=subprocess.DEVNULL)
        p.stdout.close()          # reader gone before the child can emit
        p.stdin.write(b"{}")
        p.stdin.close()
        rc = p.wait(timeout=30)
        self.assertEqual(rc, 0)
        self.assertTrue(os.path.exists(os.path.join(sw.q_dir(self.root, "kid"),
                                                    fn)))

    def test_corrupt_queue_file_counted_not_hidden(self):
        # finding 8 (ruling R4): an unparseable queue file shows up in the
        # count `ps` renders, as its own honest-unknown suffix
        msg(self.root, "a", "p", 1000, "good")
        with open(os.path.join(sw.q_dir(self.root, "a"), "9999-x.json"), "w") as f:
            f.write("{not json")
        self.assertEqual(sw.count_junk(self.root, "a"), 1)
        self.assertEqual(len(sw.list_waiting(self.root, "a")), 1)  # still skipped
        out = sw.render_ps({"a": {"name": "a", "parent": "operator",
                                  "pane": "p1"}}, {"p1"}, {"a": 1}, {"a": None},
                           "operator", [], 1000, junk={"a": 1})
        self.assertIn("q=1+1?", out)


class TestHeaderAndRelation(unittest.TestCase):
    PARENTS = {"kid": "boss", "boss": "operator", "sib": "boss",
               "other": "elsewhere"}

    def test_relations(self):
        self.assertEqual(sw.relation("operator", "kid", self.PARENTS),
                         "the OPERATOR (the human at the root)")
        self.assertEqual(sw.relation("boss", "kid", self.PARENTS), "your parent")
        self.assertEqual(sw.relation("kid", "boss", self.PARENTS), "your child")
        self.assertEqual(sw.relation("sib", "kid", self.PARENTS), "your sibling")
        self.assertEqual(sw.relation("other", "kid", self.PARENTS), "another agent")

    def test_operator_recipient_sees_children(self):
        # an agent rooted at the operator is the operator's child
        self.assertEqual(sw.relation("boss", "operator", self.PARENTS),
                         "your child")

    def test_header_names_sender_relation_and_body_whole(self):
        rec = {"from": "boss", "ts": 1750000000000, "body": "do the thing"}
        text = sw.build_delivery("f.json", rec, "your parent", "kid")
        self.assertIn("from boss", text)
        self.assertIn("your parent", text)
        self.assertIn("do the thing", text)

    def test_oversized_on_disk_message_truncated_with_marker(self):
        rec = {"from": "x", "ts": 1, "body": "A" * 20000}
        text = sw.build_delivery("f.json", rec, "another agent", "kid")
        self.assertLessEqual(len(text), sw.TURN_CAP)
        self.assertIn("[truncated", text)
        self.assertIn("queue/kid/delivered/f.json", text)

    def test_undeliverable_returns_none_never_bare_header(self):
        # regression, review finding 3 (ruling R2): a record whose head alone
        # exceeds the cap must yield NO delivery text at all
        rec = {"from": "F" * 9000, "ts": 1, "body": "the body"}
        self.assertIsNone(sw.build_delivery("f.json", rec, "another agent",
                                            "kid"))


class TestSendSize(unittest.TestCase):
    def test_fitting_message_accepted(self):
        rec = {"from": "a", "ts": 1, "body": "hello"}
        self.assertIsNone(sw.send_size_error(rec, "your parent"))

    def test_oversized_message_refused_with_file_hint(self):
        rec = {"from": "a", "ts": 1, "body": "A" * (sw.TURN_CAP + 1)}
        err = sw.send_size_error(rec, "your parent")
        self.assertIsNotNone(err)
        self.assertIn("put it in a file, send the path", err)

    def test_boundary_headers_count_against_the_one_cap(self):
        # a body of exactly TURN_CAP chars cannot fit once headed
        rec = {"from": "a", "ts": 1, "body": "A" * sw.TURN_CAP}
        self.assertIsNotNone(sw.send_size_error(rec, "x"))


class TestTombstone(Base):
    def test_claim_then_collision(self):
        fd = sw.claim_name(self.root, "worker")
        os.close(fd)
        with self.assertRaises(FileExistsError):
            sw.claim_name(self.root, "worker")

    def test_tombstone_outlives_everything_else(self):
        # only the journal file matters: no agents record, no queue — still taken
        fd = sw.claim_name(self.root, "ghost")
        os.close(fd)
        self.assertFalse(os.path.exists(sw.agent_rec_path(self.root, "ghost")))
        with self.assertRaises(FileExistsError):
            sw.claim_name(self.root, "ghost")


class TestJournalTail(Base):
    def test_short_journal_returned_verbatim(self):
        p = sw.journal_path(self.root, "a")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w") as f:
            f.write("short journal")
        self.assertEqual(sw.journal_tail(p), "short journal")

    def test_long_journal_capped_with_marker(self):
        p = sw.journal_path(self.root, "a")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        body = "x" * 10000 + "THE-END"
        with open(p, "w") as f:
            f.write(body)
        tail = sw.journal_tail(p)
        self.assertTrue(tail.startswith("[…journal truncated"))
        self.assertIn(p, tail)                    # marker points at the full file
        self.assertTrue(tail.endswith("THE-END"))  # it is the TAIL, not the head
        marker, _, kept = tail.partition("\n")
        self.assertEqual(len(kept), sw.JOURNAL_TAIL_CAP)

    def test_missing_journal_is_empty(self):
        self.assertEqual(sw.journal_tail(sw.journal_path(self.root, "nope")), "")


class TestRestore(Base):
    def test_payload_has_task_and_tail(self):
        p = sw.journal_path(self.root, "a")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w") as f:
            f.write("## entry\nworked on X")
        out = sw.build_restore("build the widget", p, "startup")
        self.assertIn("ORIGINAL TASK", out)
        self.assertIn("build the widget", out)
        self.assertIn("worked on X", out)
        self.assertIn("fresh session", out)

    def test_compaction_is_named(self):
        out = sw.build_restore("t", sw.journal_path(self.root, "a"), "compact")
        self.assertIn("CONTEXT COMPACTION", out)
        self.assertIn("(journal is empty)", out)


class TestEventFact(Base):
    def test_one_file_overwritten_no_history(self):
        sw.record_event(self.root, "a", "stop", "first words", 1000)
        sw.record_event(self.root, "a", "notification", "later words", 2000)
        d = os.path.join(self.root, "event")
        self.assertEqual(os.listdir(d), ["a.json"])
        with open(sw.event_path(self.root, "a")) as f:
            fact = json.load(f)
        self.assertEqual(fact, {"event": "notification", "ts": 2000,
                                "last_words": "later words"})

    def test_last_words_capped(self):
        sw.record_event(self.root, "a", "stop", "w" * 9000, 1)
        with open(sw.event_path(self.root, "a")) as f:
            fact = json.load(f)
        self.assertEqual(len(fact["last_words"]), sw.LAST_WORDS_CAP)


class TestPs(unittest.TestCase):
    AGENTS = {
        "boss": {"name": "boss", "parent": "operator", "pane": "p1"},
        "kid": {"name": "kid", "parent": "boss", "pane": "p2"},
        "dead": {"name": "dead", "parent": "operator", "pane": "p9"},
    }

    def render(self, **kw):
        args = dict(agents=self.AGENTS, live={"p1", "p2"},
                    queues={"boss": 0, "kid": 2, "dead": 0},
                    events={"boss": {"event": "stop", "ts": 940_000,
                                     "last_words": "shipped the report"},
                            "kid": None, "dead": None},
                    me_name="kid", op_mail=[("boss", 400_000)], now=1_000_000)
        args.update(kw)
        return sw.render_ps(**args)

    def test_tree_liveness_queue_idle_lastwords_you(self):
        out = self.render()
        self.assertIn("boss [live]", out)
        self.assertIn("kid (you) [live] q=2", out)
        self.assertIn("idle 1m", out)                    # (1_000_000-940_000)ms
        self.assertIn('last: "shipped the report"', out)
        # the child is indented under its parent
        boss_i = out.index("boss [live]")
        kid_i = out.index("kid (you)")
        self.assertGreater(kid_i, boss_i)

    def test_dead_agents_render_compactly(self):
        # ruling R5: dead agents are names on ONE shared line — no tree entry,
        # no task, no last words
        out = self.render(events={"boss": None, "kid": None,
                                  "dead": {"event": "stop", "ts": 1,
                                           "last_words": "dying words"}})
        self.assertIn("dead: dead", out)
        self.assertNotIn("dying words", out)
        self.assertNotIn("dead [", out)  # not rendered as a tree node

    def test_live_child_of_dead_parent_reattaches(self):
        # hiding the dead never orphans the living: kid climbs to the nearest
        # living ancestor when boss's pane is gone
        out = self.render(live={"p2"})   # only kid's pane is alive
        self.assertIn("dead: boss, dead", out)
        self.assertIn("└─ kid (you)", out)   # at root depth, under operator

    def test_operator_mail_on_top(self):
        out = self.render()
        self.assertTrue(out.splitlines()[0].startswith(
            "operator — 1 message(s) waiting"))
        self.assertIn("from boss, 10m ago", out)

    def test_no_mail_no_agents(self):
        out = sw.render_ps({}, set(), {}, {}, "operator", [], 1000)
        self.assertIn("operator — no waiting mail", out)
        self.assertIn("(no agents)", out)

    def test_herdr_unreachable_is_unknown_not_dead(self):
        out = self.render(live=None)
        self.assertIn("boss [?]", out)
        self.assertNotIn("[DEAD]", out)

    def test_orphan_still_rendered(self):
        agents = dict(self.AGENTS)
        agents["lost"] = {"name": "lost", "parent": "vanished", "pane": "p5"}
        out = self.render(agents=agents, live={"p1", "p2", "p5"},
                          queues={"boss": 0, "kid": 0, "dead": 0, "lost": 1},
                          events={"boss": None, "kid": None, "dead": None,
                                  "lost": None})
        self.assertIn("lost [parent vanished unknown]", out)


class TestWorldResolution(Base):
    def test_world_via_symlink_from_foreign_cwd(self):
        # the install model: ~/.local/bin/swarm is a symlink into the checkout;
        # `swarm world` must find WORLD.md at the repo root regardless of cwd
        link = os.path.join(self.root, "swarm")
        os.symlink(SWARM, link)
        foreign = os.path.join(self.root, "elsewhere")
        os.makedirs(foreign)
        p = subprocess.run([link, "world"], cwd=foreign,
                           capture_output=True, text=True, timeout=30)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertIn("THE WORLD", p.stdout)
        self.assertIn("four verbs", p.stdout)


class TestSubtree(unittest.TestCase):
    def test_close_targets_whole_subtree(self):
        agents = {
            "a": {"name": "a", "parent": "operator"},
            "b": {"name": "b", "parent": "a"},
            "c": {"name": "c", "parent": "b"},
            "z": {"name": "z", "parent": "operator"},
        }
        self.assertEqual(sorted(sw.subtree(agents, "a")), ["a", "b", "c"])
        self.assertEqual(sw.subtree(agents, "z"), ["z"])


class TestReRingDecision(Base):
    """The stop re-ring's DECISION is pure and shared with delivery: ring iff
    the queue HEAD is deliverable (ruling R7) — never for a head that
    build_delivery refuses, which would self-ring forever. The ring itself is
    a live-pane behavior, exempt per the brief."""

    def test_ring_iff_head_deliverable(self):
        self.assertIsNone(sw.next_delivery(self.root, "a", {}))  # empty -> no ring
        msg(self.root, "a", "x", 1000, "hi")
        nd = sw.next_delivery(self.root, "a", {})
        self.assertIsNotNone(nd[1])                              # deliverable -> ring

    def test_no_ring_for_undeliverable_head(self):
        d = sw.q_dir(self.root, "a")
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "1000-evil.json"), "w") as f:
            json.dump({"to": "a", "from": "F" * 9000, "ts": 1000, "body": "x"}, f)
        msg(self.root, "a", "p", 2000, "stuck behind the head")
        nd = sw.next_delivery(self.root, "a", {})
        self.assertIsNotNone(nd)          # queue is non-empty...
        self.assertIsNone(nd[1])          # ...but the head must not ring

    def test_stop_event_rings_iff_head_deliverable_process_level(self):
        # regression for ruling R7, end to end: a real `swarm event stop`
        # against a fake herdr that logs its argv. Undeliverable head + queued
        # mail behind it -> ZERO send-text; deliverable head -> exactly one.
        bindir = os.path.join(self.root, "fakebin")
        os.makedirs(bindir)
        log = os.path.join(self.root, "herdr.log")
        with open(os.path.join(bindir, "herdr"), "w") as f:
            f.write('#!/usr/bin/env bash\necho "$@" >> "%s"\necho "{}"\n' % log)
        os.chmod(os.path.join(bindir, "herdr"), 0o755)
        os.makedirs(os.path.join(self.root, "agents"))
        with open(sw.agent_rec_path(self.root, "kid"), "w") as f:
            json.dump({"name": "kid", "parent": "operator", "pane": "p1"}, f)
        env = dict(os.environ, SWARM_DIR=self.root, SWARM_AGENT_ID="kid",
                   PATH=bindir + os.pathsep + os.environ.get("PATH", ""))

        def stop():
            subprocess.run([SWARM, "event", "stop"], env=env, input=b"{}",
                           capture_output=True, timeout=60)

        def sent_texts():
            try:
                with open(log) as f:
                    return [l for l in f if l.startswith("pane send-text")]
            except OSError:
                return []

        d = sw.q_dir(self.root, "kid")
        os.makedirs(d, exist_ok=True)
        evil = os.path.join(d, "1000-evil.json")
        with open(evil, "w") as f:
            json.dump({"to": "kid", "from": "F" * 9000, "ts": 1000,
                       "body": "x"}, f)
        msg(self.root, "kid", "boss", 2000, "waiting behind")
        stop()
        self.assertEqual(sent_texts(), [])   # undeliverable head: no ring
        os.unlink(evil)                      # now the head is the real message
        stop()
        self.assertEqual(len(sent_texts()), 1)  # deliverable head: one ring


class TestNameEdges(Base):
    """Regression: NAME_RE anchored with $ let 'abc\\n' pass (Python's $
    matches before a trailing newline), claiming journal/'abc\\n'.md — a
    DISTINCT tombstone that renders identically to abc's. \\Z closes it."""

    def test_trailing_newline_names_fail_the_regex(self):
        import re
        for bad in ("abc\n", "abc-\n"):
            self.assertIsNone(re.match(sw.NAME_RE, bad),
                              f"{bad!r} must not validate")
        self.assertIsNotNone(re.match(sw.NAME_RE, "abc"))

    def test_spawn_refuses_trailing_newline_name_before_tombstone(self):
        # a real `swarm spawn` process: the refusal must land BEFORE the name
        # is claimed, so no journal/'abc\n'.md tombstone ever exists
        env = dict(os.environ, SWARM_DIR=self.root, HERDR_ENV="1")
        p = subprocess.run([SWARM, "spawn", "abc\n", "task"], env=env,
                           capture_output=True, text=True, timeout=30)
        self.assertEqual(p.returncode, 1)
        self.assertIn("bad name", p.stderr)
        self.assertFalse(os.path.isdir(os.path.join(self.root, "journal")),
                         "refused name must not claim a tombstone")


class TestQueuePut(Base):
    """Regression: cmd_send named the queue file {ts}-{sender}.json and wrote
    it via tmp+rename, so a same-millisecond same-sender same-recipient
    collision silently replaced the first message — the drop WORLD.md
    forbids. queue_put claims the name with O_EXCL and bumps ts until free."""

    def test_same_ms_collision_keeps_both_messages_in_order(self):
        fn1 = sw.queue_put(self.root, {"to": "a", "from": "p", "ts": 1000,
                                       "body": "first"})
        fn2 = sw.queue_put(self.root, {"to": "a", "from": "p", "ts": 1000,
                                       "body": "second"})
        self.assertNotEqual(fn1, fn2)
        d = sw.q_dir(self.root, "a")
        self.assertTrue(os.path.exists(os.path.join(d, fn1)))
        self.assertTrue(os.path.exists(os.path.join(d, fn2)))
        # oldest-first order preserved: the first send stays the queue head
        w = sw.list_waiting(self.root, "a")
        self.assertEqual([r["body"] for _, _, r in w], ["first", "second"])

    def test_bump_lands_on_the_next_free_millisecond(self):
        for i in range(3):
            msg(self.root, "a", "p", 1000 + i, f"pre {i}")
        fn = sw.queue_put(self.root, {"to": "a", "from": "p", "ts": 1000,
                                      "body": "late"})
        self.assertEqual(fn, "1003-p.json")
        w = sw.list_waiting(self.root, "a")
        self.assertEqual([r["body"] for _, _, r in w],
                         ["pre 0", "pre 1", "pre 2", "late"])

    def test_exhausted_bump_space_raises_never_overwrites(self):
        for i in range(1000):
            msg(self.root, "a", "p", 1000 + i, f"pre {i}")
        with self.assertRaises(FileExistsError):
            sw.queue_put(self.root, {"to": "a", "from": "p", "ts": 1000,
                                     "body": "one too many"})
        self.assertEqual(len(sw.list_waiting(self.root, "a")), 1000)


if __name__ == "__main__":
    unittest.main()
