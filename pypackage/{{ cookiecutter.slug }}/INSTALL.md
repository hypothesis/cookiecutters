# Installing {{ cookiecutter.name }}

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

Upgrading
---------

To upgrade to the latest version run:

```terminal
pipx upgrade {{ cookiecutter.slug }}
```

To see what version you have run:

```terminal
{{ cookiecutter.__entry_point }} --version
```

Uninstalling
------------

To uninstall run:

```
pipx uninstall {{ cookiecutter.slug }}
```
