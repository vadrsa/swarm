# FOLLOW-UP (not fixed here): `.swarm/config` is inside the sandbox a child can write

**Status:** open. Found by `spawn-red` during the adversarial review of the spawn-hardening PR
(`docs/audit/spawn-red-2026-07-14.md`, its BLOCKER #2). Filed rather than fixed, for reasons
stated plainly below. **Not created by that PR.**

## The mechanism (real, and verified in parts)

`.swarm/config` sits **inside** an agent's cwd. Under any permission mode that allows unattended
file writes — which is the whole point of the spawn-hardening fix — **a child can write it.**
That one file drives two privileged things:

1. **`[spawn] permission_mode`** — `configured_permission_mode()` is the fallback for every
   `swarm spawn` that does not pass `--permission-mode` explicitly. A child that writes
   `permission_mode = "bypassPermissions"` raises *every subsequent spawn in the tree* that
   omits the flag — including spawns by agents that never intended to grant a bypass.
2. **`[middleware] command`** — a pre-existing feature (`499cb2e`) that `subprocess.run`s the
   configured command on **every `swarm send`**, tree-wide. A child that writes this registers
   itself as an interceptor with code execution on every future message.

`SWARM_DIR` is exported to every child (`--env SWARM_DIR={root}`), so every agent at any depth
knows the exact path. There is no ACL, ownership check, or provenance check on the file.

## Why this is filed and not fixed in that PR

Stated in both directions, because a true mechanism must not be laundered into a false severity
— and equally must not be waved away as "pre-existing":

**Why it is real:** every individual link was verified. Unattended in-cwd writes happen (measured);
`.swarm/config` is in-cwd; the spawn fallback reads it; the middleware exec reads it. Nothing here
is speculative.

**Why it is not a blocker on the spawn-hardening PR:**

- The middleware-exec feature **predates that PR** (`499cb2e`).
- `.swarm/config` **does not exist in this repo today** — nothing reads a file that isn't there.
- Most decisively: **that PR *reduces* child privilege on the machine where the risk was actually
  incurred.** Before it, swarm passed *no* permission flag, so children inherited the machine's
  ambient default — which on this machine is `auto`, and **`auto` permits network egress** while
  `acceptEdits` blocks it (measured on an identical benign task: `auto` downloads, `acceptEdits`
  is gated). Every child ever spawned here already ran with *more* privilege than that PR grants.
  The review's framing — "this PR is what makes it live" — is incorrect for this machine.

The honest summary: the exposure was always there and nobody had looked. The PR that made us look
is not the PR that caused it.

## Fix directions (unchosen — whoever picks this up should decide)

- **Provenance/ACL check**: refuse to honor `.swarm/config` unless it is owned by the operator, or
  validate it against a checksum recorded outside the sandbox.
- **Move the privileged keys out of the sandbox** entirely — a child cannot escalate through a file
  it cannot reach. This is probably the real answer: the sandbox boundary already exists and works
  (writes outside the cwd *are* blocked, measured); the bug is that we put a privileged file inside
  it.
- **Refuse `bypassPermissions` from the config file specifically** — allow it only as an explicit
  `--permission-mode` flag typed by a human, never as an inherited default. Narrow, cheap, and
  kills the escalation path without touching the sandbox model.

The third is the smallest change that closes the spawn-escalation half; it does **not** close the
middleware-exec half, which needs one of the first two.
