{% if cookiecutter.get("postgres") == "yes" %}
from os import environ

{% endif %}
import pytest
{% if cookiecutter.get("postgres") == "yes" %}
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from {{ cookiecutter.package_name }}.db import Base
from tests.factories.factoryboy_sqlalchemy_session import (
    clear_factoryboy_sqlalchemy_session,
    set_factoryboy_sqlalchemy_session,
)
{% endif %}
{% if cookiecutter.get("postgres") == "yes" %}


@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(environ["DATABASE_URL"])

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    return engine


@pytest.fixture(scope="session")
def db_sessionfactory():
    return sessionmaker()


@pytest.fixture
def db_session(db_engine, db_sessionfactory):
    """Return the SQLAlchemy database session.

    This returns a session that is wrapped in an external transaction that is
    rolled back after each test, so tests can't make database changes that
    affect later tests.  Even if the test (or the code under test) calls
    session.commit() this won't touch the external transaction.

    This is the same technique as used in SQLAlchemy's own CI:
    https://docs.sqlalchemy.org/en/20/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites
    """
    connection = db_engine.connect()
    transaction = connection.begin()
    session = db_sessionfactory(
        bind=connection, join_transaction_mode="create_savepoint"
    )
    set_factoryboy_sqlalchemy_session(session)

    yield session

    clear_factoryboy_sqlalchemy_session()
    session.close()
    transaction.rollback()
    connection.close()
{% endif %}
{% if cookiecutter._directory == "pyramid-app" %}


@pytest.fixture
def pyramid_settings():
{% if cookiecutter.get("postgres") == "yes" %}
    return {"database_url": environ["DATABASE_URL"]}
{% else %}
    return {}
{% endif %}
{% endif %}
