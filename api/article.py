import datetime
from fastapi import APIRouter

from data.mongodb import MongoDB

article_app = APIRouter()
mongo = MongoDB()


@article_app.get('/articles')
def get_articles():
    response = mongo.get_articles_by_domain(domain='vnexpress')
    return response


@article_app.get("/")
def read_root():
    return {"Hello": "World"}
