

class BaseConfig:
    APP_HOST = "localhost"
    APP_PORT = 5500

    MONGO_URI = 'mongodb://huyhn:775748@localhost:27017'
    MONGO_DATABASE = 'scraper-news'
    MONGO_COLLECTION = 'articles'

    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'r00t'
    MYSQL_DATABASE = 'scraper-news'

    EXPIRATION_TOKEN_TIME = 2592000
