"""Tests for bin/swarm — every pure-file behavior.

Runnable as `python3 -m unittest test_swarm -v` or `python3 -m pytest test_swarm.py`.
Live-pane behaviors (doorbell, stop re-ring) are exempt per the brief; their
decision logic (select_next on a non-empty queue) is covered here.
"""
import importlib.machinery
import importlib.util
import json
import os
import shlex
import shutil
import subprocess
import tempfile
import time
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

    def test_pinned_model_shows_unpinned_shows_nothing(self):
        # A non-empty model means the agent was PINNED with --model at spawn.
        # An empty one means it was NOT pinned — the record says nothing about
        # which model is actually running (no --model execs bare `claude`, and
        # nothing propagates from the spawner), so ps says nothing: no marker,
        # no "(default)". (model) sits beside (you), not with the [system]
        # facts. One tree, all four cases.
        agents = {
            "boss":   {"name": "boss", "parent": "operator", "pane": "p1",
                       "model": "opus"},          # pinned, live
            "kid":    {"name": "kid", "parent": "boss", "pane": "p2",
                       "model": ""},              # not pinned, live
            "gone":   {"name": "gone", "parent": "operator", "pane": "p9",
                       "model": "haiku"},         # pinned, DEAD (ruling R5)
            "lost":   {"name": "lost", "parent": "vanished", "pane": "p5",
                       "model": "sonnet"},        # pinned, orphan
        }
        out = self.render(agents=agents, live={"p1", "p2", "p5"},
                          queues={"boss": 0, "kid": 2, "gone": 0, "lost": 1},
                          events={"boss": None, "kid": None, "gone": None,
                                  "lost": None})
        # a pinned agent carries its model in a slot of its OWN
        self.assertIn("boss model=opus [live] q=0", out)
        # an unpinned line is byte-identical to a swarm with no models at all
        self.assertIn("kid (you) [live] q=2", out)
        # R5 guard: a dead pinned agent is a NAME on the shared dead line only
        self.assertIn("dead: gone", out)
        self.assertNotIn("haiku", out)
        # the orphan line carries the model too
        self.assertIn("lost model=sonnet [parent vanished unknown] [live] q=1",
                      out)

    def test_you_and_pinned_together(self):
        # both facts on one agent, and they cannot be confused for each other
        agents = {"kid": {"name": "kid", "parent": "operator", "pane": "p2",
                          "model": "opus"}}
        out = self.render(agents=agents, live={"p2"}, queues={"kid": 0},
                          events={"kid": None})
        self.assertIn("kid (you) model=opus [live] q=0", out)

    def test_missing_model_key_renders_unpinned(self):
        # field records predate the key; absent must behave as not-pinned
        out = self.render()   # AGENTS fixture has no "model" key at all
        self.assertIn("boss [live] q=0", out)
        self.assertNotIn("model=", out)

    def test_pin_cannot_forge_the_you_marker(self):
        # THE KILL this slot exists to prevent. In a swarm ANY agent can run
        # `swarm spawn --model <anything>`, so the pin is ATTACKER-controlled.
        # Rendered as `(opus)` it shared syntax with `(you)` — the marker that
        # answers "which of these is ME?" — and `--model you` produced a line
        # BYTE-IDENTICAL to the real reader's. No sanitizer fixes that: 'you' is
        # CLEAN input. The fix is to leave the namespace, so the forge defeats
        # itself: a reader sees `model=you`, self-evidently a MODEL claim.
        agents = {
            "bait": {"name": "bait", "parent": "operator", "pane": "p1",
                     "model": "you"},
            "me":   {"name": "me", "parent": "operator", "pane": "p2",
                     "model": ""},
        }
        out = self.render(agents=agents, live={"p1", "p2"},
                          queues={"bait": 0, "me": 0},
                          events={"bait": None, "me": None}, me_name="me",
                          op_mail=[])
        # exactly ONE line may claim to be the reader, and it is the real one
        self.assertEqual(sum("(you)" in ln for ln in out.splitlines()), 1)
        self.assertIn("me (you) [live]", out)
        # the bait's pin renders, but as a model claim that forges nothing
        self.assertIn("bait model=you [live]", out)
        self.assertNotIn("bait (you)", out)

    def test_pin_cannot_escape_into_a_fake_marker(self):
        # 'opus) (you' closed our paren and opened a fake one, yielding a
        # WELL-FORMED line that lied. The structural characters are excluded, so
        # the payload cannot reach for a delimiter it no longer has.
        agents = {"victim": {"name": "victim", "parent": "operator",
                             "pane": "p1", "model": "opus) (you"}}
        out = self.render(agents=agents, live={"p1"}, queues={"victim": 0},
                          events={"victim": None}, me_name="operator",
                          op_mail=[])
        self.assertNotIn("(you)", out)          # no identity claim anywhere
        self.assertNotIn("(", out)              # the parens never survive
        self.assertNotIn(")", out)
        self.assertIn("victim model=opusyou [live]", out)

    def test_every_real_model_id_survives_whole(self):
        # REGRESSION GUARD against a whitelist. Excluding only the STRUCTURAL
        # characters keeps every real id intact. A tempting [A-Za-z0-9._-]
        # whitelist silently mangles 'claude-opus-4-8[1m]' -> 'claude-opus-4-81m'
        # and the Bedrock 'us.anthropic...-v1:0' -> '...-v10' — turning 'v1:0'
        # into 'v10' is EXACTLY the plausible-but-wrong id this view exists not
        # to print. This test must FAIL if anyone re-tightens the filter.
        real = [
            "opus", "sonnet", "haiku",
            "claude-opus-4-8", "claude-sonnet-5", "claude-fable-5",
            "claude-haiku-4-5-20251001",        # 25 — the longest in the field
            "claude-3-5-sonnet-20241022",       # 26
            "claude-opus-4-8[1m]",              # brackets are LEGITIMATE
            "us.anthropic.claude-opus-4-8-v1:0",  # 33 — Bedrock, colon is real
            "anthropic.claude-sonnet-4-v1:0",
        ]
        agents = {f"a{i}": {"name": f"a{i}", "parent": "operator",
                            "pane": f"p{i}", "model": m}
                  for i, m in enumerate(real)}
        out = self.render(agents=agents, live={f"p{i}" for i in range(len(real))},
                          queues={n: 0 for n in agents},
                          events={n: None for n in agents},
                          me_name="operator", op_mail=[])
        for i, m in enumerate(real):
            self.assertIn(f"a{i} model={m} [live]", out)   # WHOLE and unaltered
        self.assertNotIn("…", out)              # nothing was truncated

    def test_hostile_model_string_cannot_forge_a_row(self):
        # --model is UNVALIDATED at spawn and stored verbatim, so the view
        # clamps on render: a newline must not forge a tree row, an ANSI escape
        # must not paint the terminal, and a long id must not blow the line.
        agents = {
            "evil": {"name": "evil", "parent": "operator", "pane": "p1",
                     "model": "opus\nFAKE-LINE: injected\n└─ ghost [live] q=0"},
            "ansi": {"name": "ansi", "parent": "operator", "pane": "p2",
                     "model": "\x1b[31mred\x07"},
            "long": {"name": "long", "parent": "operator", "pane": "p3",
                     "model": "x" * 400},
        }
        out = self.render(agents=agents, live={"p1", "p2", "p3"},
                          queues={"evil": 0, "ansi": 0, "long": 0},
                          events={"evil": None, "ansi": None, "long": None},
                          me_name="operator", op_mail=[])
        body = out.splitlines()[1:]                  # drop the operator-mail line
        # THE property: three agents, three rows. The newline in evil's pin does
        # not forge a fourth row, and the box-drawing glyphs it brought to draw
        # one are excluded, so the payload cannot even look like a tree.
        self.assertEqual(len(body), 3)
        self.assertEqual(sum(ln.lstrip().startswith(("├─", "└─", "?─"))
                             for ln in body), 3)     # exactly 3 tree rows
        self.assertNotIn("\x1b", out)                # no escape survives
        self.assertNotIn("\x07", out)
        for ln in body:
            self.assertLessEqual(len(ln), 80)        # every id is capped
        # the hostile pin is DEFANGED on one row: the newline that would have
        # made a row is gone, the box-drawing that would have drawn one is gone,
        # and what is left is a single unspaced token that no reader could take
        # for real fields. It renders, and it deceives nobody.
        self.assertIn("evil model=opusFAKE-LINE:injectedghost[live]q=0 [live]",
                      out)
        # ESC and BEL are dropped; the residue is text that colours nothing
        self.assertIn("ansi model=[31mred [live]", out)
        # over-cap is cut AND visibly marked, never silently
        self.assertIn("long model=" + "x" * (sw.MODEL_CAP - 1) + "… [live]", out)

    def test_over_cap_model_is_visibly_truncated(self):
        # when the cap DOES fire it must be legible as a cut, on one line
        agents = {"big": {"name": "big", "parent": "operator", "pane": "p1",
                          "model": "claude-" + "z" * 60}}
        out = self.render(agents=agents, live={"p1"}, queues={"big": 0},
                          events={"big": None}, me_name="operator", op_mail=[])
        body = out.splitlines()[1:]
        self.assertEqual(len(body), 1)
        self.assertIn("… [live]", out)              # the cut announces itself
        field = out[out.index("model=") + 6:].split(" ")[0]
        self.assertEqual(len(field), sw.MODEL_CAP)  # cut INSIDE the cap
        self.assertTrue(field.startswith("claude-zzz"))
        self.assertTrue(field.endswith("…"))

    def test_blocked_kind_replaces_idle_not_appends(self):
        # a wedged pane's idle age is not reassuring information once the
        # reason is known — [blocked: kind] REPLACES "idle Nm", never joins it
        out = self.render(blocked={"boss": "trust"})
        self.assertIn("boss [live] q=0 [blocked: trust]", out)
        self.assertNotIn("idle 1m", out)  # boss's idle clause is gone, not doubled

    def test_each_blocked_kind_renders(self):
        for kind in ("trust", "permission", "rate-limit"):
            with self.subTest(kind=kind):
                out = self.render(blocked={"boss": kind})
                self.assertIn(f"[blocked: {kind}]", out)

    def test_unblocked_agent_unaffected_by_sibling_blocked(self):
        out = self.render(blocked={"boss": "trust"})
        self.assertIn("kid (you) [live] q=2 idle ?", out)

    def test_unknown_blocked_kind_is_ignored_not_printed(self):
        # render_ps must never print a kind it cannot vouch for — same
        # exclude-on-the-view-side reasoning as model_of's structural filter.
        # A future/corrupt value in the dict falls back to the ordinary idle
        # clause rather than leaking through verbatim.
        out = self.render(blocked={"boss": "some-new-kind-this-build-does-not-know"})
        self.assertNotIn("some-new-kind", out)
        self.assertIn("boss [live] q=0 idle 1m", out)

    def test_blocked_value_is_never_echoed_verbatim(self):
        # the hazard ps-model was burned on twice: pane text is
        # attacker-controlled (an agent can print anything to its own pane).
        # render_ps must be incapable of printing anything from the blocked
        # dict except one of the three fixed kinds — proven here by feeding a
        # value shaped like a forgery attempt and confirming nothing but the
        # literal '[blocked: ...]' template surfaces.
        payload = "x) (you"
        out = self.render(blocked={"boss": payload})
        self.assertNotIn(payload, out)
        self.assertNotIn("(you)", out.split("\n")[1])  # boss's own line

    def test_blocked_dead_agent_stays_on_the_shared_dead_line(self):
        # ruling R5 is not overridden by blocked: a dead pane cannot be
        # "blocked" (nothing is reading it), and even a stale/wrong dict
        # entry for a dead name must not resurrect it as a tree row.
        out = self.render(live={"p2"}, blocked={"boss": "trust"})
        self.assertIn("dead: boss, dead", out)
        self.assertNotIn("[blocked:", out)

    def test_no_blocked_arg_is_byte_identical_to_before(self):
        # backward compatibility: omitting the new kwarg entirely must render
        # exactly as it did before this feature existed.
        with_none = sw.render_ps(agents=self.AGENTS, live={"p1", "p2"},
                                 queues={"boss": 0, "kid": 2, "dead": 0},
                                 events={"boss": {"event": "stop", "ts": 940_000,
                                                  "last_words": "shipped the report"},
                                         "kid": None, "dead": None},
                                 me_name="kid", op_mail=[("boss", 400_000)],
                                 now=1_000_000)
        with_empty = self.render(blocked={})
        self.assertEqual(with_none, with_empty)


class TestClassifyBlocked(unittest.TestCase):
    """Pure function, untrusted input: pane text an agent fully controls must
    map to one of a CLOSED set of kinds, or None — never a substring of the
    input itself. See BLOCKED_SIGNATURES and render_ps's blocked docstring."""

    def test_permission_prompt_matches(self):
        text = "Bash(rm -rf /tmp/x)\nDo you want to proceed?\n1. Yes"
        self.assertEqual(sw.classify_blocked(text), "permission")

    def test_trust_prompt_matches(self):
        text = "Do you trust the files in this folder?\n(y/n)"
        self.assertEqual(sw.classify_blocked(text), "trust")

    def test_rate_limit_requires_both_resets_and_limit(self):
        text = "5-hour limit reached - resets at 3:00pm"
        self.assertEqual(sw.classify_blocked(text), "rate-limit")

    def test_resets_alone_is_not_rate_limit(self):
        # 'resets' is common enough prose (e.g. an agent discussing a counter,
        # a cache, a game state) that it must not fire alone
        text = "the counter resets every midnight, nothing unusual here"
        self.assertIsNone(sw.classify_blocked(text))

    def test_ordinary_output_matches_nothing(self):
        self.assertIsNone(sw.classify_blocked("running tests...\n42 passed"))

    def test_empty_text_matches_nothing(self):
        self.assertIsNone(sw.classify_blocked(""))
        self.assertIsNone(sw.classify_blocked(None))

    def test_result_is_always_a_member_of_the_closed_set_or_none(self):
        samples = ["Do you want to proceed?", "trust the files in this folder",
                  "limit reached, resets soon", "", "garbage", None,
                  "trust the files in this folder AND Do you want to proceed?"]
        for s in samples:
            with self.subTest(s=s):
                r = sw.classify_blocked(s)
                self.assertTrue(r is None or r in sw.BLOCKED_KINDS)


class TestBlockedCandidates(unittest.TestCase):
    """Cost control: blocked_candidates decides which agents are worth a live
    pane read, so ps never pays for N reads when most panes are plainly fine."""

    AGENTS = {
        "fresh": {"name": "fresh", "parent": "operator", "pane": "p1"},
        "stale": {"name": "stale", "parent": "operator", "pane": "p2"},
        "never": {"name": "never", "parent": "operator", "pane": "p3"},
        "dead":  {"name": "dead", "parent": "operator", "pane": "p9"},
    }

    def test_recently_active_agent_is_not_a_candidate(self):
        events = {"fresh": {"ts": 999_000}, "stale": None, "never": None, "dead": None}
        out = sw.blocked_candidates(self.AGENTS, {"p1", "p2", "p3", "p9"},
                                    events, now=1_000_000, threshold_ms=120_000)
        self.assertNotIn("fresh", out)

    def test_stale_idle_agent_is_a_candidate(self):
        events = {"fresh": None, "stale": {"ts": 100_000}, "never": None, "dead": None}
        out = sw.blocked_candidates(self.AGENTS, {"p1", "p2", "p3", "p9"},
                                    events, now=1_000_000, threshold_ms=120_000)
        self.assertIn("stale", out)

    def test_agent_with_no_event_fact_yet_is_a_candidate(self):
        # a session wedged on its VERY FIRST prompt (e.g. the trust dialog on
        # spawn) has never fired Stop, so it has no event fact at all — must
        # still be a candidate, not skipped for "no data"
        events = {"fresh": None, "stale": None, "never": None, "dead": None}
        out = sw.blocked_candidates(self.AGENTS, {"p1", "p2", "p3", "p9"},
                                    events, now=1_000_000)
        self.assertIn("never", out)

    def test_dead_pane_is_never_a_candidate(self):
        events = {n: None for n in self.AGENTS}
        out = sw.blocked_candidates(self.AGENTS, {"p1", "p2", "p3"},  # p9 missing
                                    events, now=1_000_000)
        self.assertNotIn("dead", out)

    def test_herdr_unreachable_still_computable_but_cmd_ps_skips_the_call(self):
        # blocked_candidates itself follows render_ps's convention: live=None
        # means liveness is UNKNOWN, not that nothing is live, so it does not
        # filter on liveness here (same as render_ps's is_dead). The actual
        # guard against reading panes we can't confirm exist lives one layer
        # up, in cmd_ps, which skips calling read_blocked at all when
        # live_pane_set() returns None (herdr unreachable) — see cmd_ps.
        events = {n: None for n in self.AGENTS}
        out = sw.blocked_candidates(self.AGENTS, None, events, now=1_000_000)
        self.assertEqual(sorted(out), ["dead", "fresh", "never", "stale"])


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


class TestHerdrRunPath(unittest.TestCase):
    """`herdr pane run` TYPES its command argument into the pane's shell, and
    (HERDR-BUG SHIM, confirmed on herdr 0.7.3) strips exactly one leading '/'
    from it first. A launcher path must survive BOTH: herdr's strip, THEN the
    shell parsing whatever survives as a word. herdr_run_path's contract is
    the round-trip below — strip-then-shell-parse recovers the original path
    byte for byte, for any content the path may hold (spaces, $, quotes,
    backticks, parens, semicolons, unicode)."""

    @staticmethod
    def _herdr_strip(s):
        # herdr pane run strips exactly ONE leading '/' from what it types.
        return s[1:] if s.startswith("/") else s

    def _assert_round_trips(self, launcher):
        sent = sw.herdr_run_path(launcher)
        stripped = self._herdr_strip(sent)
        parsed = shlex.split(stripped)
        self.assertEqual(parsed, [launcher],
                         f"round-trip failed for {launcher!r}: sent={sent!r} "
                         f"stripped={stripped!r} parsed={parsed!r}")

    def test_bare_filename_round_trips(self):
        self._assert_round_trips("launch.sh")

    def test_relative_path_round_trips(self):
        self._assert_round_trips("relative/launch.sh")

    def test_empty_string_round_trips(self):
        self._assert_round_trips("")

    def test_simple_absolute_path_round_trips(self):
        self._assert_round_trips("/Users/x/y/name.launch.sh")

    def test_space_round_trips(self):
        self._assert_round_trips("/a b/c")

    def test_wsl_realistic_path_with_space_round_trips(self):
        self._assert_round_trips(
            "/mnt/c/Users/John Smith/proj/.swarm/settings/x.launch.sh")

    def test_dollar_round_trips(self):
        self._assert_round_trips("/tmp/$HOME/x.sh")

    def test_single_quote_round_trips(self):
        self._assert_round_trips("/mnt/c/Users/O'Brien/proj/x.sh")

    def test_double_quote_round_trips(self):
        self._assert_round_trips('/tmp/"quoted"/x.sh')

    def test_backtick_round_trips(self):
        self._assert_round_trips("/tmp/`backtick`/x.sh")

    def test_parens_round_trips(self):
        self._assert_round_trips("/tmp/(paren)/x.sh")

    def test_semicolon_round_trips(self):
        self._assert_round_trips("/tmp/semi;colon/x.sh")

    def test_unicode_round_trips(self):
        self._assert_round_trips("/tmp/ünïcödé/x.sh")

    def test_several_adversarial_chars_at_once_round_trips(self):
        self._assert_round_trips("/tmp/a b$c'd\"e`f(g)h;i/x.sh")

    def test_simple_absolute_path_gets_a_raw_slash_prepended_outside_the_quoting(self):
        # pins the actual construction: '/' + shlex.quote(launcher), not the
        # other order. shlex.quote alone (no prepended slash) would leave the
        # sent string starting with a quote char, which herdr's strip would
        # eat instead of the slash -- this assertion catches that regression
        # even though it would still (accidentally) pass some round-trips.
        launcher = "/Users/x/name.launch.sh"
        sent = sw.herdr_run_path(launcher)
        self.assertTrue(sent.startswith("/"))
        self.assertEqual(sent, "/" + shlex.quote(launcher))

    def test_relative_path_is_quoted_but_not_slash_prefixed(self):
        launcher = "rel ative/x.sh"
        sent = sw.herdr_run_path(launcher)
        self.assertEqual(sent, shlex.quote(launcher))
        self.assertFalse(sent.startswith("/"))


ADVERSARIAL_PATHS = [
    "/a b/c",
    "/mnt/c/Users/John Smith/proj/.swarm/settings/x.launch.sh",
    "/tmp/$HOME/x.sh",
    "/mnt/c/Users/O'Brien/proj/x.sh",
    '/tmp/"quoted"/x.sh',
    "/tmp/`backtick`/x.sh",
    "/tmp/(paren)/x.sh",
    "/tmp/semi;colon/x.sh",
    "/tmp/ünïcödé/x.sh",
    "/tmp/a b$c'd\"e`f(g)h;i/x.sh",
]


class TestWriteLauncher(unittest.TestCase):
    """write_launcher's settings-unreadable branch interpolates the settings
    path into an `echo "..."` DOUBLE-quoted shell string. Unlike every other
    line in write_launcher (which passes the whole path through
    shlex.quote), this one used to splice {settings} directly into double
    quotes -- a $, backtick, or embedded " in the path would expand/inject
    rather than print literally. Fixed by quoting the path as its own shell
    word (shlex.quote) inside an otherwise-unquoted echo, rather than
    splicing it into a double-quoted string."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="swarm-launcher-")
        self.bindir = tempfile.mkdtemp(prefix="swarm-launcher-bin-")
        with open(os.path.join(self.bindir, "claude"), "w") as f:
            f.write("#!/usr/bin/env bash\nexit 0\n")
        os.chmod(os.path.join(self.bindir, "claude"), 0o755)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)
        shutil.rmtree(self.bindir, ignore_errors=True)

    def _build(self, settings):
        launcher = os.path.join(self.tmp, "x.launch.sh")
        statusfile = os.path.join(self.tmp, "x.status")
        taskfile = os.path.join(self.tmp, "x.task")
        with open(taskfile, "w") as f:
            f.write("task")
        sw.write_launcher(launcher, statusfile, settings, taskfile, "sonnet",
                          sw.DEFAULT_PERMISSION_MODE)
        return launcher, statusfile

    def test_generated_script_is_syntactically_valid_bash(self):
        for settings in ADVERSARIAL_PATHS:
            launcher, _ = self._build(settings)
            p = subprocess.run(["bash", "-n", launcher], capture_output=True, text=True)
            self.assertEqual(p.returncode, 0,
                             f"settings={settings!r} produced invalid bash:\n{p.stderr}")

    def test_missing_settings_error_message_is_literal_no_injection(self):
        for settings in ADVERSARIAL_PATHS:
            launcher, statusfile = self._build(settings)  # settings path never created -> unreadable
            env = dict(os.environ)
            env["PATH"] = self.bindir + ":/usr/bin:/bin"  # fake claude so we reach the settings check
            p = subprocess.run(["bash", launcher], capture_output=True, text=True,
                               timeout=10, input="", env=env)
            with open(statusfile) as f:
                status = f.read()
            # Must be the literal, unexpanded settings string -- not a shell
            # expansion of $HOME/backticks, not a truncated/broken message,
            # and no evidence of injected commands running.
            self.assertIn(f"failed: settings unreadable: {settings}", status,
                         f"settings={settings!r} did not appear literally: {status!r}")

    def test_missing_settings_no_command_execution_from_the_path(self):
        # A path holding `$(...)`-shaped or backtick-shaped text must never
        # actually run as a command -- confirm no side effect file appears.
        marker = os.path.join(self.tmp, "PWNED")
        settings = f"/tmp/$(touch {shlex.quote(marker)})/x.json"
        launcher, statusfile = self._build(settings)
        env = dict(os.environ)
        env["PATH"] = self.bindir + ":/usr/bin:/bin"
        subprocess.run(["bash", launcher], capture_output=True, text=True,
                       timeout=10, input="", env=env)
        self.assertFalse(os.path.exists(marker), "settings path executed as a command")


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

    def test_stop_ring_is_bounded_against_a_busy_pane(self):
        # regression, field evidence 2026-07-10 (WATCHLIST #3): the ring's
        # settle loop spun ~20 x 10s herdr reads against a loaded pane,
        # blocking `event stop` — and with it the agent's next turn — for
        # ~3 minutes while deliverable mail waited. The Stop-path ring is a
        # single attempt: it never reads the pane, and a busy pane cannot
        # hold the hook beyond a small bound.
        bindir = os.path.join(self.root, "fakebin")
        os.makedirs(bindir)
        log = os.path.join(self.root, "herdr.log")
        with open(os.path.join(bindir, "herdr"), "w") as f:
            f.write('#!/usr/bin/env bash\n'
                    'echo "$@" >> "%s"\n'
                    'if [ "$1 $2" = "pane read" ]; then sleep 3; fi\n'
                    'echo "{}"\n' % log)
        os.chmod(os.path.join(bindir, "herdr"), 0o755)
        os.makedirs(os.path.join(self.root, "agents"))
        with open(sw.agent_rec_path(self.root, "kid"), "w") as f:
            json.dump({"name": "kid", "parent": "operator", "pane": "p1"}, f)
        msg(self.root, "kid", "boss", 1000, "deliverable mail")
        env = dict(os.environ, SWARM_DIR=self.root, SWARM_AGENT_ID="kid",
                   PATH=bindir + os.pathsep + os.environ.get("PATH", ""))
        t0 = time.time()
        subprocess.run([SWARM, "event", "stop"], env=env, input=b"{}",
                       capture_output=True, timeout=60)
        elapsed = time.time() - t0
        self.assertLess(elapsed, 10,
                        "a busy pane must not block `event stop`")
        with open(log) as f:
            calls = f.read()
        self.assertIn("pane send-text p1", calls)  # the ring was attempted
        self.assertNotIn("pane read", calls)       # and never polls the pane


class TestPreTrustEntry(unittest.TestCase):
    """Pure patch logic over ~/.claude.json's shape. This file is Claude
    Code's own live, global settings file (real machines carry 100+ project
    entries with real usage history) — pre_trust_entry's whole contract is
    touching ONLY the one key this feature owns, nothing else, ever."""

    def test_new_project_gets_a_minimal_entry(self):
        out = sw.pre_trust_entry({}, "/tmp/experiment-1")
        self.assertEqual(out["projects"]["/tmp/experiment-1"],
                         {"hasTrustDialogAccepted": True})

    def test_existing_projects_untouched(self):
        config = {"projects": {"/Users/me/real-repo": {"hasTrustDialogAccepted": True,
                                                        "lastCost": 4.2,
                                                        "mcpServers": {"x": 1}}}}
        out = sw.pre_trust_entry(config, "/tmp/experiment-1")
        # the real repo's entry is byte-for-byte unchanged
        self.assertEqual(out["projects"]["/Users/me/real-repo"],
                         config["projects"]["/Users/me/real-repo"])
        self.assertIn("/tmp/experiment-1", out["projects"])

    def test_existing_entry_for_same_path_keeps_its_other_keys(self):
        # a dir a human already uses normally must not lose its other state
        # just because a harness later spawns --trust into it
        config = {"projects": {"/tmp/experiment-1": {"hasTrustDialogAccepted": False,
                                                      "lastCost": 1.1,
                                                      "allowedTools": ["Bash"]}}}
        out = sw.pre_trust_entry(config, "/tmp/experiment-1")
        entry = out["projects"]["/tmp/experiment-1"]
        self.assertEqual(entry["hasTrustDialogAccepted"], True)  # flipped
        self.assertEqual(entry["lastCost"], 1.1)                 # preserved
        self.assertEqual(entry["allowedTools"], ["Bash"])        # preserved

    def test_other_top_level_keys_untouched(self):
        config = {"numStartups": 500, "anonymousId": "abc123", "projects": {}}
        out = sw.pre_trust_entry(config, "/tmp/x")
        self.assertEqual(out["numStartups"], 500)
        self.assertEqual(out["anonymousId"], "abc123")

    def test_missing_projects_key_is_created(self):
        out = sw.pre_trust_entry({"numStartups": 1}, "/tmp/x")
        self.assertIn("projects", out)
        self.assertTrue(out["projects"]["/tmp/x"]["hasTrustDialogAccepted"])

    def test_input_config_is_not_mutated(self):
        # the function must return a NEW structure — a caller holding the
        # original must never see it change out from under them
        config = {"projects": {"/tmp/x": {"hasTrustDialogAccepted": False}}}
        sw.pre_trust_entry(config, "/tmp/x")
        self.assertFalse(config["projects"]["/tmp/x"]["hasTrustDialogAccepted"])

    def test_two_different_paths_both_get_entries(self):
        out = sw.pre_trust_entry({}, "/tmp/a")
        out = sw.pre_trust_entry(out, "/tmp/b")
        self.assertTrue(out["projects"]["/tmp/a"]["hasTrustDialogAccepted"])
        self.assertTrue(out["projects"]["/tmp/b"]["hasTrustDialogAccepted"])


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

    def test_trust_flag_is_recognized_not_an_unknown_flag_error(self):
        # --trust must reach argument-parsing successfully (proven by the
        # failure moving PAST "unknown flag" to the name-validation error,
        # same technique as the trailing-newline test above) without this
        # process ever reaching herdr or touching the real ~/.claude.json —
        # the bad name makes cmd_spawn die before either happens.
        env = dict(os.environ, SWARM_DIR=self.root, HERDR_ENV="1")
        p = subprocess.run([SWARM, "spawn", "abc\n", "task", "--trust"], env=env,
                           capture_output=True, text=True, timeout=30)
        self.assertEqual(p.returncode, 1)
        self.assertIn("bad name", p.stderr)
        self.assertNotIn("unknown flag", p.stderr)

    def test_unknown_flag_still_refused(self):
        env = dict(os.environ, SWARM_DIR=self.root, HERDR_ENV="1")
        p = subprocess.run([SWARM, "spawn", "ok-name", "task", "--bogus"], env=env,
                           capture_output=True, text=True, timeout=30)
        self.assertEqual(p.returncode, 1)
        self.assertIn("unknown flag", p.stderr)


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


class TestRegisteredMiddleware(Base):
    """.swarm/config's [middleware] section is registration; any defect in it
    means no middleware (None), which is the fail-open branch. The tool
    carries no policy about what the configured middleware does."""

    def _config(self, text):
        os.makedirs(self.root, exist_ok=True)
        with open(os.path.join(self.root, "config"), "w") as f:
            f.write(text)

    def test_absent_config_is_none(self):
        self.assertIsNone(sw.registered_middleware(self.root))

    def test_full_section_parsed(self):
        self._config('[middleware]\ncommand = "python3 /path/to/mw.py --flag"\n'
                     'identity = "screener"\ntimeout = 5\n')
        self.assertEqual(sw.registered_middleware(self.root),
                         ("screener", "python3 /path/to/mw.py --flag", 5))

    def test_identity_and_timeout_defaults(self):
        self._config('[middleware]\ncommand = "/path/mw"\n')
        ident, command, timeout = sw.registered_middleware(self.root)
        self.assertEqual(ident, "middleware")
        self.assertEqual(command, "/path/mw")
        self.assertEqual(timeout, sw.MIDDLEWARE_TIMEOUT)

    def test_defective_configs_are_none(self):
        for bad in ("", "[middleware]\n", "[middleware]\ncommand = \"\"\n",
                    "[other]\ncommand = \"/path\"\n", "not toml at [all"):
            self._config(bad)
            self.assertIsNone(sw.registered_middleware(self.root),
                              f"{bad!r} must read as no middleware")

    def test_fallback_parser_handles_the_flat_shape(self):
        # the tiny non-tomllib path: sections, quoted strings, bare ints,
        # comments — enough for .swarm/config, nothing more
        self._config('# a comment\n[middleware]\n'
                     'command = "python3 mw.py"  # inline note\n'
                     'timeout = 7\n[other]\nx = 1\n')
        conf = sw.read_flat_toml(os.path.join(self.root, "config"))
        self.assertEqual(conf["middleware"],
                         {"command": "python3 mw.py", "timeout": 7})
        self.assertEqual(conf["other"], {"x": 1})


if __name__ == "__main__":
    unittest.main()
