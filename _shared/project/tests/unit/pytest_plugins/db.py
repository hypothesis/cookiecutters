import pytest

from tests.factories.factoryboy_sqlalchemy_session import (
    clear_factoryboy_sqlalchemy_session,
    set_factorboy_sqlalchemy_session,
)


@pytest.fixture
def db(db_engine, db_sessionfactory):  # pragma: no cover
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
    set_factorboy_sqlalchemy_session(session)

    yield session

    clear_factoryboy_sqlalchemy_session()
    session.close()
    transaction.rollback()
    connection.close()
