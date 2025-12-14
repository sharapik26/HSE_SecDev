from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_wish():
    response = client.post(
        "/wishes/",
        json={
            "id": 1,
            "title": "New Laptop",
            "link": "https://example.com/laptop",
            "price_estimate": 1500,
            "notes": "Preferably MacBook",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "New Laptop"


def test_get_wishes():
    response = client.get("/wishes/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(w["title"] == "New Laptop" for w in data)


def test_get_wish_by_id():
    response = client.get("/wishes/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "New Laptop"


def test_update_wish():
    response = client.put(
        "/wishes/1",
        json={
            "id": 1,
            "title": "Updated Laptop",
            "link": "https://example.com/laptop",
            "price_estimate": 1600,
            "notes": "Any model",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Laptop"
    assert data["price_estimate"] == 1600


def test_delete_wish():
    response = client.delete("/wishes/1")
    assert response.status_code == 200
    data = response.json()
    assert data["detail"] == "Wish deleted"

    # проверим, что его реально нет
    response = client.get("/wishes/1")
    assert response.status_code == 404
