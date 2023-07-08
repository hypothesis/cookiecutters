{% if cookiecutter.get("postgres") == "yes" %}
from os import environ

{% endif %}
import pytest


@pytest.fixture
def pyramid_settings():  # pragma: no cover
{% if cookiecutter.get("postgres") == "yes" %}
    return {"database_url": environ["DATABASE_URL"]}
{% else %}
    return {}
{% endif %}
