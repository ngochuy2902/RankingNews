import datetime
from typing import List

import mysql.connector

from models.categories import UserCategory, Category
from models.roles import Role, UserRole
from models.scores import ScoreInsert, Score
from models.users import User, UserRegis, UserUpdate
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
        user_id = mycursor.lastrowid
        mycursor.execute('INSERT INTO user_role(user_id, role_id) VALUES (%s, %s)', (user_id, Conf.USER))
        for category in user.categories:
            mycursor.execute('INSERT INTO user_category(user_id, category_id) VALUES (%s, %s)',
                             (user_id, category))
        self.mydb.commit()

    def update_user(self, current_user_id: int, user_update: UserUpdate):
        mycursor = self.mydb.cursor()
        sql = 'UPDATE users SET year_of_birth = %s WHERE id = %s'
        value = (user_update.year_of_birth, current_user_id)
        mycursor.execute(sql, value)
        self.mydb.commit()

        mycursor.execute('DELETE FROM user_category WHERE user_id = %s', (current_user_id,))
        self.mydb.commit()

        for category_id in user_update.categories:
            mycursor.execute('INSERT INTO user_category(user_id, category_id) VALUES (%s, %s)',
                             (current_user_id, category_id))
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
            categories = mycursor.fetchall()
            result = []
            for c in categories:
                result.append(Category(**c))
            return result
        else:
            return None

    def get_all_categories(self):
        mycursor = self.mydb.cursor(dictionary=True)
        mycursor.execute('SELECT * FROM categories')
        categories = mycursor.fetchall()
        if bool(categories):
            result = []
            for c in categories:
                result.append(Category(**c))
            return result
        else:
            return None

    def add_article_scores(self, scores: List[ScoreInsert]):
        session_id = self.get_current_session_id()
        mycursor = self.mydb.cursor()
        for score in scores:
            print("add article score: ", score)
            sql = 'INSERT INTO scores (session_id, article_id, url, category, domain, score) VALUES (%s, %s, %s, %s, %s, %s)'
            value = (session_id, score.article_id, score.url, score.category, score.domain, score.score)
            mycursor.execute(sql, value)
        self.mydb.commit()

    def add_new_session(self, created_time: datetime):
        mycursor = self.mydb.cursor()
        mycursor.execute('INSERT INTO sessions(created_time, completed) VALUES (%s, %s)', (created_time, 0))
        self.mydb.commit()

    def get_current_session_id(self):
        mycursor = self.mydb.cursor(dictionary=True)
        mycursor.execute('SELECT MAX(id) FROM sessions')
        return mycursor.fetchone().get('MAX(id)')

    def get_valid_session_id(self):
        mycursor = self.mydb.cursor(dictionary=True)
        mycursor.execute('SELECT MAX(id) FROM sessions WHERE completed = %s', (1,))
        result = mycursor.fetchone()
        return result.get('MAX(id)')

    def update_session_complete(self, session_id: int):
        mycursor = self.mydb.cursor()
        finished_time = datetime.datetime.now()
        sql = 'UPDATE sessions SET finished_time = %s, completed = %s WHERE id = %s'
        value = (finished_time, 1, session_id,)
        mycursor.execute(sql, value)
        self.mydb.commit()

    def fetch_articles_ranking(self, session_id: int, category: str, limit: int):
        mycursor = self.mydb.cursor(dictionary=True)
        sql = 'SELECT * FROM scores WHERE session_id = %s AND category = %s ORDER BY score DESC LIMIT %s'
        value = (session_id, category, limit)
        mycursor.execute(sql, value)
        article_scores = mycursor.fetchall()
        result = []
        for ars in article_scores:
            result.append(Score(**ars))
        return result

    def add_audio_path(self, uuid: str, path: str):
        mycursor = self.mydb.cursor()
        sql = 'UPDATE scores SET audio_path = %s WHERE article_id = %s'
        value = (path, uuid)
        mycursor.execute(sql, value)
        self.mydb.commit()

    def get_article_score_by_uuid_and_audio_not_null(self, uuid: str):
        mycursor = self.mydb.cursor(dictionary=True)
        mycursor.execute('SELECT * FROM scores WHERE article_id = %s AND audio_path IS NOT NULL LIMIT 1', (uuid,))
        result = mycursor.fetchone()
        if result is not None:
            return Score(**result)
        else:
            return None


if __name__ == '__main__':
    mysql = MySQL()
    # print(MySQL().mydb)
    # print(MySQL().get_user_by_username(username="admin"))
    # print(mysql.get_roles_by_user_id(user_id=9))
    # print(mysql.get_categories_by_user_id(user_id=9))
    # print(mysql.add_article_scores())
    # print(mysql.get_current_session_id())
    data = mysql.fetch_articles_ranking(session_id=57, category='chinh-tri', limit=15)
    for i in data:
        print(i)
