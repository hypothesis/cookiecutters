.PHONY: help
help:
	@echo "make help              Print this help message"
	@echo "make test              Test all the cookiecutters"
	@echo "make test-pypackage    Test the pypackage cookiecutter"
	@echo "make test-pyramid-app  Test the pyramid-app cookiecutter"

.PHONY: test
test: test-pypackage test-pyramid-app

.PHONY: test-pypackage
test-pypackage:
	@bin/make_test pypackage python_versions="3.10.4, 3.9.12, 3.8.13" console_script=yes

.PHONY: test-pyramid-app
test-pyramid-app:
	@bin/make_test pyramid-app python_version=3.10.4  docker=yes services=yes db=yes frontend=yes
