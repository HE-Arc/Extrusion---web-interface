from flask_restful import Resource
from reqparser import *
from package.security.decorators import mode_master, mode_superuser, mode_user
from package.global_variable.variables import *
from run import global_var
from models import TokenModel, update_token_in_memory
import datetime
from flask_jwt_extended import (create_access_token, jwt_required,
                                decode_token)
from package.sequence.python_seq import ThreadWithTrace, perform
import queue
from flask import escape
import ipaddress

message_not_started = "cube is not started"
message_not_direct = "Api is not in direct mode"
message_not_sequence = "Api is not in sequence mode"
message_sent = "request sent"
message_wrong = "something went wrong"
current_message = message_not_started


class Network(Resource):
    """Class resource of Network

    route:/network
    This class manage the route to change network information

    """
    @jwt_required
    @mode_superuser
    def post(self):
        """Post function of network

        Change the network data to send ArtNet Data

        :return information of request
        """
        data = parser_change_network.parse_args()
        try:
            if not is_cube_started():
                ipaddress.ip_address(data['ip1'])
                ipaddress.ip_address(data['ip2'])
                ipaddress.ip_address(data['port1'])
                ipaddress.ip_address(data['port2'])
                artnet_group.set_ip(data['ip1'], data['port1'], data['ip2'], data['port2'], start_cube1, end_cube1,
                                    start_cube2, end_cube2)
                return format_response("Network set", True)
            else:
                return format_response("Cube must be off to set network datas", False)

        except ValueError:
            return format_response("Error in NetWork Data", False)
        except:
            return format_response(message_wrong, False)


class Fps(Resource):
    """Class resource of fps

    route:/fps
    this class manage the route to configure fps to send data
    """
    @jwt_required
    @mode_superuser
    def post(self):
        """post funcion of fps

        Change fps of ArtNet sending

        :return information of request
        """
        data = parser_change_fps.parse_args()
        try:
            artnet_group.set_fps(data['fps'])
            return format_response('fps set', True)
        except:
            return format_response('error', False)


class Sequence(Resource):
    """Class resource of sequence

    route:/seq
    This class manage all the request to manage sequence
    """
    @jwt_required
    @mode_user
    def post(self):
        """post function of sequence

        Add a sequence to queue

        :return information of request
        """
        if can_send_sequence():
            data = parser_seq_add.parse_args()
            program = data["code"]
            name = escape(data['name'])
            try:
                # add sequence to queue
                queue_manager.process_pool.put(ThreadWithTrace(name, target=perform, args=(program,)),
                                               block=False)
                return format_response('Sequence saved', True)
            except queue.Full:
                return format_response('Queue is full', False)
        return format_response(message_not_sequence, False)

    @jwt_required
    @mode_superuser
    def delete(self):
        """delete function of sequence

        delete a sequence in the queue

        :return information of request
        """
        if can_send_sequence():
            data = parser_seq_del.parse_args()
            index = data['index']
            try:
                queue_manager.delete(index)
                return format_response(f'sequence with index {index} delete', True)
            except KeyError:
                return format_response('something went wrong !', False)
        return format_response(message_not_sequence, False)

    @jwt_required
    @mode_superuser
    def patch(self):
        """patch function of sequence

        move a sequence in the queue

        :return information of request
        """
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
    """Class resource of token

    route:/token
    This class manage all the request to manage token

    """
    @jwt_required
    @mode_superuser
    def patch(self):
        """patch function of token

        Change the revoked status of a token in db

        :return information of request
        """
        data = parser_token_find.parse_args()
        jti = data['jti']
        if TokenModel.switch_revoked(jti):
            update_token_in_memory()
            return format_response(f'token with ${jti} changed', True)

        return format_response('something went wrong', False)

    @jwt_required
    @mode_superuser
    def get(self):
        """get function of token

        get all information of all token in db

        :return information of request
        """
        return TokenModel.return_all()

    @jwt_required
    @mode_superuser
    def delete(self):
        """delete function of token

        delete a token in db

        :return information of request
        """
        data = parser_token_find.parse_args()
        jti = data['jti']

        if TokenModel.delete_by_jti(jti):
            update_token_in_memory()
            return format_response(f'token with ${jti} deleted', True)

        return format_response('something went wrong', False)

    @jwt_required
    @mode_superuser
    def post(self):
        """post function of token

        Create a new token

        :return information of request
        """
        data = parser_token_create.parse_args()
        identity = data['identity']
        date = data['date']
        mode = data['mode']

        if TokenModel.find_by_identity(identity):
            return format_response('Token {} already exists'.format(identity), False)

        # create model
        new_token = TokenModel(
            identity=escape(identity),
            mode=mode,
            revoked=False,
            date=date
        )
        try:
            # create token with request information
            access_token = create_access_token(identity=new_token.identity,
                                               expires_delta=datetime.timedelta(days=get_days(date)),
                                               user_claims={'mode': new_token.mode})
            # get information of token to put in the model
            new_token.token = access_token
            decode = decode_token(access_token)
            new_token.jti = decode['jti']
            # save model in db
            new_token.save_to_db()
            # update token in memory
            update_token_in_memory()
            return {
                'message': 'Token {} was created'.format(identity),
                'access_token': access_token,
                'state': True
            }
        except Exception as e:
            print(e)
            return format_response('Something went wrong', False)


class StartSequence(Resource):
    """Class resource of start stop sequence

    /startsea
    This class manage the function to start and stop sequence sending
    """
    @jwt_required
    @mode_superuser
    def post(self):
        """post function of startSequence

        start or stop to send sequence to the cube

        :return information of request
        """
        if can_send_sequence():
            data = parser_change_sequence.parse_args()
            start = data['start']
            # check if cube is already started
            if start == global_var['sequence']:
                return format_response("Cube already started", True)
            if start:
                # check if cube is started
                if not is_cube_started():
                    return format_response("Can't start sending sequence, cube not started", False)
            else:
                queue_manager.kill_current_seq()

            global_var["sequence"] = start
            return format_response(f"Sequence sending state: {start}", True)
        return format_response("Cube not in sequence mode ", False)


class ChangeMode(Resource):
    """Class resource to manage mode

    /chagemode
    Change the mode of the cube

    """
    @jwt_required
    @mode_superuser
    def post(self):
        """post function of ChangeMode

        Change the mode of the cube in direct or sequence

        :return information of request
        """
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
    """Class resource Of Xyz coordinates

    /xyz
    This class manage the request of xyz coordinate system

    """
    @jwt_required
    @mode_master
    def post(self):
        """post function of /xyz

        route to illuminate a ledstrip with xyz coordinate system
        :return information of request
        """
        is_ok = False
        msg = message_not_started
        if is_cube_started():
            msg = message_not_direct
            if can_direct_send():
                data = parser_xyz.parse_args()
                try:
                    cube.xyz[data['idx_x'], data['idx_y'], data['idx_z']].show(data['brightness'])
                    msg = message_sent
                    is_ok = True
                except:
                    msg = message_wrong
        return format_response(msg, is_ok)


class XyzLedResource(Resource):  # xyz
    """Class resource Of Xyz led

    /xyzled
    This class manage the request of xyz coordinate system

    """
    @jwt_required
    @mode_master
    def post(self):
        """post function of /xyzled

        route to illuminate a led with xyz coordinate system
        :return information of request
        """
        msg = message_not_started
        is_ok = False
        if is_cube_started():
            msg = message_not_direct
            if can_direct_send():
                data = parser_xyz_led.parse_args()
                try:
                    cube.xyz[data['idx_x'], data['idx_y'], data['idx_z']].led[data['idx_led']].show(data['brightness'])
                    msg = message_sent
                    is_ok = True
                except:
                    msg = message_wrong
        return format_response(msg, is_ok)


class CubeResource(Resource):  # cube
    """Class resource Of cube

    /cube
    This class manage the request of cube

    """
    @jwt_required
    @mode_master
    def post(self):
        """post function of /cube

        route to illuminate the cube
        :return information of request
        """
        msg = message_not_started
        is_ok = False
        if is_cube_started():
            msg = message_not_direct
            if can_direct_send():
                data = parser_cube.parse_args()
                try:
                    cube.show(data['brightness'])
                    msg = message_sent
                    is_ok = True
                except:
                    msg = message_wrong
        return format_response(msg, is_ok)


class FaceResource(Resource):  # face
    """Class resource Of face

    /face
    This class manage the request of face

    """
    @jwt_required
    @mode_master
    def post(self):
        """post function of /face

        route to illuminate a face
        :return information of request
        """
        msg = message_not_started
        is_ok = False
        if is_cube_started():
            msg = message_not_direct
            if can_direct_send():
                data = parser_face.parse_args()
                try:
                    cube.faces[data['idx_face']].show(data['brightness'])
                    msg = message_sent
                    is_ok = True
                except:
                    msg = message_wrong
        return format_response(msg, is_ok)


class SquareResource(Resource):
    """Class resource Of square

    /square
    This class manage the request of square

    """
    @jwt_required
    @mode_master
    def post(self):
        """post function of /square

        route to illuminate a square
        :return information of request
        """
        msg = message_not_started
        is_ok = False
        if is_cube_started():
            msg = message_not_direct
            if can_direct_send():
                data = parser_square.parse_args()
                try:
                    cube.faces[data['idx_face']].squares[data['idx_square']].show(data['brightness'])
                    msg = message_sent
                    is_ok = True
                except:
                    msg = message_wrong
        return format_response(msg, is_ok)


class LedstripResource(Resource):
    """Class resource Of ledstrip

    /ledstrip
    This class manage the request of ledstrip

    """
    @jwt_required
    @mode_master
    def post(self):
        """post function of /ledstrip

        route to illuminate a ledstrip
        :return information of request
        """
        msg = message_not_started
        is_ok = False
        if is_cube_started():
            msg = message_not_direct
            if can_direct_send():
                data = parser_ledstrip.parse_args()
                try:
                    cube.faces[data['idx_face']].squares[data['idx_square']].ledstrips[data['idx_ledstrip']].show(
                        data['brightness'])
                    msg = message_sent
                    is_ok = True
                except:
                    msg = message_wrong
        return format_response(msg, is_ok)


class LedResource(Resource):
    """Class resource Of led

    /led
    This class manage the request of led

    """
    @jwt_required
    @mode_master
    def post(self):
        """post function of /led

        route to illuminate a led
        :return information of request
        """
        msg = message_not_started
        is_ok = False
        if is_cube_started():
            msg = message_not_direct
            if can_direct_send():
                data = parser_led.parse_args()
                try:
                    cube.faces[data['idx_face']].squares[data['idx_square']].ledstrips[data['idx_ledstrip']].led[
                        data['idx_led']].show(data['brightness'])
                    msg = message_sent
                    is_ok = True
                except:
                    msg = message_wrong
        return format_response(msg, is_ok)


def can_direct_send():
    """Know if cube is in direct mode

    :return: boolean true in direct mode
    """
    return global_var["mode"] == "direct"


def is_cube_started():
    """know if cube is started

    :return: boolean true if cube started
    """
    return global_var["started"]


def get_days(timestamp):
    """ return remaining days form timestamp

    :param timestamp: timestamp to convert
    :return: remaining days
    """
    if timestamp == 0:
        return False
    d1 = datetime.datetime.now()
    return (datetime.datetime.fromtimestamp(timestamp) - d1).days


def can_send_sequence():
    """Know if cube in sequence mode

    :return: boolean true if in sequence mode
    """
    return global_var['mode'] == "sequence"


def format_response(msg_txt, state):
    """format response of all route in api

    :param msg_txt: information message
    :param state: status of request
    :return: formatted response
    """
    return {'message': msg_txt, 'state': state}
