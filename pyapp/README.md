cookiecutters/pyapp
===================

A [Cookiecutter](https://cookiecutter.readthedocs.io/en/stable/) for Python apps.

Usage
-----

### Creating a new Python app

1. Install cookiecutter.

   You need to install cookiecutter itself before you can use
   cookiecutters/pyapp to create a new Python app. We recommend using
   [pipx](https://pypa.github.io/pipx/) to install cookiecutter.
   First [install pipx](https://pypa.github.io/pipx/#install-pipx) then run:

   ```terminal
   pipx install cookiecutter
   ```

   You now have cookiecutter installed! Try `cookiecutter --help`.

2. Now to create a new Python app run:

   ```terminal
   cookiecutter gh:hypothesis/cookiecutters --directory pyapp
   ```

   See the `README.md` file in your newly created project for instructions on
   managing the project.

### Updating a project

To update your project with the latest version of the cookiecutter run:

```terminal
make template
```

### `cookiecutter.json` settings

Your project contains a `.cookiecutter/cookiecutter.json` file with several
settings that `make template` uses. For example if you want your app to have
Docker support `"docker"` setting to `"yes"` and then re-run `make template`.

### `.cookiecutter/includes/`

You can create a `.cookiecutter/includes/` directory in your project containing
include snippets that `make template` will use. For example any text that you
put into a `.cookiecutter/includes/README.md` file will be copied to the bottom
of the project's real `README.md` file when you re-run `make template`.
The cookiecutter supports [lots of include snippets](https://github.com/hypothesis/cookiecutters/search?q=include%28&type=code).