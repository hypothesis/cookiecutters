from argparse import ArgumentParser

try:
    from importlib.metadata import version
except ModuleNotFoundError:
    from importlib_metadata import version


def cli(_argv=None):  # pylint:disable=inconsistent-return-statements
    parser = ArgumentParser()
    parser.add_argument("-v", "--version", action="store_true")

    args = parser.parse_args(_argv)

    if args.version:
        print(version("{{ cookiecutter.slug }}"))
        return 0
