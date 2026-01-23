from docutils.core import publish_string

from rst2revealjs.writer import RevealjsWriter

writer = RevealjsWriter()


def publish_revealjs(source):
    try:
        output = publish_string(
            source,
            writer=writer,
            settings_overrides={
                "doctitle_xform": False,
            },
        ).decode()
        return output
    except Exception:
        pass
