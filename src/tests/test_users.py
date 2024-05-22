import json


def test_add_user(test_app, test_database):
    client = test_app.test_client()
    res = client.post(
        "/users",
        data=json.dumps(
            {
                "username": "test_user",
                "email": "test@example.com",
            }
        ),
        content_type="application/json",
    )
    data = json.loads(res.data.decode())
    assert res.status_code == 201
    assert "test_user" in data["username"]
    assert "test@example.com" in data["email"]
    assert "created_date" in data
    assert data["active"] is True
    assert "id" in data


def test_add_user_invalid_json(test_app, test_database):
    client = test_app.test_client()
    res = client.post(
        "/users",
        data=json.dumps({}),
        content_type="application/json",
    )
    data = json.loads(res.data.decode())
    assert res.status_code == 400
    assert "Input payload validation failed" in data["message"]


def test_add_user_invalid_json_keys(test_app, test_database):
    client = test_app.test_client()
    res = client.post(
        "/users",
        data=json.dumps({"email": "john@testdriven.io"}),
        content_type="application/json",
    )
    data = json.loads(res.data.decode())
    assert res.status_code == 400
    assert "Input payload validation failed" in data["message"]


def test_add_user_duplicate_email(test_app, test_database):
    client = test_app.test_client()
    client.post(
        "/users",
        data=json.dumps({"username": "test_user", "email": "test@example.com"}),
        content_type="application/json",
    )
    res = client.post(
        "/users",
        data=json.dumps({"username": "test_user", "email": "test@example.com"}),
        content_type="application/json",
    )
    data = json.loads(res.data.decode())
    assert res.status_code == 400
    assert "Sorry. That email already exists." in data["message"]


def test_single_user(test_app, test_database, add_user):
    user = add_user("test_user", "test@example.com")
    client = test_app.test_client()
    res = client.get(f"/users/{user.id}")
    data = json.loads(res.data.decode())
    assert res.status_code == 200
    assert "test_user" in data["username"]
    assert "test@example.com" in data["email"]


def test_single_user_incorrect_id(test_app, test_database):
    client = test_app.test_client()
    res = client.get("/users/999")
    data = json.loads(res.data.decode())
    assert res.status_code == 404
    assert "User 999 does not exist" in data["message"]


def test_all_users(test_app, test_database, add_user):
    add_user("test_user", "test@example.com")
    add_user("test_user_2", "test2@example.com")
    client = test_app.test_client()
    res = client.get("/users")
    data = json.loads(res.data.decode())
    assert res.status_code == 200
    assert len(data) == 2
    assert "test_user" in data[0]["username"]
    assert "test@example.com" in data[0]["email"]
    assert "test_user_2" in data[1]["username"]
    assert "test2@example.com" in data[1]["email"]
