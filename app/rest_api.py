from typing import List

from fastapi import APIRouter

from app.exceptions import WishAlreadyExistsException, WishNotFoundException

from .database import wishes
from .models import Wish

router = APIRouter(prefix="/wishes", tags=["wishes"])


@router.post("/", response_model=Wish)
def create_wish(wish: Wish):
    for w in wishes:
        if w.id == wish.id:
            raise WishAlreadyExistsException(wish.id)
    wishes.append(wish)
    return wish


@router.get("/", response_model=List[Wish])
def get_wishes():
    return wishes


@router.get("/{wish_id}", response_model=Wish)
def get_wish(wish_id: int):
    for w in wishes:
        if w.id == wish_id:
            return w
    raise WishNotFoundException(wish_id)


@router.put("/{wish_id}", response_model=Wish)
def update_wish(wish_id: int, updated: Wish):
    for i, w in enumerate(wishes):
        if w.id == wish_id:
            wishes[i] = updated
            return updated
    raise WishNotFoundException(wish_id)


@router.delete("/{wish_id}")
def delete_wish(wish_id: int):
    for i, w in enumerate(wishes):
        if w.id == wish_id:
            del wishes[i]
            return {"detail": "Wish deleted"}
    raise WishNotFoundException(wish_id)
