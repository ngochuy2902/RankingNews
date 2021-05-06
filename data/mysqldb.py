import datetime
from typing import List

import mysql.connector

from models.categories import UserCategory
from models.roles import Role, UserRole
from models.scores import ScoreInsert
from models.users import User, UserRegis
from settings import BaseConfig as Conf


class MySQL:
    host = Conf.MYSQL_HOST
    user = Conf.MYSQL_USER
    password = Conf.MYSQL_PASSWORD
    database = Conf.MYSQL_DATABASE
    mydb = mysql.connector.connect(host=host, user=user, password=password, database=database)

    def get_user_by_username(self, username: str):
        mycursor = self.mydb.cursor(dictionary=True)
        mycursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        result = mycursor.fetchone()
        if result is not None:
            return User(**result)
        else:
            return None

    def get_user_by_user_id(self, user_id: int):
        mycursor = self.mydb.cursor(dictionary=True)
        mycursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
        result = mycursor.fetchone()
        if result is not None:
            return User(**result)
        else:
            return None

    def add_new_user(self, user: UserRegis):
        mycursor = self.mydb.cursor()
        mycursor.execute('INSERT INTO users(username, password, year_of_birth) VALUES (%s, %s, %s)',
                         (user.username, user.password, user.year_of_birth))
        self.mydb.commit()
        new_user = self.get_user_by_username(username=user.username)
        mycursor.execute('INSERT INTO user_role(user_id, role_id) VALUES (%s, %s)', (new_user.id, 2))
        for category in user.categories:
            mycursor.execute('INSERT INTO user_category(user_id, category_id) VALUES (%s, %s)', (new_user.id, category))
        self.mydb.commit()

    def get_roles_by_user_id(self, user_id: int):
        mycursor = self.mydb.cursor(dictionary=True)
        mycursor.execute('SELECT * FROM user_role WHERE user_id = %s', (user_id,))
        user_role_list = mycursor.fetchall()
        role_id_list = []
        for url in user_role_list:
            role_id_list.append(UserRole(**url).role_id)
        if bool(role_id_list):
            mycursor.execute('SELECT * FROM roles WHERE id IN (%s)', role_id_list)
            result = mycursor.fetchall()
            role_names = []
            for r in result:
                role_names.append(Role(**r).name)
            return role_names
        else:
            return None

    def get_categories_by_user_id(self, user_id: int):
        mycursor = self.mydb.cursor(dictionary=True)
        mycursor.execute('SELECT * FROM user_category WHERE user_id = %s', (user_id,))
        user_category_list = mycursor.fetchall()
        category_id_list = []
        for ucl in user_category_list:
            category_id_list.append(UserCategory(**ucl).category_id)
        if bool(category_id_list):
            category_id_list = tuple(category_id_list)
            mycursor.execute('SELECT * FROM categories WHERE id IN {}'.format(category_id_list))
            result = mycursor.fetchall()
            return result
        else:
            return None

    def add_article_scores(self, scores: List[ScoreInsert]):
        mycursor = self.mydb.cursor()
        mycursor.execute('INSERT INTO sessions(created_time) VALUES (%s)', (datetime.datetime.now(),))
        self.mydb.commit()

        session_id = mycursor.lastrowid
        for score in scores:
            sql = 'INSERT INTO scores (session_id, article_id, category, domain, score) VALUES (%s, %s, %s, %s, %s)'
            value = (session_id, score.article_id, score.category, score.domain, score.score)
            mycursor.execute(sql, value)
        self.mydb.commit()


if __name__ == '__main__':
    mysql = MySQL()
    # print(MySQL().mydb)
    # print(MySQL().get_user_by_username(username="admin"))
    # print(mysql.get_roles_by_user_id(user_id=9))
    # print(mysql.get_categories_by_user_id(user_id=9))
    print(mysql.add_article_scores())
