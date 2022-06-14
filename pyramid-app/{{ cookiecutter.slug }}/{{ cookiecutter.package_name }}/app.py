from pyramid.config import Configurator
from pyramid.view import view_config


def create_app(_=None, **settings):
    with Configurator(settings=settings) as config:
        config.add_route("index", "/")

        config.scan()

        return config.make_wsgi_app()


@view_config(route_name="index", renderer="json")
def index(_request):
    return {"Hello": "Pyramid!"}
