from unittest.mock import sentinel

from pyramid.router import Router

from {{ cookiecutter.package_name }} import app


def test_create_app():
    wsgi_app = app.create_app({})

    assert isinstance(wsgi_app, Router)


def test_index():
    assert app.index(sentinel.request) == {"Hello": "Pyramid!"}
