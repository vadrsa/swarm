# INDUSTRY-PATTERNS — the operator mailbox, named and projected from outside

**Author:** `patterns-contractor`, an outside contractor engaged by the operator,
in the tradition of `simplest` (`docs/design/SIMPLEST.md`). I am **not bound by
this repo's philosophy, its nine-concept discipline, or its graveyard.** I read
those as anthropology — a record of what this org came to believe under its own
constraints — not as law. My brief is the outside view: name the standard
software patterns the operator's fresh framing maps to, with the systems that
embody them; say how those systems handle the edge cases this org has been
circling; project the design a senior infrastructure engineer would build having
never heard this repo's doctrine; and state plainly, without translating or
softening, wherever the industry answer collides with local law. Translating or
rejecting the conflict is the org's job, not mine.

**Evidence discipline.** Claims about THIS repo cite a file:line at `main@834fec4`
or a wiring doc (`DW §n` = DECISION-WIRING, `PIPE §n` = PIPELINE-WIRING, `PROXY
§n` = PROXY-WIRING, `HOOK §n` = HOOK-WIRING) or a `WORLD.md` line (`W:n`). Claims
about industry systems name the system and the mechanism — Kafka's consumer-group
protocol, SQS FIFO's message-group-id, Erlang/OTP mailbox semantics, Temporal's
task queues, AMQP's per-queue consumer — so a skeptical reader can check them
against those systems' own docs.

**The operator's framing (my subject), near-verbatim:**

> - The operator mailbox should be unordered globally but ordered relative to the
>   agent sending the message.
> - The hook is not engine-specific: you get a way to configure an executable that
>   runs on each new message to the operator from an agent.
> - The hook blocks any new message from that specific agent — but not the others.
> - The hook executable runs in parallel for each agent.

Four properties. Every one of them is a named, load-bearing pattern in
distributed messaging, and the mapping is not loose analogy — it is the same
mechanism the industry has built and re-built for thirty years. This document
names each precisely, shows how the canonical systems handle the edge cases the
org's four wiring docs have been circling (crash mid-message, slow/poison
processor, the exact blocking semantic), says what those systems know that the
wiring docs re-derived under other names or have not reached, marks where the
file substrate genuinely differs so the projection would mislead, and then builds
the thing element-by-element.

---

## 0. The one-paragraph answer

**The operator's four properties are, in industry terms: (1) a partitioned FIFO
log keyed by sender — Kafka's partition-by-key, SQS FIFO's `MessageGroupId`,
Erlang's per-mailbox ordering; (2) a per-message interceptor / consumer middleware
— the "smart endpoint" or message-driven bean; (3) per-key head-of-line blocking
with single-active-consumer-per-key — SQS FIFO's exact delivery guarantee, Kafka's
one-consumer-per-partition rule; (4) partition-parallel consumers — a consumer
group.** Put together, the operator is asking for **a keyed work queue with
per-key ordering, per-key serial processing, and cross-key parallelism, fronted by
a message processor.** That is one of the most thoroughly solved problems in the
industry: it is *literally* the SQS FIFO delivery model, and it is *architecturally*
a Kafka consumer group. A senior infra engineer would recognize it in one
sentence and reach for one of three off-the-shelf shapes.

**Where the projection holds:** the ordering model (per-sender FIFO, global
unordered), the parallelism model (partition-parallel), and the processor shape
(a generic per-message executable) all map cleanly and the industry's edge-case
handling transfers with real force — the org has, in places, re-derived weaker
versions of guarantees the industry ships by default (idempotent claim = SQS
receipt-handle dedup; write-then-invoke = the transactional-outbox pattern;
mv-and-abort = optimistic concurrency / compare-and-swap).

**Where the substrate genuinely differs, so projection would mislead:** three
places, and they are the crux. **(a)** There is no broker process — delivery to the
operator is *pull by a human reader*, not push by a daemon (W:57-61,
bin/swarm:610-611), so nothing on this substrate can *order a consumer relative to
the human*, which is exactly the guarantee HOOK/PIPE spent themselves proving
un-buildable. The industry's blocking semantics assume a broker that owns
dispatch; this system's "broker" for the operator queue is a person with eyes.
**(b)** The processor is *cold per message* (a fresh subprocess, HOOK §6), not a
warm consumer holding a poll loop — so the industry's cheapest guarantees
(in-memory offset tracking, long-poll batching, connection-scoped visibility
timeouts) don't come for free; each costs a file. **(c)** "Blocking a sender" here
means *pausing that sender's ability to send more mail*, which is **sender-side
backpressure / flow control** — a different mechanism from the consumer-side
head-of-line blocking the same words name in a broker, and conflating them is the
single most important distinction in this document (§3).

The rest is the argument.

---

## 1. Property 1 — "unordered globally, ordered per sender" = partitioned FIFO, keyed by sender

### 1.1 The industry name

This is **partition-by-key ordering**, the single most common ordering model in
production messaging. The canonical systems:

- **Apache Kafka.** A topic is split into partitions; a message's partition is
  chosen by `hash(key) % partitions`. **Ordering is guaranteed within a partition,
  never across partitions.** Key the message by producer identity and you get
  exactly "ordered per sender, unordered globally." This is the reference
  implementation of the operator's property 1, verbatim. (Kafka docs: "Kafka only
  provides a total order over records *within* a partition, not between different
  partitions.")
- **Amazon SQS FIFO queues.** Every message carries a `MessageGroupId`. SQS
  guarantees **FIFO ordering within a group** and processes distinct groups
  **in parallel with no ordering between them.** Set `MessageGroupId = senderId`
  and property 1 is the SQS FIFO contract word-for-word — including the
  cross-group parallelism of property 4.
- **Erlang/OTP process mailboxes.** Messages from process A to process B arrive in
  send-order (the language guarantees ordered delivery between any *ordered pair* of
  processes); messages from A and C to B have no mutual order. This is per-sender
  FIFO as a *language primitive* — the actor model's oldest guarantee, and the one
  closest in spirit to a swarm of agents.
- **NATS JetStream / Azure Service Bus sessions.** Service Bus "sessions"
  (`SessionId`) are the direct analog of SQS message-groups: ordered within a
  session, parallel across sessions.

The operator did not invent an ordering model. They named **the** partitioned-FIFO
model, and chose **sender identity as the partition key** — which is the natural,
almost forced, choice when the "producers" are autonomous agents whose messages
have causal order within themselves but not across each other.

### 1.2 What the systems know that the wiring docs haven't said

The wiring docs never name an ordering model at all. DW, PIPE, and PROXY treat the
operator queue as an undifferentiated bag drained oldest-first (PIPE S0–S5,
bin/swarm delivery is "oldest first", W:17-19), and PIPE's whole "races-allowed"
argument is about ordering *the engine against the human*, never about ordering
*messages against each other*. The per-sender ordering the operator now asks for is
**a new axis the docs did not have**, and the industry's lesson is precise:

**The measured record confirms sender is the right partition key.** The operator
corpus shows each sender running a *homogeneous* stream: `updater` sent 9/9 FYIs and
zero decisions ever; `hardener` sent 11/11 mechanical verify-then-approves; scouts
and reviewers sent judgment/escalation 6/7 (ledger-miner-decisions.md §3.1). Streams
that homogeneous *per sender* but heterogeneous *across senders* are the textbook
signal that the sender is the natural partition key — the intra-sender causal thread
is real (an updater's updates are ordered among themselves) and the cross-sender
order is noise. The operator's instinct to key on sender is empirically the right
key, not just a convenient one.

**Per-key ordering is cheap and per-key ordering is enough.** Thirty years of
message systems converged on "order within a key, parallel across keys" because
**global ordering is expensive and almost never needed.** Total order requires a
single serialization point (one partition, one leader, one lock) — it caps
throughput at one consumer and makes that consumer a single point of failure. The
industry's default is: find the smallest key that preserves the causality you
actually need, partition on it, and get parallelism for free everywhere else. The
operator has independently arrived at exactly this design instinct — "ordered per
sender" is the smallest key that preserves each agent's own causal thread while
leaving the rest parallel. **A senior engineer would affirm this choice
immediately** and note only that the org's current substrate already delivers
oldest-first globally (a *stronger*, more expensive property than asked), so
moving to per-sender ordering is a *relaxation*, not a new cost.

### 1.3 Where the substrate differs

The filename convention already encodes almost everything needed:
`{ts}-{from}.json` (bin/swarm:264, queue_put). The **sender is in the key** and the
**timestamp is the intra-sender sequence number.** A per-sender-ordered read is:
group queue files by the `-{from}` suffix, sort each group by `{ts}` prefix. No new
state. The substrate is *already* a partitioned log where the partition key is the
filename suffix; nobody has read it that way because delivery was global-oldest-first.

The one genuine difference: in Kafka/SQS the partition assignment is *fixed at
write time* and the consumer is *pinned to the partition*. Here there is no
consumer pinned to anything — the "consumer" is a human running `swarm ps`
(bin/swarm:933-943) who sees a flat list. So per-sender ordering is not something
the substrate *enforces* on a reader; it is a *view* a reader (or the processor)
computes. That is fine for a correct processor and meaningless against a human who
reads the flat `ps` list — which is the recurring theme of §4.

---

## 2. Property 2 — "a generic executable run on each new message" = a message processor / interceptor

### 2.1 The industry name

This is the **message-processing endpoint** — the consumer-side handler that every
broker invokes per message. Its many industry names, all the same shape:

- **AWS Lambda event-source mapping.** You attach a function to an SQS/Kafka/Kinesis
  source; the platform invokes your function **once per message (or per batch)**,
  cold or warm, with a configured timeout. This is *exactly* the operator's
  "configurable executable that runs on each new message" — including that it is
  **generic**: the platform knows nothing about what your function does; it just
  invokes it with the payload and honors its return.
- **Message-Driven Bean (JMS/JCA), AMQP consumer callback, Kafka
  `ConsumerRecord` handler.** The classic "message listener": the container owns the
  poll loop and delivery; your code is a callback invoked per message.
- **Enterprise Integration Patterns — the "Message Endpoint" and "Event-Driven
  Consumer"** (Hohpe & Woolf). The canonical vocabulary: the endpoint is the glue
  between the messaging system and the application; the system pushes, the endpoint
  processes.

The operator's insistence that the hook is **"not engine-specific"** is the most
sophisticated part of the whole framing, and it has a precise industry name:
**mechanism/policy separation**, or in EIP terms, keeping the *channel* generic and
putting all intelligence in the *endpoint*. The broker (SQS, Kafka) does not know
or care whether your handler is a fraud detector, a decision engine, or a logger.
It provides *invocation with a timeout and a result contract*; the handler provides
*meaning*. This is why AWS can run one Lambda-invocation machine under a million
different functions. **The operator has, correctly, refused to let the swarm tool
know anything about "decision engines"** — it should provide the generic
invocation-with-timeout primitive, and let the configured executable be anything.
That is the right layering, and it is the industry's layering.

### 2.2 The result contract — what the industry standardizes that the org must

Every message-endpoint framework standardizes the *handler's return contract*,
because that is where all the correctness lives:

- **Lambda + SQS:** return normally ⇒ the message is deleted (consumed). Throw ⇒
  the message becomes visible again after the visibility timeout and is retried;
  after N retries it goes to a **dead-letter queue**. Partial-batch failures return
  a list of the message-ids that failed so only those retry.
- **AMQP:** the handler `ack`s (consumed), `nack`s (requeue or DLQ), or `reject`s.
- **Kafka:** the handler advances the *committed offset* only on success; on failure
  the offset is not committed and the message is re-polled.

The operator's hook has a three-way outcome that maps onto this exactly:
**timeout ⇒ deliver to human** (HOOK §3), **returns an answer ⇒ handled** (the hook
claims and replies), **not configured / crash ⇒ pass through** (HOOK §3). In
industry terms: **timeout and crash are "nack, leave for the default consumer"; a
returned answer is "ack, this message is consumed by the handler."** The org's
HOOK-WIRING re-derived this precisely (its "fail-open" = nack-to-human), which is
the right instinct. What it *hasn't* named is the **dead-letter queue** — the
industry's answer to the poison message (§5.3), which the org has no equivalent for
and arguably needs.

### 2.3 Where the substrate differs — cold vs warm, and it is expensive

Lambda, AMQP consumers, and Kafka handlers are **warm by default**: the container
holds a poll loop, reuses a process across many messages, and amortizes startup.
The operator's hook, as the org designed it, is **cold per message** — a fresh
`subprocess.run` per operator-bound send (HOOK §3, HOOK §6). HOOK §6 priced this
honestly and it is the projection's sharpest divergence: **a cold model-backed
handler is tens of seconds per invocation, so timeouts are modal, not tail
(HOOK §6).** The industry would not build it cold. A senior engineer's *first*
change to this design would be to make the processor a **warm consumer**: one
long-lived process that polls the operator queue and handles messages in a loop,
paying startup once. This is §7's first recommendation, and it is where the
industry answer most directly improves on the org's current design — but it
collides with local law (the org killed the standing engine, HOOK §1), and I state
that collision plainly in §8.

---

## 3. Property 3 — "blocks new messages from that sender only" — the crux, and the org has been conflating two mechanisms

This is the property that most needs an outside eye, because **"block" names two
completely different industry mechanisms and the operator's framing points at the
less obvious one.**

### 3.1 The two things "block" can mean

**Mechanism A — consumer-side head-of-line (HOL) blocking / per-key serial
dispatch.** In SQS FIFO and Kafka, within one message group / partition, **the
next message is not delivered until the current one is acknowledged.** The consumer
processes group G's messages strictly one-at-a-time, in order; message 2 of G
"blocks" behind message 1 of G until 1 is done — but groups G and H proceed in
parallel. This is **single-active-consumer-per-key with in-order, one-at-a-time
delivery.** SQS FIFO states it directly: "As long as a message with a particular
group id is in flight, SQS delivers no more messages for that group id." Kafka
achieves it structurally: one partition is assigned to exactly one consumer in a
group, and that consumer processes it serially.

**Mechanism B — sender-side backpressure / flow control.** The producer is
*prevented from enqueuing more* until the backlog drains. TCP flow control (the
receive window), Kafka producer `max.in.flight.requests` and buffer-full blocking,
reactive-streams `request(n)` demand signaling, gRPC flow control — all of these
**push back on the sender**, slowing or pausing *production*, not consumption.

**These are opposite ends of the pipe.** Mechanism A holds *messages already sent*
in a per-key queue and meters them into the processor one at a time. Mechanism B
stops the *sender* from producing. The operator's words — "the hook blocks any new
message **from that specific agent**" — most naturally read as **Mechanism B applied
per-key: while sender S has a message being processed (or a poison message stuck),
S cannot send another; other senders are unaffected.** But the *effect* they want
is Mechanism A's guarantee: **per-sender, one message is fully handled before the
next from that sender is looked at.** The two converge on the same observable
behavior — at most one in-flight message per sender — and that convergence is
exactly SQS FIFO's model. So:

**The precise industry name for property 3 is: per-`MessageGroupId` in-flight limit
of 1, i.e. single-active-message-per-sender, which yields per-sender serial
processing with cross-sender parallelism.** SQS FIFO ships this as its *default and
only* behavior. It is not exotic; it is the single most-requested guarantee that
drove AWS to build FIFO queues in 2016.

### 3.2 How the canonical systems implement it (the exact blocking semantic)

The operator's brief asks specifically *what the blocking semantic is* — sender-side
backpressure, in-flight-limit, or per-key serial dispatch. The industry answer:
**it is an in-flight-limit-of-1 per key, enforced at the consumer/broker, which
*manifests* as per-key serial dispatch, and is *usually not* enforced as sender-side
backpressure at all.** Details per system:

- **SQS FIFO:** the broker tracks, per `MessageGroupId`, whether a message is
  "in flight" (received but not yet deleted or visibility-timed-out). While one is
  in flight, `ReceiveMessage` **skips that group** and serves other groups. The
  sender is never blocked — it can keep enqueuing; the *messages* pile up in the
  group and are metered out one at a time. **The limit is on delivery, not on
  production.** This is the cleanest match to the operator's intent and it does
  *not* touch the sender.
- **Kafka:** structural. One partition → one consumer in the group → serial. No
  in-flight bookkeeping; the assignment *is* the lock. To block the *producer* you'd
  additionally cap `max.in.flight.requests.per.connection=1`, but that is a separate
  producer-side setting for ordering-under-retry, not the consumer guarantee.
- **Erlang/OTP:** the mailbox is serial by nature — a process handles one message
  from its mailbox at a time via its receive loop. Per-sender ordering plus
  one-at-a-time processing is automatic; "blocking sender S" is not a thing OTP
  does, because the receiver simply processes S's messages in order whenever it
  gets to them.
- **Temporal (workflow engine):** a **task queue** with **workflow-id serialization**
  — all tasks for one workflow execution are processed in strict sequence by design,
  different workflows in parallel. If the operator's mental model is "each sender is
  a workflow whose events must be handled in order," Temporal is the closest
  *architectural* match, and it handles crash-mid-processing natively (§4).

### 3.3 What this tells us the operator actually wants, in one line

**A per-sender in-flight limit of 1, enforced on the processing side, with
cross-sender parallelism** — SQS FIFO's delivery model, with `MessageGroupId =
sender`. The sender need not be blocked at the `swarm send` call at all; it is
sufficient (and cleaner) to block *the processor from picking up sender S's message
N+1 until message N is resolved.* Whether the org *also* wants true sender-side
backpressure (refusing `swarm send` while S has an unresolved message) is a real
fork, and it collides with a WORLD.md invariant — §8 states it: W:59 says "nothing
ever refuses a message to the operator," so **sender-side backpressure (Mechanism B
in its literal form) is forbidden by local law**, and the industry's cleaner
Mechanism-A form (meter on the processing side, never refuse the send) is both what
SQS does and what local law permits. That is a case where the industry answer and
the local rule happen to agree, and I flag it because the operator's word "block"
could be read the forbidden way.

---

## 4. Property 4 — "the executable runs in parallel for each agent" = a consumer group / partition-parallel workers

### 4.1 The industry name

This is a **consumer group over a partitioned queue** — parallelism bounded by, and
aligned to, the partition key.

- **Kafka consumer group:** N consumers share the partitions of a topic; each
  partition goes to exactly one consumer; consumers process their partitions in
  parallel. Parallelism is per-partition, and because the partition key is the
  sender, **you get exactly one worker per sender's stream, all senders in
  parallel** — the operator's property 4, verbatim.
- **SQS FIFO with multiple consumers:** distinct message-groups are handed to
  distinct receivers concurrently; within a group, serial. Same shape.
- **The "competing consumers" pattern (EIP)** constrained to **one consumer per
  key** — sometimes called **"consistent-hashing exchange"** (RabbitMQ) or
  **"partitioned consumer."**

Properties 3 and 4 are **the same mechanism seen from two sides**: "serial within a
sender, parallel across senders" is one sentence describing a partitioned consumer
group with in-flight-limit-1 per partition. The operator stated it as two bullets;
the industry states it as one pattern. That they decompose to one mechanism is
itself confirmation the framing is coherent and standard.

### 4.2 Where the substrate differs

In Kafka/SQS the parallelism is *managed* — the broker or group-coordinator assigns
partitions, rebalances on consumer join/leave, and guarantees no two consumers
touch one partition. Here, the operator's "runs in parallel for each agent" would
be **N cold subprocesses, one per sender with a waiting message, launched
concurrently** (HOOK §3's `subprocess.run` fanned out per sender). There is no
coordinator, no rebalance, no assignment protocol. The parallelism is real
(independent processes) but the *isolation guarantee* (no two workers on one
sender) must be enforced by a claim discipline (§6), not by a partition assignment.
This is the substrate's biggest structural gap from a broker: **partition
exclusivity is a convention here, a protocol invariant there.** The industry's
lesson (§6) is that you get exclusivity from an atomic claim — and the substrate
*has* one (`os.O_EXCL`, `os.replace` / `mv`), which is exactly the primitive
brokers use internally.

---

## 5. The edge cases — how the canonical systems handle what the org has been circling

The org's four wiring docs spend most of their length on three edge cases:
crash-mid-message, slow/poison processor, and the exact blocking/ordering
semantics. The industry has standard, named answers for all three. Here they are,
matched to what the docs found.

### 5.1 Crash mid-message

**Industry answer: at-least-once delivery + idempotent processing + a visibility
timeout.** No broker attempts exactly-once delivery at the transport layer (the
ones that claim it, like Kafka EOS, do it with transactional offset commits, a
heavier mechanism). The universal pattern:

1. Delivery makes a message **invisible** but does not delete it (SQS visibility
   timeout; Kafka uncommitted offset; AMQP unacked).
2. The consumer processes, then **acknowledges** (delete / commit / ack).
3. If the consumer crashes before acking, the visibility timeout expires and the
   message is **redelivered** to another consumer.
4. Because redelivery is possible, **processing must be idempotent** — the consumer
   must tolerate seeing the same message twice. This is the load-bearing discipline;
   "at-least-once + idempotent = effectively-once" is the industry's mantra.

**What the org re-derived, and what it's missing.** HOOK-WIRING's **write-then-invoke**
(HOOK §4: `queue_put` the message durably *before* invoking the hook) is the
**transactional outbox / write-ahead pattern** — persist first, act second, so a
crash never loses the record. That is exactly right and is the industry's answer to
"don't lose the message on crash." The org's **mv-and-abort** claim convention (DW
§1c: claim by `mv`, and if the `mv` fails because someone else claimed it first,
abort) is **optimistic concurrency control** — a compare-and-swap on the message's
location, the same primitive a broker uses to hand a message to exactly one
consumer. Both are correct re-derivations of industry mechanisms.

**What's missing is the redelivery leg.** HOOK §9 identifies the exact failure the
industry's visibility timeout exists to solve — a processor SIGKILLed after the
claim `mv` but before writing its result leaves an **orphan in `delivered/` with no
completion record** (HOOK §9, H-F7) — and then admits **no standing hand reconciles
it**; it's found by "the next human draining." In SQS that orphan is *automatically
redelivered* when the visibility timeout expires; here it is a manual `grep` at
some future drain. **The industry knows the answer the org flagged as an unsolved
residual: a visibility timeout with automatic requeue.** On this substrate that is a
**lease with expiry** — claim by moving to `inflight/<sender>/` with a timestamp,
and a sweeper (or the next processor pass) that returns any lease older than T back
to the queue. The org has no such sweeper because it deleted the standing process
that would run it (§7, §8). This is the single most valuable thing the industry
knows that the org hasn't built.

### 5.2 Slow processor

**Industry answer: the in-flight limit and the visibility timeout together bound
the damage; the slow message blocks only its own key.** In SQS FIFO, a slow
consumer on group G stalls G (head-of-line blocking within the group) but never
touches other groups — this is *by design* the price of per-key ordering, and it is
considered acceptable precisely because the blast radius is one key. Kafka: a slow
consumer lags its partition; consumer-group lag is *the* monitored metric, and a
persistently lagging consumer is evicted by the group coordinator (session timeout)
and its partition reassigned.

**What the org has:** HOOK §5 chose **synchronous** invocation — the sender's
`swarm send operator` blocks up to the timeout. In industry terms that is
**sender-side coupling to processor latency**, which brokers specifically avoid:
the whole point of a queue is to *decouple* producer latency from consumer latency.
A senior engineer would call synchronous invocation an anti-pattern here — it makes
every operator-send pay the processor's cold-start (HOOK §6 admits tens of seconds)
— and would decouple it: **enqueue, return immediately, let a warm consumer process
asynchronously** (§7). The org chose sync to get a "T-bounded narrowing" of a race
against the human (HOOK §5); the industry would observe that the race against the
human is unwinnable anyway on this substrate (§4 of HOOK, PIPE §5b — both correct),
so paying sender latency to narrow an unwinnable race buys little. **Decouple, and
accept the async model the substrate already is.**

### 5.3 Poison message

**Industry answer: the dead-letter queue (DLQ), gated by a redelivery counter.**
Universal across SQS, RabbitMQ, Azure Service Bus, Kafka (via a DLQ topic): after a
message has been redelivered N times without a successful ack (SQS
`maxReceiveCount`), the broker moves it to a **separate dead-letter queue** where it
stops blocking the main queue and a human/tooling can inspect it. This is *the*
answer to "a message that crashes the processor every time" — without it, a poison
message in a FIFO group blocks that group forever (SQS explicitly warns that a
poison message in a FIFO group is a HOL-blocking hazard and the DLQ is the escape).

**What the org has:** nothing named. HOOK's fail-open means a *timeout* passes the
message to the human, which is a partial poison-defense (a message that always times
out eventually reaches a human). But a message that makes the *processor itself*
crash (not time out) repeatedly, while blocking that sender's later messages, has no
counter and no DLQ — it would re-poison every processor pass. **The industry answer
is a redelivery counter + a `deadletter/` directory.** On this substrate: increment
a claim-attempt count in the lease record, and after N, move the message to
`queue/operator/deadletter/` where it no longer blocks the sender's stream and a
human inspects it. This pairs with the visibility timeout of §5.1 — they are the
same machinery (lease + counter + DLQ), and the org needs all of it or none.

### 5.4 The exact blocking semantic — settled

Collecting §3: the blocking semantic the operator wants is **an in-flight-limit of
1 per sender, enforced on the processing/claim side, manifesting as per-sender
serial dispatch, with a visibility-timeout lease so a crashed processor's hold
expires and a DLQ so a poison message stops blocking its sender after N attempts.**
That is SQS FIFO's model, complete. It is **not** sender-side send-refusal
(forbidden by W:59, and unnecessary), and it is **not** global serialization (that
would kill property 4).

---

## 6. What the industry knows that the wiring docs re-derived, missed, or can't have

A consolidated ledger, because this is the outside view's highest-value output.

| Industry mechanism | Canonical system | Org's status |
|---|---|---|
| Partition-by-key ordering (order within key, parallel across) | Kafka partitions, SQS `MessageGroupId` | **Not named.** The docs deliver global oldest-first; per-sender ordering is the operator's new ask (§1). Cheap to add — the key is already in the filename. |
| Generic per-message endpoint, policy in the handler not the channel | Lambda event-source, JMS MDB, EIP Message Endpoint | **Re-derived, correctly** (the operator's "not engine-specific" = mechanism/policy separation, §2). This is the framing's most sophisticated instinct. |
| Handler return contract: ack / nack / retry | SQS delete-vs-throw, AMQP ack/nack | **Re-derived as fail-open** (timeout/crash = nack-to-human, answer = ack; HOOK §2–3). Sound. |
| Transactional outbox / write-ahead: persist before acting | Outbox pattern; SQS durability | **Re-derived as write-then-invoke** (HOOK §4). Exactly right; the docs' soundest single claim. |
| Optimistic concurrency / CAS to hand a message to one worker | Kafka partition assignment, SQS receipt-handle | **Re-derived as mv-and-abort** (DW §1c). Correct; `os.O_EXCL`/`mv` *is* the CAS primitive brokers use. |
| **Visibility timeout + automatic requeue** (crash recovery) | SQS visibility timeout, AMQP unacked-requeue, Kafka session timeout | **MISSING.** The org flagged the exact failure (HOOK §9 orphan, H-F7) and left it as an un-reconciled residual. The industry auto-recovers it with a lease-with-expiry. **§5.1 — highest-value gap.** |
| **Dead-letter queue + redelivery counter** (poison message) | SQS DLQ + `maxReceiveCount`, RabbitMQ DLX | **MISSING.** No counter, no DLQ; a processor-crashing message could re-poison every pass and HOL-block its sender. **§5.3.** |
| Producer/consumer latency **decoupling** (async processing) | every broker's reason to exist | **Rejected in favor of sync** (HOOK §5). The industry would call sync here an anti-pattern (§5.2). |
| Warm consumer / poll loop amortizing startup | Lambda warm containers, Kafka consumer, AMQP prefetch | **Rejected — cold per message** (HOOK §6), which the doc itself prices as making timeouts modal. The industry would run it warm (§7). |
| Consumer-group coordination: exclusive partition assignment, rebalance | Kafka group coordinator | **Can't have natively** — no broker process; exclusivity is a claim convention, not a protocol (§4.2). The substrate's `mv` gives per-message exclusivity but not standing partition ownership. |

**And the one thing the industry can't teach here, which the docs got right by
being forced to:** the operator queue has **no consumer the broker controls — the
terminal consumer is a human reading a flat `ps` list** (W:57-61, bin/swarm:610-611,
933-943). Every broker's ordering and blocking guarantee assumes the broker owns
dispatch to the consumer. Here the tool *never delivers to the operator queue* —
that is the load-bearing asymmetry PROXY §1 and PIPE §5b both found. So **no
mechanism on this substrate can order the processor relative to the human**, which
is precisely the guarantee HOOK and PIPE spent themselves proving un-buildable, and
they were right. The industry has no counter-lesson because the industry never
builds a queue whose final consumer is outside the broker's control. **This is the
one place the org's local knowledge beats the projection**, and I say so: on the
human-facing edge, trust the wiring docs, not this document.

---

## 7. The projection — what a senior infra engineer builds, element by element

Having never heard this repo's doctrine, here is the design I'd build for "an
operator mailbox, per-sender ordered, with a per-message processor that serializes
per sender and parallelizes across senders." I map each element onto what exists
here.

### 7.1 The queue: a partitioned log, key = sender

- **Industry:** an SQS FIFO queue with `MessageGroupId = senderId`, or a Kafka topic
  partitioned by sender.
- **Projected onto swarm:** `queue/operator/` **is already** a partitioned log —
  files are `{ts}-{sender}.json` (bin/swarm:264). No change to the write path; the
  partition key and sequence number are already in every filename. A per-sender
  view is `group by suffix, sort by prefix`. **Cost: zero new state; a read
  convention.** (W stays intact — this is a *view*, not a stored index.)

### 7.2 The processor: a warm, single-active-per-sender consumer

- **Industry:** a consumer group; one worker per partition; each worker runs a poll
  loop, processes its partition's head message, acks, advances. In-flight-limit 1
  per partition gives per-sender serial; multiple workers give cross-sender parallel.
- **Projected onto swarm:** a **warm processor** that polls `queue/operator/`,
  groups by sender, and for each sender with no in-flight message, claims the head
  message and runs the configured executable on it. Concretely: it can fan out one
  cold `subprocess.run` **per sender** (honoring property 4's parallelism and
  property 3's per-sender serialism — never two concurrent invocations for one
  sender), or hold a warm handler. **The key correction vs the org's current design:
  the poll loop is warm even if each handler invocation is a cold subprocess** —
  startup is amortized at the loop level, and the loop enforces the per-sender
  in-flight limit that a pile of independent per-send subprocesses cannot. This is
  the standing engine the org deleted (HOOK §1) — see §8.

### 7.3 The claim: an atomic lease with expiry (visibility timeout)

- **Industry:** receive → invisible-with-timeout → process → delete; timeout expiry
  requeues.
- **Projected onto swarm:** claim by `os.replace`/`mv` of the message into
  `queue/operator/inflight/<sender>/` with the claim timestamp in a sidecar (or the
  claim line in the operator ledger, DW §3b). The `mv` is the atomic
  compare-and-swap (only one worker wins — DW §1c already relies on this). **Add what
  the org lacks:** a **lease expiry** — any file in `inflight/` older than T is
  returned to `queue/operator/` by the next processor pass (or a sweep step). This
  turns HOOK §9's un-reconciled orphan (H-F7) into an auto-recovered redelivery,
  which is the whole point of a visibility timeout. **This is the single most
  important addition the projection makes.**

### 7.4 The result contract: ack / nack / DLQ

- **Industry:** success ⇒ delete; failure ⇒ requeue up to `maxReceiveCount` then DLQ.
- **Projected onto swarm:**
  - **Handled** (executable returns an answer): move to `queue/operator/delivered/`
    with a completion record — the ack. (DW §3b's claim ritual is already this.)
  - **Passed** (timeout / not-configured / crash-without-claim): leave in
    `queue/operator/` for the human — the nack-to-human. (HOOK §3's fail-open,
    correct.)
  - **Poison** (repeatedly crashes the processor): a **redelivery counter** in the
    lease; after N, move to `queue/operator/deadletter/` and stop retrying that
    sender's head so the sender's later mail unblocks. **This is new** and it is
    §5.3's missing DLQ.

### 7.5 Identity of the processor's replies

- **Industry:** a consumer that acts on a message acts *as itself* — its own
  service identity in traces and downstream calls. Never impersonate the producer or
  the system.
- **Projected onto swarm:** the processor replies in **its own wire name**, injected
  via `SWARM_AGENT_ID` (HOOK §7 got this exactly right — a bare subprocess inherits
  the sender's env and launders the reply under the sender or the OPERATOR header).
  The industry principle — *the handler is a distinct principal, attribute to it* —
  is identical to HOOK §7's identity rule. No divergence; the org's instinct here is
  the industry's.

### 7.6 Backpressure — on the processing side only, never refuse the send

- **Industry:** meter delivery per key (in-flight limit); do not block the producer
  unless the buffer is truly full. For a mailbox to a human, you *never* drop or
  refuse — you queue and meter.
- **Projected onto swarm:** the in-flight-limit-1-per-sender lives in the processor's
  claim logic (don't claim sender S's message N+1 while N is in-flight), **not** in
  `cmd_send`. `swarm send operator` always succeeds and always durably enqueues
  (W:59, and queue_put's never-drop). This is where the industry answer and local
  law agree (§3.3, §8).

### 7.7 Observability: consumer lag and in-flight age

- **Industry:** monitor consumer-group lag (backlog age) and in-flight message age;
  alarm on a stuck partition.
- **Projected onto swarm:** `swarm ps` already shows operator queue depth and
  idle-since (bin/swarm:933-943). Add nothing new for the human; the processor's
  ledger and `inflight/` timestamps are the lag signal a maintainer greps. (The org
  would resist a new view — PHILOSOPHY §8's standing bias, "prompt-level convention
  first, a visibility verb second, an engine never — unless the record shows the
  convention failing" — and here a new view is unnecessary; the signals already
  exist.)

---

## 8. Where the industry answer collides with local law — stated plainly

My brief says to state conflicts plainly and let the org resolve them. Here they
are, each with the industry's reasoning, not softened.

**Conflict 1 — the warm standing consumer vs the deleted standing engine.** The
industry builds the processor as a **warm, long-lived consumer** (§2.3, §7.2): it is
the only way to amortize startup, hold the per-sender in-flight limit, and run the
lease-expiry sweeper. The org **deleted exactly this** — HOOK §1 celebrates that the
operator's correction "dissolves the standing engine entirely… no custody queue, no
reclaim sweep." **The industry's reasoning:** the standing consumer is not
incidental complexity; it is *where the ordering, in-flight-limit, and crash-recovery
guarantees live.* A cold-per-message processor cannot enforce a per-sender in-flight
limit (nothing coordinates two independent subprocesses for the same sender) and
cannot run a visibility-timeout sweeper (nothing is standing to sweep). **Properties
3 and 4 as the operator stated them essentially require a standing coordinator** —
you cannot get "serial per sender, parallel across senders, with crash recovery"
from stateless per-message fan-out. The org's cold-hook design can approximate it
per-message but cannot guarantee it. **This is the deepest conflict: the operator's
own four properties point back at the standing engine the org just deleted.** I
report it; resolving it is the org's call.

**Conflict 2 — asynchronous decoupling vs synchronous invocation.** The industry
decouples producer and consumer latency (§5.2); the org chose synchronous
(HOOK §5), paying the sender the processor's cold-start on every operator send. The
industry's reasoning: coupling the producer to consumer latency defeats the queue's
purpose and, here, buys only a narrowing of a race the substrate makes unwinnable
anyway (§5.2). **Recommendation: async.** This conflicts with HOOK §5's reasoning
but *not* with any WORLD.md sentence — it's a design-quality conflict, not a
contract one.

**Conflict 3 — a dead-letter queue vs the graves' aversion to states-on-the-wire.**
The industry's poison-message answer is a `deadletter/` directory plus a redelivery
counter (§5.3). The org's anthropology is hostile to exactly this shape: SIMPLEST
deleted the "inbox three-state machine: `inbox/` → `rendered/` → `read/`"
(SIMPLEST §2 row 13), and DECISIONS names "Grave 2 — the `type` field… wire-side and
consumerless" (DECISIONS §2). The recorded cause of death for these is
**states-with-no-consumer on the wire**. **The industry's reasoning for why a DLQ is
different:** a DLQ is *not* a no-consumer state — its consumer is the maintainer who
inspects poison messages, and its purpose is to *unblock the per-sender FIFO*, a real
need with a real reader. The graves killed folders *nobody drained*; a DLQ is drained
by whoever fixes poison messages, which is the same "definer-is-consumer" test the org
itself applies (DECISIONS §2). If the org wants per-sender HOL blocking (property 3),
it needs the DLQ, because per-key FIFO **without** a DLQ means one poison message
blocks a sender forever — SQS's own documented hazard. **You cannot take property 3
and refuse the DLQ; they are a package.** I state it; the org decides whether property
3 is worth the folder.

**Conflict 4 — sender-side backpressure vs "nothing ever refuses a message to the
operator" (W:59).** IF the operator meant property 3 as literal Mechanism-B
send-refusal (block the `swarm send` while S has an unresolved message), that
**violates W:59** outright. The industry doesn't need it — the in-flight limit lives
on the processing side (§3, §6, §7.6) — so here local law and the industry's cleaner
form **agree**, and the literal-backpressure reading should be dropped. I flag it
only because "block any new message from that agent" can be misread as refusing the
send, which the contract forbids and the better design avoids anyway.

**Where local law rightly beats the projection (stated for symmetry):** no
mechanism can order the processor relative to the *human*, because the human is a
consumer outside the tool's dispatch (W:57-61, bin/swarm:610-611). PIPE §5b and
HOOK's KILL-1 are correct and the industry has no counter-lesson (§6, last
paragraph). Any projection that promises the human sees "only processed mail" is
wrong on this substrate. Trust the docs here.

---

## 9. What I would build first

If the org wants the operator's four properties for real, the industry build order
is:

1. **The per-sender view (§7.1) — zero cost, do it regardless.** Group
   `queue/operator/` by the `-{sender}` filename suffix, order each group by the
   `{ts}` prefix. This *is* property 1, and it needs no new state, no contract
   touch, and no standing process. It is pure upside and it is the foundation
   properties 3–4 sit on. **Ship this first, alone, and see if it's enough** — often
   the ordering view is all anyone needed.

2. **A warm poll-loop processor with per-sender in-flight-limit 1 (§7.2) —** the
   heart of properties 3 and 4. This resurrects a standing consumer (Conflict 1) and
   is the real decision. Build it warm; fan out one handler invocation per sender;
   never two for one sender concurrently. If the org will not accept a standing
   consumer, then properties 3 and 4 cannot be *guaranteed* — only approximated
   per-message — and that limitation should be stated to the operator, because it is
   inherent, not incidental.

3. **The lease-with-expiry (visibility timeout, §7.3, §5.1) —** turns HOOK §9's
   un-reconciled orphan into automatic redelivery. Build it *with* the warm
   processor (the loop is what sweeps expired leases); it is nearly free once the
   loop exists and it closes the org's biggest named-but-unsolved gap.

4. **The redelivery counter + DLQ (§7.4, §5.3) —** only if property 3 (per-sender
   HOL blocking) is actually adopted, because that's what makes a poison message
   dangerous. If the org keeps races-allowed (no per-sender serialism), skip it.

5. **Async decoupling (§5.2, Conflict 2) —** flip the invocation from synchronous to
   fire-and-forget-into-the-warm-loop. Do this whenever the warm processor lands; it
   falls out for free and removes the sender-latency the cold-sync design pays.

**The honest headline for the operator:** properties 1 (per-sender ordering) and the
generic-processor framing (property 2) are cheap, standard, and safe — build them.
Properties 3 and 4 (per-sender serial, cross-sender parallel, with crash and poison
handling) are *also* standard — they are SQS FIFO — but on this substrate they
**require a standing coordinator**, which is the exact thing the org's latest
correction deleted. That is not a flaw in the operator's framing; it is the
framing's honest cost, and it is the industry's cost too: **you do not get per-key
serial-with-parallel-and-recovery from stateless fan-out — you get it from a
consumer group, and a consumer group is a standing thing.** The operator has, in
four bullets, re-specified SQS FIFO. The only question the org must answer is
whether it will run the standing consumer that SQS FIFO's guarantees require, or
accept the weaker per-message approximation its doctrine currently prefers.

---

## 10. Summary

The operator's four properties are, precisely: **(1)** partitioned FIFO keyed by
sender (Kafka partitions / SQS `MessageGroupId` / Erlang per-mailbox order); **(2)**
a generic per-message endpoint with policy in the handler, not the channel (Lambda
event-source / JMS MDB / EIP Message Endpoint); **(3)** per-sender in-flight-limit
of 1 enforced on the processing side, i.e. single-active-message-per-sender (SQS
FIFO's exact delivery guarantee), **not** sender-side send-refusal (which W:59
forbids and which is unnecessary); **(4)** a partition-parallel consumer group
(Kafka consumer group / competing-consumers-per-key). Properties 3 and 4 are one
mechanism — a partitioned consumer group with in-flight-limit 1 — seen from two
sides. **Together they are SQS FIFO.**

The org's wiring docs have **re-derived** several industry mechanisms correctly
under local names — write-then-invoke = transactional outbox, mv-and-abort =
optimistic concurrency, fail-open = nack-to-human, the identity injection =
attribute-to-the-handler — and this is to their credit. They are **missing** the
two mechanisms the industry considers mandatory for a keyed FIFO with a fallible
processor: the **visibility-timeout lease** (auto-recovers the crash-mid-message
orphan the org flagged but left unsolved, HOOK §9/H-F7) and the **dead-letter queue
+ redelivery counter** (the poison-message escape without which per-sender FIFO
blocks a sender forever). They **diverge** from the industry, at real cost, on two
design choices — cold-per-message vs warm consumer, and synchronous vs async — both
of which the industry would reverse.

The genuine substrate difference that makes projection mislead is singular and the
docs found it first: **the operator queue's terminal consumer is a human outside the
tool's dispatch** (W:57-61, bin/swarm:610-611), so nothing can order the processor
relative to the human — HOOK's and PIPE's un-buildability findings are correct and
the industry has no counter. Build the per-sender view now (free); build the warm
consumer with a lease and DLQ if properties 3 and 4 are wanted for real — and tell
the operator plainly that those two properties re-specify SQS FIFO and therefore
require the standing consumer the org's doctrine has been trying to delete.
