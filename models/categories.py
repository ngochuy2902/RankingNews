from pydantic import BaseModel, Field


class Category(BaseModel):
    id: int = Field(..., alias='id')
    name: str = Field(..., alias='name')
    description: str = Field(..., alias='description')


class UserCategory(BaseModel):
    user_id: int = Field(..., alias='user_id')
    category_id: int = Field(..., alias='category_id')
