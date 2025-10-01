from typing import List

from fastapi import APIRouter, HTTPException

from .database import wishes
from .models import Wish

router = APIRouter(prefix="/wishes", tags=["wishes"])


@router.post("/", response_model=Wish)
def create_wish(wish: Wish):
    for w in wishes:
        if w.id == wish.id:
            raise HTTPException(
                status_code=400, detail="Wish with this ID already exists"
            )
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
    raise HTTPException(status_code=404, detail="Wish not found")


@router.put("/{wish_id}", response_model=Wish)
def update_wish(wish_id: int, updated: Wish):
    for i, w in enumerate(wishes):
        if w.id == wish_id:
            wishes[i] = updated
            return updated
    raise HTTPException(status_code=404, detail="Wish not found")


@router.delete("/{wish_id}")
def delete_wish(wish_id: int):
    for i, w in enumerate(wishes):
        if w.id == wish_id:
            del wishes[i]
            return {"detail": "Wish deleted"}
    raise HTTPException(status_code=404, detail="Wish not found")
