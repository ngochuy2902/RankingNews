from data.mongodb import MongoDB
from data.mysqldb import MySQL
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


class ShowArticle:
    mysql = MySQL()
    mongodb = MongoDB()
    category_service = CategoryService()

    def get_articles_by_current_user_id(self, current_user_id: int):
        categories = self.category_service.get_category_by_current_user_id(user_id=current_user_id)
        category_names = [i.name for i in categories]
        current_session_id = self.mysql.get_current_session_id()
        number_of_articles_per_category = get_number_of_articles_per_category(Config.NUMBER_OF_ARTICLES,
                                                                              len(categories))
        article_scores = []
        for i in range(len(categories)):
            articles = self.mysql.fetch_articles_ranking(session_id=current_session_id,
                                                         category=category_names[i],
                                                         limit=number_of_articles_per_category[i])
            article_scores.extend(articles)
        result = []
        for i in article_scores:
            result.append(self.mongodb.get_article_by_uuid(i.article_id))
        return result


if __name__ == '__main__':
    show_article = ShowArticle()
    data = show_article.get_articles_by_current_user_id(current_user_id=12)
    for i in data:
        print(i)
