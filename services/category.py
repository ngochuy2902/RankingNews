from data.mysqldb import MySQL


class CategoryService:
    mysql = MySQL()

    def get_category_by_current_user_id(self, user_id: int):
        categories = self.mysql.get_categories_by_user_id(user_id=user_id)
        return categories

    def get_all_categories(self):
        return self.mysql.get_all_categories()


if __name__ == '__main__':
    category_service = CategoryService()
    print(category_service.get_category_by_current_user_id(9))
