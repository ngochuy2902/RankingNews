import datetime
from fastapi import APIRouter

from data.mongodb import MongoDB

app = APIRouter()
mongo = MongoDB()


@app.get('/articles')
def get_articles():
    date_time = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    response = mongo.get_data(category="chinh-tri", date_time=date_time)
    return response


@app.get("/")
def read_root():
    return {"Hello": "World"}
