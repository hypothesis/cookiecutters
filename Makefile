.PHONY: help
help:
	@echo "make help              Print this help message"
	@echo "make test              Test all the cookiecutters"
	@echo "make sure              Test all the cookiecutters"
	@echo "make test-pypackage    Test the pypackage cookiecutter"
	@echo "make test-pyapp        Test the pyapp cookiecutter"
	@echo "make test-pyramid-app  Test the pyramid-app cookiecutter"

.PHONY: test sure
test sure: test-pypackage test-pyapp test-pyramid-app

.PHONY: test-pypackage
test-pypackage:
	@bin/make_test pypackage console_script=yes devdata=yes services=yes

.PHONY: test-pyapp
test-pyapp:
	@bin/make_test pyapp db=yes devdata=yes docker=yes services=yes

.PHONY: test-pyramid-app
test-pyramid-app:
	@bin/make_test pyramid-app db=yes devdata=yes docker=yes frontend=yes services=yes
