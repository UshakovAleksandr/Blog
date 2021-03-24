import pytest
from api import db
from app import app
from api.models.user import UserModel
from api.models.tag import TagModel
from api.models.note import NoteModel
from base64 import b64encode


@pytest.fixture()
def client():
    client = app.test_client()
    return client


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

    return user1, user1_data


@pytest.fixture()
def create_test_user2(db_create):
    user2_data = {
        "username": 'user2',
        'password': 'user2'
    }
    user2 = UserModel(**user2_data)
    user2.save()

    return user2, user2_data


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

    return users_lst


@pytest.fixture()
def create_test_tag1_by_user1(create_test_user1):
    tag_data1 = {
        "name": 'test tag 1'
    }

    tag1 = TagModel(author_id=create_test_user1[0].id, **tag_data1)
    tag1.save()

    return tag1, create_test_user1


@pytest.fixture()
def create_test_tag1_and_tag2_by_user1(create_test_user1):

    tags_data = [
        {
            "name": 'test tag 1'
        },
        {
            "name": 'test tag 2'
        }
    ]

    tags_lst = []
    for tag_data in tags_data:
        tag = TagModel(author_id=create_test_user1[0].id, **tag_data)
        tag.save()
        tags_lst.append(tag)

    return tags_lst


@pytest.fixture()
def create_test_note1_by_user1(create_test_user1):
    note_data1 = {
        "note": 'test note 1'
    }

    note1 = NoteModel(author_id=create_test_user1[0].id, **note_data1)
    note1.save()

    return note1, create_test_user1


@pytest.fixture()
def create_test_note2_by_user2(create_test_user2):
    note_data2 = {
        "note": 'test note 2'
    }

    note2 = NoteModel(author_id=create_test_user2[0].id, **note_data2)
    note2.save()

    return note2, create_test_user2


@pytest.fixture()
def create_test_note1_and_note2_by_user1(create_test_user1):
    notes_data = [
        {
            "note": 'test note 1'
        },
        {
            "note": 'test note 2'
        },
    ]
    notes_lst = []
    for note_data in notes_data:
        note = NoteModel(author_id=create_test_user1[0].id, **note_data)
        note.save()
        notes_lst.append(note)

    return user_data


@pytest.fixture()
def create_test_user1_note1_tag1_tag2(create_test_user1):
    note_data1 = {
        "note": 'test note 1'
    }
    note1 = NoteModel(author_id=create_test_user1[0].id, **note_data1)
    note1.save()

    tags_data = [
        {
            "name": 'test tag 1'
        },
        {
            "name": 'test tag 2'
        }
    ]
    tags_lst = []
    for tag_data in tags_data:
        tag = TagModel(author_id=create_test_user1[0].id, **tag_data)
        tag.save()
        tags_lst.append(tag)

    return note1, tags_lst, create_test_user1


@pytest.fixture()
def create_test_user2_note2_tag3_tag4(create_test_user2):
    note_data2 = {
        "note": 'test note 2'
    }
    note2 = NoteModel(author_id=create_test_user2[0].id, **note_data2)
    note2.save()

    tags_data = [
        {
            "name": 'test tag 3'
        },
        {
            "name": 'test tag 4'
        }
    ]
    tags_lst = []
    for tag_data in tags_data:
        tag = TagModel(author_id=create_test_user2[0].id, **tag_data)
        tag.save()
        tags_lst.append(tag)

    return note2, tags_lst, create_test_user2


@pytest.fixture()
def auth_headers(create_test_user1):
    return {
        'Authorization': 'Basic ' + b64encode(
            f"{create_test_user1[1]['username']}:{create_test_user1[1]['password']}".encode('ascii')).decode('utf-8')
    }


@pytest.fixture()
def user_data():
    user_data = {
        "username": 'user',
        'password': 'user'
    }
    return user_data


@pytest.fixture()
def new_user_data():
    new_user_data = {
        "username": 'user1',
        'password': 'user1'
    }
    return new_user_data


@pytest.fixture()
def user_data_to_change():
    user_data_to_change = {
        "username": 'user1'
    }
    return user_data_to_change


@pytest.fixture()
def tag_data1():
    tag_data1 = {
        "name": 'test tag 1'
    }
    return tag_data1


@pytest.fixture()
def tag_data_to_change():
    tag_data_to_change = {
        "name": 'test tag 2'
    }
    return tag_data_to_change


@pytest.fixture()
def note_data():
    note_data = {
        "note": 'test note 1'
    }
    return note_data


@pytest.fixture()
def note_data_to_change():
    note_data_to_change = {
        "note": 'test note 2'
    }
    return note_data_to_change


@pytest.fixture()
def note_data_to_change_bool():
    note_data_to_change_bool = {
        "private": bool("False")
    }
    return note_data_to_change_bool


@pytest.fixture()
def tags_set_data():
    tags_set_data = {
        "tags": [
            1, 2
        ]
    }
    return tags_set_data


@pytest.fixture()
def tags_set_data_wrong():
    tags_set_data_wrong = {
        "tags": [
            1, 3
        ]
    }
    return tags_set_data_wrong
