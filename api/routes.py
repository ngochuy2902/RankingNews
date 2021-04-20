from fastapi import APIRouter
from .article import app

api_router = APIRouter()
api_router.include_router(app)
