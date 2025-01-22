bind = "{{ cookiecutter.get("__gunicorn_bind") or "0.0.0.0:" + cookiecutter.port }}"
worker_tmp_dir = "/dev/shm"
{% if include_exists("conf/gunicorn.conf.py/tail") %}
{{ include("conf/gunicorn.conf.py/tail") -}}
{% endif %}
