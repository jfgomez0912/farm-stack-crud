from decouple import config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute

from routers import tasks


def custom_generate_unique_id(route: APIRoute):
    return f"{route.tags[0]}-{route.name}"


origins: list[str] = [
    config("FRONTEND_URL"),  # type: ignore
]

app = FastAPI(generate_unique_id_function=custom_generate_unique_id)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(tasks.router)


@app.get("/ping", tags=["general"])
def welcome() -> dict[str, str]:
    return {"message": "Welcome to the API!"}
