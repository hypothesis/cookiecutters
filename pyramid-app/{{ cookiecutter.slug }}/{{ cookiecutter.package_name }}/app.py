{% if cookiecutter.get("postgres") == "yes" %}
from os import environ

{% endif %}
from pyramid.config import Configurator
from pyramid.view import view_config


def create_app(_=None, **settings):
    with Configurator(settings=settings) as config:
        {% if cookiecutter.get("postgres") == "yes" %}
        config.registry.settings["database_url"] = environ["DATABASE_URL"]

        config.registry.settings["tm.annotate_user"] = False
        config.registry.settings["tm.manager_hook"] = "pyramid_tm.explicit_manager"
        config.include("pyramid_tm")

        config.include("{{ cookiecutter.package_name }}.models")
        config.include("{{ cookiecutter.package_name }}.db")

        {% endif %}
        config.add_route("index", "/")
        config.add_route("status", "/_status")

        config.scan()

        return config.make_wsgi_app()


@view_config(route_name="index", renderer="string")
def index(_request):
    return "Hello world!"


@view_config(route_name="status", renderer="json", http_cache=0)
def status(_request):
    return {"status": "okay"}
