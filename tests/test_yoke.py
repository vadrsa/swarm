"""Tests for harness/yoke — the installable opencode-fork TUI harness.

Covers the 3 fixes required by docs/design/PRODUCTIZE.md §5 over the R&D
reference (swarm-rnd/harness/spawn-oc-tui.py):
  1. --reason accepted and recorded (tombstone + agent record).
  2. No hardcoded SWARM_DIR/bin-dir/fork-dir/pump-src: --swarm-dir/SWARM_DIR
     env, --yoke-fork/YOKE_FORK env, both refusing clearly when absent; the
     bin dir and pump source resolve relative to yoke's own (real) location.
  3. free_port() — a real ephemeral-port helper, present and correct even
     though the shipped TUI path never calls it.

Also covers install.sh's yoke symlink (install/uninstall round-trip).

Tests that would need the actual opencode fork + bun are refused loudly via
pytest.skip, never silently passed — this suite exercises yoke's own argument
handling, file-contract writes, and resolution logic without booting bun.
"""
import importlib.machinery
import importlib.util
import json
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
YOKE = os.path.join(REPO, "harness", "yoke")
INSTALL_SH = os.path.join(REPO, "install.sh")

loader = importlib.machinery.SourceFileLoader("yokemod", YOKE)
spec = importlib.util.spec_from_loader("yokemod", loader)
yokemod = importlib.util.module_from_spec(spec)
loader.exec_module(yokemod)


FAKE_HERDR = r'''#!/usr/bin/env bash
echo "$@" >> "$FAKE_HERDR_LOG"
case "$1 $2" in
  "tab create") echo '{"result":{"root_pane":{"pane_id":"pane-77"},"tab":{"tab_id":"tab-77"}}}' ;;
  "pane run")   : ;;
  *) : ;;
esac
exit 0
'''


def run_yoke(args, env_extra, cwd=None):
    env = {k: v for k, v in os.environ.items()
           if k not in ("SWARM_DIR", "YOKE_FORK", "HERDR_WORKSPACE_ID")}
    env["PATH"] = "/usr/bin:/bin"
    env.update(env_extra)
    return subprocess.run([sys.executable, YOKE] + args, capture_output=True,
                          text=True, env=env, cwd=cwd or os.getcwd(), timeout=30)


class Base(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="yoke-test-")
        self.swarm_dir = os.path.join(self.root, ".swarm")
        self.fork_dir = os.path.join(self.root, "fake-fork")
        self.bindir = tempfile.mkdtemp(prefix="yoke-test-bin-")

    def tearDown(self):
        shutil.rmtree(self.root, ignore_errors=True)
        shutil.rmtree(self.bindir, ignore_errors=True)

    def fake_herdr(self):
        log = os.path.join(self.root, "herdr.log")
        with open(os.path.join(self.bindir, "herdr"), "w") as f:
            f.write(FAKE_HERDR)
        os.chmod(os.path.join(self.bindir, "herdr"), 0o755)
        env = {"PATH": self.bindir + ":/usr/bin:/bin", "FAKE_HERDR_LOG": log}
        return env, log


class TestNoHardcodedPaths(unittest.TestCase):
    """Fix 2: grep the shipped source for any machine-specific literal."""

    def test_no_hardcoded_vadrsa_path_in_source(self):
        with open(YOKE) as f:
            src = f.read()
        self.assertNotIn("/Users/vadrsa", src,
                          "yoke must resolve all paths dynamically; found a "
                          "hardcoded machine-specific literal")

    def test_no_hardcoded_swarm_rnd_path_literal(self):
        # The docstring's provenance note ("ported from swarm-rnd/...") is
        # fine — it's prose, not a path the code resolves at runtime. What
        # must never appear is an actual assigned path literal.
        with open(YOKE) as f:
            src = f.read()
        self.assertNotIn('"/Users/vadrsa/git/swarm-rnd', src)
        self.assertNotIn("'/Users/vadrsa/git/swarm-rnd", src)


class TestSwarmDirResolution(Base):
    def test_swarm_dir_flag_used_when_present(self):
        self.assertEqual(yokemod.resolve_swarm_dir("/tmp/explicit"), "/tmp/explicit")

    def test_swarm_dir_env_used_when_flag_absent(self):
        old = os.environ.get("SWARM_DIR")
        os.environ["SWARM_DIR"] = "/tmp/from-env"
        try:
            self.assertEqual(yokemod.resolve_swarm_dir(None), "/tmp/from-env")
        finally:
            if old is None:
                os.environ.pop("SWARM_DIR", None)
            else:
                os.environ["SWARM_DIR"] = old

    def test_flag_takes_precedence_over_env(self):
        old = os.environ.get("SWARM_DIR")
        os.environ["SWARM_DIR"] = "/tmp/from-env"
        try:
            self.assertEqual(yokemod.resolve_swarm_dir("/tmp/flag"), "/tmp/flag")
        finally:
            if old is None:
                os.environ.pop("SWARM_DIR", None)
            else:
                os.environ["SWARM_DIR"] = old

    def test_neither_present_refuses_at_process_level(self):
        env, _ = self.fake_herdr()
        p = run_yoke(["kid", "do the thing", "--model", "zai/glm-5.1",
                      "--parent", "boss", "--reason", "test",
                      "--yoke-fork", self.fork_dir], env)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("swarm dir", p.stderr.lower())
        # nothing should have been written since SWARM_DIR was never resolved
        self.assertFalse(os.path.exists(self.swarm_dir))

    def test_swarm_dir_env_routes_writes_at_process_level(self):
        env, _ = self.fake_herdr()
        env["SWARM_DIR"] = self.swarm_dir
        p = run_yoke(["kid", "do the thing", "--model", "zai/glm-5.1",
                      "--parent", "boss", "--reason", "test reason",
                      "--yoke-fork", self.fork_dir], env)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertTrue(os.path.exists(os.path.join(self.swarm_dir, "journal", "kid.md")))
        self.assertTrue(os.path.exists(os.path.join(self.swarm_dir, "agents", "kid.json")))


class TestForkDirResolution(Base):
    def test_yoke_fork_flag_used_when_present(self):
        self.assertEqual(yokemod.resolve_fork_dir("/tmp/explicit-fork"), "/tmp/explicit-fork")

    def test_yoke_fork_env_used_when_flag_absent(self):
        old = os.environ.get("YOKE_FORK")
        os.environ["YOKE_FORK"] = "/tmp/from-env-fork"
        try:
            self.assertEqual(yokemod.resolve_fork_dir(None), "/tmp/from-env-fork")
        finally:
            if old is None:
                os.environ.pop("YOKE_FORK", None)
            else:
                os.environ["YOKE_FORK"] = old

    def test_neither_present_refuses_at_process_level(self):
        env, _ = self.fake_herdr()
        env["SWARM_DIR"] = self.swarm_dir
        p = run_yoke(["kid", "do the thing", "--model", "zai/glm-5.1",
                      "--parent", "boss", "--reason", "test"], env)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("fork", p.stderr.lower())
        self.assertFalse(os.path.exists(self.swarm_dir),
                          "a refusal before the tombstone must not burn the name")


class TestReasonFix(Base):
    """Fix 1: --reason lands verbatim in both the journal tombstone and the
    agent record, instead of yoke fabricating its own."""

    def test_reason_lands_in_tombstone_and_record(self):
        env, _ = self.fake_herdr()
        env["SWARM_DIR"] = self.swarm_dir
        p = run_yoke(["kid", "do the thing", "--model", "zai/glm-5.1",
                      "--parent", "boss",
                      "--reason", "cheap model, I will re-read the diff myself",
                      "--yoke-fork", self.fork_dir], env)
        self.assertEqual(p.returncode, 0, p.stderr)

        with open(os.path.join(self.swarm_dir, "journal", "kid.md")) as f:
            journal = f.read()
        self.assertIn("cheap model, I will re-read the diff myself", journal)

        with open(os.path.join(self.swarm_dir, "agents", "kid.json")) as f:
            rec = json.load(f)
        self.assertEqual(rec["reason"], "cheap model, I will re-read the diff myself")
        self.assertEqual(rec["pane"], "pane-77")
        self.assertEqual(rec["tab"], "tab-77")

    def test_missing_reason_falls_back_but_does_not_crash(self):
        env, _ = self.fake_herdr()
        env["SWARM_DIR"] = self.swarm_dir
        p = run_yoke(["kid", "do the thing", "--model", "zai/glm-5.1",
                      "--parent", "boss", "--yoke-fork", self.fork_dir], env)
        self.assertEqual(p.returncode, 0, p.stderr)
        with open(os.path.join(self.swarm_dir, "agents", "kid.json")) as f:
            rec = json.load(f)
        self.assertTrue(rec["reason"], "fallback reason must still be non-empty")
        self.assertIn("no --reason given", rec["reason"])


class TestFilesResolveRelativeToYokeLocation(Base):
    """The bin dir and pump source must resolve relative to yoke's own real
    location (surviving a symlink), never a hardcoded absolute path."""

    def test_pump_plugin_copied_into_workspace(self):
        env, _ = self.fake_herdr()
        env["SWARM_DIR"] = self.swarm_dir
        p = run_yoke(["kid", "do the thing", "--model", "zai/glm-5.1",
                      "--parent", "boss", "--reason", "test",
                      "--yoke-fork", self.fork_dir], env)
        self.assertEqual(p.returncode, 0, p.stderr)
        out = json.loads(p.stdout)
        ws = out["workspace"]
        pump_dst = os.path.join(ws, ".opencode", "plugin", "swarm-pump.js")
        self.assertTrue(os.path.exists(pump_dst))
        with open(pump_dst) as f, open(os.path.join(REPO, "harness", "swarm-pump.js")) as g:
            self.assertEqual(f.read(), g.read())

    def test_launcher_script_uses_resolved_bin_dir_not_a_literal(self):
        env, _ = self.fake_herdr()
        env["SWARM_DIR"] = self.swarm_dir
        p = run_yoke(["kid", "do the thing", "--model", "zai/glm-5.1",
                      "--parent", "boss", "--reason", "test",
                      "--yoke-fork", self.fork_dir], env)
        self.assertEqual(p.returncode, 0, p.stderr)
        out = json.loads(p.stdout)
        ws = out["workspace"]
        with open(os.path.join(ws, "launch.sh")) as f:
            script = f.read()
        expected_bin_dir = os.path.normpath(os.path.join(REPO, "bin"))
        self.assertIn(expected_bin_dir, script)
        self.assertIn(self.fork_dir, script)

    def test_works_through_a_symlink_to_yoke(self):
        symlink_dir = tempfile.mkdtemp(prefix="yoke-symlink-")
        try:
            link = os.path.join(symlink_dir, "yoke")
            os.symlink(YOKE, link)
            env = {k: v for k, v in os.environ.items()
                   if k not in ("SWARM_DIR", "YOKE_FORK", "HERDR_WORKSPACE_ID")}
            env["PATH"] = self.bindir + ":/usr/bin:/bin"
            env["SWARM_DIR"] = self.swarm_dir
            fake_herdr_env, _ = self.fake_herdr()
            env.update(fake_herdr_env)
            env["SWARM_DIR"] = self.swarm_dir
            p = subprocess.run([sys.executable, link, "kid", "task",
                                 "--model", "zai/glm-5.1", "--parent", "boss",
                                 "--reason", "test", "--yoke-fork", self.fork_dir],
                                capture_output=True, text=True, env=env, timeout=30)
            self.assertEqual(p.returncode, 0, p.stderr)
            out = json.loads(p.stdout)
            with open(os.path.join(out["workspace"], "launch.sh")) as f:
                script = f.read()
            expected_bin_dir = os.path.normpath(os.path.join(REPO, "bin"))
            self.assertIn(expected_bin_dir, script,
                          "bin dir must resolve through the symlink to yoke's real location")
        finally:
            shutil.rmtree(symlink_dir, ignore_errors=True)


class TestFreePort(unittest.TestCase):
    """Fix 3: a real free-port helper, present even though the TUI path never
    calls it (the shelved serve path is what would use it)."""

    def test_free_port_returns_a_bindable_port(self):
        port = yokemod.free_port()
        self.assertIsInstance(port, int)
        self.assertGreater(port, 0)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.bind(("127.0.0.1", port))
        finally:
            s.close()

    def test_free_port_gives_distinct_ports_across_calls(self):
        # Not guaranteed by the OS, but with the socket released each time
        # collisions across a handful of sequential calls are effectively
        # impossible — enough to catch a regression to a fixed/hashed value.
        ports = {yokemod.free_port() for _ in range(5)}
        self.assertGreater(len(ports), 1)

    def test_free_port_is_not_a_salted_hash_of_the_name(self):
        # The R&D bug this fix replaces: 4200 + (abs(hash(name)) % 400).
        # free_port() takes no name argument at all — prove the signature.
        import inspect
        params = inspect.signature(yokemod.free_port).parameters
        self.assertEqual(len(params), 0)


class TestUnknownFlag(Base):
    def test_unknown_flag_refused(self):
        env, _ = self.fake_herdr()
        env["SWARM_DIR"] = self.swarm_dir
        p = run_yoke(["kid", "task", "--model", "zai/glm-5.1", "--parent",
                      "boss", "--reason", "test", "--bogus", "x"], env)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("unknown flag", p.stderr.lower())


class TestInstallUninstall(unittest.TestCase):
    """install.sh symlinks yoke onto PATH beside swarm, and removes it on
    --uninstall. Runs against a fake $HOME so the real machine is untouched."""

    def setUp(self):
        self.fake_home = tempfile.mkdtemp(prefix="yoke-install-home-")

    def tearDown(self):
        shutil.rmtree(self.fake_home, ignore_errors=True)

    def _run_install(self, args=()):
        env = dict(os.environ)
        env["HOME"] = self.fake_home
        return subprocess.run(["bash", INSTALL_SH, *args], capture_output=True,
                              text=True, env=env, timeout=60)

    def test_install_symlinks_yoke_next_to_swarm(self):
        p = self._run_install()
        self.assertEqual(p.returncode, 0, p.stderr)
        yoke_link = os.path.join(self.fake_home, ".local", "bin", "yoke")
        swarm_link = os.path.join(self.fake_home, ".local", "bin", "swarm")
        self.assertTrue(os.path.islink(yoke_link))
        self.assertTrue(os.path.islink(swarm_link))
        self.assertEqual(os.path.realpath(yoke_link), os.path.realpath(YOKE))

    def test_uninstall_removes_yoke_symlink_too(self):
        self._run_install()
        yoke_link = os.path.join(self.fake_home, ".local", "bin", "yoke")
        self.assertTrue(os.path.islink(yoke_link))
        p = self._run_install(["--uninstall"])
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertFalse(os.path.exists(yoke_link))

    def test_reinstall_is_idempotent(self):
        self._run_install()
        p = self._run_install()
        self.assertEqual(p.returncode, 0, p.stderr)
        yoke_link = os.path.join(self.fake_home, ".local", "bin", "yoke")
        self.assertTrue(os.path.islink(yoke_link))


class TestNeedsRealForkGatedSkips(unittest.TestCase):
    """Anything that would need the actual opencode fork checkout + bun to
    truly boot is gated here and skipped LOUDLY, never silently passed."""

    def test_real_tui_boot_needs_fork_and_bun(self):
        if shutil.which("bun") is None:
            pytest_skip("needs opencode fork + bun: bun not on PATH in this test env")
        pytest_skip("needs opencode fork + bun: no fork checkout is vendored in "
                     "this repo (docs/design/PRODUCTIZE.md §5, 'the fork "
                     "dependency') — this is an integration test for PR 4, not PR 2")


def pytest_skip(reason):
    try:
        import pytest
        pytest.skip(reason)
    except ImportError:
        raise unittest.SkipTest(reason)


if __name__ == "__main__":
    unittest.main()
