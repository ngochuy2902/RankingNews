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

    ADMIN = 1
    USER = 2

    CATEGORIES = ["chinh-tri", "xa-hoi", "van-hoa", "giao-duc", "khoa-hoc", "cong-nghe", "y-te", "the-thao", "giai-tri"]

    CATEGORIES_NAME = {"chinh-tri": "chính trị",
                       "xa-hoi": "xã hội",
                       "van-hoa": "văn hoá",
                       "giao-duc": "giáo dục",
                       "khoa-hoc": "khoa học",
                       "cong-nghe": "công nghệ",
                       "y-te": "y tế",
                       "the-thao": "thể thao",
                       "giai-tri": "giải trí"}

    SCORE_KEYWORD = {
        "chinh-tri": ["chính phủ", "chủ tịch", "thủ tướng", "quốc hội", "bộ trưởng", "nga", "trung quốc", "mỹ"],
        "xa-hoi": ["hôn nhân"],
        "van-hoa": ["văn hoá", "di sản"],
        "kinh-te": ["vàng", "usd", "xăng", "dầu"],
        "giao-duc": ["thi", "tốt nghiệp", "đại học", "tuyển", "Covid"],
        "khoa-hoc": ["covid"],
        "cong-nghe": ["covid"],
        "y-te": ["covid", "dịch"],
        "the-thao": ["bóng đá", "UEFA", "world cup", "euro", "c1", "champion league"],
        "giai-tri": ["oscar", "showbiz"],
    }

    PROBABILITY_MIN_HASHING = 0.4

    NUMBER_OF_ARTICLES = 15

    BASE_AUDIO_DIR = '/Users/huyhn/Study/DATN/audio/'

    AUDIO_API_URL = 'http://localhost:3002/create'
