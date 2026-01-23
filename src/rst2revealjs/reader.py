from docutils.readers.standalone import Reader

from .transforms import RevealjsSectionizeTransform


class RevealjsReader(Reader):
    def read(self, source, parser, settings):
        settings.doctitle_xform = False  # To force setting
        return super().read(source, parser, settings)

    def get_transforms(self):
        return super().get_transforms() + [RevealjsSectionizeTransform]
