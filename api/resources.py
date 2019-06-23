from flask_restful import reqparse, Resource
from package.global_variable.variables import *
from run import global_var

parser_cube = reqparse.RequestParser()
parser_cube.add_argument('brightness', type=int, choices=range(16),
                         required=True)

parser_face = reqparse.RequestParser()
parser_face.add_argument('idx_face', type=int, help='This field cannot be blank', required=True)
parser_face.add_argument('brightness', type=int, help='This field cannot be blank', required=True)

parser_square = reqparse.RequestParser()
parser_square.add_argument('idx_face', type=int, help='This field cannot be blank', required=True)
parser_square.add_argument('idx_square', type=int, help='This field cannot be blank', required=True)
parser_square.add_argument('brightness', type=int, help='This field cannot be blank', required=True)

parser_ledstrip = reqparse.RequestParser()
parser_ledstrip.add_argument('idx_face', type=int, help='This field cannot be blank', required=True)
parser_ledstrip.add_argument('idx_square', type=int, help='This field cannot be blank', required=True)
parser_ledstrip.add_argument('idx_ledstrip', type=int, help='This field cannot be blank', required=True)
parser_ledstrip.add_argument('brightness', type=int, help='This field cannot be blank', required=True)

parser_led = reqparse.RequestParser()
parser_led.add_argument('idx_face', type=int, help='This field cannot be blank', required=True)
parser_led.add_argument('idx_square', type=int, help='This field cannot be blank', required=True)
parser_led.add_argument('idx_ledstrip', type=int, help='This field cannot be blank', required=True)
parser_led.add_argument('idx_led', type=int, help='This field cannot be blank', required=True)
parser_led.add_argument('brightness', type=int, help='This field cannot be blank', required=True)

parser_xyz = reqparse.RequestParser()
parser_xyz.add_argument('idx_x', type=int, help='This field cannot be blank', required=True)
parser_xyz.add_argument('idx_y', type=int, help='This field cannot be blank', required=True)
parser_xyz.add_argument('idx_z', type=int, help='This field cannot be blank', required=True)
parser_xyz.add_argument('brightness', type=int, help='This field cannot be blank', required=True)

parser_xyz_led = reqparse.RequestParser()
parser_xyz_led.add_argument('idx_x', type=int, help='This field cannot be blank', required=True)
parser_xyz_led.add_argument('idx_y', type=int, help='This field cannot be blank', required=True)
parser_xyz_led.add_argument('idx_z', type=int, help='This field cannot be blank', required=True)
parser_xyz_led.add_argument('idx_led', type=int, help='This field cannot be blank', required=True)
parser_xyz_led.add_argument('brightness', type=int, help='This field cannot be blank', required=True)


class XyzResource(Resource):  # xyz

    def post(self):
        data = parser_xyz.parse_args()
        msg = "cube not started"
        if global_var["started"]:
            cube.xyz[data['idx_x']][data['idx_y']][data['idx_z']].show(data['brightness'])
            msg = "request sent"
        return {'message': msg}


class XyzLedResource(Resource):  # xyz

    def post(self):
        data = parser_xyz_led.parse_args()
        msg = "cube not started"
        if global_var["started"]:
            cube.xyz[data['idx_x']][data['idx_y']][data['idx_z']].led[data['idx_led']].show(data['brightness'])
            msg = "request sent"
        return {'message': msg}


class CubeResource(Resource):  # cube

    def post(self):
        data = parser_cube.parse_args()
        msg = "cube not started"
        if global_var["started"]:
            cube.show(data['brightness'])
            msg = "request sent"
        return {'message': msg}


class FaceResource(Resource):  # face

    def post(self):
        data = parser_face.parse_args()
        msg = "cube not started"
        if global_var["started"]:
            cube.faces[data['idx_face']].show(data['brightness'])
            msg = "request sent"
        return {'message': msg}


class SquareResource(Resource):
    def post(self):
        data = parser_square.parse_args()
        msg = "cube not started"
        if global_var["started"]:
            cube.faces[data['idx_face']].squares[data['idx_square']].show(data['brightness'])
            msg = "request sent"
        return {'message': msg}


class LedstripResource(Resource):
    def post(self):
        data = parser_ledstrip.parse_args()
        msg = "cube not started"
        if global_var["started"]:
            cube.faces[data['idx_face']].squares[data['idx_square']].ledstrips[data['idx_ledstrip']].show(
                data['brightness'])
            msg = "request sent"
        return {'message': msg}


class LedResource(Resource):
    def post(self):
        data = parser_led.parse_args()
        msg = "cube not started"
        if global_var["started"]:
            address = cube.faces[data['idx_face']].squares[data['idx_square']].ledstrips[data['idx_ledstrip']].led[
                data['idx_led']]
            if address is not None:
                address.show(data['brightness'])
                msg = "request sent"
            else:
                msg = "error led address"
        return {'message': msg}