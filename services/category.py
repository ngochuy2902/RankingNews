from data.mysqldb import MySQL
from services.auth.auth_handler import decodeJWT


class CategoryService:
    mysql = MySQL()

    def get_category_by_current_user_id(self, user_id: int):
        categories = self.mysql.get_categories_by_user_id(user_id=user_id)
        return categories
