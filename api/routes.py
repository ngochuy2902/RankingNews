from fastapi import APIRouter
from .article import article_app
from .auth import auth_app
from .category import category_app

api_router = APIRouter()
api_router.include_router(article_app)
api_router.include_router(auth_app)
api_router.include_router(category_app)
