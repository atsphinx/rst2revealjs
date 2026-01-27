from docutils.readers.standalone import Reader

from .engine import DEFAULT_VERSION
from .transforms import RevealjsEngineTransform, RevealjsSectionizeTransform


class RevealjsReader(Reader):
    settings_spec = Reader.settings_spec + (
        "Reveal.js Support Options",
        None,
        (
            (
                "Using version of Reveal.js (set latest by default).",
                ["--revealjs-version"],
                {"dest": "revealjs_version", "default": DEFAULT_VERSION},
            ),
            (
                "Reveal.js theme",
                ["--revealjs-theme"],
                {"dest": "revealjs_theme", "default": "black"},
            ),
        ),
    )

    def read(self, source, parser, settings):
        settings.doctitle_xform = False  # To force setting
        return super().read(source, parser, settings)

    def get_transforms(self):
        return super().get_transforms() + [
            RevealjsSectionizeTransform,
            RevealjsEngineTransform,
        ]
