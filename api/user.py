from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

from models.users import UserInfo, UserUpdate
from services.auth import oauth2
from services.category import CategoryService
from services.user import UserService

user_app = APIRouter(prefix="/user", tags=["User"])
category_service = CategoryService()
user_service = UserService()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@user_app.get('/me')
async def user_me(current_user: UserInfo = Depends(oauth2.get_current_user)):
    return current_user


@user_app.put('/update')
async def update_user(user: UserUpdate, current_user: UserInfo = Depends(oauth2.get_current_user)):
    user_service.update_user(user, current_user)
