from flask_restful import Resource
from reqparser import *
from package.security.decorators import mode_master, mode_superuser
from package.global_variable.variables import *
from run import global_var
from models import TokenModel, update_token_in_memory
import datetime
from flask_jwt_extended import (create_access_token, jwt_required,
                                decode_token)
from package.sequence.python_seq import ThreadWithTrace, perform
import queue
from flask import escape

message_not_started = "cube is not started"
message_not_direct = "Api is not in direct mode"
message_not_sequence = "Api is not in sequence mode"
message_sent = "request sent"
message_wrong = "something went wrong"
current_message = message_not_started


class Sequence(Resource):
    def post(self):
        if can_send_sequence():
            data = parser_seq_add.parse_args()
            program = data["code"]
            try:
                queue_manager.process_pool.put(ThreadWithTrace(data["name"], target=perform, args=(program,)),
                                               block=False)
                return format_response('Sequence saved', True)
            except queue.Full:
                return format_response('Queue is full', False)
        return format_response(message_not_sequence, False)

    def delete(self):
        if can_send_sequence():
            data = parser_seq_del.parse_args()
            index = data['index']
            try:
                queue_manager.delete(index)
                return format_response(f'sequence with index {index} delete', True)
            except KeyError:
                return format_response('something went wrong !', False)
        return format_response(message_not_sequence, False)

    def patch(self):
        if can_send_sequence():
            data = parser_seq_move.parse_args()
            old_index = data['old_index']
            new_index = data['new_index']
            try:
                queue_manager.move(old_index, new_index)
                return format_response(f'sequence with index {old_index} now in {new_index} index', True)
            except KeyError:
                return format_response('something went wrong !', False)
        return format_response(message_not_sequence, False)


class Token(Resource):
    @jwt_required
    @mode_superuser
    def patch(self):
        data = parser_token_find.parse_args()
        jti = data['jti']
        if TokenModel.switch_revoked(jti):
            update_token_in_memory()
            return format_response(f'token with ${jti} changed', True)

        return format_response('something went wrong', False)

    @jwt_required
    @mode_superuser
    def get(self):
        return TokenModel.return_all()

    @jwt_required
    @mode_superuser
    def delete(self):
        data = parser_token_find.parse_args()
        jti = data['jti']

        if TokenModel.delete_by_jti(jti):
            update_token_in_memory()
            return format_response(f'token with ${jti} deleted', True)

        return format_response('something went wrong', False)

    @jwt_required
    @mode_superuser
    def post(self):
        data = parser_token_create.parse_args()
        identity = data['identity']
        date = data['date']
        mode = data['mode']

        if TokenModel.find_by_identity(identity):
            return format_response('Token {} already exists'.format(identity), False)

        new_token = TokenModel(
            identity=escape(identity),
            mode=mode,
            revoked=False,
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
                'state': True
            }
        except Exception as e:
            return format_response('Something went wrong', False)


class ChangeSequence(Resource):
    def post(self):
        if can_send_sequence():
            data = parser_change_sequence.parse_args()
            start = data['start']
            if start == global_var['sequence']:
                return format_response("Cube already in this mode", True)
            if start:
                if not is_cube_started():
                    return format_response("Can't start sending sequence, cube not started", False)
            else:
                queue_manager.kill_current_seq()

            global_var["sequence"] = start
            return format_response(f"Sequence sending state: {start}", True)
        return format_response("Cube not in sequence mode ", False)


class ChangeMode(Resource):
    def post(self):
        data = parser_mode.parse_args()
        mode = data['mode']
        global_var['mode'] = mode
        if can_direct_send():
            queue_manager.kill_current_seq()
            global_var["sequence"] = False
        else:
            cube.blackout_cube()
        return format_response(f"api is now in mode {data['mode']}", True)


class XyzResource(Resource):  # xyz

    def post(self):
        msg = message_not_started
        if is_cube_started():
            msg = message_not_direct
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
        if is_cube_started():
            msg = message_not_direct
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
        if is_cube_started():
            msg = message_not_direct
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
        if is_cube_started():
            msg = message_not_direct
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
        if is_cube_started():
            msg = message_not_direct
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
        if is_cube_started():
            msg = message_not_direct
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
        if is_cube_started():
            msg = message_not_direct
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
    return global_var["mode"] == "direct"


def is_cube_started():
    return global_var["started"]


def get_days(timestamp):
    if timestamp == 0:
        return False
    d1 = datetime.datetime.now()
    return (datetime.datetime.fromtimestamp(timestamp) - d1).days


def can_send_sequence():
    return global_var['mode'] == "sequence"


def format_response(msg_txt, state):
    return {'message': msg_txt, 'state': state}
