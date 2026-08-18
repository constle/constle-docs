---
title: Network isolation
description: >-
  How the sandbox's no-default-route topology and the Squid allowlist proxy
  combine into a network policy the agent cannot step around.
---

# How network isolation actually works

<figure class="constle-diagram" markdown>
![The agent sandbox has no default route. Its only next hop is the Squid proxy,
which checks network.allowed_hosts by dstdomain match, not by IP. api.groq.com is
CONNECT ALLOWED — the TLS tunnel opens and the server replies. evil.example.com is
CONNECT REFUSED with a 403; the tunnel is never opened. A note reads: matching is by
name, but blocking isn't — a separate rule denies destinations given as raw IPs,
including the real IP of an allowed host, so resolving a hostname yourself and
connecting straight to the address is not a way around the allowlist. Both attempts
appear in internal/audit/egress-probe-2026-08-08.jsonl as a network_allowed and a
network_blocked event.](assets/diagrams/network-isolation-light.svg#only-light)
![The agent sandbox has no default route. Its only next hop is the Squid proxy,
which checks network.allowed_hosts by dstdomain match, not by IP. api.groq.com is
CONNECT ALLOWED — the TLS tunnel opens and the server replies. evil.example.com is
CONNECT REFUSED with a 403; the tunnel is never opened. A note reads: matching is by
name, but blocking isn't — a separate rule denies destinations given as raw IPs,
including the real IP of an allowed host, so resolving a hostname yourself and
connecting straight to the address is not a way around the allowlist. Both attempts
appear in internal/audit/egress-probe-2026-08-08.jsonl as a network_allowed and a
network_blocked event.](assets/diagrams/network-isolation-dark.svg#only-dark)
</figure>

--8<-- "README.md:network"
