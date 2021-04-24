import mysql.connector
from settings import BaseConfig as Conf


class MySQL:
    host = Conf.MYSQL_HOST
    user = Conf.MYSQL_USER
    password = Conf.MYSQL_PASSWORD

    def connect(self):
        return mysql.connector.connect(self.host, self.user, self.password)


if __name__ == '__main__':
    print(MySQL.connect())
