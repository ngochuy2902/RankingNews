from fastapi import APIRouter
from dto.user import UserReq
from services.user import UserService

auth_app = APIRouter()
user_service = UserService()


@auth_app.post('/register', status_code=201)
def register(user: UserReq):
    user_service.register(user)


@auth_app.post('/register', status_code=200)
def login(user: UserReq):
    return user_service.check_login(user)
