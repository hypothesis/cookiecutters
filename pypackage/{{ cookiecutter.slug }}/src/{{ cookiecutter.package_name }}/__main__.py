import sys

from {{ cookiecutter.package_name }}.cli import cli

sys.exit(cli())
