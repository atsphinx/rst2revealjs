"""Writer for docutils."""

from __future__ import annotations

from pathlib import Path

from docutils import nodes
from docutils.writers import html5_polyglot as base_writer

from .nodes import revealjs_deck


class RevealjsTranslator(base_writer.HTMLTranslator):
    """Custom translator to render body that is Reveal.js presentation.

    It requires having nested section in doctree.
    We recommend to override settings that ``doctitle_xform`` is ``False``
    when source is simple content.
    """

    documenttag_args = {"tagname": "main", "class": "reveal"}

    def visit_section(self, node: nodes.section):
        if "revealjs_section_level" in node:
            self.section_level = node["revealjs_section_level"]
        super().visit_section(node)

    def visit_literal_block(self, node: nodes.Element):
        """Begin ``literal_block`` .

        Override base method to open ``pre`` and ``code`` tags simply.

        :ref: https://github.com/attakei/sphinx-revealjs/blob/master/sphinx_revealjs/writers.py
        """

        def _starttag(tagname: str, suffix: str = "\n", **attributes):
            """Build start tag to avoide override classes."""
            text = [f"<{tagname}"]
            for key, value in attributes.items():
                if value is None:
                    text.append(key.lower())
                else:
                    text.append(f'{key}="{value}"')
            text[-1] += f">{suffix}"
            return " ".join(text)

        # Detect language
        if len(node["classes"]) < 2:
            return super().visit_literal_block(node)
        lang = node["classes"][1]
        # Build <pre> tag
        attrs_pre = {}
        if "data-id" in node:
            attrs_pre["data-id"] = node["data-id"]
        elif isinstance(node.parent, nodes.section) and len(node.parent["ids"]):
            attrs_pre["data-id"] = node.parent["ids"][0]
        self.body.append(_starttag("pre", **attrs_pre))
        # Build <code> tag
        attrs_code = {
            "class": f"language-{lang}",
            "data-trim": None,
            "data-noescape": None,
        }
        if "data-line-numbers" in node:
            attrs_code["data-line-numbers"] = node["data-line-numbers"]
        elif "linenos" in node:
            attrs_code["data-line-numbers"] = "data-line-numbers"
        if "data-ln-start-from" in node:
            attrs_code["data-ln-start-from"] = node["data-ln-start-from"]
            if "data-line-numbers" not in attrs_code:
                attrs_code["data-line-numbers"] = "data-line-numbers"
        self.body.append(_starttag("code", suffix="", **attrs_code))
        # Write code content and close tags.
        self.body.append(node.astext())
        self.body.append("</code></pre>\n")
        # It doesn't walk children, because code content has already been appended.
        raise nodes.SkipNode

    def visit_revealjs_deck(self, node: revealjs_deck):
        self.body.append(self.starttag(node, "div", CLASS="slides"))

    def depart_revealjs_deck(self, node: revealjs_deck):
        engine = node.attributes["engine"]
        self.stylesheet = engine.build_stylesheet()
        self.body.append("</div>")
        self.body.append(engine.build_script())


class RevealjsWriter(base_writer.Writer):
    default_template = Path(__file__).parent / "template.txt"

    def __init__(self):
        super().__init__()
        self.translator_class = RevealjsTranslator

    def write(self, document, destination):
        document.settings.initial_header_level = 0  # To force setting
        return super().write(document, destination)
