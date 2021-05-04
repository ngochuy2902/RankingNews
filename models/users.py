from dataclasses import dataclass
from typing import List

from pydantic import BaseModel, Field


class User(BaseModel):
    id: int = Field(..., alias='id')
    username: str = Field(..., alias='username')
    password: str = Field(..., alias='password')
    year_of_birth: int = Field(..., alias='year_of_birth')
    email: str = Field(alias='email', default=None)


class UserRegis(BaseModel):
    username: str
    password: str
    year_of_birth: int
    categories: List[int]


class UserLogin(BaseModel):
    username: str
    password: str


class UserInfo(BaseModel):
    id: int
    username: str
    year_of_birth: int
    roles: List[str]
    email: str = None


def get_user_name(user):
    return user.username


if __name__ == '__main__':
    userRegis = UserRegis(username="huyhn", password="775748", year_of_birth=1999, categories=[1, 2, 3])
    userLogin = UserLogin(username="huyhn", password="775748")
    print("userRegis = ", userRegis)
    print("userRegisName = ", get_user_name(userRegis))
    print("userLogin = ", userLogin)
    print("userLoginName = ", get_user_name(userLogin))
