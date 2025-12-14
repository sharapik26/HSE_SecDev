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
