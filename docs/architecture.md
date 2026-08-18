---
title: Architecture
description: >-
  Constle's four layers — runtime and sandbox, identity and governance,
  communication, and the planned commerce layer.
---

# The four layers

--8<-- "README.md:architecture-intro"

<figure class="constle-diagram" markdown>
![Four stacked layers. 01 Runtime and Sandbox, shipped: Firecracker microVM or
two-network Docker sandbox, no default route, Squid egress allowlist, wall-clock
kill switch — internal/sandbox/. 02 Identity and Governance, shipped: W3C did:key
identity, signed and hash-chained audit log, human gates at the MCP proxy,
per-run and per-day USD ledger — internal/identity/, internal/audit/,
internal/mcpgate/, internal/spending/. 03 Communication, shipped: A2A Ed25519-signed
envelopes, host-side sign and verify, declared peers only, no discovery by design —
internal/a2a/. 04 Commerce, planned and drawn in outline: direction only, no code
yet, tracked in ROADMAP.md.](assets/diagrams/architecture-light.svg#only-light)
![Four stacked layers. 01 Runtime and Sandbox, shipped: Firecracker microVM or
two-network Docker sandbox, no default route, Squid egress allowlist, wall-clock
kill switch — internal/sandbox/. 02 Identity and Governance, shipped: W3C did:key
identity, signed and hash-chained audit log, human gates at the MCP proxy,
per-run and per-day USD ledger — internal/identity/, internal/audit/,
internal/mcpgate/, internal/spending/. 03 Communication, shipped: A2A Ed25519-signed
envelopes, host-side sign and verify, declared peers only, no discovery by design —
internal/a2a/. 04 Commerce, planned and drawn in outline: direction only, no code
yet, tracked in ROADMAP.md.](assets/diagrams/architecture-dark.svg#only-dark)
</figure>

--8<-- "README.md:architecture-detail"

## Layer by layer

=== "Layer 1 — Runtime & Sandbox"

    !!! shipped "Shipped"

        `internal/sandbox/`

    A Firecracker microVM or a two-network Docker sandbox, in both cases with
    **no default route**. Egress traverses a Squid proxy that allowlists
    `network.allowed_hosts` by name, and a wall-clock kill switch stops the
    agent when `limits.max_duration_seconds` elapses.

    Both backends render their proxy policy from the same function, so Docker
    and Firecracker enforce one ruleset rather than two that drift.

    [How network isolation actually works :octicons-arrow-right-24:](network-isolation.md)

=== "Layer 2 — Identity & Governance"

    !!! shipped "Shipped"

        `internal/identity/` · `internal/audit/` · `internal/mcpgate/` ·
        `internal/spending/`

    A W3C `did:key` identity whose private key never enters the sandbox; a
    JSONL audit log that is Ed25519-signed and hash-chained once a DID is
    declared; human approval gates at the MCP proxy; and a per-run and
    per-day USD ledger metered at the tool-call boundary.

    The daily ledger is durable across runs and keyed by DID, so renaming an
    agent does not reset its spend.

    [Spending and gate caveats :octicons-arrow-right-24:](limitations.md)

=== "Layer 3 — Communication"

    !!! shipped "Shipped"

        `internal/a2a/`

    Agent-to-agent messages as Ed25519-signed envelopes, exchanged only with
    peers named in the manifest. The **host** signs and verifies; the sandbox
    performs no cryptography and never learns a peer's real endpoint.

    There is no discovery mechanism, by design — an agent can only talk to
    what its manifest declared before it started.

=== "Layer 4 — Commerce"

    !!! planned "Planned — no code in this repository"

        Agents discovering and paying each other for work. Direction only;
        see [ROADMAP.md](https://github.com/constle/constle/blob/main/ROADMAP.md).

## Why the direction of control matters

Every layer above runs in the host `constle` process. The agent runs in the
sandbox, and the two are not peers: the agent's private key, the real MCP
server URLs, and the real A2A peer endpoints are all host-side and never
cross the boundary. What the agent sees is a set of per-run gate addresses.

That is the whole security argument, and it is worth stating plainly, because
it is what separates Constle from a monitoring overlay:

!!! quote ""

    A control the agent can reach is a control the agent can be talked into
    disabling. These controls are not reachable from inside the sandbox — not
    because the agent is trusted to leave them alone, but because there is no
    route, no key, and no endpoint in there to act on.

A prompt injection that convinces the model to exfiltrate a document does not
fail because the model reconsiders. It fails at the network layer, below the
model, and the attempt is written to the audit log as a `network_blocked`
event — which is how the operator finds out it happened at all.
