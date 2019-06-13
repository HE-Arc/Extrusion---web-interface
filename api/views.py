from run import app
from flask_restful import reqparse
from flask import jsonify

from package.global_variable.variables import *

parser_cube = reqparse.RequestParser()
parser_cube.add_argument('brightness', type=int, help='This field cannot be blank', required=True)

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


@app.route('/')
def index():
    return jsonify({'message': 'Hello, World!'})


@app.route('/cube', methods=['POST'])
def cube_page():
    data = parser_cube.parse_args()
    cube.show(data['brightness'])
    return jsonify({'message': 'OK'})


@app.route('/face', methods=['POST'])
def face():
    data = parser_face.parse_args()
    cube.faces[data['idx_face']].show(data['brightness'])
    return jsonify({'message': 'OK'})


@app.route('/square', methods=['POST'])
def square():
    data = parser_square.parse_args()
    cube.faces[data['idx_face']].squares[data['idx_square']].show(data['brightness'])
    return jsonify({'message': 'OK'})


@app.route('/ledstrip', methods=['POST'])
def ledstrip():
    data = parser_ledstrip.parse_args()
    cube.faces[data['idx_face']].squares[data['idx_square']].ledstrips[data['idx_ledstrip']].show(data['brightness'])
    return jsonify({'message': 'OK'})


@app.route('/start')
def start():
    artnet_group.start(True)
    return jsonify({'message': 'start'})


@app.route('/stop')
def stop():
    artnet_group.stop()
    return jsonify({'message': 'stop'})
