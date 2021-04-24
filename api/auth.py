from fastapi import APIRouter
from models.users import UserReq
from services.user import UserService

app = APIRouter()
# user_service = UserService()

from services.user import user_service
@app.post('/register/user/')
def register(user: UserReq):
