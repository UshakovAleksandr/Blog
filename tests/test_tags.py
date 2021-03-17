import json
from api import db
from app import app, Config
from unittest import TestCase
from api.models.tag import TagModel


class TestUsers(TestCase):
    def setUp(self):
        self.app = app
        self.app.config.update({
            'SQLALCHEMY_DATABASE_URI': Config.TEST_DATABASE_URI
        })
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def test_get_tag_by_id(self):
        tag_data = {
            "name": 'test tag'
        }

        tag = TagModel(**tag_data)
        tag.save()
        tag_id = tag.id

        res = self.client.get(f"/tags/{tag_id}")
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data["name"], tag_data["name"])

    def test_get_tag_by_id_not_found(self):
        res = self.client.get(f"/tags/1")
        self.assertEqual(res.status_code, 404)
        data = json.loads(res.data)
        self.assertEqual(data["error"], "Tag with id=1 not found")

    def test_get_tags(self):
        tags_data = [
            {
                "name": 'test1 tag'
            },
            {
                "name": 'test2 tag'
            }
        ]

        for tag_data in tags_data:
            tag = TagModel(**tag_data)
            tag.save()

        res = self.client.get("/tags")
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data[0]["name"], tags_data[0]["name"])
        self.assertEqual(data[1]["name"], tags_data[1]["name"])

    def test_get_tags_not_found(self):
        res = self.client.get("/tags")
        self.assertEqual(res.status_code, 404)
        data = json.loads(res.data)
        self.assertEqual(data["error"], "No tags yet")

    def test_post_tag_creation(self):
        tag_data = {
            "name": 'test tag'
        }

        res = self.client.post("/tags", data=json.dumps(tag_data), content_type="application/json")
        self.assertEqual(res.status_code, 201)
        data = json.loads(res.data)
        self.assertEqual(data["name"], tag_data["name"])

    def test_post_tag_creation_the_same_name(self):
        tag_data = {
            "name": 'test tag'
        }
        res = self.client.post("/tags", data=json.dumps(tag_data), content_type="application/json")
        self.assertEqual(res.status_code, 201)
        data = json.loads(res.data)
        self.assertEqual(data["name"], tag_data["name"])

        tag_data = {
            "name": 'test tag'
        }
        res = self.client.post("/tags", data=json.dumps(tag_data), content_type="application/json")
        self.assertEqual(res.status_code, 404)
        data = json.loads(res.data)
        self.assertEqual(data["error"], "An error occurred while adding new tag" 
                                        " or a tag with such name is already exist. " 
                                        "You can only add a unique tag")

    def test_put_tag_by_id(self):
        tag_data = {
            "name": 'test tag'
        }

        tag = TagModel(**tag_data)
        tag.save()
        tag_id = tag.id

        res = self.client.get(f"/tags/{tag_id}")
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data["name"], tag_data["name"])

        tag_data_to_change = {
            "name": 'test tag1'
        }

        res = self.client.put(f"tags/{tag_id}", data=json.dumps(tag_data_to_change),
                              content_type="application/json")
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data["name"], tag_data_to_change["name"])

    def test_put_tag_by_id_not_found(self):
        tag_data_to_change = {
            "name": 'test tag1'
        }

        res = self.client.put("tags/1", data=json.dumps(tag_data_to_change),
                              content_type="application/json")
        self.assertEqual(res.status_code, 404)
        data = json.loads(res.data)
        self.assertEqual(data["error"], "Tag with id=1 not found")

    def test_put_tag_by_id_change_to_the_same_name(self):
        tag_data1 = {
            "name": 'test tag 1'
        }

        tag1 = TagModel(**tag_data1)
        tag1.save()
        tag1_id = tag1.id

        res = self.client.get(f"/tags/{tag1_id}")
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data["name"], tag_data1["name"])

        tag_data2 = {
            "name": 'test tag 2'
        }

        tag2 = TagModel(**tag_data2)
        tag2.save()
        tag_id2 = tag2.id

        res = self.client.get(f"/tags/{tag_id2}")
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data["name"], tag_data2["name"])

        tag_data_to_change = {
            "name": 'test tag 2'
        }

        res = self.client.put(f"tags/{tag1_id}", data=json.dumps(tag_data_to_change),
                              content_type="application/json")
        self.assertEqual(res.status_code, 404)
        data = json.loads(res.data)
        self.assertEqual(data["error"], f"An error occurred while changing tag"
                                        f" or a tag with such name is already exist.")

    def test_delete_tag_by_id(self):
        tag_data = {
            "name": 'test tag'
        }

        tag = TagModel(**tag_data)
        tag.save()
        tag_id = tag.id

        res = self.client.get(f"/tags/{tag_id}")
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data["name"], tag_data["name"])

        res = self.client.delete(f"tags/{tag_id}")
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data, f"Tag with id={tag_id} deleted")

    def test_delete_tag_by_id_not_found(self):
        res = self.client.delete("tags/1")
        self.assertEqual(res.status_code, 404)
        data = json.loads(res.data)
        self.assertEqual(data["error"], "Tag with id=1 not found")

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()