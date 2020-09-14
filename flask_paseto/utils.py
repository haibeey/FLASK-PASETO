from flask import request,current_app
from datetime import datetime, timedelta

CONFIG_DEFAULTS = {
    'PASETO_EXPIRATION_DELTA': 300, #seconds
    'PASETO_NOT_BEFORE_DELTA': 0, #seconds
    'PASETO_REQUIRED_CLAIMS': ['exp', 'iat', 'nbf'],
}


class PasetoError(Exception):
    def __init__(self, error, description, status_code=401, headers=None):
        self.error = error
        self.description = description
        self.status_code = status_code
        self.headers = headers

    def __repr__(self):
        return 'PASETOError: %s' % self.error

    def __str__(self):
        return '%s. %s' % (self.error, self.description)

def _paseto_required():
    auth_header = request.headers.get('Authorization', None)
    if not auth_header:
        raise PasetoError("Missing Header","No Header sent in Request")
    
    parts = auth_header.split()

    if len(parts) == 1:
        raise PasetoError('Invalid Paseto header', 'Token missing')
    elif len(parts) > 2:
        raise PasetoError('Invalid Paseto header', 'Token contains spaces')
    return parts[1]