from pyramid.router import Router

from {{ cookiecutter.package_name }} import app


def test_create_app():
    wsgi_app = app.create_app({})

    assert isinstance(wsgi_app, Router)


def test_index(pyramid_request):
    assert app.index(pyramid_request) == "Hello world!"


def test_status(pyramid_request):
    assert app.status(pyramid_request) == {"status": "okay"}
