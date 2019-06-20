from run import app
from flask_restful import reqparse
from flask import jsonify, request
from package.sequence.laucher_with_prog import Launcher as L1
from package.sequence.sequence_launcher import Launcher as L2
from package.sequence.interpreter import perform
from package.global_variable.variables import *

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

parser_xyz = reqparse.RequestParser()
parser_xyz.add_argument('idx_x', type=int, help='This field cannot be blank', required=True)
parser_xyz.add_argument('idx_y', type=int, help='This field cannot be blank', required=True)
parser_xyz.add_argument('idx_z', type=int, help='This field cannot be blank', required=True)
parser_xyz.add_argument('brightness', type=int, help='This field cannot be blank', required=True)


@app.route('/xyz', methods=['POST'])
def xyz():
    data = parser_xyz.parse_args()
    msg = "cube not started"
    if started is True:
        cube.show_xyz(data['idx_x'], data['idx_y'], data['idx_z'], data['brightness'])
        msg = "request sent"
    return jsonify({'message': msg})


@app.route('/cube', methods=['POST'])
def cube_page():
    try:
        data = parser_cube.parse_args()
        msg = "cube not started"
        if started is True:
            cube.show(data['brightness'])
            msg = "request sent"
    except:
        msg = 'Brightness is between 0 and 15'
    return jsonify({'message': msg})


@app.route('/face', methods=['POST'])
def face():
    data = parser_face.parse_args()
    msg = "cube not started"
    if started is True:
        cube.faces[data['idx_face']].show(data['brightness'])
        msg = "request sent"
    return jsonify({'message': msg})


@app.route('/square', methods=['POST'])
def square():
    data = parser_square.parse_args()
    msg = "cube not started"
    if started is True:
        cube.faces[data['idx_face']].squares[data['idx_square']].show(data['brightness'])
        msg = "request sent"
    return jsonify({'message': msg})


@app.route('/ledstrip', methods=['POST'])
def ledstrip():
    data = parser_ledstrip.parse_args()
    msg = "cube not started"
    if started is True:
        cube.faces[data['idx_face']].squares[data['idx_square']].ledstrips[data['idx_ledstrip']].show(
            data['brightness'])
        msg = "request sent"
    return jsonify({'message': msg})


@app.route('/start')
def start():
    global access, state, started
    msg = "already started"
    if started is not True:
        artnet_group.start(True)
        msg = "start"
        state = "free"
        started = True
    return jsonify({'message': msg})


@app.route('/stop')
def stop():
    global access, state, started
    msg = "artnet didnt start"
    if started:
        try:
            artnet_group.stop()
            msg = "stop"
            started = False
        except AttributeError:
            msg = "artnet didnt start"
        for k in launcher_access.keys():
            launcher_access[k] = False
    cube.blackout_cube()
    return jsonify({'message': msg})


@app.route('/reset')
def reset():
    global state
    state = "free"
    for k in launcher_access.keys():
        launcher_access[k] = False
    launcher_pool.clear()
    launcher_access.clear()
    cube.blackout_cube()
    return jsonify({'message': 'reset'})


@app.route('/seq', methods=['POST'])
def seq():
    global state
    out = "nothing"
    prog = request.data.decode('utf-8')
    if state == "free" and mode == "user":
        launcher_pool.append(L1(prog))
        state = "busy"
        launcher_pool.pop(0).start()
        out = "Launch"

    return out


@app.route('/seq2', methods=['POST'])
def seq2():
    global state
    orders = []
    prog = request.data.decode('utf-8')
    if state == "free" and mode == "user":
        orders = perform(prog)
        launcher_pool.append(L2(orders))
        state = "busy"
        launcher_pool.pop(0).start()
    out = "busy"
    for p in orders:
        out += str(p) + "<br>"

    return out
