from fastapi import APIRouter, Depends
from models.users import UserInfo
from services.auth import oauth2
from services.article import ShowArticle

article_app = APIRouter(prefix="/articles", tags=["Articles"])
show_article = ShowArticle()


@article_app.get('/me')
async def get_articles(current_user: UserInfo = Depends(oauth2.get_current_user)):
    return show_article.get_articles_by_current_user_id(current_user_id=current_user.id)
