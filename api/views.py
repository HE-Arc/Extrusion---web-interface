from run import app, api, global_var
import resources
from flask import jsonify, render_template
from package.global_variable.variables import *
from copy import deepcopy

api.add_resource(resources.XyzResource, '/xyz')
api.add_resource(resources.XyzLedResource, '/xyzled')
api.add_resource(resources.CubeResource, '/cube')
api.add_resource(resources.FaceResource, '/face')
api.add_resource(resources.SquareResource, '/square')
api.add_resource(resources.LedstripResource, '/ledstrip')
api.add_resource(resources.LedResource, '/led')
api.add_resource(resources.ChangeMode, '/changemode')
api.add_resource(resources.Token, '/token')
api.add_resource(resources.Sequence, '/seq')
api.add_resource(resources.ChangeSequence, '/changeseq')


@app.route('/start')
def start():
    msg = "already started"
    if global_var["started"] is not True:
        artnet_group.start(True)
        msg = "started"
        global_var["started"] = True
    return jsonify({'message': msg})


@app.route('/stop')
def stop():
    try:
        artnet_group.stop()
        msg = "stopped"
        global_var["started"] = False
        global_var["mode"] = "direct"
        global_var["sequence"] = False
        queue_manager.delete_all()
    except AttributeError:
        msg = "artnet didnt start"
    cube.blackout_cube()
    return jsonify({'message': msg})


@app.route('/state')
def state():
    info = deepcopy(global_var)
    info['nb_seq_in_queue'] = str(queue_manager.get_queue())
    return jsonify(info)


@app.route('/reset')
def reset():
    queue_manager.delete_all()
    return jsonify({'message': 'reset'})


@app.route('/stopseq')
def stopseq():
    msg = queue_manager.kill_current_seq()
    return jsonify({'message': msg})


@app.route('/security')
def tokens():
    return render_template('tokens.html')
