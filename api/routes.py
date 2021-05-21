from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .article import article_app
from .auth import auth_app
from .category import category_app
from .user import user_app
from .rank import rank_app
from .audio import audio_app

app_main = FastAPI()

origins = [
    "http://localhost:3000",
    "*"
]

app_main.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app_main.include_router(article_app)
app_main.include_router(auth_app)
app_main.include_router(category_app)
app_main.include_router(user_app)
app_main.include_router(rank_app)
app_main.include_router(audio_app)
