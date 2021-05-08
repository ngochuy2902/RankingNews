from data.mysqldb import MySQL
from score import Score
from settings import BaseConfig as Config
from speech import TextToSpeech


class Rank:
    score = Score()
    categories = Config.CATEGORIES
    mysql = MySQL()
    tts = TextToSpeech()

    def rank_by_session(self):
        article_scores_inserted = []
        for category in self.categories:
            article_scores = self.score.score_by_category(category=category)
            article_scores_inserted.extend(article_scores)
        self.mysql.add_article_scores(article_scores_inserted)
        self.tts.create_audio()
        self.mysql.update_session_complete(session_id=self.mysql.get_current_session_id())


if __name__ == '__main__':
    rank = Rank()
    rank.rank_by_session()
