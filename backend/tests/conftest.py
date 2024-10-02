import pytest


@pytest.fixture
def app():
    from flask_migrate import Migrate

    from backend.app import app as app_, db
    migrate = Migrate(app_, db)

    yield app_

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def account_name():
    return 'Test Account'


@pytest.fixture
def account_name_no_2():
    return 'Test Account 2'
