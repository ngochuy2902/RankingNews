from data.mongodb import MongoDB

mongo = MongoDB()


class Rank:
    def rank_by_category(self, category: str):
        articles = mongo.get_articles_by_category(category)

