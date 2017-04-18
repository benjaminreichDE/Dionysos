import pytest
import pytest_flask
import app
from flask import Flask, url_for

@pytest.fixture
def app():
    return app.app


def test_all_routes(app):
    client = app.test_client()
    for route in ['/', '/leaderboard', '/transactions', '/login', '/register', '/forgot']:
        assert client.get(url_for(route)).status_code == 200
