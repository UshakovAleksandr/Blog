import json


class TestNotes:

    def test_get_note_by_id(self, client, create_test_note1_by_user1, auth_headers):
        res = client.get(f"/notes/{create_test_note1_by_user1[1][0].id}", headers=auth_headers)
        assert res.status_code == 200
        data = json.loads(res.data)
        assert data["note"], create_test_note1_by_user1[0].note
