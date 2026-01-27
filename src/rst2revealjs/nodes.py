from __future__ import annotations

from typing import TypedDict

from docutils import nodes

from .engine import RevealjsEngine


class revealjs_deck(nodes.General, nodes.Element):
    class Attributes(TypedDict):
        engine: RevealjsEngine

    attributes: Attributes
