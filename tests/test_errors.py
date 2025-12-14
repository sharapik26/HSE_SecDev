from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_not_found_item_problem_details():
    r = client.get("/items/999")
    assert r.status_code == 404
    body = r.json()
    assert body["title"] == "not_found"
    assert body["status"] == 404
    assert "correlation_id" in body
    assert r.headers.get("X-Correlation-Id") == body["correlation_id"]


def test_validation_error_problem_details():
    r = client.post("/items", json={"name": ""})
    assert r.status_code == 422
    body = r.json()
    assert body["title"] == "validation_error"
    assert body["status"] == 422
    assert body["correlation_id"] == r.headers.get("X-Correlation-Id")
