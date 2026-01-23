"""Writer for docutils."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from docutils import nodes
from docutils.writers import html5_polyglot as base_writer

from .engine import RevealjsEngine


@dataclass
class WriterOptions:
    revealjs_version: str
    revealjs_theme: str


class RevealjsTranslator(base_writer.HTMLTranslator):
    """Custom translator to render body that is Reveal.js presentation.

    It requires having nested section in doctree.
    We recommend to override settings that ``doctitle_xform`` is ``False``
    when source is simple content.
    """

    documenttag_args = {"tagname": "main", "class": "reveal"}

    def __init__(self, document: nodes.document) -> None:
        super().__init__(document)
        self.revealjs: RevealjsEngine = self.document["revealjs"]
        self.stylesheet = self.revealjs.build_stylesheet()
        self.reveal = self.revealjs.build_script()

    def visit_section(self, node: nodes.section):
        if "revealjs_section_level" in node:
            self.section_level = node["revealjs_section_level"]
        super().visit_section(node)

    def visit_document(self, node: nodes.document):
        super().visit_document(node)
        self.body.append(self.starttag(node, "div", CLASS="slides"))

    def depart_document(self, node: nodes.document):
        self.body.append("</div>\n")
        self.body.append(self.reveal)
        super().depart_document(node)


class RevealjsWriter(base_writer.Writer):
    default_template = Path(__file__).parent / "template.txt"
    default_revealjs_version = "5.2.1"

    settings_spec = base_writer.Writer.settings_spec + (
        "Revealjs Writer Options",
        None,
        (
            (
                "Using version of Reveal.js",
                ["--revealjs-version"],
                {
                    "default": default_revealjs_version,
                    "dest": "revealjs_version",
                    "metavar": "<VERSION_TEXT>",
                    "type": str,
                },
            ),
            (
                "Reveal.js theme",
                ["--revealjs-theme"],
                {
                    "default": "black",
                    "dest": "revealjs_theme",
                    "metavar": "<str>",
                    "type": str,
                },
            ),
        ),
    )

    def __init__(self):
        super().__init__()
        self.translator_class = RevealjsTranslator

    def write(self, document, destination):
        document.settings.initial_header_level = 0  # To force setting
        return super().write(document, destination)

    def translate(self) -> None:
        assert self.document
        settings: WriterOptions = self.document.settings
        data = {
            "version": settings.revealjs_version,
            "theme": settings.revealjs_theme,
        }
        self.revealjs = RevealjsEngine(**data)
        self.document["revealjs"] = self.revealjs
        super().translate()
