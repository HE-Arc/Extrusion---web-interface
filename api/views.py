from run import app
from flask_restful import reqparse
from flask import jsonify, request
from package.sequence.interpreter import perform
from package.sequence.sequence_launcher import Launcher
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
    global access
    artnet_group.start(True)
    access = True
    return jsonify({'message': 'start'})


@app.route('/stop')
def stop():
    global access
    artnet_group.stop()
    cube.blackout_cube()
    access = False
    return jsonify({'message': 'stop'})


@app.route('/reset')
def reset():
    global access
    artnet_group.stop()
    access = False
    launcher_pool.clear()
    return jsonify({'message': 'stop'})


@app.route('/seq', methods=['POST'])
def seq():
    prog = request.data.decode('utf-8')
    orders = perform(prog)
    Launcher(orders).start()
    out = ""
    for p in orders:
        out += str(p) + "<br>"

    return out
