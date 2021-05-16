from models.users import UserRegis, UserLogin, UserInfo, UserUpdate
from data.mysqldb import mysql
from passlib.context import CryptContext
from fastapi import HTTPException
from services.auth.auth_handler import signJWT, decodeJWT


class UserService:
    mydata = mysql
    pwd_context = CryptContext(
        schemes=["pbkdf2_sha256"],
        default="pbkdf2_sha256",
        pbkdf2_sha256__default_rounds=30000
    )

    async def is_exist_user(self, user_req):
        user = await self.mydata.get_user_by_username(username=user_req.username)
        if user is not None:
            return True
        else:
            return False

    async def check_login(self, user_req: UserLogin):
        flag = await self.is_exist_user(user_req)
        if flag:
            user = self.mydata.get_user_by_username(username=user_req.username)
            if self.check_encrypted_password(user_req.password, user.password):
                user_role = self.mydata.get_roles_by_user_id(user_id=user.id)
                return signJWT(user_id=user.id, user_role=user_role)
            else:
                raise HTTPException(status_code=403, detail="Wrong username or password")
        else:
            raise HTTPException(status_code=403, detail="Wrong username or password")

    def register(self, user_req: UserRegis):
        if self.is_exist_user(user_req) is False:
            password_encrypt = self.pwd_context.hash(user_req.password)
            new_user = UserRegis(username=user_req.username,
                                 password=password_encrypt,
                                 year_of_birth=user_req.year_of_birth,
                                 categories=user_req.categories,
                                 email=user_req.email)
            self.mydata.add_new_user(new_user)
        else:
            raise HTTPException(status_code=400, detail="Username already exists")

    def check_encrypted_password(self, password: str, hashed: str) -> bool:
        return self.pwd_context.verify(password, hashed)

    def get_current_user(self, token: str):
        data = decodeJWT(token)
        if not bool(data):
            raise HTTPException(status_code=403, detail="Invalid token or expired token.")
        user = self.mydata.get_user_by_user_id(data.get('user_id'))
        roles = self.mydata.get_roles_by_user_id(data.get('user_id'))
        categories = self.mydata.get_categories_by_user_id(data.get('user_id'))
        user_res = UserInfo(id=user.id, username=user.username, year_of_birth=user.year_of_birth, roles=roles,
                            categories=categories, email=user.email)
        return user_res

    def update_user(self, user_update: UserUpdate, current_user: UserInfo):
        if current_user:
            self.mydata.update_user(current_user_id=current_user.id, user_update=user_update)
        else:
            raise HTTPException(status_code=403, detail="Unauthorized")


if __name__ == '__main__':
    user_service = UserService()
    # user_service.register(UserRegis(username='user', password='user', year_of_birth=1988, categories=[4, 5, 6]))
    print(user_service.check_login(UserLogin(username='admin', password='admin')))
    # print(user_service.pwd_context.hash('admin'))
    # print(user_service.get_user(
    #     token='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJ1c2VyX2lkIjo5LCJ1c2VyX3JvbGUiOm51bGwsImV4cGlyZXMiOjE2MjIxODAwNTIuNzI0NjI3fQ.UXn-WkC7Sk6NMQmj7Ruy35yuaWlLVLK1plkka1No0ZpjJyJHbysR3Ly0Im5z-STJ79XogaBTjFNOqVAu-8FW3g'))
