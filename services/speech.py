#!/usr/bin/python
# -*- coding: utf-8 -*-
import time

from gtts import gTTS
from data.mysqldb import MySQL
from data.mongodb import MongoDB
from settings import BaseConfig as Config
from thread import MyThread
import asyncio
import threading
import os


class TextToSpeech:
    sql = MySQL()
    mongodb = MongoDB()

    def text_to_speech(self):
        session_id = self.sql.get_current_session_id()
        create_list = []
        for category in Config.CATEGORIES:
            category_name = Config.CATEGORIES_NAME.get(category)
            article_scores = self.sql.fetch_articles_ranking(session_id=session_id, category=category, limit=15)
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
                    audio_detail = {"text": text, "uuid": article.id}
                    create_list.append(audio_detail)
        return create_list

    def create_audio(self, create_list=None):
        if create_list is None:
            create_list = self.text_to_speech()
        print('create audio list size: ', len(create_list))
        for cl in create_list:
            text = cl.get('text')
            uuid = cl.get('uuid')
            thread = MyThread(text=text, uuid=uuid)
            thread.start()
            time.sleep(10)


if __name__ == '__main__':
    ttsG = TextToSpeech()
    # ttsG.create_audio()
    # print("done")
    tts = gTTS(text='text', tld='com.vn', lang='vi')
    tts.save(Config.BASE_AUDIO_DIR + "test" + ".mp3")
