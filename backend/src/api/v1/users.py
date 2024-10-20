from fastapi import APIRouter
from pydantic import BaseModel, Field
from tortoise.exceptions import DoesNotExist
from ulid import ULID

from responses.NotFound404 import NotFound404Exception, not_found_404_response
from tables import User

router = APIRouter()


class V1UserResponseModel(BaseModel):
    id: str
    username: str
    family_name: str
    given_name: str


class V1UserCreateAndUpdateRequestModel(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=64,
        description="Username should be between 3 and 64 characters",
    )
    family_name: str = Field(
        ..., max_length=255, description="Family name must not exceed 255 characters"
    )
    given_name: str = Field(
        ..., max_length=255, description="Given name must not exceed 255 characters"
    )


# GET /users - Retrieve all users
@router.get("/users")
async def get_users_v1() -> list[V1UserResponseModel]:
    users = await User.all().values("id", "username", "family_name", "given_name")
    return [
        V1UserResponseModel(
            id=user["id"],
            username=user["username"],
            family_name=user["family_name"],
            given_name=user["given_name"],
        )
        for user in users
    ]


# GET /users/{id} - Retrieve a specific user by ID
@router.get(
    "/users/{id}",
    responses={400: not_found_404_response},
)
async def get_user_details_v1(id: str) -> V1UserResponseModel:
    try:
        user = await User.get(id=id).values(
            "id", "username", "family_name", "given_name"
        )
        return V1UserResponseModel(
            id=user["id"],
            username=user["username"],
            family_name=user["family_name"],
            given_name=user["given_name"],
        )
    except DoesNotExist:
        raise NotFound404Exception


# POST /users - Create a new user with validation, return True if successful
@router.post(
    "/users",
    status_code=201,
)
async def create_user_v1(body: V1UserCreateAndUpdateRequestModel) -> str:
    user = User(
        id=str(ULID()),
        username=body.username,
        family_name=body.family_name,
        given_name=body.given_name,
    )
    await user.save()
    return user.id


# PATCH /users/{id} - Update certain fields of a user by ID, return True if successful
@router.patch("/users/{id}", responses={400: not_found_404_response})
async def update_user_v1(id: str, body: V1UserCreateAndUpdateRequestModel) -> str:
    try:
        user = await User.get(id=id)
        user.username = body.username
        user.family_name = body.family_name
        user.given_name = body.given_name
        await user.save()
        return user.id
    except DoesNotExist:
        raise NotFound404Exception


# DELETE /users/{id} - Delete a user by ID, return True if successful
@router.delete("/users/{id}", responses={400: not_found_404_response})
async def delete_user_v1(id: str) -> str:
    try:
        user = await User.get(id=id)
        await user.delete()
        return user.id
    except DoesNotExist:
        raise NotFound404Exception
