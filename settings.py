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

    RANK_KEYWORD = {
        "chinh-tri": ["chính phủ", "chủ tịch", "thủ tướng", "quốc hội", "bộ trưởng", "nga", "trung quốc", "mỹ"],
        "xa-hoi": ["hôn nhân"],
        "van-hoa": ["văn hoá", "di sản"],
        "kinh-te": ["vàng", "usd", "xăng", "dầu"],
        "giao-duc": ["thi", "tốt nghiệp", "đại học", "tuyển", "covid"],
        "khoa-hoc": ["covid"],
        "cong-nghe": ["covid"],
        "y-te": ["covid", "dịch"],
        "the-thao": ["bóng đá", "UEFA", "world cup", "euro", "c1", "champion league"],
        "giai-tri": ["oscar", "showbiz"],
        }

    PROBABILITY_MIN_HASHING = 0.5
