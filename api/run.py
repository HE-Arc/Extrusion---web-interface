from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask import jsonify
from package.sequence.sequence_manager import SequenceManager
from package.security.blacklist import is_jti_blacklisted
from flask_cors import CORS
import datetime
from passlib.hash import pbkdf2_sha256 as sha256

app = Flask(__name__)
api = Api(app)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://cube:cube@localhost/cube'
app.config['SECRET_KEY'] = b'\x89#.\x1e\xa9\xe8\xd9h\x99\xb6\xc0\xbb\xbfq\xd0\xd8+\xff\x97\x00a;%j'
app.config['JWT_SECRET_KEY'] = b'\x89\x94\xba\xc6\xbb\xcbZ\x9c{V\xcfUq5\xba\x01zv2\x89C\xda\x86\xa9'
app.config['admin_user'] = "lewis"
app.config['admin_pwd'] = sha256.hash("lol")

app.config[
    'SUPERUSER_TOKEN'] = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NjM5MTMyODYsIm5iZiI6MTU2MzkxMzI4NiwianRpIjoiMjgxMThhZDYtZGU0YS00MzJmLTk3ZTMtMTk4MmUwMzBjNmU5IiwiaWRlbnRpdHkiOiJTdXBlclVzZXIgYWRtaW4gUGFuZWwiLCJmcmVzaCI6ZmFsc2UsInR5cGUiOiJhY2Nlc3MiLCJ1c2VyX2NsYWltcyI6eyJtb2RlIjoic3VwZXJ1c2VyIn19.l47Lm8qekR1bIM90nPIRr7rVRRRYnxjK_55u8E1i_pg"

app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']

db = SQLAlchemy(app)
jwt = JWTManager(app)
global_var = {"started": False, "mode": "direct", "sequence": False}

sequence_manager = SequenceManager(global_var).start()

import views, models

db.create_all()
models.update_token_in_memory()


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    """callback function to check blacklisted token

    this function is call to every route with a token access
    if token status
    is true : refuse access
    is false : authorize access

    :param decrypted_token: token in header
    :return: if token is revoked or not
    """
    return is_jti_blacklisted(decrypted_token['jti'])


@jwt.expired_token_loader
def my_expired_token_callback(expired_token):
    """callback function to expired token

    function call when a expired token is given to the api

    :param expired_token: token
    :return: error 401
    """
    token_type = expired_token['type']
    return jsonify({
        'status': 401,
        'sub_status': 42,
        'msg': 'The {} token has expired'.format(token_type)
    }), 401
