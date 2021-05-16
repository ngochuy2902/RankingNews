from uvicorn import Server, Config

from .config import APP_HOST, APP_PORT
from .routes import init_app


def run_server():
    config = Config(app=init_app(), host=APP_HOST, port=APP_PORT)
    server = Server(config=config)

    server.run()
