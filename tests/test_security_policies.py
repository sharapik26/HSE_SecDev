from fastapi.testclient import TestClient

from app.main import MAX_CONTENT_LENGTH, app

client = TestClient(app)


def test_payload_too_large():
    too_big = "x" * (MAX_CONTENT_LENGTH + 1)
    r = client.post("/items", data=too_big, headers={"Content-Type": "text/plain"})
    assert r.status_code == 413
    body = r.json()
    assert body["title"] == "payload_too_large"
    assert "exceeds" in body["detail"]
    assert body["correlation_id"] == r.headers.get("X-Correlation-Id")


def test_correlation_id_is_propagated():
    cid = "cid-test-123"
    r = client.get("/items/999", headers={"X-Correlation-Id": cid})
    assert r.status_code == 404
    body = r.json()
    assert body["correlation_id"] == cid
    assert r.headers.get("X-Correlation-Id") == cid
