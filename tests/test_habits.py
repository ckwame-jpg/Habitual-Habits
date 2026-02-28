def test_create_habit(client, auth_header):
    resp = client.post("/habits/", json={
        "title": "Exercise",
        "description": "Daily workout",
        "frequency": "daily",
    }, headers=auth_header)
    assert resp.status_code == 200
    data = resp.json()
    assert data["title"] == "Exercise"
    assert data["frequency"] == "daily"
    assert "id" in data
    assert "user_id" in data


def test_list_habits(client, auth_header):
    client.post("/habits/", json={"title": "Read", "frequency": "daily"}, headers=auth_header)
    client.post("/habits/", json={"title": "Meditate", "frequency": "daily"}, headers=auth_header)
    resp = client.get("/habits/", headers=auth_header)
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_get_habit(client, auth_header):
    create_resp = client.post("/habits/", json={"title": "Read", "frequency": "daily"}, headers=auth_header)
    habit_id = create_resp.json()["id"]
    resp = client.get(f"/habits/{habit_id}", headers=auth_header)
    assert resp.status_code == 200
    assert resp.json()["title"] == "Read"


def test_get_habit_not_found(client, auth_header):
    resp = client.get("/habits/999", headers=auth_header)
    assert resp.status_code == 404


def test_update_habit(client, auth_header):
    create_resp = client.post("/habits/", json={"title": "Read", "frequency": "daily"}, headers=auth_header)
    habit_id = create_resp.json()["id"]
    resp = client.put(f"/habits/{habit_id}", json={
        "title": "Read Books",
        "frequency": "weekly",
    }, headers=auth_header)
    assert resp.status_code == 200
    assert resp.json()["title"] == "Read Books"
    assert resp.json()["frequency"] == "weekly"


def test_delete_habit(client, auth_header):
    create_resp = client.post("/habits/", json={"title": "Read", "frequency": "daily"}, headers=auth_header)
    habit_id = create_resp.json()["id"]
    resp = client.delete(f"/habits/{habit_id}", headers=auth_header)
    assert resp.status_code == 200
    # Verify it's gone
    resp = client.get(f"/habits/{habit_id}", headers=auth_header)
    assert resp.status_code == 404


def test_unauthenticated_request(client):
    resp = client.get("/habits/")
    assert resp.status_code == 401
