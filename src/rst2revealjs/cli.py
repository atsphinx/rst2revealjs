"""CLI Entrypoint."""

from docutils.core import publish_cmdline

from .writer import RevealjsWriter


def main():
    publish_cmdline(writer=RevealjsWriter())
