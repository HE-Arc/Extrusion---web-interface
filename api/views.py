from run import app
from flask_restful import reqparse
from flask import jsonify

from package.global_variable.variables import *

parser = reqparse.RequestParser()
parser.add_argument('idx_face', type=int, help='This field cannot be blank', required=True)
parser.add_argument('brightness', type=int, help='This field cannot be blank', required=True)


@app.route('/')
def index():
    return jsonify({'message': 'Hello, World!'})


@app.route('/face', methods=['POST'])
def face():
    data = parser.parse_args()
    cube.face[data['idx_face']].show(data['brightness'])
    return jsonify({'message': 'OK'})


@app.route('/start')
def start():
    artnet_group.start(True)
    return jsonify({'message': 'start'})


@app.route('/stop')
def stop():
    artnet_group.stop()
    return jsonify({'message': 'stop'})
