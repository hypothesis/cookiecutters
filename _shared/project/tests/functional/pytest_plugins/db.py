import pytest

from tests.factories.factoryboy_sqlalchemy_session import (
    clear_factoryboy_sqlalchemy_session,
    set_factorboy_sqlalchemy_session,
)


@pytest.fixture
def db(db_engine, db_sessionfactory):  # pragma: no cover
    """Return a standalone database session for preparing database state."""

    connection = db_engine.connect()
    session = db_sessionfactory(bind=connection)
    set_factorboy_sqlalchemy_session(session)

    try:
        yield session
    finally:
        clear_factoryboy_sqlalchemy_session()
        session.close()
        connection.close()
