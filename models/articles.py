from datetime import datetime

from pydantic import BaseModel, Field


class Article(BaseModel):
    id: str = Field(..., alias="uuid_url")
    url: str = Field(..., alias='url')
    domain: str = Field(..., alias='domain')
    title: str = Field(..., alias='title')
    category: str = Field(..., alias='category')
    category_url: str = Field(..., alias='category_url')
    time: datetime = Field(..., alias='time')
    content: str = Field(..., alias='content')


class ArticleShow(BaseModel):
    id: str
    url: str
    domain: str
    title: str
    category: str
    time: datetime
    content: str
    audio_path: str

