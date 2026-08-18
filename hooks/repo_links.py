"""Rewrite repo-relative links that arrive inside snippet-included text.

The docs pages do not copy the README or the specs; they pull marked sections
out of the real files with `pymdownx.snippets`, so there is exactly one source
of truth for that prose. The cost of that is links: inside README.md a link
like `[ROADMAP.md](ROADMAP.md)` or `[Known limitations](#known-limitations)`
resolves against the repository, and once the same text is rendered on a docs
page those targets are either somewhere else or nowhere at all.

This hook closes that gap at build time, so authors keep writing plain
repo-relative links in the README and the site stays correct.

**Where this runs, and why it has to run there.** Snippets is a Markdown
*preprocessor* (priority 32), so it expands long after MkDocs' `on_page_markdown`
event has already fired — a hook using that event would only ever see
`--8<-- "README.md:quickstart"`, never the text it pulls in. So the rewrite is
registered as a *treeprocessor* at priority 2 instead: that is after every
preprocessor (all snippets are expanded and the tree is built) and before
MkDocs' own `relpath` treeprocessor at priority 0, which is what resolves
internal links and emits the "target is not found" warnings. Operating on the
element tree also means link targets in code samples are untouched for free —
a path inside a fenced block is text in a `<code>` element, never an `href`.

One rule keeps this honest rather than magic: a target with no entry in
`LINK_MAP` is left exactly as written, so MkDocs' own link validation still
reports it. A new repo-relative link in the README surfaces as a build warning
instead of silently 404ing on the site.
"""

from __future__ import annotations

import posixpath
from typing import TYPE_CHECKING

import markdown
from markdown.treeprocessors import Treeprocessor

if TYPE_CHECKING:
    from xml.etree import ElementTree as etree

# Repo-relative link target -> replacement.
#
# Values that are absolute URLs are used as-is. Values that are docs-root-
# relative paths are converted to page-relative ones below, so a page at any
# nesting depth links correctly and MkDocs can still validate the target.
LINK_MAP: dict[str, str] = {
    # Source files that have a page on this site.
    "spec/agent-manifest.md": "reference/agent-manifest.md",
    # Files that stay in the repository and have no page here.
    "LICENSE": "https://github.com/constle/constle/blob/main/LICENSE",
    "ROADMAP.md": "https://github.com/constle/constle/blob/main/ROADMAP.md",
    "CONTRIBUTING.md": "https://github.com/constle/constle/blob/main/CONTRIBUTING.md",
    "SECURITY.md": "https://github.com/constle/constle/blob/main/SECURITY.md",
    "spec/a2a.md": "https://github.com/constle/constle/blob/main/spec/a2a.md",
    "spec/identity.md": "https://github.com/constle/constle/blob/main/spec/identity.md",
    "spec/agent-manifest.yaml": (
        "https://github.com/constle/constle/blob/main/spec/agent-manifest.yaml"
    ),
    # In-README anchors whose sections became pages of their own. Each maps to
    # the page that now holds the section.
    "#known-limitations": "limitations.md",
    "#verifying-a-release": "cli.md#verifying-a-release",
}


class _RepoLinkTreeprocessor(Treeprocessor):
    """Rewrite `href`s listed in `LINK_MAP` before MkDocs resolves them."""

    def run(self, root: etree.Element) -> None:
        page_dir = posixpath.dirname(self._current_src_uri())

        for element in root.iter("a"):
            href = element.get("href")
            if href is None:
                continue
            replacement = LINK_MAP.get(href)
            if replacement is None:
                continue
            element.set("href", self._resolve(replacement, page_dir))

    def _current_src_uri(self) -> str:
        """The source path of the page being rendered.

        MkDocs builds a fresh `Markdown` instance per page and registers its
        `relpath` treeprocessor with that page's `File` attached, which makes it
        the authoritative answer to "which page is this?" and avoids threading
        page state through module-level globals.
        """
        registry = self.md.treeprocessors
        if "relpath" not in registry:
            # Not running under MkDocs (e.g. a direct Markdown conversion in a
            # test); page-relative resolution is meaningless, so treat the docs
            # root as the current directory.
            return ""
        return getattr(registry["relpath"].file, "src_uri", "") or ""

    @staticmethod
    def _resolve(replacement: str, page_dir: str) -> str:
        if replacement.startswith(("http://", "https://", "#", "/")):
            return replacement
        return posixpath.relpath(replacement, page_dir or ".")


class _RepoLinkExtension(markdown.Extension):
    def extendMarkdown(self, md: markdown.Markdown) -> None:  # noqa: N802
        # Priority 2: after all preprocessors (snippets have been expanded) and
        # before MkDocs' `relpath` treeprocessor at priority 0.
        md.treeprocessors.register(_RepoLinkTreeprocessor(md), "constle_repo_links", 2)


def on_config(config):
    """Register the rewrite as a Markdown extension instance.

    MkDocs passes `config.markdown_extensions` straight to `markdown.Markdown`,
    which accepts already-constructed `Extension` objects alongside the usual
    dotted names — so appending here is enough to get it loaded for every page.
    """
    config.markdown_extensions.append(_RepoLinkExtension())
    return config
