from fastapi import HTTPException


class WishAlreadyExistsException(HTTPException):
    def __init__(self, wish_id: int):
        super().__init__(
            status_code=400, detail=f"Wish with ID {wish_id} already exists"
        )


class WishNotFoundException(HTTPException):
    def __init__(self, wish_id: int):
        super().__init__(status_code=404, detail=f"Wish with ID {wish_id} not found")
