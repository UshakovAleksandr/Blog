import json


class TestNotes:

    def test_get_note_by_id(self, client, create_test_note1_by_user1, auth_headers):
        res = client.get(f"/notes/{create_test_note1_by_user1[1][0].id}", headers=auth_headers)
        assert res.status_code == 200
        data = json.loads(res.data)
        assert data["note"], create_test_note1_by_user1[0].note

    def test_get_note_by_id_not_found(self, client, create_test_user1, auth_headers):
        res = client.get('/notes/1', headers=auth_headers)
        assert res.status_code == 404
        data = json.loads(res.data)
        assert data["error"] == "Note with id=1 not found"

    def test_get_note_by_id_note_doesnt_belong_to_user(self, client, create_test_note1_by_user1,
                                                       create_test_note2_by_user2, auth_headers):
        res = client.get(f"/notes/{create_test_note2_by_user2[0].id}", headers=auth_headers)
        assert res.status_code == 403
        data = json.loads(res.data)
        assert data["error"] == f"Access denied to note with id={create_test_note2_by_user2[0].id}"

    def test_get_notes(self, client, create_test_note1_and_note2_by_user1, auth_headers):
        res = client.get(f"/notes", headers=auth_headers)
        assert res.status_code == 200
        data = json.loads(res.data)
        assert len(data) == 2

    def test_get_notes_not_found(self, client, create_test_user1, auth_headers):
        res = client.get(f"/notes", headers=auth_headers)
        assert res.status_code == 404
        data = json.loads(res.data)
        assert data["error"] == "You have no notes yet"

    def test_post_create_note(self, client, create_test_user1, note_data, auth_headers):
        res = client.post("/notes", headers=auth_headers,
                          data=json.dumps(note_data), content_type="application/json")
        assert res.status_code == 201
        data = json.loads(res.data)
        assert data["note"], note_data["note"]

    def test_put_note_by_id(self, client, create_test_note1_by_user1, auth_headers, note_data_to_change):
        res = client.put(f"/notes/{create_test_note1_by_user1[0].id}", headers=auth_headers,
                         data=json.dumps(note_data_to_change), content_type="application/json")
        assert res.status_code == 200
        data = json.loads(res.data)
        assert data["note"], note_data_to_change["note"]

    def test_put_note_by_id_not_found(self, client, create_test_note1_by_user1, auth_headers, note_data_to_change):
        res = client.put("/notes/2", headers=auth_headers,
                         data=json.dumps(note_data_to_change), content_type="application/json")
        assert res.status_code == 404
        data = json.loads(res.data)
        assert data["error"] == "Note with id=2 not found"

    #def test_put_note_by_id_note_doesnt_belong_to_user(self, client, c):
















