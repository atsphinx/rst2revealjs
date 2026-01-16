"""Writer for docutils."""

from __future__ import annotations

from pathlib import Path

from docutils import frontend, nodes
from docutils.writers import html5_polyglot as base_writer


class RevealjsTranslator(base_writer.HTMLTranslator):
    """Custom translator to render body that is Reveal.js presentation.

    It requires having nested section in doctree.
    We recommend to override settings that ``doctitle_xform`` is ``False``
    when source is simple content.
    """

    def __init__(self, document: nodes.document) -> None:
        super().__init__(document)
        self.initial_header_level = 1

    def visit_document(self, node: nodes.document):
        super().visit_document(node)
        self.body.append(self.starttag(node, "div", CLASS="reveal"))
        self.body.append(self.starttag(node, "div", CLASS="slides"))

    def depart_document(self, node: nodes.document):
        self.body.append("</div>\n")
        self.body.append("</div>\n")
        super().depart_document(node)

    def visit_section(self, node: nodes.section):
        if self.section_level == 0:
            # Wen it visit root of section,
            # it appends ``<section>`` element to render vertical section.
            self.body.append("<section>")
        elif self.section_level == 1:
            # Wen it visit first sub-section,
            # it closes first vertical section and creates vertical section.
            self.body.append("</section>")
            self.body.append("</section>")
            self.body.append("<section>")
        elif self.section_level == 2:
            # Wen it visit content of sub-section,
            # it closes previous section.
            first = next(node.parent.findall(nodes.section, include_self=False))
            if first == node:
                self.body.append("</section>")
        super().visit_section(node)

    def depart_section(self, node: nodes.section):
        if self.section_level > 1:
            super().depart_section(node)


class RevealjsWriter(base_writer.Writer):
    default_template = Path(__file__).parent / "template.txt"

    settings_spec = frontend.filter_settings_spec(
        base_writer.Writer.settings_spec,
        template=(
            f'Template file. (UTF-8 encoded, default: "{default_template}")',
            ["--template"],
            {"default": default_template, "metavar": "<file>"},
        ),
    )

    def __init__(self):
        super().__init__()
        self.translator_class = RevealjsTranslator
