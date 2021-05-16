from fastapi import APIRouter, Depends
from models.users import UserInfo
from services.auth import oauth2
from services.article import ArticleService

article_app = APIRouter(prefix="/articles", tags=["Articles"])
show_article = ArticleService()


@article_app.get('')
async def get_articles():
    return show_article.get_articles_no_login()


@article_app.get('/me')
async def get_articles(current_user: UserInfo = Depends(oauth2.get_current_user)):
    return show_article.get_articles_by_current_user_id(current_user_id=current_user.id)
