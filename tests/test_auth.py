def test_register(client):
    resp = client.post("/register", json={"email": "new@example.com", "password": "pass123"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["email"] == "new@example.com"
    assert "id" in data
    assert "password" not in data


def test_register_duplicate_email(client):
    client.post("/register", json={"email": "dup@example.com", "password": "pass123"})
    resp = client.post("/register", json={"email": "dup@example.com", "password": "pass456"})
    assert resp.status_code == 400
    assert "already registered" in resp.json()["detail"]


def test_login_success(client):
    client.post("/register", json={"email": "user@example.com", "password": "pass123"})
    resp = client.post("/login", data={"username": "user@example.com", "password": "pass123"})
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):
    client.post("/register", json={"email": "user@example.com", "password": "pass123"})
    resp = client.post("/login", data={"username": "user@example.com", "password": "wrong"})
    assert resp.status_code == 401


def test_login_nonexistent_user(client):
    resp = client.post("/login", data={"username": "nobody@example.com", "password": "pass123"})
    assert resp.status_code == 401
