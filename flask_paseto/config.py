from flask import current_app


class Config:
    @property
    def _secret_key(self):
        secret = current_app.config.get('PASETO_SECRET_KEY')
        if not secret:
            raise RuntimeError(
                    'PASETO_SECRET_KEY'
                    'must be set when using paseto symmetric/local API')
  
        if not isinstance(secret, str):
            raise ValueError("Given secret key not a string")
        return secret

    @property
    def _public_key(self):
        key = current_app.config.get('PASETO_PUBLIC_KEY')
        if not key:
            raise RuntimeError('PASETO_PUBLIC_KEY must be set when'
                               'using paseto asymmetric/public API')
        return key

    @property
    def _private_key(self):
        key = current_app.config.get('PASETO_PRIVATE_KEY')
        if not key:
            raise RuntimeError('PASETO_PRIVATE_KEY must be set when '
                               'using paseto asymmetric/public API')
        return key
