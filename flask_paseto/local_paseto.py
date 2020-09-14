import paseto,json
from .config import Config
from flask import request
from .utils import _paseto_required
from flask import current_app


def create_access_token(claims,footer=None):
    token = paseto.create(
        key=Config()._secret_key,
        purpose='local',
        claims=claims,
        footer=footer,
        exp_seconds=current_app.config.get('PASETO_EXPIRATION_DELTA')
    )

    return token.decode("utf-8")

def decode_token():
    token = _paseto_required()
    parsed = paseto.parse(
        key=Config()._secret_key,
        purpose='local',
        token=token.encode(),
    )
    return parsed

def get_paseto_claim():
    return decode_token()["message"]