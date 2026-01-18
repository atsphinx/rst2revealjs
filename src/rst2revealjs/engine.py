"""Revealjs.js handler."""

from dataclasses import asdict, dataclass
from string import Template

DEFAULT_INIT_SCRIPT = """
import Reveal from "https://cdnjs.cloudflare.com/ajax/libs/reveal.js/$version/reveal.esm.min.js";

let deck = new Reveal();
deck.initialize();
"""


@dataclass
class RevealjsEngine:
    version: str
    theme: str = "black"

    def build_stylesheet(self) -> list[str]:
        urls = [
            f"https://cdnjs.cloudflare.com/ajax/libs/reveal.js/{self.version}/reveal.min.css",
        ]
        # TODO: Suppoort external theme.
        urls.append(
            f"https://cdnjs.cloudflare.com/ajax/libs/reveal.js/{self.version}/theme/{self.theme}.min.css",
        )
        return [f'<link rel="stylesheet" href="{url}">' for url in urls]

    def build_script(self) -> str:
        tmpl = Template(DEFAULT_INIT_SCRIPT)
        return f"""
        <script type="module">
        {tmpl.substitute(**asdict(self))}
        </script>
        """
