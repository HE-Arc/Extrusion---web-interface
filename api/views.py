from run import app, api, global_var
import resources
from flask import jsonify
from package.global_variable.variables import *

api.add_resource(resources.Xyz, '/xyz')
api.add_resource(resources.CubeResource, '/cube')
api.add_resource(resources.FaceResource, '/face')
api.add_resource(resources.SquareResource, '/square')
api.add_resource(resources.LedstripResource, '/ledstrip')
api.add_resource(resources.SeqResource, '/seq')
api.add_resource(resources.Seq2Resource, '/seq2')


@app.route('/start')
def start():
    msg = "already started"
    if global_var["started"] is not True:
        artnet_group.start(True)
        msg = "start"
        global_var["state"] = "free"
        global_var["started"] = True
    return jsonify({'message': msg})


@app.route('/stop')
def stop():
    msg = "artnet didnt start"
    if global_var["started"]:
        try:
            artnet_group.stop()
            msg = "stop"
            global_var["started"] = False
        except AttributeError:
            msg = "artnet didnt start"
        for k in launcher_access.keys():
            launcher_access[k] = False
    cube.blackout_cube()
    return jsonify({'message': msg})


@app.route('/reset')
def reset():
    global_var["state"] = "free"
    for k in launcher_access.keys():
        launcher_access[k] = False
    launcher_pool.clear()
    launcher_access.clear()
    cube.blackout_cube()
    return jsonify({'message': 'reset'})
