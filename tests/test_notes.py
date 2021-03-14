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
        res = self.client.get("/users")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data[0]["username"], user_data["username"])

        note_data = {
            "note": 'test note 1'
        }

        note = NoteModel(author_id=user.id, **note_data)
        note.save()
        note_id = note.id

        headers = {
            'Authorization': 'Basic ' + b64encode(
                f"{user_data['username']}:{user_data['password']}".encode('ascii')).decode('utf-8')
        }

        res = self.client.get(f"/notes/{note_id}", headers=headers)
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data["note"], f"test note {note_id}")

    def test_get_note_by_id_not_found(self):
        user_data = {
            "username": 'test',
            'password': 'test'
        }

        user = UserModel(**user_data)
        user.save()
        res = self.client.get("/users")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data[0]["username"], user_data["username"])

        headers = {
            'Authorization': 'Basic ' + b64encode(
                f"{user_data['username']}:{user_data['password']}".encode('ascii')).decode('utf-8')
        }
        res = self.client.get('/notes/1', headers=headers)
        self.assertEqual(res.status_code, 404)
        data = json.loads(res.data)
        self.assertEqual(data["error"], "Note with id=1 not found")

    def test_get_note_by_id_note_doesnt_belong_to_user(self):
        user_data1 = {
            "username": 'test1',
            'password': 'test1'
        }
        user1 = UserModel(**user_data1)
        user1.save()
        res = self.client.get("/users")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data[0]["username"], user_data1["username"])
        note_data1 = {
            "note": 'test note 1'
        }
        note1 = NoteModel(author_id=user1.id, **note_data1)
        note1.save()
        note1_id = note1.id

        user_data2 = {
            "username": 'test2',
            'password': 'test2'
        }
        user2 = UserModel(**user_data2)
        user2.save()
        res = self.client.get("/users")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data[0]["username"], user_data1["username"])
        note_data2 = {
            "note": 'test note 2'
        }
        note2 = NoteModel(author_id=user1.id, **note_data2)
        note2.save()

        headers = {
            'Authorization': 'Basic ' + b64encode(
                f"{user_data2['username']}:{user_data2['password']}".encode('ascii')).decode('utf-8')
        }

        res = self.client.get(f"/notes/{note1_id}", headers=headers)
        self.assertEqual(res.status_code, 403)
        data = json.loads(res.data)
        self.assertEqual(data["error"], f"Access denied to note with id={note1_id}")

    def test_get_notes(self):
        user_data = {
                "username": 'test',
                'password': 'test'
            }

        user = UserModel(**user_data)
        user.save()
        res = self.client.get("/users")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data[0]["username"], user_data["username"])

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
            'Authorization': 'Basic ' + b64encode(
                f"{user_data['username']}:{user_data['password']}".encode('ascii')).decode('utf-8')
        }
        res = self.client.get('/notes', headers=headers)
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(len(data), 2)

    def test_get_notes_not_found(self):
        user_data = {
                "username": 'test',
                'password': 'test'
            }

        user = UserModel(**user_data)
        user.save()
        res = self.client.get("/users")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data[0]["username"], user_data["username"])

        headers = {
            'Authorization': 'Basic ' + b64encode(
                f"{user_data['username']}:{user_data['password']}".encode('ascii')).decode('utf-8')
        }
        res = self.client.get('/notes', headers=headers)
        self.assertEqual(res.status_code, 404)
        data = json.loads(res.data)
        self.assertEqual(data["error"], "You have no notes yet")

    def test_post_create_note(self):
        user_data = {
            "username": 'test',
            'password': 'test'
        }
        user = UserModel(**user_data)
        user.save()
        res = self.client.get("/users")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data[0]["username"], user_data["username"])
        headers = {
            'Authorization': 'Basic ' + b64encode(
                f"{user_data['username']}:{user_data['password']}".encode('ascii')).decode('utf-8')
        }

        note_data = {
            "note": 'test note 1'
        }
        res = self.client.post("/notes", headers=headers, data=json.dumps(note_data), content_type="application/json")
        self.assertEqual(res.status_code, 201)
        data = json.loads(res.data)
        self.assertEqual(data["note"], note_data["note"])

    def test_put_note_by_id(self):
        user_data = {
            "username": 'test',
            'password': 'test'
        }

        user = UserModel(**user_data)
        user.save()
        res = self.client.get("/users")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data[0]["username"], user_data["username"])

        note_data = {
            "note": 'test note 1'
        }

        note = NoteModel(author_id=user.id, **note_data)
        note.save()
        note_id = note.id

        headers = {
            'Authorization': 'Basic ' + b64encode(
                f"{user_data['username']}:{user_data['password']}".encode('ascii')).decode('utf-8')
        }

        res = self.client.get(f"/notes/{note_id}", headers=headers)
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data["note"], "test note 1")

        note_data_to_change = {
            "note": 'test note 2',
            "private": bool("False")
        }

        res = self.client.put(f"/notes/{note_id}", headers=headers, data=json.dumps(note_data_to_change),
                              content_type="application/json")
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data["note"], note_data_to_change["note"])
        self.assertEqual(data["private"], note_data_to_change["private"])

    def test_put_note_by_id_not_found(self):
        user_data = {
            "username": 'test',
            'password': 'test'
        }

        user = UserModel(**user_data)
        user.save()
        res = self.client.get("/users")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data[0]["username"], user_data["username"])

        headers = {
            'Authorization': 'Basic ' + b64encode(
                f"{user_data['username']}:{user_data['password']}".encode('ascii')).decode('utf-8')
        }

        note_data_to_change = {
            "note": 'test note 2',
            "private": bool("False")
        }

        res = self.client.put("/notes/1", headers=headers, data=json.dumps(note_data_to_change),
                              content_type="application/json")
        self.assertEqual(res.status_code, 404)
        data = json.loads(res.data)
        self.assertEqual(data["error"], "Note with id=1 not found")

    def test_put_note_by_id_note_doesnt_belong_to_user(self):
        user_data1 = {
            "username": 'test1',
            'password': 'test1'
        }
        user1 = UserModel(**user_data1)
        user1.save()
        res = self.client.get("/users")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data[0]["username"], user_data1["username"])
        note_data1 = {
            "note": 'test note 1'
        }
        note1 = NoteModel(author_id=user1.id, **note_data1)
        note1.save()
        note1_id = note1.id

        user_data2 = {
            "username": 'test2',
            'password': 'test2'
        }
        user2 = UserModel(**user_data2)
        user2.save()
        res = self.client.get("/users")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data[0]["username"], user_data1["username"])
        note_data2 = {
            "note": 'test note 2'
        }
        note2 = NoteModel(author_id=user1.id, **note_data2)
        note2.save()

        note_data_to_change = {
            "note": 'test note 2',
            "private": bool("False")
        }

        headers = {
            'Authorization': 'Basic ' + b64encode(
                f"{user_data2['username']}:{user_data2['password']}".encode('ascii')).decode('utf-8')
        }

        res = self.client.put(f"/notes/{note1_id}", headers=headers, data=json.dumps(note_data_to_change),
                              content_type="application/json")
        self.assertEqual(res.status_code, 403)
        data = json.loads(res.data)
        self.assertEqual(data["error"], f"Access denied to note with id={note1_id}")

    def test_delete_note_by_id(self):
        user_data = {
            "username": 'test',
            'password': 'test'
        }

        user = UserModel(**user_data)
        user.save()
        res = self.client.get("/users")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data[0]["username"], user_data["username"])

        note_data = {
            "note": 'test note 1'
        }

        note = NoteModel(author_id=user.id, **note_data)
        note.save()
        note_id = note.id

        headers = {
            'Authorization': 'Basic ' + b64encode(
                f"{user_data['username']}:{user_data['password']}".encode('ascii')).decode('utf-8')
        }

        res = self.client.delete(f"/notes/{note_id}", headers=headers)
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data, f"Note with id={note_id} deleted")

    def test_delete_note_by_id_not_found(self):
        user_data = {
            "username": 'test',
            'password': 'test'
        }

        user = UserModel(**user_data)
        user.save()
        res = self.client.get("/users")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data[0]["username"], user_data["username"])

        headers = {
            'Authorization': 'Basic ' + b64encode(
                f"{user_data['username']}:{user_data['password']}".encode('ascii')).decode('utf-8')
        }

        res = self.client.delete(f"/notes/1", headers=headers)
        self.assertEqual(res.status_code, 404)
        data = json.loads(res.data)
        self.assertEqual(data["error"], f"Note with id=1 not found")

    def test_delete_note_by_id_note_doesnt_belong_to_user(self):
        user_data1 = {
            "username": 'test1',
            'password': 'test1'
        }
        user1 = UserModel(**user_data1)
        user1.save()
        res = self.client.get("/users")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data[0]["username"], user_data1["username"])
        note_data1 = {
            "note": 'test note 1'
        }
        note1 = NoteModel(author_id=user1.id, **note_data1)
        note1.save()
        note1_id = note1.id

        user_data2 = {
            "username": 'test2',
            'password': 'test2'
        }
        user2 = UserModel(**user_data2)
        user2.save()
        res = self.client.get("/users")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data[0]["username"], user_data1["username"])

        headers = {
            'Authorization': 'Basic ' + b64encode(
                f"{user_data2['username']}:{user_data2['password']}".encode('ascii')).decode('utf-8')
        }

        res = self.client.delete(f"/notes/{note1_id}", headers=headers)
        self.assertEqual(res.status_code, 403)
        data = json.loads(res.data)
        self.assertEqual(data["error"], f"Access denied to note with id={note1_id}")

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
