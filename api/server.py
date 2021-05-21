from uvicorn import Server, Config

from .routes import app_main
from .config import APP_HOST, APP_PORT


def run_server():
    config = Config(app=app_main, host=APP_HOST, port=APP_PORT)
    server = Server(config=config)

    server.run()
