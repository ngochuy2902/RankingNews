import datetime

from pymongo import MongoClient

from settings import BaseConfig as Conf
from models.articles import Article


class MongoDB:
    myclient = MongoClient(Conf.MONGO_URI)
    mydb = myclient[Conf.MONGO_DATABASE]
    mycol = mydb[Conf.MONGO_COLLECTION]

    def get_articles_by_category(self, category: str):
        time = datetime.datetime.now().replace(day=datetime.datetime.now().day-2, hour=0, minute=0, second=0)
        query = {"category": category, "time": {"$gt": time}}

        articles = self.mycol.find(query)
        response = []
        for item in articles:
            response.append(Article(**item))
        return response

    def get_articles_by_domain(self, domain: str):
        query = {"domain": domain}

        articles = self.mycol.find(query)
        response = []
        for item in articles:
            response.append(Article(**item))
        return response

    def get_articles_by_domain_category(self, domain: str, category: str):
        query = {"domain": domain, "category": category}

        articles = self.mycol.find(query)
        response = []
        for item in articles:
            response.append(Article(**item))
        return response

    def get_articles_by_url(self, url: str):
        query = {"url": {"$regex": url}}
        # return Article(**self.mycol.find_one(query))
        return self.mycol.find_one(query)


if __name__ == '__main__':
    data = MongoDB().get_articles_by_category(category="the-thao")
    # data = MongoDB().get_articles_by_domain(domain="vnexpress")
    # data = MongoDB().get_articles_by_domain_category(domain="nhandan", category="chinh-tri")
    # data = MongoDB().get_articles_by_url(url='1370159.html')
    if data is None:
        print("Noneeee")
    else:
        print(len(data))
        for i in data:
            print(i)
