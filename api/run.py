from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask import jsonify
from package.sequence.sequence_manager import SequenceManager
from package.security.blacklist import is_jti_blacklisted
import os

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'caseàchocs12'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']
app.config['SUPERUSER_TOKEN'] = os.environ["SUPERUSER_TOKEN"]

db = SQLAlchemy(app)
jwt = JWTManager(app)
global_var = {"started": False, "mode": "direct", "sequence": False}

sequence_manager = SequenceManager(global_var).start()

import views, models

models.update_token_in_memory()


@app.before_first_request
def create_tables():
    db.create_all()


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return is_jti_blacklisted(decrypted_token['jti'])


@jwt.expired_token_loader
def my_expired_token_callback(expired_token):
    token_type = expired_token['type']
    return jsonify({
        'status': 401,
        'sub_status': 42,
        'msg': 'The {} token has expired'.format(token_type)
    }), 401
