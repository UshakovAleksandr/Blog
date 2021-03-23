import json


class TestUsers:

    def test_get_user_by_id(self, client, create_test_user1):
        res = client.get("/users")
        assert res.status_code == 200
        data = json.loads(res.data)
        assert data[0]["username"] == create_test_user1.username

    def test_get_user_not_found_by_id(self, client, db_create):
        res = client.get("/users/1")
        assert res.status_code == 404
        data = json.loads(res.data)
        assert data["error"] == "No user with id=1"

    def test_get_users(self, client, db_create, create_test_user1_and_user2):
        res = client.get("/users")
        assert res.status_code == 200
        data = json.loads(res.data)
        assert data[0]["username"] == create_test_user1_and_user2[0].username
        assert data[1]["username"] == create_test_user1_and_user2[1].username

    def test_get_users_not_found(self, client, db_create):
        res = client.get("/users")
        assert res.status_code == 404
        data = json.loads(res.data)
        assert data["error"] == "No users yet"

    def test_post_user_creation(self, client, db_create):
        user_data = {
            "username": 'user',
            'password': 'user'
        }

        res = client.post("/users", data=json.dumps(user_data), content_type="application/json")
        assert res.status_code == 201
        data = json.loads(res.data)
        assert data["username"] == user_data["username"]
        assert data["id"] == 1

    def test_post_user_creation_the_same_username(self, client, db_create, create_test_user1):
        new_user_data = {
            "username": 'user1',
            'password': 'user1'
        }
        res = client.post('/users', data=json.dumps(new_user_data), content_type="application/json")
        assert res.status_code == 404
        data = json.loads(res.data)
        assert data["error"] == f"An error occurred while adding new user" \
                                "or a user with such name is already exist. " \
                                "You can only add a unique name"

    def test_put_user_by_id(self, client, db_create, create_test_user1):
        user_data_to_change = {
            "username": 'admin1'
        }

        res = client.put(f"/users/{create_test_user1.id}", data=json.dumps(user_data_to_change),
                         content_type="application/json")
        assert res.status_code == 200
        data = json.loads(res.data)
        assert data["username"] == user_data_to_change["username"]

    def test_put_user_by_id_not_found(self, client, db_create):
        user_data_to_change = {
            "username": 'admin1'
        }

        res = client.put(f"/users/1", data=json.dumps(user_data_to_change),
                         content_type="application/json")
        assert res.status_code == 404
        data = json.loads(res.data)
        assert data["error"] == "No user with id=1"

    def test_put_user_by_id_change_to_the_same_username(self, client, db_create, create_test_user1_and_user2):
        user_data_to_change = {
            "username": 'user1'
        }

        res = client.put(f"/users/{create_test_user1_and_user2[1].id}",
                         data=json.dumps(user_data_to_change), content_type="application/json")
        assert res.status_code == 404
        data = json.loads(res.data)
        assert data["error"] == "An error occurred while changing the user"

    def test_delete_by_id(self, client, db_create, create_test_user1):
        res = client.delete(f"users/{create_test_user1.id}")
        assert res.status_code == 200
        data = json.loads(res.data)
        assert data == f"User with id={create_test_user1.id} deleted"

    def test_delete_by_id_not_found(self, client, db_create):
        res = client.delete(f"users/1")
        assert res.status_code == 404
        data = json.loads(res.data)
        assert data["error"] == "User with id=1 is not exists"
