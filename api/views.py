from run import app, api, global_var
import resources
from flask import jsonify
from package.global_variable.variables import *
from flask import request
from package.sequence.laucher_with_prog import Launcher as L1
from package.sequence.sequence_launcher import Launcher as L2
from package.sequence.python_seq import ThreadWithTrace
from package.sequence.python_seq import perform as perf
from package.sequence.interpreter import perform

api.add_resource(resources.XyzResource, '/xyz')
api.add_resource(resources.XyzLedResource, '/xyzled')
api.add_resource(resources.CubeResource, '/cube')
api.add_resource(resources.FaceResource, '/face')
api.add_resource(resources.SquareResource, '/square')
api.add_resource(resources.LedstripResource, '/ledstrip')
api.add_resource(resources.LedResource, '/led')

current_thread = None


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


@app.route('/seq', methods=['POST'])
def seq():
    out = "nothing"
    prog = request.data.decode('utf-8')
    if global_var["state"] == "free" and global_var["mode"] == "user":
        launcher_pool.append(L1(prog))
        global_var["state"] = "busy"
        current_thread = launcher_pool.pop(0).start()
        out = "Launch"

    return out


@app.route('/seq2', methods=['POST'])
def seq2():
    orders = []
    prog = request.data.decode('utf-8')
    if global_var["state"] == "free" and global_var["mode"] == "user":
        orders = perform(prog)
        launcher_pool.append(L2(orders))
        global_var["state"] = "busy"
        launcher_pool.pop(0).start()
    out = "busy"
    for p in orders:
        out += str(p) + "<br>"

    return out


@app.route('/seqpython', methods=['POST'])
def seq_python():
    global current_thread
    out = "nothing"
    prog = request.data.decode('utf-8')
    if global_var["state"] == "free" and global_var["mode"] == "user":
        out = "Launch"
        process_pool.append(ThreadWithTrace(target=perf, args=(prog,)))
        current_thread = process_pool.pop(0)
        current_thread.start()
    return out


@app.route('/stopprocess')
def stop_process():
    global current_thread
    current_thread.kill()
    cube.blackout_cube()
    return "ok"
