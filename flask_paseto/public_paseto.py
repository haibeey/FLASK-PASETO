import paseto
from .config import Config
from flask import request
from .utils import _paseto_required
from flask import current_app
def create_access_token_public(identity, footer=None):
    token = paseto.create(
        key=Config()._private_key,
        purpose='public',
        claims=identity,
        footer=footer,
        exp_seconds=current_app.config.get('PASETO_EXPIRATION_DELTA')
    )

    return token.decode("utf-8")

def decode_token_public():
    token = _paseto_required()
    parsed = paseto.parse(
        key=Config()._public_key,
        purpose='public',
        token=token.encode(),
    )
    return parsed

def get_paseto_claim_public():
    return decode_token_public()["message"]