from typing import List, Optional

from fastapi import APIRouter, Query
from pydantic import BaseModel

from tables import User

router = APIRouter()


class V2UserResponseModel(BaseModel):
    id: str
    username: str
    family_name: str
    given_name: str


class V2UserListResponseModel(BaseModel):
    items: List[V2UserResponseModel]
    cursor: str


# GET /v2/users - Cursor-based pagination for retrieving users
@router.get("/users", response_model=V2UserListResponseModel)
async def get_users_v2(
    cursor: Optional[str] = Query(
        None, description="The last user ID from the previous page"
    ),  # Cursor for pagination
) -> V2UserListResponseModel:
    # Hardcoded limit
    limit = 50

    # Build the query
    query = User.all().order_by("id")

    if cursor:
        # Only get users with IDs greater than the provided cursor
        query = query.filter(id__gt=cursor)

    # Fetch the results with a limit
    users = await query.limit(limit).values(
        "id", "username", "family_name", "given_name"
    )

    # Prepare the response data
    items = [
        V2UserResponseModel(
            id=user["id"],
            username=user["username"],
            family_name=user["family_name"],
            given_name=user["given_name"],
        )
        for user in users
    ]

    # If there are possibly more results, as in we managed to fetch 50 items,
    # return the last item's ID as the cursor to continue search
    cursor = items[-1].id if len(items) == limit else ""

    return V2UserListResponseModel(items=items, cursor=cursor)
