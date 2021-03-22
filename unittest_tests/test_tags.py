import json
from api import db
from app import app, Config
from unittest import TestCase
from api.models.user import UserModel
from api.models.tag import TagModel
from base64 import b64encode


class TestTags(TestCase):
    def setUp(self):
        self.app = app
        self.app.config.update({
            'SQLALCHEMY_DATABASE_URI': Config.TEST_DATABASE_URI
        })
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def create_test_user1(self):
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

    def create_test_tag1_by_user1(self):
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

        tag_data1 = {
            "name": 'test tag'
        }

        tag1 = TagModel(author_id=user1.id, **tag_data1)
        tag1.save()

        return tag1, user1, user_data1

    def create_test_tag1_and_tag2_by_user1(self):
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

        tags_data = [
            {
                "name": 'test1 tag'
            },
            {
                "name": 'test2 tag'
            }
        ]

        ids = []
        for tag_data in tags_data:
            tag = TagModel(author_id=user1.id, **tag_data)
            tag.save()
            ids.append(tag.id)

        return user1, user_data1, tags_data

    def auth_headers(self, user):
        return {
            'Authorization': 'Basic ' + b64encode(
                f"{user['username']}:{user['password']}".encode('ascii')).decode('utf-8')
        }

    def test_get_tag_by_id(self):
        user_and_tag = TestTags.create_test_tag1_by_user1(self)

        res = self.client.get(f"/tags/{user_and_tag[0].id}", headers=TestTags.auth_headers(self, user_and_tag[2]))
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data["name"], user_and_tag[0].name)

    def test_get_tag_by_id_not_found(self):
        user = TestTags.create_test_user1(self)

        res = self.client.get(f"/tags/1", headers=TestTags.auth_headers(self, user))
        self.assertEqual(res.status_code, 404)
        data = json.loads(res.data)
        self.assertEqual(data["error"], "Tag with id=1 not found")

    def test_get_tags(self):
        user_and_tags = TestTags.create_test_tag1_and_tag2_by_user1(self)

        res = self.client.get("/tags", headers=TestTags.auth_headers(self, user_and_tags[1]))
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data[0]["name"], user_and_tags[2][0]["name"])
        self.assertEqual(data[1]["name"], user_and_tags[2][1]["name"])

    def test_get_tags_not_found(self):
        user = TestTags.create_test_user1(self)

        res = self.client.get("/tags", headers=TestTags.auth_headers(self, user))
        self.assertEqual(res.status_code, 404)
        data = json.loads(res.data)
        self.assertEqual(data["error"], "No tags yet")

    def test_post_tag_creation(self):
        TestTags.create_test_tag1_by_user1(self)

    def test_post_tag_creation_the_same_name(self):
        user_and_tag = TestTags.create_test_tag1_by_user1(self)

        tag_data = {
            "name": 'test tag'
        }
        res = self.client.post("/tags", headers=TestTags.auth_headers(self, user_and_tag[2]),
                               data=json.dumps(tag_data), content_type="application/json")
        self.assertEqual(res.status_code, 404)
        data = json.loads(res.data)
        self.assertEqual(data["error"], "An error occurred while adding new tag" 
                                        " or a tag with such name is already exist. " 
                                        "You can only add a unique tag")

    def test_put_tag_by_id(self):
        user_and_tag = TestTags.create_test_tag1_by_user1(self)

        tag_data_to_change = {
            "name": 'test3 tag'
        }

        res = self.client.put("tags/1", headers=TestTags.auth_headers(self, user_and_tag[2]),
                              data=json.dumps(tag_data_to_change), content_type="application/json")
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data["name"], tag_data_to_change["name"])

    def test_put_tag_by_id_not_found(self):
        user = TestTags.create_test_user1(self)

        tag_data_to_change = {
            "name": 'test3 tag'
        }

        res = self.client.put("tags/1", headers=TestTags.auth_headers(self, user),
                              data=json.dumps(tag_data_to_change), content_type="application/json")
        self.assertEqual(res.status_code, 404)
        data = json.loads(res.data)
        self.assertEqual(data["error"], "Tag with id=1 not found")

    def test_put_tag_by_id_change_to_the_same_name(self):
        user_and_tags = TestTags.create_test_tag1_and_tag2_by_user1(self)

        tag_data_to_change = {
            "name": 'test2 tag'
        }

        res = self.client.put("tags/1", headers=TestTags.auth_headers(self, user_and_tags[1]),
                              data=json.dumps(tag_data_to_change), content_type="application/json")
        self.assertEqual(res.status_code, 404)
        data = json.loads(res.data)
        self.assertEqual(data["error"], f"An error occurred while changing tag"
                                        f" or a tag with such name is already exist.")

    def test_delete_tag_by_id(self):
        user_and_tag = TestTags.create_test_tag1_by_user1(self)

        res = self.client.delete("tags/1", headers=TestTags.auth_headers(self, user_and_tag[2]))
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data, "Tag with id=1 deleted")

    def test_delete_tag_by_id_not_found(self):
        user = TestTags.create_test_user1(self)

        res = self.client.delete("tags/1", headers=TestTags.auth_headers(self, user))
        self.assertEqual(res.status_code, 404)
        data = json.loads(res.data)
        self.assertEqual(data["error"], "Tag with id=1 not found")

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
