from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask import request
from flask import jsonify

app = Flask(__name__)
api = Api(app)
db = SQLAlchemy(app)
jwt = JWTManager(app)

import views, models, resources

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'some-secret-string'
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

api.add_resource(resources.UserRegistration, '/registration')
api.add_resource(resources.UserLogin, '/login')
api.add_resource(resources.UserLogoutAccess, '/logout/access')
api.add_resource(resources.UserLogoutRefresh, '/logout/refresh')
api.add_resource(resources.TokenRefresh, '/token/refresh')
api.add_resource(resources.AllUsers, '/users')
api.add_resource(resources.SecretResource, '/secret')


@app.route('/txt', methods=['POST'])
def api_text():
    lol = request.data.decode('utf-8')
    txt = ""
    i = 0
    for line in lol.splitlines():
        print(line)
        txt += line
        i += 1
    return txt + str(i)


@app.route('/json', methods=['POST'])
def api_json():
    lol = request.get_json()
    return lol[0]


@app.before_first_request
def create_tables():
    db.create_all()


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return models.RevokedTokenModel.is_jti_blacklisted(jti)
