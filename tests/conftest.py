import pytest
from api import db
from app import app
from api.models.user import UserModel


# @pytest.fixture()
# def app():
#     _app = app
#     yield _app


@pytest.fixture()
def client():
    client = app.test_client()
    yield client


@pytest.fixture()
def db_create():
    app.config.update({
        'SQLALCHEMY_DATABASE_URI': "sqlite:///:memory:"
    })
    with app.app_context():
        db.create_all()

    yield db

    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def create_test_user1(db_create):
    user1_data = {
        "username": 'user1',
        'password': 'user1'
    }
    user1 = UserModel(**user1_data)
    user1.save()

    yield user1


@pytest.fixture()
def create_test_user1_and_user2(db_create):
    users_data = [
        {
            "username": 'user1',
            'password': 'user1'
        },
        {
            "username": 'user2',
            'password': 'user2'
        },
    ]
    users_lst = []
    for user_data in users_data:
        user = UserModel(**user_data)
        user.save()
        users_lst.append(user)

    yield users_lst
