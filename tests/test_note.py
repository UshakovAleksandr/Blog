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

    def test_put_note_by_id_note_doesnt_belong_to_user(self, client, create_test_note1_by_user1,
                                                       create_test_note2_by_user2, note_data_to_change_bool,
                                                       auth_headers):
        res = client.put(f"/notes/{create_test_note2_by_user2[0].id}", headers=auth_headers,
                         data=json.dumps(note_data_to_change_bool), content_type="application/json")
        assert res.status_code == 403
        data = json.loads(res.data)
        assert data["error"] == f"Access denied to note with id={create_test_note2_by_user2[0].id}"

    def test_delete_note_by_id(self, client, create_test_note1_by_user1, auth_headers):
        res = client.delete(f"/notes/{create_test_note1_by_user1[0].id}", headers=auth_headers)
        assert res.status_code == 200
        data = json.loads(res.data)
        assert data == f"Note with id={create_test_note1_by_user1[0].id} deleted"

    def test_delete_note_by_id_not_found(self, client, create_test_user1, auth_headers):
        res = client.delete(f"/notes/1", headers=auth_headers)
        assert res.status_code == 404
        data = json.loads(res.data)
        assert data["error"] == f"Note with id=1 not found"

    def test_delete_note_by_id_note_doesnt_belong_to_user(self, client, create_test_note1_by_user1,
                                                          create_test_note2_by_user2, auth_headers):
        res = client.delete(f"/notes/{create_test_note2_by_user2[0].id}", headers=auth_headers)
        assert res.status_code == 403
        data = json.loads(res.data)
        assert data["error"] == f"Access denied to note with id={create_test_note2_by_user2[0].id}"

    def test_put_tag_set_to_note(self, client, create_test_user1_note1_tag1_tag2, tags_set_data, auth_headers):
        res = client.put(f"/notes/{create_test_user1_note1_tag1_tag2[0].id}/tags/set", headers=auth_headers,
                         data=json.dumps(tags_set_data), content_type="application/json")
        assert res.status_code == 200
        data = json.loads(res.data)
        assert data["tags"][0]["name"] == create_test_user1_note1_tag1_tag2[1][0].name
        assert data["tags"][1]["name"] == create_test_user1_note1_tag1_tag2[1][1].name

    def test_put_tag_set_to_note_note_not_found(self, client, create_test_user1_note1_tag1_tag2,
                                                tags_set_data, auth_headers):
        res = client.put("/notes/2/tags/set", headers=auth_headers,
                         data=json.dumps(tags_set_data), content_type="application/json")
        assert res.status_code == 404
        data = json.loads(res.data)
        assert data["error"] == "note with id=2 not found"

    def test_put_tag_set_to_note_note_doesnt_belong_to_user(self, client, create_test_user1_note1_tag1_tag2,
                                                            create_test_user2_note2_tag3_tag4, tags_set_data,
                                                            auth_headers):
        res = client.put(f"/notes/{create_test_user2_note2_tag3_tag4[0].id}/tags/set", headers=auth_headers,
                         data=json.dumps(tags_set_data), content_type="application/json")
        assert res.status_code == 403
        data = json.loads(res.data)
        assert data["error"] == f"Access denied to note with id={create_test_user2_note2_tag3_tag4[0].id}"

    def test_put_tag_set_to_note_tag_not_found(self, client, create_test_user1_note1_tag1_tag2,
                                               tags_set_data_wrong, auth_headers):
        res = client.put(f"/notes/{create_test_user1_note1_tag1_tag2[0].id}/tags/set", headers=auth_headers,
                         data=json.dumps(tags_set_data_wrong), content_type="application/json")
        assert res.status_code == 404
        data = json.loads(res.data)
        assert data["error"] == f"Tag with id={tags_set_data_wrong['tags'][1]} not found"

    def test_put_tag_set_to_note_tag_doesnt_belong_to_user(self, client, create_test_user1_note1_tag1_tag2,
                                                           create_test_user2_note2_tag3_tag4, tags_set_data_wrong,
                                                           auth_headers):
        res = client.put(f"/notes/{create_test_user1_note1_tag1_tag2[0].id}/tags/set", headers=auth_headers,
                         data=json.dumps(tags_set_data_wrong), content_type="application/json")
        assert res.status_code == 403
        data = json.loads(res.data)
        assert data["error"] == f"Access denied to tag with id={tags_set_data_wrong['tags'][1]}"

    def test_put_tag_remove_from_note(self, client, create_test_user1_note1_tag1_tag2,
                                      tags_set_data, auth_headers):
        client.put(f"/notes/{create_test_user1_note1_tag1_tag2[0].id}/tags/set", headers=auth_headers,
                   data=json.dumps(tags_set_data), content_type="application/json")
        res = client.put(f"/notes/{create_test_user1_note1_tag1_tag2[0].id}/tags/remove", headers=auth_headers,
                         data=json.dumps(tags_set_data), content_type="application/json")
        assert res.status_code == 200
        data = json.loads(res.data)
        assert data["tags"] == []

    def test_put_tag_remove_from_note_note_not_found(self, client, create_test_user1_note1_tag1_tag2,
                                                     tags_set_data, auth_headers):
        client.put(f"/notes/{create_test_user1_note1_tag1_tag2[0].id}/tags/set", headers=auth_headers,
                   data=json.dumps(tags_set_data), content_type="application/json")
        res = client.put("/notes/2/tags/remove", headers=auth_headers,
                         data=json.dumps(tags_set_data), content_type="application/json")
        assert res.status_code == 404
        data = json.loads(res.data)
        assert data["error"] == "note with id=2 not found"

    def test_get_note_by_tags(self, client, create_test_user1_note1_tag1_tag2, tags_set_data, auth_headers):
        client.put(f"/notes/{create_test_user1_note1_tag1_tag2[0].id}/tags/set", headers=auth_headers,
                   data=json.dumps(tags_set_data), content_type="application/json")
        res = client.get("/notes/filter?tags=test tag 1&tags=test tag 2")
        assert res.status_code == 200
        data = json.loads(res.data)
        assert data[0]["note"] == create_test_user1_note1_tag1_tag2[0].note

    def test_get_note_by_tags_note_not_found(self, client, create_test_user1_note1_tag1_tag2,
                                             tags_set_data, auth_headers):
        client.put(f"/notes/{create_test_user1_note1_tag1_tag2[0].id}/tags/set", headers=auth_headers,
                   data=json.dumps(tags_set_data), content_type="application/json")
        res = client.get("/notes/filter?tags=test tag 1&tags=test tag 3")
        assert res.status_code == 404
        data = json.loads(res.data)
        assert data["error"] == "Note with tag_name=test tag 3 not found"

    def test_get_all_public_notes(self, client, create_test_note1_and_note2_by_user1, note_private_data,
                                  auth_headers):
        client.put(f"/notes/{create_test_note1_and_note2_by_user1[0].id}", headers=auth_headers,
                   data=json.dumps(note_private_data), content_type="application/json")
        client.put("/notes/2", headers=auth_headers,
                   data=json.dumps(note_private_data), content_type="application/json")
        res = client.get("/notes/public")
        assert res.status_code == 200
        data = json.loads(res.data)
        assert data[0]["note"] == create_test_note1_and_note2_by_user1[0].note
        assert data[1]["note"] == "test note 2"

    def test_get_all_public_notes_not_found(self, client, create_test_note1_and_note2_by_user1):
        res = client.get("/notes/public")
        assert res.status_code == 404
        data = json.loads(res.data)
        assert data["error"] == "Public notes not found"

    def test_get_all_no_archive_notes_notes(self, client, create_test_note1_and_note2_by_user1, auth_headers):
        res = client.get(f"/notes/no_archive", headers=auth_headers)
        assert res.status_code == 200
        data = json.loads(res.data)
        assert data[0]["note"] == create_test_note1_and_note2_by_user1[0].note
        assert data[1]["note"] == create_test_note1_and_note2_by_user1[1].note

    def test_get_all_no_archive_notes_notes_not_found(self, client, create_test_user1, auth_headers):
        res = client.get(f"/notes/no_archive", headers=auth_headers)
        assert res.status_code == 404
        data = json.loads(res.data)
        assert data["error"] == "You have no notes yet"

    def test_get_all_archive_notes(self, client, create_test_note1_and_note2_by_user1, auth_headers):
        client.put(f"/notes/{create_test_note1_and_note2_by_user1[0].id}/to_archive", headers=auth_headers)
        client.put(f"/notes/2/to_archive", headers=auth_headers)
        res = client.get("/notes/archive", headers=auth_headers)
        assert res.status_code == 200
        data = json.loads(res.data)
        assert data[0]["note"] == create_test_note1_and_note2_by_user1[0].note
        assert data[1]["note"] == "test note 2"

    def test_get_all_archive_notes_notes_not_found(self, client, create_test_user1, auth_headers):
        res = client.get("/notes/archive", headers=auth_headers)
        assert res.status_code == 404
        data = json.loads(res.data)
        assert data["error"] == "You have no notes yet"

    def test_put_set_note_to_archive(self, client, create_test_note1_by_user1, auth_headers):
        res = client.put(f"/notes/{create_test_note1_by_user1[0].id}/to_archive", headers=auth_headers)
        assert res.status_code == 200
        data = json.loads(res.data)
        assert data["note"] == create_test_note1_by_user1[0].note

    def test_put_set_note_to_archive_note_not_found(self, client, auth_headers):
        res = client.put(f"/notes/1/to_archive", headers=auth_headers)
        assert res.status_code == 404
        data = json.loads(res.data)
        assert data["error"] == "Note with id=1 not found"

    def test_put_set_note_to_archive_note_doesnt_belong_to_user(self, client, create_test_note1_by_user1,
                                                                create_test_note2_by_user2, auth_headers):
        res = client.put(f"/notes/{create_test_note2_by_user2[0].id}/to_archive", headers=auth_headers)
        assert res.status_code == 403
        data = json.loads(res.data)
        assert data["error"] == f"Access denied to note with id={create_test_note2_by_user2[0].id}"

    def test_put_restore_note_from_archive(self, client, create_test_note1_by_user1, auth_headers):
        client.put(f"/notes/{create_test_note1_by_user1[0].id}/to_archive", headers=auth_headers)
        res = client.put(f"/notes/{create_test_note1_by_user1[0].id}/restore", headers=auth_headers)
        assert res.status_code == 200
        data = json.loads(res.data)
        assert data["note"] == create_test_note1_by_user1[0].note

    def test_put_restore_note_from_archive_note_not_found(self, client, create_test_note1_by_user1, auth_headers):
        res = client.put("/notes/2/restore", headers=auth_headers)
        assert res.status_code == 404
        data = json.loads(res.data)
        assert data["error"] == "Note with id=2 not found"

    def test_put_restore_note_from_archive_note_doesnt_belong_to_user(self, client, create_test_note1_by_user1,
                                                                      create_test_note2_by_user2, auth_headers):
        client.put(f"/notes/{create_test_note1_by_user1[0].id}/to_archive", headers=auth_headers)
        res = client.put(f"/notes/2/restore", headers=auth_headers)
        assert res.status_code == 403
        data = json.loads(res.data)
        assert data["error"] == "Access denied to note with id=2"
