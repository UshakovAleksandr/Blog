import json
from api import db
from app import app, Config
from unittest import TestCase
from api.models.user import UserModel
from api.models.note import NoteModel
from api.models.tag import TagModel
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

    def create_test_user_and_no_notes(self):
        user_data = {
            "username": 'admin',
            'password': 'admin'
        }

        user = UserModel(**user_data)
        user.save()
        res = self.client.get("/users")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data[0]["username"], user_data["username"])
        return user_data

    def create_test_user1_note1_by_user1(self):
        user_data1 = {
            "username": 'admin',
            'password': 'admin'
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

        return note1, user1, user_data1

    def create_test_user2_note2_by_user2(self):
        user_data2 = {
            "username": 'admin1',
            'password': 'admin1'
        }

        user2 = UserModel(**user_data2)
        user2.save()
        res = self.client.get("/users")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data[1]["username"], user_data2["username"])

        note_data = {
            "note": 'test note 2'
        }

        note = NoteModel(author_id=user2.id, **note_data)
        note.save()

        return note, user2, user_data2

    def create_test_note1_and_note2_by_user1(self):
        user_data = {
            "username": 'admin',
            'password': 'admin'
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

        return user, user_data

    def create_test_user1_note1_tag1_tag1(self):
        user_data = {
            "username": 'admin',
            'password': 'admin'
        }

        user = UserModel(**user_data)
        user.save()
        res = self.client.get("/users")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data[0]["username"], user_data["username"])

        note_data1 = {
            "note": 'test note 1'
        }

        note = NoteModel(author_id=user.id, **note_data1)
        note.save()

        tags_data = [
            {
                "name": 'test1 tag'
            },
            {
                "name": 'test2 tag'
            }
        ]
        for tag_data in tags_data:
            tag = TagModel(author_id=user.id, **tag_data)
            tag.save()

        return user, note, user_data, tags_data

    def auth_headers(self, user):
        return {
            'Authorization': 'Basic ' + b64encode(
                f"{user['username']}:{user['password']}".encode('ascii')).decode('utf-8')
        }

    def test_get_note_by_id(self):
        user_and_note = TestNotes.create_test_user1_note1_by_user1(self)
        print(user_and_note)
        res = self.client.get(f"/notes/{user_and_note[0].id}",
                              headers=TestNotes.auth_headers(self, user_and_note[2]))
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data["note"], user_and_note[0].note)

    def test_get_note_by_id_not_found(self):
        user_and_note = TestNotes.create_test_user1_note1_by_user1(self)

        res = self.client.get('/notes/2', headers=TestNotes.auth_headers(self, user_and_note[2]))
        self.assertEqual(res.status_code, 404)
        data = json.loads(res.data)
        self.assertEqual(data["error"], "Note with id=2 not found")

    def test_get_note_by_id_note_doesnt_belong_to_user(self):
        user_and_note1 = TestNotes.create_test_user1_note1_by_user1(self)
        user_and_note2 = TestNotes.create_test_user2_note2_by_user2(self)

        res = self.client.get(f"/notes/{user_and_note1[0].id}", headers=TestNotes.auth_headers(self, user_and_note2[2]))
        self.assertEqual(res.status_code, 403)
        data = json.loads(res.data)
        self.assertEqual(data["error"], f"Access denied to note with id={user_and_note1[0].id}")

    def test_get_notes(self):
        user = TestNotes.create_test_note1_and_note2_by_user1(self)

        res = self.client.get('/notes', headers=TestNotes.auth_headers(self, user[1]))
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(len(data), 2)

    def test_get_notes_not_found(self):
        user = TestNotes.create_test_user_and_no_notes(self)

        res = self.client.get('/notes', headers=TestNotes.auth_headers(self, user))
        self.assertEqual(res.status_code, 404)
        data = json.loads(res.data)
        self.assertEqual(data["error"], "You have no notes yet")

    def test_post_create_note(self):
        user = TestNotes.create_test_user_and_no_notes(self)
        note_data = {
            "note": 'test note 1'
        }
        res = self.client.post("/notes", headers=TestNotes.auth_headers(self, user),
                               data=json.dumps(note_data), content_type="application/json")
        self.assertEqual(res.status_code, 201)
        data = json.loads(res.data)
        self.assertEqual(data["note"], note_data["note"])

    def test_put_note_by_id(self):
        user_and_note = TestNotes.create_test_user1_note1_by_user1(self)

        note_data_to_change = {
            "note": 'test note 2'
        }

        res = self.client.put(f"/notes/{user_and_note[0].id}",
                              headers=TestNotes.auth_headers(self, user_and_note[2]),
                              data=json.dumps(note_data_to_change),
                              content_type="application/json")
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data["note"], note_data_to_change["note"])

    def test_put_note_by_id_not_found(self):
        user_and_note = TestNotes.create_test_user1_note1_by_user1(self)

        note_data_to_change = {
            "note": 'test note 2',
            "private": bool("False")
        }

        res = self.client.put("/notes/2", headers=TestNotes.auth_headers(self, user_and_note[2]),
                              data=json.dumps(note_data_to_change),
                              content_type="application/json")
        self.assertEqual(res.status_code, 404)
        data = json.loads(res.data)
        self.assertEqual(data["error"], "Note with id=2 not found")

    def test_put_note_by_id_note_doesnt_belong_to_user(self):
        user_and_note1 = TestNotes.create_test_user1_note1_by_user1(self)
        user_and_note2 = TestNotes.create_test_user2_note2_by_user2(self)

        note_data_to_change = {
            "private": bool("False")
        }

        res = self.client.put(f"/notes/{user_and_note2[0].id}",
                              headers=TestNotes.auth_headers(self, user_and_note1[2]),
                              data=json.dumps(note_data_to_change),
                              content_type="application/json")
        self.assertEqual(res.status_code, 403)
        data = json.loads(res.data)
        self.assertEqual(data["error"], f"Access denied to note with id={user_and_note2[0].id}")

    def test_delete_note_by_id(self):
        user_and_note = TestNotes.create_test_user1_note1_by_user1(self)

        res = self.client.delete(f"/notes/{user_and_note[0].id}",
                                 headers=TestNotes.auth_headers(self, user_and_note[2]))
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data, f"Note with id={user_and_note[0].id} deleted")

    def test_delete_note_by_id_not_found(self):
        user_and_note = TestNotes.create_test_user1_note1_by_user1(self)

        res = self.client.delete(f"/notes/2", headers=TestNotes.auth_headers(self, user_and_note[2]))
        self.assertEqual(res.status_code, 404)
        data = json.loads(res.data)
        self.assertEqual(data["error"], f"Note with id=2 not found")

    def test_delete_note_by_id_note_doesnt_belong_to_user(self):
        user_and_note1 = TestNotes.create_test_user1_note1_by_user1(self)
        user_and_note2 = TestNotes.create_test_user2_note2_by_user2(self)

        res = self.client.delete(f"/notes/{user_and_note1[0].id}",
                                 headers=TestNotes.auth_headers(self, user_and_note2[2]))
        self.assertEqual(res.status_code, 403)
        data = json.loads(res.data)
        self.assertEqual(data["error"], f"Access denied to note with id={user_and_note1[0].id}")

    def test_put_tag_set_to_note(self):
        user_note_tags = TestNotes.create_test_user1_note1_tag1_tag1(self)

        tags_set_data = {
            "tags": [
                1, 2
            ]
        }

        res = self.client.put(f"/notes/{user_note_tags[0].id}/tags/set",
                              headers=TestNotes.auth_headers(self, user_note_tags[2]),
                              data=json.dumps(tags_set_data),
                              content_type="application/json")
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data["tags"][0]["name"], user_note_tags[3][0]["name"])
        self.assertEqual(data["tags"][1]["name"], user_note_tags[3][1]["name"])

    def test_put_tag_set_to_note_note_not_found(self):
        user_note_tags = TestNotes.create_test_user1_note1_tag1_tag1(self)

        tags_set_data = {
            "tags": [
                1, 2
            ]
        }

        res = self.client.put(f"/notes/2/tags/set", headers=TestNotes.auth_headers(self, user_note_tags[2]),
                              data=json.dumps(tags_set_data), content_type="application/json")
        self.assertEqual(res.status_code, 404)
        data = json.loads(res.data)
        self.assertEqual(data["error"], "note with id=2 not found")

    def test_put_tag_set_to_note_tag_not_found(self):
        user_note_tags = TestNotes.create_test_user1_note1_tag1_tag1(self)

        tags_set_data = {
            "tags": [
                1, 3
            ]
        }

        res = self.client.put(f"/notes/{user_note_tags[0].id}/tags/set",
                              headers=TestNotes.auth_headers(self, user_note_tags[2]),
                              data=json.dumps(tags_set_data), content_type="application/json")
        self.assertEqual(res.status_code, 404)
        data = json.loads(res.data)
        self.assertEqual(data["error"], f"Tag with id={tags_set_data['tags'][1]} not found")

    def test_get_note_by_tags(self):
        user_note_tags = TestNotes.create_test_user1_note1_tag1_tag1(self)
        tags_set_data = {
            "tags": [
                1, 2
            ]
        }

        res = self.client.put(f"/notes/{user_note_tags[0].id}/tags/set",
                              headers=TestNotes.auth_headers(self, user_note_tags[2]),
                              data=json.dumps(tags_set_data),
                              content_type="application/json")
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data["tags"][0]["name"], user_note_tags[3][0]["name"])
        self.assertEqual(data["tags"][1]["name"], user_note_tags[3][1]["name"])

        res = self.client.get("/notes/filter?tags=test1 tag&tags=test2 tag")
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data[0]["note"], user_note_tags[1].note)

    def test_get_note_by_tags_note_not_found(self):
        user_note_tags = TestNotes.create_test_user1_note1_tag1_tag1(self)

        tags_set_data = {
            "tags": [
                1, 2
            ]
        }
        res = self.client.put(f"/notes/{user_note_tags[0].id}/tags/set",
                              headers=TestNotes.auth_headers(self, user_note_tags[2]),
                              data=json.dumps(tags_set_data),
                              content_type="application/json")
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data["tags"][0]["name"], user_note_tags[3][0]["name"])
        self.assertEqual(data["tags"][1]["name"], user_note_tags[3][1]["name"])

        res = self.client.get("/notes/filter?tags=test1 tag&tags=test3 tag")
        self.assertEqual(res.status_code, 404)
        data = json.loads(res.data)
        self.assertEqual(data["error"], f"Note with tag_name=test3 tag not found")

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
