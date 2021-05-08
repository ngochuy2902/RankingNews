from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from models.users import User, UserRegis, UserLogin, UserInfo
from services.auth import oauth2
from services.category import CategoryService
from services.user import UserService

auth_app = APIRouter(tags=["Authentication"])
category_service = CategoryService()
user_service = UserService()


@auth_app.post('/register', status_code=status.HTTP_201_CREATED)
async def register(user: UserRegis):
    user_service.register(user)


@auth_app.post('/login', status_code=status.HTTP_200_OK)
async def login(req: OAuth2PasswordRequestForm = Depends()):
    user = UserLogin(username=req.username, password=req.password)
    return user_service.check_login(user)
