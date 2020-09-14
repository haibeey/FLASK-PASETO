import logging,paseto
from functools import wraps
from collections import OrderedDict
from .utils import _paseto_required,CONFIG_DEFAULTS,PasetoError
from flask import current_app, request, jsonify, _request_ctx_stack
from .local_paseto import create_access_token,decode_token,get_paseto_claim
from .public_paseto import create_access_token_public,decode_token_public,get_paseto_claim_public


logger = logging.getLogger(__name__)

def paseto_required(func):
    """
        View decorator that requires a valid PASETO token to be present in the request
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        _paseto_required()
        return func(*args, **kwargs)

    return wrapper 

def _default_error_handler(error):
    logger.error(error)
    return jsonify(OrderedDict([
        ('status_code', error.status_code),
        ('error', error.error),
        ('description', error.description),
    ])), error.status_code, error.headers

def _default_token_expire_handler(error):
    logger.error(error)
    return jsonify({
        'status_code':400,
        'description':'The Token sent along with this request is expired'
    })

class Paseto(object):
    def __init__(self,app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        if not app.config.get('SECRET_KEY'):
            app.config.setdefault('PASETO_SECRET_KEY', app.config['SECRET_KEY'])
        for k, v in CONFIG_DEFAULTS.items():
            if app.config.get(k) is None:
                app.config.setdefault(k, v)

        app.errorhandler(PasetoError)(_default_error_handler)
        app.errorhandler(paseto.PasetoTokenExpired)(_default_token_expire_handler)

        if not hasattr(app, 'extensions'): 
            app.extensions = {}

        app.extensions['jwt'] = self



    