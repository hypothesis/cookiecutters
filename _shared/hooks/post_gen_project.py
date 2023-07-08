import json
import os.path
from collections import OrderedDict
from fnmatch import fnmatch
from os import getcwd, remove, rmdir, walk
from pathlib import Path
from shutil import move
from subprocess import run


def remove_conditional_files():
    paths_to_remove = []

    {% if cookiecutter.get("docker") != "yes" %}
    paths_to_remove.extend(["docker.env", "Dockerfile", "bin/make_docker_run"])
    {% endif %}

    {% if cookiecutter.get("frontend") != "yes" %}
    paths_to_remove.extend(["package.json", "yarn.lock"])
    {% endif %}

    {% if cookiecutter.get("postgres") != "yes" %}
    paths_to_remove.extend([
        "bin/create-db",
        "bin/make_db",
        "conf/alembic.ini",
        "{{ cookiecutter.package_name }}/db.py",
        "{{ cookiecutter.package_name }}/models/__init__.py",
        "tests/factories/__init__.py",
        "tests/factories/factoryboy_sqlalchemy_session.py",
        "tests/pytest_plugins/db.py",
        "tests/unit/pytest_plugins/db.py",
        "tests/functional/pytest_plugins/db.py",
    ])
    {% endif %}

    {% if cookiecutter.get("devdata") != "yes" %}
    paths_to_remove.extend(["bin/make_devdata"])
    {% endif %}

    {% if not has_services() %}
    paths_to_remove.extend(["docker-compose.yml"])
    {% endif %}

    {% if cookiecutter.get("pypi") != "yes" %}
    paths_to_remove.extend([".github/workflows/pypi.yml"])
    {% endif %}

    {% if cookiecutter.get("console_script") != "yes" %}
    paths_to_remove.extend(["src/{{ cookiecutter.package_name }}/__main__.py"])
    paths_to_remove.extend(["src/{{ cookiecutter.package_name }}/cli.py"])
    paths_to_remove.extend(["tests/unit/{{ cookiecutter.package_name }}/cli_test.py"])
    paths_to_remove.extend(["tests/functional/cli_test.py"])
    {% endif %}

    {% if not include_exists(".github/workflows/environments.json") %}
    # The deployment workflows only make sense if environments.json exists.
    paths_to_remove.extend([
        ".github/workflows/deploy.yml",
        ".github/workflows/redeploy.yml",
    ])
    {% endif %}

    for path in paths_to_remove:
        if os.path.exists(path):
            try:
                remove(path)
            except IsADirectoryError:
                rmdir(path)


def write_cookiecutter_json_file():
    """Create the project's cookiecutter.json file."""
    cookiecutter_json_path = Path(".cookiecutter/cookiecutter.json")

    cookiecutter_json_path.parent.mkdir(exist_ok=True)

    extra_context = {{ cookiecutter }}
    directory = extra_context.pop("_directory")
    del extra_context["create_github_repo"]
    del extra_context["_extensions"]
    del extra_context["_template"]
    del extra_context["_output_dir"]
    del extra_context["_jinja2_env_vars"]
    if "__target_dir__" in extra_context:
        del extra_context["__target_dir__"]
    if "__ignore__" in extra_context:
        del extra_context["__ignore__"]

    with open(cookiecutter_json_path, "w") as file:
        json.dump(
            {
                "template": "https://github.com/hypothesis/cookiecutters",
                "checkout": None,
                "directory": directory,
                "ignore": [],
                "extra_context": extra_context,
            },
            file,
            indent=2,
        )


def compile_requirements_files():
    """Compile the project's requirements/*.txt files."""
    print("=> Compiling requirements files")
    run(["make", "requirements"])


def create_git_repo():
    """Create the project's git repo and do the initial commit."""
    print("=> Initializing git repo")
    run(["git", "init", "-b", "main"], check=True)
    print("=> Making the first git commit")
    run(["git", "add", "."], check=True)
    run(["git", "commit", "-m", "Initial commit"], check=True)


def create_github_repo():
    """Create the project's GitHub repo."""
    run(
        [
            "gh",
            "repo",
            "create",
            "{{ cookiecutter.github_owner }}/{{ cookiecutter.slug }}",
            "--{{ cookiecutter.get('visibility', 'private') }}",
            "--description",
            "{{ cookiecutter.short_description }}",
            "--disable-wiki",
            "--source",
            ".",
            "--push",
        ],
        check=True,
    )


def main():
    cookiecutter = {{ cookiecutter }}
    target_dir = cookiecutter.get("__target_dir__")

    remove_conditional_files()

    if target_dir:
        # We are updating an existing project.
        target_dir = Path(target_dir)
        temp_dir = getcwd()

        project_ignore_patterns = cookiecutter.get("__ignore__")

        template_ignore_patterns = [".git/*"]

        {% if cookiecutter._directory in ['pyapp', 'pyramid-app'] %}
        template_ignore_patterns.extend([
            "{{ cookiecutter.package_name }}/__init__.py",
            "{{ cookiecutter.package_name }}/app.py",
            "{{ cookiecutter.package_name }}/models/__init__.py",
            "Dockerfile",
            "package.json",
            "yarn.lock",
            ".docker.env",
            "{{ cookiecutter.package_name }}/pshell.py",
            "tests/__init__.py",
            "tests/factories/__init__.py",
            "tests/unit/__init__.py",
            "tests/unit/{{ cookiecutter.package_name }}/__init__.py",
            "tests/unit/{{ cookiecutter.package_name }}/app_test.py",
            "tests/functional/__init__.py",
            "tests/functional/app_test.py",
        ])
        {% else %}
        template_ignore_patterns.extend([
            "src/{{ cookiecutter.package_name }}/__init__.py",
            "src/{{ cookiecutter.package_name }}/__main__.py",
            "src/{{ cookiecutter.package_name }}/core.py",
            "src/{{ cookiecutter.package_name }}/cli.py",
            "tests/__init__.py",
            "tests/unit/__init__.py",
            "tests/unit/{{ cookiecutter.package_name }}/__init__.py",
            "tests/unit/{{ cookiecutter.package_name }}/core_test.py",
            "tests/unit/{{ cookiecutter.package_name }}/cli_test.py",
            "tests/functional/__init__.py",
            "tests/functional/cli_test.py",
            "tests/functional/sanity_test.py",
        ])
        {% endif %}

        for root, _dirs, files in walk(temp_dir):
            for file in files:
                source_path = Path(root) / file
                relative_path = source_path.relative_to(temp_dir)
                target_path = target_dir / relative_path

                if any((fnmatch(relative_path, pattern) for pattern in project_ignore_patterns)):
                    continue

                if target_path.exists() and any((fnmatch(relative_path, pattern) for pattern in template_ignore_patterns)):
                    continue

                target_path.parent.mkdir(parents=True, exist_ok=True)
                move(source_path, target_path)
    else:
        # We're creating a new project for the first time.
        write_cookiecutter_json_file()

        {% if cookiecutter._directory in ['pyapp', 'pyramid-app'] %}
        compile_requirements_files()
        {% endif %}

        create_git_repo()

        if {{ cookiecutter.get("create_github_repo") == "yes" }}:
            create_github_repo()


if __name__ == "__main__":
    main()
