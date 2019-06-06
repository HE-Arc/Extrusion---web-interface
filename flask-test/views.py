from run import app
from flask import jsonify
from flask import request
from package.sequence.interpreter import perform


@app.route('/')
def index():
    return jsonify({'message': 'Hello, World!'})


@app.route('/txt', methods=['POST'])
def api_text():
    prog = request.data.decode('utf-8')
    orders = perform(prog)
    out = ""
    for p in orders:
        out += str(p) + "<br>"

    return out


@app.route('/json', methods=['POST'])
def api_json():
    lol = request.get_json()
    return lol[0]
