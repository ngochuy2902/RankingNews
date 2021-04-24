from models.users import UserRegis, UserLogin
from data.mysqldb import MySQL
from passlib.context import CryptContext
from fastapi import HTTPException
from services.auth.auth_handler import signJWT


class UserService:
    mydata = MySQL()
    pwd_context = CryptContext(
        schemes=["pbkdf2_sha256"],
        default="pbkdf2_sha256",
        pbkdf2_sha256__default_rounds=30000
    )

    def is_exist_user(self, user_req):
        user = self.mydata.get_user_by_username(username=user_req.username)
        if user is not None:
            return True
        else:
            return False

    def check_login(self, user_req: UserLogin):
        if self.is_exist_user(user_req):
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
                                 categories=user_req.categories)
            self.mydata.add_new_user(new_user)
        else:
            raise HTTPException(status_code=400, detail="Username is exist")

    def check_encrypted_password(self, password: str, hashed: str) -> bool:
        return self.pwd_context.verify(password, hashed)


if __name__ == '__main__':
    user_service = UserService()
    # user_service.register(UserRegis(username='user', password='user', year_of_birth=1988, categories=[4, 5, 6]))
    # print(user_service.check_login(UserLogin(username='admin', password='admin')))
    # print(user_service.pwd_context.hash('admin'))
