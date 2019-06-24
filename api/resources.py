from flask_restful import reqparse, Resource
from package.global_variable.variables import *
from run import global_var

limit_brightness = 16
limit_x = 11
limit_y = 11
limit_z = 13
limit_face = 6
limit_square = 24
limit_ledstrip = 4
limit_led = 27

parser_mode = reqparse.RequestParser()
parser_mode.add_argument('mode', choices=('user', 'master'),
                         help="{error_msg}. mode can be user or master", required=True)

parser_cube = reqparse.RequestParser()
parser_cube.add_argument('brightness', type=int, choices=range(limit_brightness),
                         default=15, help="{error_msg}. brightness is between 0 and 15, 15 by default")

parser_face = reqparse.RequestParser(bundle_errors=True)
parser_face.add_argument('idx_face', type=int, choices=range(limit_face),
                         help='{error_msg}. idx_face is between 0 and 5', required=True)
parser_face.add_argument('brightness', type=int, choices=range(limit_brightness),
                         default=15, help="{error_msg}. brightness is between 0 and 15, 15 by default")

parser_square = reqparse.RequestParser(bundle_errors=True)
parser_square.add_argument('idx_face', type=int, choices=range(limit_face),
                           help='{error_msg}. idx_face is between 0 and 5', required=True)
parser_square.add_argument('idx_square', type=int, choices=range(limit_square),
                           help='{error_msg}. idx_square is between 0 and 23', required=True)
parser_square.add_argument('brightness', type=int, choices=range(limit_brightness),
                           default=15, help="{error_msg}. brightness is between 0 and 15, 15 by default")

parser_ledstrip = reqparse.RequestParser(bundle_errors=True)
parser_ledstrip.add_argument('idx_face', type=int, choices=range(limit_face),
                             help='{error_msg}. idx_face is between 0 and 5', required=True)
parser_ledstrip.add_argument('idx_square', type=int, choices=range(limit_square),
                             help='{error_msg}. idx_square is between 0 and 23', required=True)
parser_ledstrip.add_argument('idx_ledstrip', type=int, choices=range(limit_ledstrip),
                             help='{error_msg}. idx_ledstrip is between 0 and 4',
                             required=True)
parser_ledstrip.add_argument('brightness', type=int, choices=range(limit_brightness),
                             default=15, help="{error_msg}. brightness is between 0 and 15, 15 by default")

parser_led = reqparse.RequestParser(bundle_errors=True)
parser_led.add_argument('idx_face', type=int, choices=range(limit_face),
                        help='{error_msg}. idx_face is between 0 and 5', required=True)
parser_led.add_argument('idx_square', type=int, choices=range(limit_square),
                        help='{error_msg}. idx_square is between 0 and 23', required=True)
parser_led.add_argument('idx_ledstrip', type=int, choices=range(limit_ledstrip),
                        help='{error_msg}. idx_ledstrip is between 0 and 4',
                        required=True)
parser_led.add_argument('idx_led', type=int, choices=range(limit_led), help='{error_msg}. idx_led is between 0 and 26',
                        required=True)
parser_led.add_argument('brightness', type=int, choices=range(limit_brightness),
                        default=15, help="{error_msg}. brightness is between 0 and 15, 15 by default")

parser_xyz = reqparse.RequestParser(bundle_errors=True)
parser_xyz.add_argument('idx_x', type=int, choices=range(limit_x), help='{error_msg}. idx_x is between 0 and 10',
                        required=True)
parser_xyz.add_argument('idx_y', type=int, choices=range(limit_y), help='{error_msg}. idx_y is between 0 and 10',
                        required=True)
parser_xyz.add_argument('idx_z', type=int, choices=range(limit_z), help='{error_msg}. idx_z is between 0 and 12',
                        required=True)
parser_xyz.add_argument('brightness', type=int, choices=range(limit_brightness),
                        default=15, help="{error_msg}. brightness is between 0 and 15, 15 by default")

parser_xyz_led = reqparse.RequestParser(bundle_errors=True)
parser_xyz_led.add_argument('idx_x', type=int, choices=range(limit_x), help='{error_msg}. idx_x is between 0 and 10',
                            required=True)
parser_xyz_led.add_argument('idx_y', type=int, choices=range(limit_y), help='{error_msg}. idx_y is between 0 and 10',
                            required=True)
parser_xyz_led.add_argument('idx_z', type=int, choices=range(limit_z), help='{error_msg}. idx_z is between 0 and 12',
                            required=True)
parser_xyz_led.add_argument('idx_led', type=int, choices=range(limit_led),
                            help='{error_msg}. idx_led is between 0 and 26',
                            required=True)
parser_xyz_led.add_argument('brightness', type=int, choices=range(limit_brightness),
                            default=15, help="{error_msg}. brightness is between 0 and 15, 15 by default")

message_not_started = "cube is not started"
message_not_master_free = "Api is not in master mode or not free"
message_sent = "request sent"
message_wrong = "something went wrong"
current_message = message_not_started


class ChangeMode(Resource):
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
    return global_var["mode"] == "master" and global_var["state"] == "free"


def is_started():
    return global_var["started"]
