from datetime import datetime

from data.mysqldb import mysql
from models.crawler import Crawler
from services.score import ScoreService
from settings import BaseConfig as Config
from services.speech import SpeechService


class RankService:
    score_service = ScoreService()
    categories = Config.CATEGORIES
    mysql = mysql
    tts = SpeechService()

    def rank_by_session(self, crawler: Crawler):
        article_scores_inserted = []
        for category in self.categories:
            article_scores = self.score_service.score_by_category(category=category)
            article_scores_inserted.extend(article_scores)
        self.mysql.add_new_session(created_time=crawler.created_time)
        self.mysql.add_article_scores(scores=article_scores_inserted)
        self.tts.create_audio()
        self.mysql.update_session_complete(session_id=self.mysql.get_current_session_id())
        print("complete ranking")


if __name__ == '__main__':
    rank = RankService()
    crawler = Crawler(created_time=datetime.now())
    rank.rank_by_session(crawler)
