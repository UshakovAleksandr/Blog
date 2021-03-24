import json


class TestTags:

    def test_get_tag_by_id(self, client, create_test_tag1_by_user1, auth_headers):
        """
        Тест получения тега по id
        :param client: клиент flask
        :param create_test_tag1_by_user1: создание пользователя и тега
        :param auth_headers: аутентификация
        """
        res = client.get(f"/tags/{create_test_tag1_by_user1[0].id}", headers=auth_headers)
        assert res.status_code == 200
        data = json.loads(res.data)
        assert data["name"] == create_test_tag1_by_user1[0].name

    def test_get_tag_by_id_not_found(self, client, create_test_user1, auth_headers):
        """
        Тест получения тега по id, тег не найден
        :param client: клиент flask
        :param create_test_user1: создание пользователя
        :param auth_headers: аутентификация
        """
        res = client.get("/tags/1", headers=auth_headers)
        assert res.status_code == 404
        data = json.loads(res.data)
        assert data["error"] == "Tag with id=1 not found"

    def test_get_tags(self, client, create_test_tag1_and_tag2_by_user1, auth_headers):
        """
        Тест получения тегов
        :param client: клиент flask
        :param create_test_tag1_and_tag2_by_user1: создание пользователя и тегов
        :param auth_headers: аутентификация
        """
        res = client.get(f"/tags", headers=auth_headers)
        assert res.status_code == 200
        data = json.loads(res.data)
        assert data[0]["name"] == create_test_tag1_and_tag2_by_user1[0].name
        assert data[1]["name"] == create_test_tag1_and_tag2_by_user1[1].name

    def test_get_tags_not_found(self, client, create_test_user1, auth_headers):
        """
        Тест получения тегов, теги не найдены
        :param client: клиент flask
        :param create_test_user1: создание пользователя
        :param auth_headers: аутентификация
        """
        res = client.get(f"/tags", headers=auth_headers)
        assert res.status_code == 404
        data = json.loads(res.data)
        assert data["error"] == "No tags yet"

    def test_post_tag_creation(self, client, create_test_user1, auth_headers, tag_data1):
        """
        Тест создания тега
        :param client: клиент flask
        :param create_test_user1: создание пользователя
        :param auth_headers: аутентификация
        :param tag_data1: параметры для создания
        """
        res = client.post("/tags", headers=auth_headers,
                          data=json.dumps(tag_data1), content_type="application/json")
        assert res.status_code == 201
        data = json.loads(res.data)
        assert data["name"] == tag_data1["name"]

    def test_post_tag_creation_the_same_name(self, client, create_test_tag1_by_user1, auth_headers, tag_data1):
        """
        Тест создания дубля тега
        :param client: клиент flask
        :param create_test_tag1_by_user1: создание пользователя и тега
        :param auth_headers: аутентификация
        :param tag_data1: параметры для создания
        """
        res = client.post("/tags", headers=auth_headers,
                          data=json.dumps(tag_data1), content_type="application/json")
        assert res.status_code == 404
        data = json.loads(res.data)
        assert data["error"] == "An error occurred while adding new tag or" \
                                " a tag with such name is already exist." \
                                " You can only add a unique tag"

    def test_put_tag_by_id(self, client, create_test_tag1_by_user1, auth_headers, tag_data_to_change):
        """
        Тест изменения тега по id
        :param client: клиент flask
        :param create_test_tag1_by_user1: создание пользователя и тега
        :param auth_headers: аутентификация
        :param tag_data_to_change: параметры для изменения
        """
        res = client.put(f"tags/{create_test_tag1_by_user1[1][0].id}",
                         headers=auth_headers,
                         data=json.dumps(tag_data_to_change), content_type="application/json")
        assert res.status_code == 200
        data = json.loads(res.data)
        assert data["name"] == tag_data_to_change["name"]

    def test_put_tag_by_id_not_found(self, client, create_test_tag1_by_user1, auth_headers, tag_data_to_change):
        """
        Тест изменения тега по id, тег не найден
        :param client: клиент flask
        :param create_test_tag1_by_user1: создание пользователя и тега
        :param auth_headers: аутентификация
        :param tag_data_to_change: параметры для изменения
        """
        res = client.put("tags/2", headers=auth_headers,
                         data=json.dumps(tag_data_to_change), content_type="application/json")
        assert res.status_code == 404
        data = json.loads(res.data)
        assert data["error"] == "Tag with id=2 not found"

    def test_put_tag_by_id_change_to_the_same_name(self, client, create_test_tag1_and_tag2_by_user1,
                                                   auth_headers, tag_data_to_change):
        """
        Тест изменения тега по id на дубль
        :param client: клиент flask
        :param create_test_tag1_and_tag2_by_user1: создание пользователя и тега
        :param auth_headers: аутентификация
        :param tag_data_to_change: параметры для изменения
        """
        res = client.put("tags/1", headers=auth_headers,
                         data=json.dumps(tag_data_to_change), content_type="application/json")
        assert res.status_code == 404
        data = json.loads(res.data)
        assert data["error"] == f"An error occurred while changing tag " \
                                f"or a tag with such name is already exist."

    def test_delete_tag_by_id(self, client, create_test_tag1_by_user1, auth_headers):
        """
        Тест удаления тега по id
        :param client: клиент flask
        :param create_test_tag1_by_user1: создание пользователя и тега
        :param auth_headers: аутентификация
        """
        res = client.delete("tags/1", headers=auth_headers)
        assert res.status_code == 200
        data = json.loads(res.data)
        assert data == "Tag with id=1 deleted"

    def test_delete_tag_by_id_not_found(self, client, create_test_user1, auth_headers):
        """
        Тест удаления тега по id, тег не найден
        :param client: клиент flask
        :param create_test_user1: создание пользователя и тега
        :param auth_headers: аутентификация
        """
        res = client.delete("tags/1", headers=auth_headers)
        assert res.status_code == 404
        data = json.loads(res.data)
        assert data["error"] == "Tag with id=1 not found"
