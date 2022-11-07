{%- macro badges() %}
    {% if cookiecutter.get("visibility") == "public" %}
    <a href="{{ cookiecutter.__github_url }}/actions/workflows/ci.yml?query=branch%3Amain"><img src="https://img.shields.io/github/workflow/status/{{ cookiecutter.github_owner }}/{{ cookiecutter.slug }}/CI/main"></a>
    {% endif %}
    {% if cookiecutter._directory == 'pypackage' %}
    <a href="{{ cookiecutter.__pypi_url }}"><img src="https://img.shields.io/pypi/v/{{ cookiecutter.slug }}"></a>
    {% endif %}
    <a><img src="https://img.shields.io/badge/python-{{ python_versions()|pyformat(PyFormats.MAJOR_DOT_MINOR_FMT)|separator(" | ") }}-success"></a>
    <a href="{{ cookiecutter.__github_url }}/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-BSD--2--Clause-success"></a>
    <a href="https://github.com/hypothesis/cookiecutters/tree/main/{{ cookiecutter._directory }}"><img src="https://img.shields.io/badge/cookiecutter-{{ cookiecutter._directory|replace("-", "--") }}-success"></a>
    <a href="https://black.readthedocs.io/en/stable/"><img src="https://img.shields.io/badge/code%20style-black-000000"></a>
{% endmacro %}

{%- macro intro() %}
    # {{ cookiecutter.name }}

    {{ cookiecutter.short_description }}
{% endmacro %}

{%- macro installing() %}
    ## Installing

    We recommend using [pipx](https://pypa.github.io/pipx/) to install
    {{ cookiecutter.name }}.
    First [install pipx](https://pypa.github.io/pipx/#install-pipx) then run:

    ```terminal
    pipx install {{ cookiecutter.slug }}
    ```

    You now have {{ cookiecutter.name }} installed! For some help run:

    ```
    {{ cookiecutter.__entry_point }} --help
    ```

    ## Upgrading

    To upgrade to the latest version run:

    ```terminal
    pipx upgrade {{ cookiecutter.slug }}
    ```

    To see what version you have run:

    ```terminal
    {{ cookiecutter.__entry_point }} --version
    ```

    ## Uninstalling

    To uninstall run:

    ```
    pipx uninstall {{ cookiecutter.slug }}
    ```
{% endmacro %}

{%- macro setting_up() %}
    ## Setting up Your {{ cookiecutter.name }} Development Environment

    First you'll need to install:

    * [Git](https://git-scm.com/).
      On Ubuntu: `sudo apt install git`, on macOS: `brew install git`.
    * [GNU Make](https://www.gnu.org/software/make/).
      This is probably already installed, run `make --version` to check.
    * [pyenv](https://github.com/pyenv/pyenv).
      Follow the instructions in pyenv's README to install it.
      The **Homebrew** method works best on macOS.
      The **Basic GitHub Checkout** method works best on Ubuntu.
      You _don't_ need to set up pyenv's shell integration ("shims"), you can
      [use pyenv without shims](https://github.com/pyenv/pyenv#using-pyenv-without-shims).
    {% if cookiecutter.get("services") == "yes" %}
    * [Docker](https://docs.docker.com/install/).
      Follow the [instructions on the Docker website](https://docs.docker.com/install/)
      to install it.  
      You **don't** need to install Docker Compose, the development environment
      will install it automatically for you in tox.  
      You **do** need to set up the `docker` command to work without `sudo`,
      on Linux this means following Docker's [Post-installation steps for Linux](https://docs.docker.com/engine/install/linux-postinstall/).
    {% endif %}
    {% if cookiecutter.get("frontend") == "yes" %}
    * [Node](https://nodejs.org/) and npm.
      On Ubuntu: `sudo snap install --classic node`.
      On macOS: `brew install node`.
    * [Yarn](https://yarnpkg.com/): `sudo npm install -g yarn`.
    {% endif %}
    {% if include_exists("hacking/prerequisites") %}
        {{- include("hacking/prerequisites", indent=4) -}}
    {% endif %}

    Then to set up your development environment:

    ```terminal
    git clone {{ cookiecutter.__github_url }}.git
    cd {{ cookiecutter.slug }}
    {% if cookiecutter.get("services") == "yes" %}
    make services
    {% endif %}
    {% if cookiecutter.get("devdata") == "yes" %}
    make devdata
    {% endif %}
    make help
    ```
{% endmacro %}

{%- macro releasing() %}
    ## Releasing a New Version of the Project

    1. First, to get PyPI publishing working you need to go to:
       <https://github.com/organizations/hypothesis/settings/secrets/actions/PYPI_TOKEN>
       and add {{ cookiecutter.slug }} to the `PYPI_TOKEN` secret's selected
       repositories.

    2. Now that the {{ cookiecutter.slug }} project has access to the `PYPI_TOKEN` secret
       you can release a new version by just [creating a new GitHub release](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository).
       Publishing a new GitHub release will automatically trigger
       [a GitHub Actions workflow](.github/workflows/pypi.yml)
       that will build the new version of your Python package and upload it to
       <{{ cookiecutter.__pypi_url }}>.
{% endmacro %}

{%- macro app_python_version() %}
    ## Changing the Project's Python Version

    To change what version of Python the project uses:

    1. Change the Python version in the
       [cookiecutter.json](.cookiecutter/cookiecutter.json) file. For example:

       ```json
       "python_version": "3.10.4",
       ```

    2. Re-run the cookiecutter template:

       ```terminal
       make template
       ```

    3. Re-compile the `requirements/*.txt` files.
       This is necessary because the same `requirements/*.in` file can compile to
       different `requirements/*.txt` files in different versions of Python:

       ```terminal
       make requirements
       ```

    4. Commit everything to git and send a pull request
{% endmacro %}

{%- macro package_python_version() %}
    ## Changing the Project's Python Versions

    To change what versions of Python the project uses:

    1. Change the Python versions in the
       [cookiecutter.json](.cookiecutter/cookiecutter.json) file. For example:

       ```json
       "python_versions": "3.10.4, 3.9.12",
       ```

    2. Re-run the cookiecutter template:

       ```terminal
       make template
       ```

    3. Commit everything to git and send a pull request
{% endmacro %}

{%- macro app_python_dependencies() %}
    ## Changing the Project's Python Dependencies

    ### To Add a New Dependency

    Add the package to the appropriate [`requirements/*.in`](requirements/)
    file(s) and then run:

    ```terminal
    make requirements
    ```

    ### To Remove a Dependency

    Remove the package from the appropriate [`requirements/*.in`](requirements)
    file(s) and then run:

    ```terminal
    make requirements
    ```

    ### To Upgrade or Downgrade a Dependency

    We rely on [Dependabot](https://github.com/dependabot) to keep all our
    dependencies up to date by sending automated pull requests to all our repos.
    But if you need to upgrade or downgrade a package manually you can do that
    locally.

    To upgrade a package to the latest version in all `requirements/*.txt` files:

    ```terminal
    make requirements --always-make args='--upgrade-package <FOO>'
    ```

    To upgrade or downgrade a package to a specific version:

    ```terminal
    make requirements --always-make args='--upgrade-package <FOO>==<X.Y.Z>'
    ```

    To upgrade **all** packages to their latest versions:

    ```terminal
    make requirements --always-make args=--upgrade
    ```
{% endmacro %}

{%- macro package_python_dependencies() %}
    ## Changing the Project's Python Dependencies

    To change the production dependencies in the `setup.cfg` file:

    1. Change the dependencies in the [`.cookiecutter/includes/setuptools/install_requires`](.cookiecutter/includes/setuptools/install_requires) file.
       If this file doesn't exist yet create it and add some dependencies to it.
       For example:

       ```
       pyramid
       sqlalchemy
       celery
       ```

    2. Re-run the cookiecutter template:

       ```terminal
       make template
       ```

    3. Commit everything to git and send a pull request

    To change the project's formatting, linting and test dependencies:

    1. Change the dependencies in the [`.cookiecutter/includes/tox/deps`](.cookiecutter/includes/tox/deps) file.
       If this file doesn't exist yet create it and add some dependencies to it.
       Use tox's [factor-conditional settings](https://tox.wiki/en/latest/config.html#factors-and-factor-conditional-settings)
       to limit which environment(s) each dependency is used in.
       For example:

       ```
       lint: flake8,
       format: autopep8,
       lint,tests: pytest-faker,
       ```

    2. Re-run the cookiecutter template:

       ```terminal
       make template
       ```

    3. Commit everything to git and send a pull request
{% endmacro -%}

{{ badges()|dedent }}
{{ intro()|dedent }}
{% if include_exists("README/head.md") %}
  {{- include("README/head.md") }}
{% endif %}
{% if cookiecutter.get("console_script") == "yes" -%}
    {{ installing()|dedent }}
{% endif %}
{{ setting_up()|dedent }}
{% if cookiecutter._directory == 'pypackage' -%}
    {{ releasing()|dedent }}
{% endif %}
{% if cookiecutter._directory == 'pyramid-app' -%}
    {{ app_python_version()|dedent }}
{% else -%}
    {{ package_python_version()|dedent }}
{% endif %}
{% if cookiecutter._directory == 'pyramid-app' -%}
    {{ app_python_dependencies()|dedent }}
{%- else -%}
    {{ package_python_dependencies()|dedent }}
{%- endif %}
{% if include_exists("README/tail.md") %}

{{ include("README/tail.md") -}}
{% endif %}
