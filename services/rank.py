import requests

from data.mysqldb import MySQL
from models.ranker import Ranker
from services.score import ScoreService
from services.speech import SpeechService
from settings import BaseConfig as Config


class RankService:
    score_service = ScoreService()
    categories = Config.CATEGORIES
    mysql = MySQL()
    tts = SpeechService()

    def rank_by_session(self, ranker: Ranker):

        try:
            article_scores_inserted = []
            for category in self.categories:
                article_scores = self.score_service.score_by_category(category=category)
                article_scores_inserted.extend(article_scores)
            self.mysql.add_article_scores(session_id=ranker.session_id, scores=article_scores_inserted)

            data = Ranker(session_id=ranker.session_id, status='RANKER_SUCCESS')
            json_data = data.__dict__
            requests.post(url=Config.UPDATE_AUDIO_CRAWLER_STATUS_API_URL, json=json_data)
            print("complete ranking")
        except(Exception,) as ex:
            data = Ranker(session_id=ranker.session_id, status='RANKER_FAILED')
            json_data = data.__dict__
            requests.post(url=Config.UPDATE_AUDIO_CRAWLER_STATUS_API_URL, json=json_data)
            print(f'Error run spider: {ex}')


if __name__ == '__main__':
    data = Ranker(session_id=10, status='RANKER_SUCCESS')
    json_data = data.__dict__
    print(json_data)
    requests.post(url=Config.UPDATE_AUDIO_CRAWLER_STATUS_API_URL, json=json_data)
