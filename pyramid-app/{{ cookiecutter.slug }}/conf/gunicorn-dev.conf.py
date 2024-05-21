from glob import glob

bind = "0.0.0.0:{{ cookiecutter.port }}"
reload = True
reload_extra_files = glob("{{ cookiecutter.package_name }}/templates/**/*", recursive=True)
timeout = 0
