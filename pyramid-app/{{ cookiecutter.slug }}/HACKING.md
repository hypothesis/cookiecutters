# Setting up Your {{ cookiecutter.name }} Development Environment

First you'll need to install:

* [Git](https://git-scm.com/).
  On Ubuntu: `sudo apt install git`, on macOS: `brew install git`.
* [pyenv](https://github.com/pyenv/pyenv).
  See [pyenv's README](https://github.com/pyenv/pyenv#readme) for install instructions.
  First you need to [install the Python build dependencies](https://github.com/pyenv/pyenv/wiki#suggested-build-environment)
  then on macOS use the **Homebrew** installation method,
  on Ubuntu use the **Basic GitHub Checkout** method.
  You _don't_ need to set up pyenv's shell integration ("shims"), you can
  [use pyenv without shims](https://github.com/pyenv/pyenv#using-pyenv-without-shims).
* [GNU Make](https://www.gnu.org/software/make/).
  This is probably already installed or will have been installed while installing pyenv, run `make --version` to check.
{%- if cookiecutter.get("services") == "yes" %}
* [Docker](https://docs.docker.com/install/).
  Follow the [instructions on the Docker website](https://docs.docker.com/install/)
  to install it.  
  You **don't** need to install Docker Compose, the development environment
  will install it automatically for you in tox.  
  You **do** need to set up the `docker` command to work without `sudo`,
  on Linux this means following Docker's [Post-installation steps for Linux](https://docs.docker.com/engine/install/linux-postinstall/).
{%- endif %}
{%- if cookiecutter.get("frontend") == "yes" %}
* [Node](https://nodejs.org/) and npm.
  On Ubuntu: `sudo snap install --classic node`.
  On macOS: `brew install node`.
* [Yarn](https://yarnpkg.com/): `sudo npm install -g yarn`.
{%- endif %}
{{- include("hacking/prerequisites") }}

Then to set up your development environment:

```terminal
git clone {{ cookiecutter.__github_url }}.git
cd {{ cookiecutter.package_name }}
make services
make devdata
make help
```

{{- include("HACKING.md") }}

Changing the Project's Python Version
-------------------------------------

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

Changing the Project's Python Dependencies
------------------------------------------

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
