from contextlib import asynccontextmanager

from fastapi import FastAPI
from tortoise.contrib.fastapi import RegisterTortoise

from api.v1.users import router as v1_users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with RegisterTortoise(
        app,
        db_url="sqlite://database.db",
        modules={"models": ["tables"]},
        # don't do this in production 🙉 🙈 🙊
        # usually, migration scripts or CLI is used to generate tables
        generate_schemas=True,
        add_exception_handlers=True,
    ):
        yield


app = FastAPI(
    title="PyCon APAC 2024",
    description="Demonstrating FastAPI + Next.js integration with OpenAPI TypeScript and React Query",
    lifespan=lifespan,
)


# @app.get("/")
# def read_root() -> str:
#     return "Hello, World!"


app.include_router(v1_users_router, prefix="/v1")
