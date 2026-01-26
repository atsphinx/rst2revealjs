from docutils import nodes
from docutils.transforms import Transform

from .engine import RevealjsEngine
from .nodes import revealjs_deck


class RevealjsEngineTransform(Transform):
    """docutils transform to bind Reveal.js engine object."""

    default_priority = 350

    def apply(self, **kwargs):
        settings = self.document.settings
        data = {
            "version": settings.revealjs_version,
            "theme": settings.revealjs_theme,
        }
        engine = RevealjsEngine.from_cdn(**data)
        node = revealjs_deck(engine=engine)
        self.document.children.append(node)


class RevealjsSectionizeTransform(Transform):
    """docutils transform to Reveal.js style section structure."""

    default_priority = 350

    def apply(self, **kwargs):
        def _rebuild(root: nodes.section):
            new_root = nodes.section()
            sub_sections = []
            for child in list(root.findall(nodes.section, include_self=False)):
                if child.parent == root:
                    child["revealjs_section_level"] = 3
                    root.remove(child)
                    sub_sections.append(child)
            new_root.children = [root] + sub_sections
            return new_root

        idx = self.document.first_child_matching_class(nodes.section)
        if idx is None:
            raise ValueError("Invalid document for revealjs")
        sections = [self.document[idx]]
        sections[0]["revealjs_section_level"] = 1
        for node in self.document.children[:idx]:
            self.document.remove(node)
            sections[0].insert(0, node)
        self.document.remove(sections[0])
        for node in list(sections[0].findall(nodes.section, include_self=False)):
            if node.parent == sections[0]:
                node["revealjs_section_level"] = 2
                sections[0].remove(node)
                sections.append(node)
        new_sections = []
        for vertical in sections:
            new_sections.append(_rebuild(vertical))

        self.document.children = new_sections + self.document.children
