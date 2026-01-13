"""Writer for docutils."""

from docutils.writers import html5_polyglot as base_writer


class RevealjsTranslator(base_writer.HTMLTranslator):
    pass


class RevealjsWriter(base_writer.Writer):
    def __init__(self):
        super().__init__()
        self.translator_class = RevealjsTranslator
