import datetime

from data.mongodb import MongoDB
from settings import BaseConfig as Config


class Rank:
    mongo = MongoDB()
    keyword = Config.RANK_KEYWORD

    def rank_by_domain_category(self, domain: str, category: str):
        articles_by_domain_category = self.mongo.get_articles_by_domain_category(domain=domain, category=category)
        articles_by_category = self.mongo.get_articles_by_category(category=category)
        rs = []
        for article in articles_by_domain_category:
            time = (datetime.datetime.now() - article.time).total_seconds()
            time_mark = 1/time*1000000
            mark = time_mark
            print(time_mark)
            if article.title in self.keyword[category]:
                print(article.title)
                mark = mark + 3
            rs.append({"url": article.url, "mark": mark})
        return rs


if __name__ == '__main__':
    rank = Rank()
    data = rank.rank_by_domain_category(domain="vnexpress", category="giao-duc")
    print(len(data))
    for i in data:
        print(i)
