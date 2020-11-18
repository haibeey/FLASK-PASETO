# FLASK-PASETO
#### FLASK-PASETO adds basic support for [PASETO](https://github.com/paragonie/paseto) v2 to your Flask app.

### Installation 
Flask-Paseto relies on [paseto](https://github.com/rlittlefield/pypaseto) which in turns relies on [pysodium](https://github.com/stef/pysodium).
pysoduim is a wrapper for the popular [libsoduim](https://github.com/jedisct1/libsodium) cryptography library.
This [guide](https://py-ipv8.readthedocs.io/en/latest/preliminaries/install_libsodium/) shows how to install libsodium on mac and windows.
on linux libsodium could be install using ```sudo apt-get install -y libsodium-dev``` or ```yum install libsodium``` depending on your linux distribution.

To install Flask-Paseto use the command below to get the latest version
```
    pip install flask_paseto
```

#### Example  usage
``` 
    import pysodium

    from flask_paseto import (
        Paseto,
        paseto_required,
        create_access_token,
        create_access_token_public,
        get_paseto_claim,
        get_paseto_claim_public
    )

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

    app.run()
````
The client http request must provide a generated paseto token 
``` 
    GET /protected/public HTTP/1.1
    Authorization: Bearer v2.local.epxJJp-rchdlMondp12dxN9MV7GACjW0swwyOgo5pliQo2fJmC-1WqhrmWDTQBkg08In7zXD6ieM-xpaY2eMWr-mAu64nVi8VvTWi5bc3dhGHGR-Mg8QQ8HJIzPldLfSDLQXwQ
```
#### Configuration Options
| Option                | Description                                                                                     |
|-----------------------| ------------------------------------------------------------------------------------------------|
|PASETO_SECRET_KEY      | This is the secret key used by paseto to sign your data. *It requires 32 byte strings*          |
|PASETO_PUBLIC_KEY      | This is the public key generated as part of the key pair generated for paseto                   |
|PASETO_PRIVATE_KEY     | This is the private key generated as part of the key pair generated for paseto                  |
|PASETO_EXPIRATION_DELTA| The additional time from the current time the token was created before expiration               |  
             
