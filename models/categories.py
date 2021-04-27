from pydantic import BaseModel, Field


class Category(BaseModel):
    id: int = Field(..., alias='id')
    name: str = Field(..., alias='name')
