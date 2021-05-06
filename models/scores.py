from pydantic import BaseModel, Field


class Score(BaseModel):
    id: int = Field(..., alias='id')
    session_id: int = Field(..., alias='session_id')
    article_id: str = Field(..., alias='article_id')
    category: str = Field(..., alias='category')
    domain: str = Field(..., alias='domain')
    score: float = Field(..., alias='score')


class ScoreInsert(BaseModel):
    article_id: str
    category: str
    domain: str
    score: float
