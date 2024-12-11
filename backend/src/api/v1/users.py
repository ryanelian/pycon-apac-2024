from fastapi import APIRouter
from pydantic import BaseModel, Field
from tortoise.exceptions import DoesNotExist
from ulid import ULID
from typing import Union, Literal

from responses.NotFound404 import NotFound404Exception, not_found_404_response
from tables import User

router = APIRouter()

class PasscodeNotRequired(BaseModel):
    require_passcode: Literal[False] = False


class PasscodeRequired(BaseModel):
    require_passcode: Literal[True] = True
    passcode_length: int = Field(ge=6, le=6)


class V1UserResponseModel(BaseModel):
    id: str
    passcode: Union[PasscodeNotRequired, PasscodeRequired]


# GET /users - Retrieve all users
@router.get("/users")
async def get_users_v1() -> list[V1UserResponseModel]:
    return []
