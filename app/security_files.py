import uuid
from pathlib import Path
from typing import NamedTuple

from fastapi import UploadFile

from .errors import ApiError

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
JPEG_SOI = b"\xff\xd8"
JPEG_EOI = b"\xff\xd9"


class SaveResult(NamedTuple):
    path: Path
    name: str
    content_type: str


def _sniff_mime(data: bytes) -> str | None:
    if data.startswith(PNG_MAGIC):
        return "image/png"
    if data.startswith(JPEG_SOI) and data.endswith(JPEG_EOI):
        return "image/jpeg"
    return None


async def save_uploaded_file(
    file: UploadFile, root: Path, max_bytes: int
) -> SaveResult:
    data = await file.read(max_bytes + 1)
    if len(data) > max_bytes:
        raise ApiError(
            title="payload_too_large",
            detail=f"file exceeds limit {max_bytes} bytes",
            status=413,
        )

    mime = _sniff_mime(data)
    if mime is None:
        raise ApiError(
            title="unsupported_media_type",
            detail="only png or jpeg allowed",
            status=415,
        )

    root = root.resolve()
    root.mkdir(parents=True, exist_ok=True)
    ext = ".png" if mime == "image/png" else ".jpg"
    name = f"{uuid.uuid4()}{ext}"
    path = (root / name).resolve()

    if not str(path).startswith(str(root)):
        raise ApiError(title="path_traversal", detail="invalid path", status=400)
    if any(p.is_symlink() for p in path.parents):
        raise ApiError(title="symlink_parent", detail="symlink in path", status=400)

    path.write_bytes(data)
    return SaveResult(path=path, name=name, content_type=mime)
