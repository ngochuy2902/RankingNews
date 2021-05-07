import threading
from gtts import gTTS
from settings import BaseConfig as Config
from data.mysqldb import MySQL


class MyThread(threading.Thread):
    def __init__(self, text: str, uuid: str):
        threading.Thread.__init__(self)
        self.text = text
        self.uuid = uuid

    def run(self):
        create_gtts(self.text, self.uuid)


def create_gtts(text: str, uuid: str):
    mysql = MySQL()
    tts = gTTS(text=text, lang='vi')
    path = Config.BASE_AUDIO_DIR + uuid + ".mp3"
    tts.save(path)
    mysql.add_audio_path(uuid, path)
