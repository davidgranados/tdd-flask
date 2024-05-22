import os

import pytest
from dotenv import load_dotenv

from src import create_app, db
from src.api.models import User


APP_ENV = os.getenv("APP_ENV")

if APP_ENV is None or APP_ENV == "local":
    dotenv_path = os.path.join(os.path.dirname(__file__), "../../envs/.env.test.local")
    load_dotenv(dotenv_path)


@pytest.fixture(scope="module")
def test_app():
    app = create_app("src.config.TestingConfig")
    with app.app_context():
        yield app  # testing happens here


@pytest.fixture(scope="function")
def test_database():
    db.create_all()
    yield db  # testing happens here
    db.session.remove()
    db.drop_all()


@pytest.fixture(scope='function')
def add_user():
    def _add_user(username, email):
        user = User(username=username, email=email)
        db.session.add(user)
        db.session.commit()
        return user
    return _add_user
