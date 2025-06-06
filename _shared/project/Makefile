comma := ,

.PHONY: help
help = help::; @echo $$$$(tput bold)$(strip $(1)):$$$$(tput sgr0) $(strip $(2))
$(call help,make help,print this help message)

.PHONY: services
{% if has_services() %}
$(call help,make services,start the services that the app needs)
services: args?=up -d --wait
services: python
	@docker compose $(args)
{% endif %}

{% if cookiecutter.get("_directory") == "pyramid-app" and cookiecutter.get("postgres") == "yes" %}
.PHONY: db
$(call help,make db,initialize the DB and upgrade it to the latest migration)
db: args?=upgrade head
db: python
	@tox -qe dev --run-command 'python3 -m {{ cookiecutter.package_name }}.scripts.init_db --create --stamp'
	@PYTHONPATH=$(CURDIR) TOX_TESTENV_PASSENV=PYTHONPATH tox -qe dev --run-command 'alembic $(args)'

{% endif %}
.PHONY: devdata
{% if cookiecutter.get("devdata") == "yes" %}
$(call help,make devdata,load development data and environment variables)
devdata: python
{% if cookiecutter.get("_directory") == "pyramid-app" and cookiecutter.get("postgres") == "yes" %}
	@tox -qe dev --run-command 'python3 -m {{ cookiecutter.package_name }}.scripts.init_db --create --stamp'
{% endif %}
	@PYTHONPATH=$(CURDIR) TOX_TESTENV_PASSENV=PYTHONPATH tox -qe dev --run-command 'python bin/make_devdata'
{% endif %}
{% if cookiecutter.get("_directory") in ["pyapp", "pyramid-app"] %}

.PHONY: dev
$(call help,make dev,run the whole app \(all workers\))
dev: python
	@pyenv exec tox -qe dev
{% endif %}
{% if cookiecutter.get("_directory") == "pyramid-app" %}

.PHONY: web
$(call help,make web,run just a single web worker process)
web: python
	@pyenv exec tox -qe dev --run-command 'gunicorn --bind :{{ cookiecutter.port }} --workers 1 --reload --timeout 0 --paste conf/development.ini'
{% endif %}

.PHONY: shell
$(call help,make shell,"launch a Python shell in this project's virtualenv")
shell: python
{% if cookiecutter._directory == 'pyapp' %}
	@PYTHONPATH=$(CURDIR) TOX_TESTENV_PASSENV=PYTHONPATH pyenv exec tox -qe dev --run-command 'ipython'
{% elif cookiecutter._directory == 'pyramid-app' %}
	@PYTHONPATH=$(CURDIR) TOX_TESTENV_PASSENV=PYTHONPATH pyenv exec tox -qe dev --run-command 'pshell conf/development.ini'
{% else %}
	@pyenv exec tox -qe dev
{% endif %}

{% if cookiecutter.get("postgres") == "yes" %}
.PHONY: sql
$(call help,make sql,"Connect to the dev database with a psql shell")
sql: python
	@docker compose exec postgres psql --pset expanded=auto -U postgres

{% endif %}
.PHONY: lint
$(call help,make lint,"lint the code and print any warnings")
lint: python
	@pyenv exec tox -qe lint

{% if cookiecutter.get("linter") == "ruff" %}
.PHONY: fix
$(call help,make fix,"apply fixes to resolve lint violations")
fix: python
	@pyenv exec tox -qe lint -- ruff check --fix-only {{ cookiecutter.package_name}} tests bin

.PHONY: noqa
$(call help,make noqa,"add noqa comments to suppress lint violations")
noqa: python
	@pyenv exec tox -qe lint -- ruff check --add-noqa {{ cookiecutter.package_name}} tests bin

{% endif %}
.PHONY: typecheck
$(call help,make typecheck,"type check the code and print any warnings")
typecheck: python
	@pyenv exec tox -qe typecheck

.PHONY: format
$(call help,make format,"format the code")
format: python
	@pyenv exec tox -qe format

.PHONY: checkformatting
$(call help,make checkformatting,"crash if the code isn't correctly formatted")
checkformatting: python
	@pyenv exec tox -qe checkformatting

.PHONY: test
{% if cookiecutter.get("_directory") in ["pyapp", "pyramid-app"] %}
$(call help,make test,"run the unit tests")
{% else %}
$(call help,make test,"run the unit tests in Python {{ python_versions()|first|pyformat(PyFormats.MAJOR_DOT_MINOR_FMT) }}")
{% endif %}
test: python
	@pyenv exec tox -qe tests

{% for python_version in python_versions()|rest %}
{% set target = 'test-py%s'|format(python_version|pyformat(PyFormats.MAJOR_MINOR_FMT)) %}
.PHONY: {{ target }}
$(call help,make {{ target }},"run the unit tests in Python {{ python_version|pyformat(PyFormats.MAJOR_DOT_MINOR_FMT) }}")
{{ target }}: python
	@pyenv exec tox -qe py{{ python_version|pyformat(PyFormats.MAJOR_MINOR_FMT) }}-tests

{% endfor %}
.PHONY: coverage
$(call help,make coverage,"run the tests and print the coverage report")
coverage: python
{% if cookiecutter._directory in ['pyapp', 'pyramid-app'] %}
	@pyenv exec tox -qe 'tests,coverage'
{% else %}
	@pyenv exec tox --parallel -qe 'tests,py{{ "{" }}{{ python_versions()|rest|pyformat(PyFormats.MAJOR_MINOR_FMT)|separator(",") }}{{ "}" }}-tests,coverage'
{% endif %}

.PHONY: functests
{% if cookiecutter.get("_directory") in ["pyapp", "pyramid-app"] %}
$(call help,make functests,"run the functional tests")
{% else %}
$(call help,make functests,"run the functional tests in Python {{ python_versions()|first|pyformat(PyFormats.MAJOR_DOT_MINOR_FMT) }}")
{% endif %}
functests: python
	@pyenv exec tox -qe functests

{% for python_version in python_versions()|rest %}
{% set target = 'functests-py%s'|format(python_version|pyformat(PyFormats.MAJOR_MINOR_FMT)) %}
.PHONY: {{ target }}
$(call help,make {{ target }},"run the functional tests in Python {{ python_version|pyformat(PyFormats.MAJOR_DOT_MINOR_FMT) }}")
{{ target }}: python
	@pyenv exec tox -qe py{{ python_version|pyformat(PyFormats.MAJOR_MINOR_FMT) }}-functests

{% endfor %}
.PHONY: sure
$(call help,make sure,"make sure that the formatting$(comma) linting and tests all pass")
sure: python
sure:
{% if cookiecutter._directory in ['pyapp', 'pyramid-app'] %}
	@pyenv exec tox --parallel -qe 'checkformatting,lint,typecheck,tests,coverage,functests'
{% else %}
	@pyenv exec tox --parallel -qe 'checkformatting,lint,typecheck,tests,py{{ "{" }}{{ python_versions()|rest|pyformat(PyFormats.MAJOR_MINOR_FMT)|separator(",") }}{{ "}" }}-tests,coverage,functests,py{{ "{" }}{{ python_versions()|rest|pyformat(PyFormats.MAJOR_MINOR_FMT)|separator(",") }}{{ "}" }}-functests'
{% endif %}

{% if cookiecutter._directory in ['pyapp', 'pyramid-app'] %}
# Tell make how to compile requirements/*.txt files.
#
# `touch` is used to pre-create an empty requirements/%.txt file if none
# exists, otherwise tox crashes.
#
# $(subst) is used because in the special case of making prod.txt we actually
# need to touch dev.txt not prod.txt and we need to run `tox -e dev ...`
# not `tox -e prod ...`
#
# $(basename $(notdir $@))) gets just the environment name from the
# requirements/%.txt filename, for example requirements/foo.txt -> foo.
requirements/%.txt: requirements/%.in python
	@touch -a $(subst prod.txt,dev.txt,$@)
	@tox -qe $(subst prod,dev,$(basename $(notdir $@))) --run-command 'pip --quiet --disable-pip-version-check install pip-tools pip-sync-faster'
	@tox -qe $(subst prod,dev,$(basename $(notdir $@))) --run-command 'pip-compile --allow-unsafe --quiet $(args) $<'

# Inform make of the dependencies between our requirements files so that it
# knows what order to re-compile them in and knows to re-compile a file if a
# file that it depends on has been changed.
requirements/dev.txt: requirements/prod.txt
requirements/tests.txt: requirements/prod.txt
requirements/functests.txt: requirements/prod.txt
requirements/lint.txt: requirements/tests.txt requirements/functests.txt
requirements/typecheck.txt: requirements/prod.txt

# Add a requirements target so you can just run `make requirements` to
# re-compile *all* the requirements files at once.
#
# This needs to be able to re-create requirements/*.txt files that don't exist
# yet or that have been deleted so it can't just depend on all the
# requirements/*.txt files that exist on disk $(wildcard requirements/*.txt).
#
# Instead we generate the list of requirements/*.txt files by getting all the
# requirements/*.in files from disk ($(wildcard requirements/*.in)) and replace
# the .in's with .txt's.
.PHONY: requirements requirements/
$(call help,make requirements,"compile the requirements files")
requirements requirements/: $(foreach file,$(wildcard requirements/*.in),$(basename $(file)).txt)

{% endif %}
.PHONY: template
$(call help,make template,"update from the latest cookiecutter template")
template: python
	@pyenv exec tox -e template -- $$(if [ -n "$${template+x}" ]; then echo "--template $$template"; fi) $$(if [ -n "$${checkout+x}" ]; then echo "--checkout $$checkout"; fi) $$(if [ -n "$${directory+x}" ]; then echo "--directory $$directory"; fi)

{% if cookiecutter.get("docker") == "yes" %}
.PHONY: docker
$(call help,make docker,"make the app's docker image")
docker:
	@git archive --format=tar HEAD | docker build -t hypothesis/{{ cookiecutter.slug }}:dev -

.PHONY: docker-run
$(call help,make docker-run,"run the app's docker image")
docker-run:
	@bin/make_docker_run

{% endif %}
.PHONY: clean
$(call help,make clean,"delete temporary files etc")
clean:
	@rm -rf build dist .tox .coverage coverage .eslintcache node_modules supervisord.log supervisord.pid yarn-error.log
	@find . -path '*/__pycache__*' -delete
	@find . -path '*.egg-info*' -delete
{% if include_exists("make_clean") %}
	{{- include("make_clean") -}}
{% endif %}

.PHONY: python
python:
	@bin/make_python

-include {{ cookiecutter.package_name }}.mk
{% if cookiecutter.get("frontend") == "yes" %}
-include frontend.mk
{% endif %}
