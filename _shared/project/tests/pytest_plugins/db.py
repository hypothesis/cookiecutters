from os import environ

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from {{ cookiecutter.package_name }}.db import Base


@pytest.fixture(scope="session")
def db_engine():  # pragma: no cover
    engine = create_engine(environ["DATABASE_URL"])

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    return engine


@pytest.fixture(scope="session")
def db_sessionfactory():  # pragma: no cover
    return sessionmaker()
