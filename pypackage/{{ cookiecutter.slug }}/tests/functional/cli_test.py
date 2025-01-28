from subprocess import run


def test_help():
    """Test the {{ cookiecutter.__entry_point }} --help command."""
    run(["{{ cookiecutter.__entry_point }}", "--help"], check=True)  # noqa: S603,S607


def test_version():
    """Test the {{ cookiecutter.__entry_point }} --version command."""
    run(["{{ cookiecutter.__entry_point }}", "--version"], check=True)  # noqa: S603,S607
