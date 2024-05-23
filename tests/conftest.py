import pytest
from server import app
from models import Base, engine

from flask import Flask, request

@pytest.fixture(scope="session", autouse=True)
def init_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="session")
def flask_app():
    app.config.update({
        "TESTING": True,
    })
    yield app
@pytest.fixture()
def client(flask_app):
    return flask_app.test_client()

@pytest.fixture()
def runner(flask_app):
    return flask_app.test_cli_runner()

