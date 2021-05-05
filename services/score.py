import datetime
from typing import List

from data.mongodb import MongoDB
from settings import BaseConfig as Config
from lsh.lsh import LSH


class Score:
    mongo = MongoDB()
    keyword = Config.SCORE_KEYWORD
    lsh = LSH()

    def check_contains_keyword(self, text: str, key_list: List[str]):
        for i in key_list:
            if i in text:
                return True
        return False

    def score_by_category(self, category: str):
        articles_by_category = self.mongo.get_articles_by_category(category=category)
        article_contents = [article.content for article in articles_by_category]
        matrix = self.lsh.init_matrix(list_docs=article_contents)
        min_hash = self.lsh.min_hashing(matrix=matrix, n_permutation=15)
        rs = []
        for article in articles_by_category:
            time = (datetime.datetime.now() - article.time).total_seconds()
            time_score = 1 / time * 1000000
            score = time_score
            if self.check_contains_keyword(article.title, self.keyword[category]):
                print(article.title)
                score = score + 10
            index = self.lsh.get_index_of_doc(article.content, article_contents)
            for i in range(len(articles_by_category)):
                if i != index and articles_by_category[i].domain != article.domain:
                    sim = self.lsh.jaccard_signature(min_hash[:, index], min_hash[:, i])
                    # sim = self.lsh.jaccard_signature(matrix[:, index], matrix[:, i])
                    if sim > Config.PROBABILITY_MIN_HASHING:
                        score = score + 20
                        print('========================')
                        print('sim = ', sim)
                        print(articles_by_category[index])
                        print(articles_by_category[i])
            rs.append({"id": article.id, "url": article.url, "score": score})
        return rs


if __name__ == '__main__':
    score = Score()
    data = score.score_by_category(category="chinh-tri")
    print(len(data))
    for i in data:
        print(i)
