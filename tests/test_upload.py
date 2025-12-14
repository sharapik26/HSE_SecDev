import os
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import MAX_UPLOAD_BYTES, app


def _client(tmp_path: Path):
    os.environ["UPLOAD_DIR"] = str(tmp_path)
    return TestClient(app)


def test_upload_png_success(tmp_path: Path):
    client = _client(tmp_path)
    png = b"\x89PNG\r\n\x1a\n" + b"\x00" * 10
    r = client.post(
        "/upload",
        files={"file": ("ok.png", png, "image/png")},
    )
    assert r.status_code == 200
    body = r.json()
    assert body["content_type"] == "image/png"
    stored = tmp_path / body["stored_as"]
    assert stored.exists()
    assert stored.read_bytes().startswith(b"\x89PNG")


def test_upload_rejects_bad_magic(tmp_path: Path):
    client = _client(tmp_path)
    r = client.post(
        "/upload",
        files={"file": ("bad.txt", b"not an image", "text/plain")},
    )
    assert r.status_code == 415
    body = r.json()
    assert body["title"] == "unsupported_media_type"


def test_upload_rejects_oversize(tmp_path: Path):
    client = _client(tmp_path)
    too_big = b"\x89PNG\r\n\x1a\n" + b"0" * (MAX_UPLOAD_BYTES + 1)
    r = client.post(
        "/upload",
        files={"file": ("big.png", too_big, "image/png")},
    )
    assert r.status_code == 413
    body = r.json()
    assert body["title"] == "payload_too_large"
