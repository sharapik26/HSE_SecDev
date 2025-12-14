from typing import Optional

from pydantic import BaseModel, Field


class Wish(BaseModel):
    id: int
    title: str = Field(..., min_length=1, max_length=100)
    link: Optional[str] = None
    price_estimate: Optional[float] = Field(None, ge=0)
    notes: Optional[str] = None
