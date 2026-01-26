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

    def visit_document(self, node: nodes.document):
        super().visit_document(node)
        self.body.append(self.starttag(node, "div", CLASS="slides"))

    def depart_document(self, node: nodes.document):
        self.body.append("</div>\n")
        super().depart_document(node)

    def visit_revealjs_deck(self, node: revealjs_deck):
        engine = node.attributes["engine"]
        self.stylesheet = engine.build_stylesheet()
        self.body.append(engine.build_script())

    def depart_revealjs_deck(self, node: revealjs_deck):
        pass


class RevealjsWriter(base_writer.Writer):
    default_template = Path(__file__).parent / "template.txt"

    def __init__(self):
        super().__init__()
        self.translator_class = RevealjsTranslator

    def write(self, document, destination):
        document.settings.initial_header_level = 0  # To force setting
        return super().write(document, destination)
