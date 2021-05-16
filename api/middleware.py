from fastapi import FastAPI, APIRouter
from starlette.middleware.cors import CORSMiddleware


def add_middleware(app: FastAPI) -> FastAPI:
    origins = [
        "http://localhost:3000",
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app
