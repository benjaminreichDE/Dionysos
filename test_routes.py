import pytest
from flask import url_for
from app import app as application


@pytest.fixture(scope='function')
def app():
    application.app_context().push()
    application.config['DEBUG'] = True
    application.config['TESTING'] = True
    return application


# noinspection PyShadowingNames
def test_routes(app):
    client = app.test_client()
    for route in ['home', 'leaderboard', 'transactions', 'login', 'register', 'forgot']:
        assert client.get(url_for(route)).status_code == 200
