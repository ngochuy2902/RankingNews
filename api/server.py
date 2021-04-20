from uvicorn import Server, Config

from .routes import api_router
from .config import APP_HOST, APP_PORT


def run_server():
    config = Config(app=api_router, host=APP_HOST, port=APP_PORT)
    server = Server(config=config)

    server.run()
