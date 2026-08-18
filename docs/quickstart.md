---
title: Quickstart
description: >-
  Build the Constle CLI, validate a manifest, run an agent inside a sandbox,
  and verify its signed audit log — in about a minute.
---

# 60-second quickstart

!!! note "You will need"

    **Go 1.26+** to build the CLI, **Docker** for the sandbox backend, and a
    free [Groq API key](https://console.groq.com) for the example agent.
    Firecracker is optional — the CLI auto-detects a backend and falls back to
    Docker.

--8<-- "README.md:quickstart"

## Where to go next

- [The Agentfile](agentfile.md) — every field the runtime consumes, and what
  each one is actually enforced by.
- [Architecture](architecture.md) — what the sandbox, the proxy, and the gates
  are each doing during that run.
- [Known limitations](limitations.md) — why the run above printed
  `NOT ENFORCED`, and four other gaps like it.
