import sys

from {{ cookiecutter.package_name }}.app import run

sys.exit(run())
