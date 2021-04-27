from pydantic import BaseModel, Field


class Role(BaseModel):
    id: int = Field(..., alias='id')
    name: str = Field(..., alias='name')


class UserRole(BaseModel):
    user_id: int = Field(..., alias='user_id')
    role_id: int = Field(..., alias='role_id')
