from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from services.user import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
user_service = UserService()


def get_current_user(data: str = Depends(oauth2_scheme)):
    user = user_service.get_current_user(token=data)
    return user
