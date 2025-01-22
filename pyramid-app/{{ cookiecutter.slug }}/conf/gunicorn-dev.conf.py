from glob import glob

bind = "0.0.0.0:{{ cookiecutter.port }}"
reload = True
reload_extra_files = glob("{{ cookiecutter.package_name }}/templates/**/*", recursive=True)
timeout = 0
{% if include_exists("conf/gunicorn-dev.conf.py/tail") %}
{{ include("conf/gunicorn-dev.conf.py/tail") -}}
{% endif %}
