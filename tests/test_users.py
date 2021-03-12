import json
from api import db
from app import app, Config
from unittest import TestCase
from api.models.user import UserModel


class TestUsers(TestCase):
    def setUp(self):
        self.app = app
        self.app.config.update({
            'SQLALCHEMY_DATABASE_URI': Config.TEST_DATABASE_URI
        })
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def test_get_user_by_id(self):
        user_data = {
            "username": 'admin',
            'password': 'admin'
        }
        user = UserModel(**user_data)
        user.save()
        user_id = user.id

        res = self.client.get(f'/users/{user_id}')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["username"], user_data["username"])

    def test_get_user_not_found_by_id(self):
        res = self.client.get('/users/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["error"], "No user with id=1")

    def test_get_users(self):
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
        self.assertEqual(data[0]["username"], users_data[0]["username"])
        self.assertEqual(data[1]["username"], users_data[1]["username"])

    def test_get_users_not_found(self):
        res = self.client.get("/users")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["error"], "No users yet")

    def test_post_user_creation(self):
        user_data = {
           "username": 'admin',
           'password': 'admin'
        }
        res = self.client.post('/users', data=json.dumps(user_data), content_type="application/json")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 201)
        self.assertIn("admin", data.values())

    def test_post_user_creation_the_same_username(self):
        user_data = {
            "username": 'admin',
            'password': 'admin'
        }
        res = self.client.post('/users', data=json.dumps(user_data), content_type="application/json")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 201)
        self.assertIn("admin", data.values())

        new_user_data = {
            "username": 'admin',
            'password': 'admin'
        }
        res = self.client.post('/users', data=json.dumps(new_user_data), content_type="application/json")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["error"], "An error occurred while adding new user"
                                        "or a user with such name is already exist. "
                                        "You can only add a unique name")

    def test_put_user_by_id(self):
        user_data = {
            "username": 'admin',
            'password': 'admin'
        }
        user = UserModel(**user_data)
        user.save()
        user_id = user.id
        res = self.client.get(f"/users/{user_id}")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["username"], user_data["username"])

        user_data_to_change = {
            "username": 'admin1'
        }
        res = self.client.put(f"/users/{user_id}", data=json.dumps(user_data_to_change),
                              content_type="application/json")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["username"], user_data_to_change["username"])

    def test_put_user_by_id_not_found(self):
        user_data_to_change = {
            "username": 'admin1'
        }
        res = self.client.put("/users/1", data=json.dumps(user_data_to_change),
                              content_type="application/json")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["error"], "No user with id=1")

    def test_put_user_by_id_change_to_the_same_username(self):
        user_data1 = {
            "username": 'admin1',
            'password': 'admin1'
        }
        user1 = UserModel(**user_data1)
        user1.save()
        user_id = user1.id
        res = self.client.get(f"/users/{user_id}")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["username"], user_data1["username"])

        user_data1 = {
            "username": 'admin2',
            'password': 'admin2'
        }
        user2 = UserModel(**user_data1)
        user2.save()
        user_id = user2.id
        res = self.client.get(f"/users/{user_id}")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["username"], user_data1["username"])

        user_data_to_change = {
            "username": 'admin1'
        }
        res = self.client.put(f"/users/{user_id}", data=json.dumps(user_data_to_change),
                              content_type="application/json")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["error"], "An error occurred while changing the user")

    def test_delete_by_id(self):
        user_data = {
            "username": 'admin',
            'password': 'admin'
        }
        user = UserModel(**user_data)
        user.save()
        user_id = user.id
        res = self.client.delete(f"/users/{user_id}")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data, f"User with id={user_id} deleted")

    def test_delete_by_id_not_found(self):
        res = self.client.delete("/users/1")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["error"], "User with id=1 is not exists")

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


# python -m unittest tests/test_users.py