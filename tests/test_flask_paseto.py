import time,json,pytest
from datetime import datetime, timedelta
from flask import Flask, json, jsonify
import pysodium

from flask_paseto import (
    Paseto,
    paseto_required,
    create_access_token,
    create_access_token_public,
    get_paseto_claim,
    get_paseto_claim_public
)

def mock_app():
    app = Flask(__name__)

    app.config['PASETO_SECRET_KEY'] = '0'*32 # must be 32 byte
    pk, sk = pysodium.crypto_sign_keypair()
    app.config['PASETO_PRIVATE_KEY']=sk
    app.config['PASETO_PUBLIC_KEY']=pk


    paseto = Paseto(app)

    @app.route('/protected/local/')
    @paseto_required
    def protected():
        claims = get_paseto_claim()
        return jsonify(claims), 200

    @app.route('/create/local/token/')
    def create_token():
        ret = {'access_token': create_access_token({'test user':'yes'})}
        return jsonify(ret), 200
    
    @app.route('/create/public/token/')
    def create_public_token():
        ret = {'access_token': create_access_token_public({'public test user':'yes'})}
        return jsonify(ret), 200

    @app.route('/protected/public/')
    @paseto_required
    def protected_public():
        claims = get_paseto_claim_public()
        return jsonify(claims), 200

    return app


def test_initialize():
    app = Flask(__name__)
    paseto = Paseto(app)
    assert isinstance(paseto, Paseto)


def test_local():
    app = mock_app().test_client()
    resp = app.get('/create/local/token/')
    resp = json.loads(resp.get_data())
    header={'Authorization':'Bearer {}'.format(resp['access_token'])} 
    resp=app.get('/protected/local/',headers=header)
    assert json.loads(
        resp.get_data().decode('utf-8')
    ).get('test user')=='yes'

    resp=app.get('/protected/local/')
    assert (b'Missing Header' in resp.get_data())
  

def test_public():
    app = mock_app().test_client()
    resp = app.get('/create/public/token/')
    resp = json.loads(resp.get_data())
    header={'Authorization':'Bearer {}'.format(resp['access_token'])} 
    resp=app.get('/protected/public/',headers=header)
    assert json.loads(
        resp.get_data().decode('utf-8')
    ).get('public test user')=='yes'

    resp=app.get('/protected/public/')
    assert (b'Missing Header' in resp.get_data())

def test_expired_token():
    main_app = mock_app()
    main_app.config['PASETO_EXPIRATION_DELTA']=1
    app = main_app.test_client()
    resp = app.get('/create/local/token/')
    resp = json.loads(resp.get_data())
    header={'Authorization':'Bearer {}'.format(resp['access_token'])}
    from time import sleep 
    sleep(2)
    resp=app.get('/protected/local/',headers=header)
    assert json.loads(
        resp.get_data().decode('utf-8')
    ).get('description')=='The Token sent along with this request is expired'

    resp=app.get('/protected/local/')
    assert (b'Missing Header' in resp.get_data())


