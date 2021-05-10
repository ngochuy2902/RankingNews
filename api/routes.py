from fastapi import FastAPI
from .article import article_app
from .auth import auth_app
from .category import category_app
from .user import user_app
from .rank import rank_app
from .audio import audio_app

api_router = FastAPI()
api_router.include_router(article_app)
api_router.include_router(auth_app)
api_router.include_router(category_app)
api_router.include_router(user_app)
api_router.include_router(rank_app)
api_router.include_router(audio_app)
