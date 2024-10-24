from fastapi import HTTPException


class BaseHTTPException(HTTPException):
    description: str
    status_code: int

    def __init__(self, description: str):
        super().__init__(status_code=self.status_code, detail=description)

    @classmethod
    def as_dict(cls) -> dict[str, str]:
        return {"description": cls.description}
