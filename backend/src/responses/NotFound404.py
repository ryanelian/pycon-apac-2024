from fastapi import HTTPException
from pydantic import BaseModel


class NotFound404(BaseModel):
    detail: str


not_found_404_response = {
    "model": NotFound404,
    "description": "Resource not found",
    "content": {"application/json": {"example": {"detail": "Resource not found"}}},
}


class NotFound404Exception(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Resource not found")
