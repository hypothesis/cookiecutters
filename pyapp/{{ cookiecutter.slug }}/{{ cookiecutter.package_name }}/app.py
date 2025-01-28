import time

from {{ cookiecutter.package_name }}.core import hello_world


def run():
    while True:
        print(hello_world())  # noqa: T201
        time.sleep(1)
