from pathlib import Path

from bs4 import BeautifulSoup
from docutils.core import publish_doctree, publish_from_doctree

from rst2revealjs.reader import RevealjsReader
from rst2revealjs.writer import RevealjsWriter

SOURCE = """
==================
Presentation Title
==================

Section title 1
===============

Description of section.

Section 1-1
-----------

This is content.

Section 1-2
-----------

This is content.
"""


def save_pseudoxml(doctree, suffix: str):
    itself = Path(__file__)
    filename = f"{itself.stem}-{suffix}.pxml"
    (itself.parent / filename).write_bytes(
        publish_from_doctree(doctree, writer_name="pseudoxml")
    )


def save_html(content: str, suffix: str):
    itself = Path(__file__)
    filename = f"{itself.stem}-{suffix}.html"
    (itself.parent / filename).write_text(content)


def test_it():
    doctree = publish_doctree(source=SOURCE.strip(), reader=RevealjsReader())
    save_pseudoxml(doctree, "test_it")
    out = publish_from_doctree(doctree, writer=RevealjsWriter())
    out = out.decode().strip()
    save_html(out, "test_it")
    assert out.startswith("<!DOCTYPE html>")
    assert out.endswith("</html>")
    soup = BeautifulSoup(out, "lxml")
    assert len(soup.find_all("section")) == 6
    assert soup.title.text == "Presentation Title"
    assert soup.find("h1").text == "Presentation Title"
