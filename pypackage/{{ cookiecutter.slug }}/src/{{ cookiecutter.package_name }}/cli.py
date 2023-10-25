from argparse import ArgumentParser
from importlib.metadata import version


def cli(_argv=None):  # pylint:disable=inconsistent-return-statements
    parser = ArgumentParser()
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=version("{{ cookiecutter.slug }}"),
    )

    args = parser.parse_args(_argv)
