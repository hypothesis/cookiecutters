from {{ cookiecutter.package_name }}.core import hello_world


class TestHelloWorld:
    def test_it(self):
        assert hello_world() == "Hello, world!"
