# Constle docs

Source for the Constle documentation site, published to
**[docs.constle.dev](https://docs.constle.dev)**.

Constle itself lives in [constle/constle](https://github.com/constle/constle).

## Building it

Most of the prose on the site is not in this repository. The pages pull marked
sections out of `constle/constle`'s `README.md` and `spec/` with
`pymdownx.snippets`, so that there is one source of truth for it and the site
cannot drift from what the project actually says. That repository has to be
checked out to `_upstream/` before the site will build:

```bash
git clone https://github.com/constle/constle-docs
cd constle-docs
git clone --depth 1 https://github.com/constle/constle _upstream

python -m venv .venv && source .venv/bin/activate
pip install -r docs/requirements.txt

mkdocs serve
```

`_upstream/` is gitignored. If it is missing the build fails at the first
include rather than publishing pages with the prose silently absent.

CI does the same thing with a second `actions/checkout` step, so a push here
builds against `constle/constle`'s `main`.

## Licence

Apache 2.0 — see [LICENSE](LICENSE).
