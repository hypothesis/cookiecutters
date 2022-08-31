import pytest

from {{ cookiecutter.package_name }}.cli import cli

try:
    from importlib.metadata import version
except ModuleNotFoundError:
    from importlib_metadata import version


def test_it():
    cli([])


def test_help():
    with pytest.raises(SystemExit) as exc_info:
        cli(["--help"])

    assert not exc_info.value.code


def test_version(capsys):
    exit_code = cli(["--version"])

    assert capsys.readouterr().out.strip() == version("{{ cookiecutter.slug }}")
    assert not exit_code
