from flask_restful import Resource
from reqparser import *
from package.security.decorators import mode_master, mode_superuser
from package.global_variable.variables import *
from run import global_var
from models import TokenModel, update_token_in_memory
import datetime
from flask_jwt_extended import (create_access_token, jwt_required,
                                decode_token, verify_jwt_in_request)

message_not_started = "cube is not started"
message_not_master_free = "Api is not in master mode or not free"
message_sent = "request sent"
message_wrong = "something went wrong"
current_message = message_not_started


class Token(Resource):
    def patch(self):
        data = parser_token_find.parse_args()
        jti = data['jti']
        if TokenModel.switch_revoked(jti):
            update_token_in_memory()
            return {'message': True}

        return {'message': False}

    @jwt_required
    @mode_superuser
    def get(self):
        return TokenModel.return_all()

    def delete(self):
        data = parser_token_find.parse_args()
        jti = data['jti']

        if TokenModel.delete_by_jti(jti):
            update_token_in_memory()
            return {'message': 'Token {} delete'.format(jti)}

        return {'message': 'Token {} doesnt exist'.format(jti)}

    def post(self):
        data = parser_token_create.parse_args()
        identity = data['identity']
        date = data['date']
        mode = data['mode']

        if TokenModel.find_by_identity(identity):
            return {'message': 'Token {} already exists'.format(identity)}

        new_token = TokenModel(
            identity=identity,
            mode=mode,
            revoked=True,
            date=date
        )
        print(get_days(date))
        try:
            access_token = create_access_token(identity=new_token.identity,
                                               expires_delta=datetime.timedelta(days=get_days(date)),
                                               user_claims={'mode': new_token.mode})
            new_token.token = access_token
            decode = decode_token(access_token)
            new_token.jti = decode['jti']
            new_token.save_to_db()
            update_token_in_memory()
            return {
                'message': 'Token {} was created'.format(identity),
                'access_token': access_token,
            }
        except Exception as e:
            print(e)
            return {'message': 'Something went wrong'}, 500


class ChangeMode(Resource):
    @jwt_required
    @mode_master
    def post(self):
        data = parser_mode.parse_args()
        global_var['mode'] = data['mode']
        return {'message': f"api is now in mode {data['mode']}"}


class XyzResource(Resource):  # xyz

    def post(self):
        msg = message_not_started
        if is_started():
            msg = message_not_master_free
            if can_direct_send():
                data = parser_xyz.parse_args()
                try:
                    cube.xyz[data['idx_x'], data['idx_y'], data['idx_z']].show(data['brightness'])
                    msg = message_sent
                except:
                    msg = message_wrong
        return {'message': msg}


class XyzLedResource(Resource):  # xyz

    def post(self):
        msg = message_not_started
        if is_started():
            msg = message_not_master_free
            if can_direct_send():
                data = parser_xyz_led.parse_args()
                try:
                    cube.xyz[data['idx_x'], data['idx_y'], data['idx_z']].led[data['idx_led']].show(data['brightness'])
                    msg = message_sent
                except:
                    msg = message_wrong
        return {'message': msg}


class CubeResource(Resource):  # cube

    def post(self):
        msg = message_not_started
        if is_started():
            msg = message_not_master_free
            if can_direct_send():
                data = parser_cube.parse_args()
                try:
                    cube.show(data['brightness'])
                    msg = message_sent
                except:
                    msg = message_wrong
        return {'message': msg}


class FaceResource(Resource):  # face
    def post(self):
        msg = message_not_started
        if is_started():
            msg = message_not_master_free
            if can_direct_send():
                data = parser_face.parse_args()
                try:
                    cube.faces[data['idx_face']].show(data['brightness'])
                    msg = message_sent
                except:
                    msg = message_wrong
        return {'message': msg}


class SquareResource(Resource):
    def post(self):
        msg = message_not_started
        if is_started():
            msg = message_not_master_free
            if can_direct_send():
                data = parser_square.parse_args()
                try:
                    cube.faces[data['idx_face']].squares[data['idx_square']].show(data['brightness'])
                    msg = message_sent
                except:
                    msg = message_wrong
        return {'message': msg}


class LedstripResource(Resource):
    def post(self):
        msg = message_not_started
        if is_started():
            msg = message_not_master_free
            if can_direct_send():
                data = parser_ledstrip.parse_args()
                try:
                    cube.faces[data['idx_face']].squares[data['idx_square']].ledstrips[data['idx_ledstrip']].show(
                        data['brightness'])
                    msg = message_sent
                except:
                    msg = message_wrong
        return {'message': msg}


class LedResource(Resource):
    def post(self):
        msg = message_not_started
        if is_started():
            msg = message_not_master_free
            if can_direct_send():
                data = parser_led.parse_args()
                try:
                    cube.faces[data['idx_face']].squares[data['idx_square']].ledstrips[data['idx_ledstrip']].led[
                        data['idx_led']].show(data['brightness'])
                    msg = message_sent
                except:
                    msg = message_wrong
        return {'message': msg}


def can_direct_send():
    return global_var["state"] == "free"


def is_started():
    return global_var["started"]


def get_days(timestamp):
    d1 = datetime.datetime.now()
    return (datetime.datetime.fromtimestamp(timestamp) - d1).days
