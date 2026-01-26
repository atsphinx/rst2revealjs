"""Revealjs.js handler."""

from __future__ import annotations

from dataclasses import asdict, dataclass

from jinja2 import Template

DEFAULT_VERSION = "5.2.1"

DEFAULT_INIT_SCRIPT = """
{% for name, url in imports|items %}
import {{name}} from "{{url}}";
{% endfor %}

let deck = new Reveal({{arguments}});
deck.initialize();
"""


@dataclass
class RevealjsEngine:
    styles: list[str]
    imports: dict[str, str]
    arguments: str = ""

    def build_stylesheet(self) -> list[str]:
        return [f'<link rel="stylesheet" href="{url}">' for url in self.styles]

    def build_script(self) -> str:
        tmpl = Template(DEFAULT_INIT_SCRIPT)
        return f"""
        <script type="module">
        {tmpl.render(**asdict(self))}
        </script>
        """

    @classmethod
    def from_cdn(cls, version: str, theme: str = "black") -> RevealjsEngine:
        styles = [
            f"https://cdnjs.cloudflare.com/ajax/libs/reveal.js/{version}/reveal.min.css",
            f"https://cdnjs.cloudflare.com/ajax/libs/reveal.js/{version}/theme/{theme}.min.css",
        ]
        imports = {
            "Reveal": f"https://cdnjs.cloudflare.com/ajax/libs/reveal.js/{version}/reveal.esm.min.js",
        }
        return cls(
            styles=styles,
            imports=imports,
        )
