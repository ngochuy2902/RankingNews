from dataclasses import dataclass
from typing import List

from pydantic import BaseModel, Field


class User(BaseModel):
    id: int = Field(..., alias='id')
    username: str = Field(..., alias='username')
    password: str = Field(..., alias='password')
    year_of_birth: int = Field(..., alias='year_of_birth')
    email: str = Field(alias='email', default=None)


@dataclass
class UserRegis:
    username: str
    password: str
    year_of_birth: int
    categories: List[int]

    def __int__(self, username=None, password=None, year_of_birth=None, categories=None):
        self.username = username
        self.password = password
        self.year_of_birth = year_of_birth
        self.categories = categories


@dataclass
class UserLogin:
    username: str
    password: str

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password


def get_user_name(user):
    return user.username


if __name__ == '__main__':
    userRegis = UserRegis(username="huyhn", password="775748", year_of_birth=1999, categories=[1, 2, 3])
    userLogin = UserLogin(username="huyhn", password="775748")
    print("userRegis = ", userRegis)
    print("userRegisName = ", get_user_name(userRegis))
    print("userLogin = ", userLogin)
    print("userLoginName = ", get_user_name(userLogin))
