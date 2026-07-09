"""Tests for simplest/swarm — every pure-file behavior.

Runnable as `python3 -m unittest test_swarm -v` or `python3 -m pytest test_swarm.py`.
Live-pane behaviors (doorbell, stop re-ring) are exempt per the brief; their
decision logic (select_next on a non-empty queue) is covered here.
"""
import importlib.machinery
import importlib.util
import json
import os
import shutil
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SWARM = os.path.join(HERE, "swarm")

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
        text = sw.build_delivery("f.json", rec, "your parent", 0, "kid")
        self.assertIn("from boss", text)
        self.assertIn("your parent", text)
        self.assertIn("do the thing", text)
        self.assertNotIn("more waiting", text)  # no trailer when queue is empty

    def test_queue_depth_trailer(self):
        rec = {"from": "boss", "ts": 1, "body": "b"}
        text = sw.build_delivery("f.json", rec, "your parent", 3, "kid")
        self.assertIn("3 more waiting", text)

    def test_oversized_on_disk_message_truncated_with_marker(self):
        rec = {"from": "x", "ts": 1, "body": "A" * 20000}
        text = sw.build_delivery("f.json", rec, "another agent", 0, "kid")
        self.assertLessEqual(len(text), sw.TURN_CAP)
        self.assertIn("[truncated", text)
        self.assertIn("queue/kid/delivered/f.json", text)


class TestSendSize(unittest.TestCase):
    def test_fitting_message_accepted(self):
        rec = {"from": "a", "ts": 1, "body": "hello"}
        self.assertIsNone(sw.send_size_error("f.json", rec, "your parent", "b"))

    def test_oversized_message_refused_with_file_hint(self):
        rec = {"from": "a", "ts": 1, "body": "A" * (sw.TURN_CAP + 1)}
        err = sw.send_size_error("f.json", rec, "your parent", "b")
        self.assertIsNotNone(err)
        self.assertIn("put it in a file, send the path", err)

    def test_boundary_headers_count_against_the_one_cap(self):
        # a body of exactly TURN_CAP chars cannot fit once headed
        rec = {"from": "a", "ts": 1, "body": "A" * sw.TURN_CAP}
        self.assertIsNotNone(sw.send_size_error("f.json", rec, "x", "b"))


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
        self.assertIn("dead [DEAD]", out)
        self.assertIn("idle 1m", out)                    # (1_000_000-940_000)ms
        self.assertIn('last: "shipped the report"', out)
        # the child is indented under its parent
        boss_i = out.index("boss [live]")
        kid_i = out.index("kid (you)")
        self.assertGreater(kid_i, boss_i)

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
        out = self.render(agents=agents,
                          queues={"boss": 0, "kid": 0, "dead": 0, "lost": 1},
                          events={"boss": None, "kid": None, "dead": None,
                                  "lost": None})
        self.assertIn("lost [parent vanished unknown]", out)


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
    """The stop re-ring's DECISION is pure: ring iff messages wait. The ring
    itself is a live-pane behavior, exempt per the brief."""

    def test_ring_iff_queue_non_empty(self):
        self.assertIsNone(sw.select_next(self.root, "a"))   # empty -> no ring
        msg(self.root, "a", "x", 1000, "hi")
        self.assertIsNotNone(sw.select_next(self.root, "a"))  # waiting -> ring


if __name__ == "__main__":
    unittest.main()
