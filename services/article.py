from data.mongodb import MongoDB
from data.mysqldb import mysql
from models.articles import ArticleShow
from .category import CategoryService
from settings import BaseConfig as Config


def get_number_of_articles_per_category(number_of_articles: int, number_of_category: int):
    result = []
    for i in range(number_of_category):
        result.append(number_of_articles // number_of_category)
    r = number_of_articles - number_of_category * (number_of_articles // number_of_category)
    for i in range(r):
        result[i] = result[i] + 1
    return result


class ArticleService:
    mysql = mysql
    mongodb = MongoDB()
    category_service = CategoryService()

    def get_articles_by_current_user_id(self, current_user_id: int):
        categories = self.category_service.get_category_by_current_user_id(user_id=current_user_id)
        category_names = [i.name for i in categories]
        valid_session_id = self.mysql.get_valid_session_id()
        number_of_articles_per_category = get_number_of_articles_per_category(Config.NUMBER_OF_ARTICLES,
                                                                              len(categories))
        article_scores = []
        for i in range(len(categories)):
            articles = self.mysql.fetch_articles_ranking(session_id=valid_session_id,
                                                         category=category_names[i],
                                                         limit=number_of_articles_per_category[i])
            article_scores.extend(articles)
        result = []
        for i in article_scores:
            article_mongo = self.mongodb.get_article_by_uuid(i.article_id)
            article_show = ArticleShow(id=article_mongo.id,
                                       url=article_mongo.url,
                                       domain=article_mongo.domain,
                                       title=article_mongo.title,
                                       category=article_mongo.category,
                                       time=article_mongo.time,
                                       content=article_mongo.content,
                                       audio_path=i.audio_path)
            result.append(article_show)
        return result

    def get_articles_no_login(self):
        category_names = Config.CATEGORIES
        valid_session_id = self.mysql.get_valid_session_id()
        number_of_articles_per_category = get_number_of_articles_per_category(Config.NUMBER_OF_ARTICLES,
                                                                              len(category_names))
        article_scores = []
        for i in range(len(category_names)):
            articles = self.mysql.fetch_articles_ranking(session_id=valid_session_id,
                                                         category=category_names[i],
                                                         limit=number_of_articles_per_category[i])
            article_scores.extend(articles)
        result = []
        for i in article_scores:
            article_mongo = self.mongodb.get_article_by_uuid(i.article_id)
            article_show = ArticleShow(id=article_mongo.id,
                                       url=article_mongo.url,
                                       domain=article_mongo.domain,
                                       title=article_mongo.title,
                                       category=article_mongo.category,
                                       time=article_mongo.time,
                                       content=article_mongo.content,
                                       audio_path=i.audio_path)
            result.append(article_show)
        return result


if __name__ == '__main__':
    show_article = ArticleService()
    data = show_article.get_articles_by_current_user_id(current_user_id=12)
    for i in data:
        print(i)
