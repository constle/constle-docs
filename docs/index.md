---
title: Overview
description: >-
  A runtime that enforces what an AI agent is allowed to do — network, spend,
  approvals, identity — from outside the agent.
---

# Constle

--8<-- "README.md:pitch"

Constle runs an AI agent inside a sandbox with no default route, allowlists
every packet it sends, meters what it spends, pauses sensitive calls for a
human, and signs the audit log. None of that runs in the agent's process — so
there is nothing in there for a prompt injection to switch off.

Three of the four layers are shipped. The [quickstart](quickstart.md) builds the
CLI and runs a real agent under enforcement in about a minute; the
[architecture](architecture.md) explains what each layer is doing while it runs.

<figure class="constle-diagram constle-diagram--wide" markdown>
![How a request moves through Constle. The agent process runs in the sandbox. Its
network calls go to the Squid proxy, which checks network.allowed_hosts and marks
each one ALLOWED or BLOCKED. Its tool calls go to the MCP gate proxy, which checks
human_gates.require_approval_for and hands a matching call to a human to approve or
deny; APPROVED calls are forwarded, DENIED or TIMEOUT stops the run under
on_timeout abort. Every outcome — allow, block, and gate decision alike — is written
to the signed, hash-chained audit log in
internal/audit/.](assets/diagrams/flow-light.svg#only-light)
![How a request moves through Constle. The agent process runs in the sandbox. Its
network calls go to the Squid proxy, which checks network.allowed_hosts and marks
each one ALLOWED or BLOCKED. Its tool calls go to the MCP gate proxy, which checks
human_gates.require_approval_for and hands a matching call to a human to approve or
deny; APPROVED calls are forwarded, DENIED or TIMEOUT stops the run under
on_timeout abort. Every outcome — allow, block, and gate decision alike — is written
to the signed, hash-chained audit log in
internal/audit/.](assets/diagrams/flow-dark.svg#only-dark)
<figcaption>Every path an agent's request can take, and the one place they all
end up.</figcaption>
</figure>

## Enforcement, demonstrated

--8<-- "README.md:demo"

## What Constle enforces

<figure class="constle-diagram" markdown>
![Capability, mechanism and status for nine capabilities. Sandboxed execution:
Firecracker microVM or two-network Docker sandbox, no default gateway, falls back
loudly, never silently — shipped. Network egress: Squid proxy allowlist, name-based
matching, raw-IP bypass blocked, every allow and block audited — shipped. Max
duration: the agent is killed when max_duration_seconds elapses, recorded as
terminated_by_limit — shipped. Audit log: signed, hash-chained JSONL per agent per
day, constle audit verify catches tampering — shipped. Spending limits: hard
per-run and per-day USD caps metered at the MCP gate, daily ledger durable across
runs — shipped. Human gates: a protocol-aware gate proxy pauses sensitive tool calls
for approval and times out to abort — shipped. Cryptographic identity: W3C did:key
Ed25519, the private key never enters the sandbox, fails closed if missing —
shipped. Agent-to-agent messaging: signed envelopes to declared peers only, no
discovery mechanism by design — shipped. Agent commerce: not
built.](assets/diagrams/capability-grid-light.svg#only-light)
![Capability, mechanism and status for nine capabilities. Sandboxed execution:
Firecracker microVM or two-network Docker sandbox, no default gateway, falls back
loudly, never silently — shipped. Network egress: Squid proxy allowlist, name-based
matching, raw-IP bypass blocked, every allow and block audited — shipped. Max
duration: the agent is killed when max_duration_seconds elapses, recorded as
terminated_by_limit — shipped. Audit log: signed, hash-chained JSONL per agent per
day, constle audit verify catches tampering — shipped. Spending limits: hard
per-run and per-day USD caps metered at the MCP gate, daily ledger durable across
runs — shipped. Human gates: a protocol-aware gate proxy pauses sensitive tool calls
for approval and times out to abort — shipped. Cryptographic identity: W3C did:key
Ed25519, the private key never enters the sandbox, fails closed if missing —
shipped. Agent-to-agent messaging: signed envelopes to declared peers only, no
discovery mechanism by design — shipped. Agent commerce: not
built.](assets/diagrams/capability-grid-dark.svg#only-dark)
</figure>

??? note "The same nine rows as text, with the caveats spelled out"

    The diagram above is a summary. This is the table it summarises — longer, and
    the version to search, copy, or read with a screen reader.

    --8<-- "README.md:enforces"

## What Constle is not

--8<-- "README.md:isnot"

## Before you rely on any of this

!!! warning "The gaps are documented, not hidden"

    Spending is metered only at the MCP gate, `max_per_month_usd` parses but
    does nothing, and `sandbox.network.egress` has no consumer at all.
    [The full list](limitations.md) is short and worth the two minutes.
