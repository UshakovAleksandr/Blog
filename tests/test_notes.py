import json
from api import db
from app import app, Config
from unittest import TestCase
from api.models.user import UserModel
from api.models.note import NoteModel
from base64 import b64encode


class TestNotes(TestCase):
    def setUp(self):
        self.app = app
        self.app.config.update({
            'SQLALCHEMY_DATABASE_URI': Config.TEST_DATABASE_URI
        })
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