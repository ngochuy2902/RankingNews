import random
import time

import requests
from gtts import gTTS
from data.mongodb import MongoDB
from data.mysqldb import mysql
from settings import BaseConfig as Config


class SpeechService:
    sql = mysql
    mongodb = MongoDB()

    def get_list_audio(self):
        session_id = self.sql.get_current_session_id()
        create_list = []
        for category in Config.CATEGORIES:
            category_name = Config.CATEGORIES_NAME.get(category)
            article_scores = self.sql.fetch_articles_ranking(session_id=session_id,
                                                             category=category,
                                                             limit=Config.NUMBER_OF_ARTICLES)
            for ac in article_scores:
                print(ac)
                old_score = self.sql.get_article_score_by_uuid_and_audio_not_null(ac.article_id)
                if old_score:
                    self.sql.add_audio_path(ac.article_id, old_score.audio_path)
                else:
                    article = self.mongodb.get_article_by_uuid(ac.article_id)
                    text = "Tin " + category_name + ". "
                    text = text + article.title + ". "
                    text = text + article.content
                    text = text.replace("\"", "").replace("tp", "thành phố").replace("TP", "thành phố")
                    text = text.replace("-", " ").replace("/", " tháng ")
                    audio_detail = {"text": text, "uuid": article.id}
                    create_list.append(audio_detail)
        return create_list

    def create_audio(self, create_list=None):
        if create_list is None:
            create_list = self.get_list_audio()
        print('create audio list size: ', len(create_list))
        index = 1
        for cl in create_list:
            text = cl.get('text')
            uuid = cl.get('uuid')
            print('create audio: ', index)
            # try:
            #     self.create_gtts(text=text, uuid=uuid)
            #     completed = completed + 1
            # except(Exception,):
            #     pass
            self.create_gtts_by_js(uuid=uuid, text=text)

            delay = random.randint(10, 20)
            if index % 10 == 0:
                delay = random.randint(30, 60)
            print("delay in: ", delay)
            time.sleep(delay)
            index = index + 1
        print('create audio is completed')

    def create_gtts(self, text: str, uuid: str):
        tts = gTTS(text=text, lang='vi')
        path = Config.BASE_AUDIO_DIR + uuid + ".mp3"
        print("create gtts: ", uuid)
        try:
            tts.save(path)
            self.sql.add_audio_path(uuid, path)
            print("create gtts completed: ", uuid)
        except(Exception,) as ex:
            print("create gtts failed with uuid: ", uuid)
            print("Ex: ", ex)

    def create_gtts_by_js(self, uuid: str, text: str):
        data = {"uuid": uuid, "text": text}
        requests.post(url=Config.AUDIO_API_URL, json=data)


if __name__ == '__main__':
    # ttsG = TextToSpeech()
    # ttsG.create_audio()
    # print("done")
    ttsG = gTTS(text='huy huy huy huy huy', tld='com.vn', lang='vi')
    ttsG.save(Config.BASE_AUDIO_DIR + "test5" + ".mp3")
