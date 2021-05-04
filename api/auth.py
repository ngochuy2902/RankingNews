from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from models.users import User, UserRegis, UserLogin
from services.category import CategoryService
from services.user import UserService

auth_app = APIRouter()
category_service = CategoryService()
user_service = UserService()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = user_service.get_current_user(token)
    return user


@auth_app.post('/register', status_code=201)
async def register(user: UserRegis):
    user_service.register(user)


@auth_app.post('/login/', status_code=200)
async def login(req: OAuth2PasswordRequestForm = Depends()):
    user = UserLogin(req.username, req.password)
    return user_service.check_login(user)


@auth_app.get('/user/me')
async def user_me(current_user: User = Depends(get_current_user)):
    return current_user

#
# @auth_app.get('/user/categories')
# async def get_category_by_current_user(current_user: User = Depends(get_current_user)):
#     return category_service.get_category_by_current_user_id(current_user.id)


