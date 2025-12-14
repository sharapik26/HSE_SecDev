import os
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from .rest_api import router as wishes_router

app = FastAPI(title="SecDev Course App", version="0.1.0")

MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", "1048576"))


class ApiError(Exception):
    def __init__(
        self,
        title: str,
        detail: str,
        status: int = 400,
        type_: str = "about:blank",
    ):
        self.title = title
        self.detail = detail
        self.status = status
        self.type_ = type_


def _correlation_id(request: Request) -> str:
    return getattr(request.state, "correlation_id", str(uuid4()))


def _problem_response(request: Request, *, status: int, title: str, detail: str):
    cid = _correlation_id(request)
    payload = {
        "type": "about:blank",
        "title": title,
        "status": status,
        "detail": detail,
        "correlation_id": cid,
    }
    return JSONResponse(
        status_code=status, content=payload, headers={"X-Correlation-Id": cid}
    )


@app.middleware("http")
async def add_correlation_and_limits(request: Request, call_next):
    request.state.correlation_id = request.headers.get("X-Correlation-Id", str(uuid4()))

    content_length = request.headers.get("content-length")
    if content_length is not None:
        try:
            length = int(content_length)
        except ValueError:
            return _problem_response(
                request,
                status=400,
                title="bad_request",
                detail="invalid content-length header",
            )
        if length > MAX_CONTENT_LENGTH:
            return _problem_response(
                request,
                status=413,
                title="payload_too_large",
                detail=f"content-length exceeds {MAX_CONTENT_LENGTH} bytes",
            )

    response = await call_next(request)
    response.headers["X-Correlation-Id"] = _correlation_id(request)
    return response


@app.exception_handler(ApiError)
async def api_error_handler(request: Request, exc: ApiError):
    return _problem_response(
        request,
        status=exc.status,
        title=exc.title,
        detail=exc.detail,
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    detail = exc.detail if isinstance(exc.detail, str) else "http_error"
    return _problem_response(
        request,
        status=exc.status_code,
        title="http_error",
        detail=detail,
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return _problem_response(
        request,
        status=422,
        title="validation_error",
        detail="; ".join(err["msg"] for err in exc.errors()),
    )


@app.get("/health")
def health():
    return {"status": "ok"}


class ItemIn(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)


# Example minimal entity (for tests/demo)
_DB = {"items": []}


@app.post("/items")
def create_item(item: ItemIn):
    created = {"id": len(_DB["items"]) + 1, "name": item.name}
    _DB["items"].append(created)
    return created


@app.get("/items/{item_id}")
def get_item(item_id: int):
    for it in _DB["items"]:
        if it["id"] == item_id:
            return it
    raise ApiError(code="not_found", message="item not found", status=404)


app.include_router(wishes_router)
