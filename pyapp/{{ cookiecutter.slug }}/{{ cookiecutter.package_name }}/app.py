import time

from {{ cookiecutter.package_name }}.core import hello_world


def run():
    while True:
        print(hello_world())
        time.sleep(1)
