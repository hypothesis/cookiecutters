{% if cookiecutter.get("postgres") == "yes" %}
from {{ cookiecutter.package_name }} import models
{% endif %}
from tests import factories
{% if cookiecutter.get("postgres") == "yes" %}
from tests.factories.factoryboy_sqlalchemy_session import (
    set_factorboy_sqlalchemy_session,
)
{% endif %}


def setup(env):
{% if cookiecutter.get("postgres") == "yes" %}
    env["tm"] = env["request"].tm
    env["tm"].__doc__ = "Active transaction manager (a transaction is already begun)."

    env["db"] = env["request"].db
    env["db"].__doc__ = "Active DB session."

    env["m"] = env["models"] = models
    env["m"].__doc__ = "The {{ cookiecutter.package_name }}.models package."

{% endif %}
    env["f"] = env["factories"] = factories
    env["f"].__doc__ = "The test factories for quickly creating objects."
{% if cookiecutter.get("postgres") == "yes" %}
    set_factorboy_sqlalchemy_session(env["request"].db)
{% endif %}
