from fastapi import APIRouter
from pydantic import BaseModel, Field
from ulid import ULID
from typing import Literal, Annotated

router = APIRouter()

class RequiredPasscode(BaseModel):
    required: Literal[False]

class OptionalPasscode(BaseModel):
    required: Literal[True]
    passcode_length: int = Field(ge=6, le=6)

Passcode = OptionalPasscode | RequiredPasscode

class AnnotatedResponse(BaseModel):
    id: str
    passcode: Annotated[Passcode, Field(discriminator="required")]

@router.get("/annotated")
async def annotated() -> AnnotatedResponse:
    return SampleResponse(id=ULID().new(), passcode={"required": False})

class UnionResponse(BaseModel):
    id: str
    passcode: OptionalPasscode | RequiredPasscode

@router.get("/union")
async def union() -> UnionResponse:
    return UnionResponse(id=ULID().new(), passcode={"required": False})
