def test_create_user(client):
    response = client.post(
        "/users/",
        json={"name": "Test User", "email": "testuser@example.com"},
    )
    assert response.status_code == 200
    assert response.json()["email"] == "testuser@example.com"
    assert response.json()["name"] == "Test User"

def test_user_login(client):
    response = client.post(
        "/users/login",
        data={"username": "testuser@example.com", "password": "testpassword"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
