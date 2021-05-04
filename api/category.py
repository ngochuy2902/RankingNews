from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordBearer

from models.users import User
from services.category import CategoryService
from services.user import UserService

category_app = APIRouter()
user_service = UserService()
category_service = CategoryService()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = user_service.get_current_user(token)
    return user


@category_app.get('/user/categories', status_code=status.HTTP_200_OK)
def get_category_by_current_user(current_user: User = Depends(get_current_user)):
    return category_service.get_category_by_current_user_id(current_user.id)
