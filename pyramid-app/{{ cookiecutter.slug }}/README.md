{% if cookiecutter.get("visibility") == "public" -%}
<a href="{{ cookiecutter.__github_url }}/actions/workflows/ci.yml?query=branch%3Amain"><img src="https://img.shields.io/github/workflow/status/{{ cookiecutter.github_owner }}/{{ cookiecutter.slug }}/CI/main"></a>
{% endif -%}
<a><img src="https://img.shields.io/badge/python-{{ python_versions()|pyformat(PyFormats.MAJOR_DOT_MINOR_FMT)|separator(" | ") }}-success"></a>
<a href="{{ cookiecutter.__github_url }}/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-BSD--2--Clause-success"></a>
<a href="https://github.com/hypothesis/cookiecutters/tree/main/pyramid-app"><img src="https://img.shields.io/badge/cookiecutter-pyramid--app-success"></a>
<a href="https://black.readthedocs.io/en/stable/"><img src="https://img.shields.io/badge/code%20style-black-000000"></a>

# {{ cookiecutter.name }}

{{ cookiecutter.short_description }}

Hacking
-------

For how to set up the {{ cookiecutter.name }} development environment see
[HACKING.md]({{ cookiecutter.__github_url }}/blob/main/HACKING.md).
{{ include("README.md") }}
