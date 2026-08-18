---
title: Known limitations
description: >-
  Five places where an Agentfile field currently looks stronger than the
  Constle runtime actually is, each traced to the code that makes it so.
---

# Known limitations

--8<-- "README.md:limitations-intro"

<figure class="constle-diagram" markdown>
![Five warning cards. One: human gates match tool names by exact string, nothing
else — a gate fires only on a byte-exact match to the MCP tool name, and an
unmatched entry warns loudly rather than failing silently. Two: max_per_month_usd
is parsed but not enforced — only max_per_run_usd and max_per_day_usd are. Three:
traffic through allowed_hosts isn't metered for spending — cost is metered only at
the MCP gate, because metering plain HTTPS would mean TLS-intercepting the agent.
Four: the A2A replay guard is in-memory and per-run — the seen-ID set does not
survive a restart. Five: sandbox.network.egress is declared but has no consumer —
allowed_hosts is the entire network
policy.](assets/diagrams/known-limitations-light.svg#only-light)
![Five warning cards. One: human gates match tool names by exact string, nothing
else — a gate fires only on a byte-exact match to the MCP tool name, and an
unmatched entry warns loudly rather than failing silently. Two: max_per_month_usd
is parsed but not enforced — only max_per_run_usd and max_per_day_usd are. Three:
traffic through allowed_hosts isn't metered for spending — cost is metered only at
the MCP gate, because metering plain HTTPS would mean TLS-intercepting the agent.
Four: the A2A replay guard is in-memory and per-run — the seen-ID set does not
survive a restart. Five: sandbox.network.egress is declared but has no consumer —
allowed_hosts is the entire network
policy.](assets/diagrams/known-limitations-dark.svg#only-dark)
<figcaption>All five at a glance. Each one is stated in full below, with the
source file that makes it so.</figcaption>
</figure>

--8<-- "README.md:limitations-detail"
