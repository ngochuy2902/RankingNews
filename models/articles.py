from datetime import date

from pydantic import BaseModel, Field


class Article(BaseModel):
    id: str = Field(..., alias="uuid_url")
    url: str = Field(..., alias='url')
    domain: str = Field(..., alias='domain')
    title: str = Field(..., alias='title')
    category: str = Field(..., alias='category')
    category_url: str = Field(..., alias='category_url')
    time: date = Field(..., alias='time')
    content: str = Field(..., alias='content')
