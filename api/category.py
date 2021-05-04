from fastapi import APIRouter, Depends, status

from models.users import User
from services.auth import oauth2
from services.category import CategoryService
from services.user import UserService

category_app = APIRouter(prefix="/categories", tags=["Categories"])
user_service = UserService()
category_service = CategoryService()


@category_app.get('/user', status_code=status.HTTP_200_OK)
def get_category_by_current_user(current_user: User = Depends(oauth2.get_current_user)):
    return category_service.get_category_by_current_user_id(current_user.id)
