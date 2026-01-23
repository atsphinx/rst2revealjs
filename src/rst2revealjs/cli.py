"""CLI Entrypoint."""

from docutils.core import publish_cmdline

from .reader import RevealjsReader
from .writer import RevealjsWriter


def main():
    publish_cmdline(reader=RevealjsReader(), writer=RevealjsWriter())
