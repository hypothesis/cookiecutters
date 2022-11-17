import json
import textwrap
from pathlib import Path
from textwrap import dedent

from jinja2.ext import Extension, pass_context


class PyFormats:
    MAJOR_DOT_MINOR_DOT_PATCH_FMT = "{major}.{minor}.{patch}"
    MAJOR_DOT_MINOR_FMT = "{major}.{minor}"
    MAJOR_MINOR_FMT = "{major}{minor}"


class PythonVersion:
    """A Python version with major, minor and patch version numbers."""

    def __init__(self, obj, fmt=None, quotes=None):
        try:
            self.major, self.minor, self.patch = obj.parts
        except AttributeError:
            parts = obj.split(".", maxsplit=2)
            self.major = parts[0]
            self.minor = parts[1] if len(parts) >= 2 else None
            self.patch = parts[2] if len(parts) >= 3 else None

        self.fmt = fmt or getattr(obj, "fmt", PyFormats.MAJOR_DOT_MINOR_DOT_PATCH_FMT)
        self.quotes = quotes or getattr(obj, "quotes", None)

    @property
    def parts(self):
        return (self.major, self.minor, self.patch)

    def __repr__(self):
        string = self.fmt.format(
            major=self.major, minor=self.minor or 0, patch=self.patch or 0
        )

        if self.quotes:
            return f"{self.quotes}{string}{self.quotes}"

        return string


class PythonVersions:
    """A collection of PythonVersion objects."""

    def __init__(self, obj, fmt=None, quotes=None, separator=None):
        if isinstance(obj, PythonVersion):
            objs = [obj]
        elif isinstance(obj, str):
            objs = obj.replace(",", " ").split()
        else:
            objs = obj

        self.python_versions = [
            PythonVersion(obj, fmt=fmt, quotes=quotes) for obj in objs
        ]

        self.separator = separator or getattr(obj, "separator", ", ")

    def __getitem__(self, i):
        return self.python_versions[i]

    def __repr__(self):
        return self.separator.join(
            repr(python_version) for python_version in self.python_versions
        )


class LocalJinja2Extension(Extension):
    def __init__(self, environment):
        super().__init__(environment)
        environment.globals.update(
            {
                "python_versions": self.python_versions,
                "include_exists": self.include_exists,
                "include": self.include,
                "include_json": self.include_json,
                "PyFormats": PyFormats,
            }
        )
        environment.filters.update(
            {
                "oldest": self.oldest,
                "pyformat": self.pyformat,
                "quote": self.quote,
                "separator": self.separator,
                "rest": self.rest,
                "dedent": self.dedent,
            }
        )

    @pass_context
    def python_versions(self, context):
        """Return a list of all the project's Python versions."""
        ctx = context["cookiecutter"]
        python_versions_string = ctx.get("python_versions") or ctx["python_version"]
        return PythonVersions(python_versions_string)

    @pass_context
    def include_exists(self, context, path):
        """Return True if the project has a file at .cookiecutter/includes/{path}."""
        try:
            with self._open(context, path):
                return True
        except (FileNotFoundError, NotADirectoryError):
            return False

    @pass_context
    def include(self, context, path, indent=0):
        """Return the lines from the project's .cookiecutter/includes/{path} or an empty string."""
        try:
            with self._open(context, path) as file_obj:
                return textwrap.indent("".join(file_obj.readlines()), " " * indent)
        except (FileNotFoundError, NotADirectoryError):
            return ""

    @pass_context
    def include_json(self, context, path):
        """Return the project's .cookiecutter/includes/{path} data or None.

        Return the contents of the project's .cookiecutter/includes/{path} JSON
        file deserialized into a Python object.

        Return None if the project has no .cookiecutter/includes/{path} file.
        """
        with self._open(context, path) as file_obj:
            return json.load(file_obj)

    def oldest(self, python_versions):
        """Return the oldest from `python_versions` by version number."""
        return sorted(
            list(PythonVersions(python_versions)),
            key=lambda version: [int(part) for part in version.parts],
        )[0]

    def pyformat(self, python_versions, fmt):
        """Return a copy of `python_versions` in the given `fmt`."""
        return PythonVersions(python_versions, fmt=fmt)

    def quote(self, python_versions, quotes):
        """Return a copy of `python_versions` wrapped in `quotes`."""
        return PythonVersions(python_versions, quotes=quotes)

    def separator(self, python_versions, separator):
        """Return a copy of `python_versions` separated by `separator`'s."""
        return PythonVersions(python_versions, separator=separator)

    def rest(self, list_):
        """Return a list of all but the first item in `list_`."""
        return list_[1:]

    def dedent(self, s):
        """Return `s` dedented."""
        return dedent(s)

    def _open(self, context, path):
        """Return the file at `path` in the project's .cookiecutter/includes dir."""
        target_dir = context["cookiecutter"].get("__target_dir__")

        if not target_dir:
            # We're creating a new project for the first time rather than
            # updating an existing project, so there are no include files yet.
            raise FileNotFoundError()

        return open(Path(target_dir) / ".cookiecutter/includes" / path, "r")
