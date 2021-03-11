import json
from api import db
from app import app
from unittest import TestCase
from api.models.user import UserModel
from api.models.note import NoteModel
from base64 import b64encode


class TestUsers(TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def test_users_get(self):
        users_data = [
           {
               "username": 'admin',
               'password': 'admin'
           },
           {
               "username": 'ivan',
               'password': '12345'
           },
        ]
        for user_data in users_data:
            user = UserModel(**user_data)
            user.save()

        res = self.client.get('/users')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        print(data)
        self.assertEqual(data[0]["username"], users_data[0]["username"])
        self.assertEqual(data[1]["username"], users_data[1]["username"])

    def test_user_creation(self):
        user_data = {
           "username": 'admin',
           'password': 'admin'
        }
        res = self.client.post('/users', data=json.dumps(user_data), content_type="application/json")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 201)
        self.assertIn('admin', data.values())

    def test_user_get_by_id(self):
        user_data = {
            "username": 'admin',
            'password': 'admin'
        }
        # user = UserModel(username=user_data['username'], password=user_data['password'])
        user = UserModel(**user_data)
        user.save()
        user_id = user.id
        response = self.client.get(f'/users/{user_id}')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["username"], user_data["username"])

    def test_user_not_found_by_id(self):
        response = self.client.get("/users/2")
        self.assertEqual(response.status_code, 404)

    def test_user_not_found(self):
        res = self.client.get('/users/1')
        self.assertEqual(res.status_code, 404)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


class TestNotes(TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def test_get_note_by_id(self):
        user_data = {
                "username": 'test',
                'password': 'test'
            }

        user = UserModel(**user_data)
        user.save()

        notes_data = [
            {
                "note": 'test note 1'
            },
            {
                "note": 'test note 2'
            },
        ]
        ids = []
        for note_data in notes_data:
            note = NoteModel(author_id=user.id, **note_data)
            note.save()
            ids.append(note.id)

        headers = {
            'Authorization': 'Basic ' + b64encode(f"{user_data['username']}:{user_data['password']}".encode('ascii')).decode('utf-8')
        }
        res = self.client.get('/notes', headers=headers)
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(len(data), 2)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


# python -m unittest tests/test.py