import time
from typing import Dict
import jwt
from settings import BaseConfig as config

JWT_SECRET = 'scraper-news'
JWT_ALGORITHM = 'HS512'


def token_response(token: str):
    return {
        "access_token": token
    }


def signJWT(user_id: int, user_role: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "user_role": user_role,
        "expires": time.time() + config.EXPIRATION_TOKEN_TIME
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}


if __name__ == '__main__':
    # print(signJWT(user_id=1, user_role="ADMIN"))
    print(decodeJWT(token='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VyX3JvbGUiOiJBRE1JTiIsImV4cGlyZXMiOjE2MjE3NDMwMDMuMjc1MDAyfQ.6WAqHKEvqIy6ODIAOk4t0n_lC9TP_Y3vDHkckOhew8nEZvTvbM72h-1zYa0_yAv62XWjfwIWgo6KaJy1KE52ew'))
