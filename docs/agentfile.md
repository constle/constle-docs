---
title: The Agentfile
description: >-
  One declarative YAML file describing what an agent needs. Annotated example
  plus pointers into the full field reference.
---

# The Agentfile

--8<-- "README.md:agentfile"

## Enforcement labels

The [field reference](reference/agent-manifest.md) tags every field with one of
four labels. The distinction between the middle two is the one that matters: a
`DECLARED` field parses, validates, and does nothing.

| Label | Meaning |
|---|---|
| <span class="constle-pill constle-pill--shipped">Enforced</span> | The runtime actively prevents violations at execution time. |
| <span class="constle-pill">Validated</span> | Checked for well-formedness at parse time. Not enforced during execution. |
| <span class="constle-pill constle-pill--planned">Declared</span> | Parsed and audit-logged; the runtime does not act on it yet. |
| <span class="constle-pill">Informational</span> | Not read by the runtime at all. For humans and external tooling. |

## Full reference

- [Field reference](reference/agent-manifest.md) — every section and field of
  the AgentManifest, with types, defaults, and enforcement labels.
- [Annotated example file](https://github.com/constle/constle/blob/main/spec/agent-manifest.yaml)
  — `spec/agent-manifest.yaml`, executable rather than aspirational.
  `constle validate` passes on it.
- [A2A specification](https://github.com/constle/constle/blob/main/spec/a2a.md)
  — envelope format, signing, and the peer model behind the `a2a` section.
- [Identity specification](https://github.com/constle/constle/blob/main/spec/identity.md)
  — `did:key` generation, key storage, and how a run fails closed on a missing
  key.
