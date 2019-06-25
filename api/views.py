from run import app, api, global_var
import resources
from flask import jsonify
from package.global_variable.variables import *
from flask import request
from package.sequence.python_seq import ThreadWithTrace
from package.sequence.python_seq import perform as perf

api.add_resource(resources.XyzResource, '/xyz')
api.add_resource(resources.XyzLedResource, '/xyzled')
api.add_resource(resources.CubeResource, '/cube')
api.add_resource(resources.FaceResource, '/face')
api.add_resource(resources.SquareResource, '/square')
api.add_resource(resources.LedstripResource, '/ledstrip')
api.add_resource(resources.LedResource, '/led')
api.add_resource(resources.ChangeMode, '/changemode')
api.add_resource(resources.Token, '/token')

@app.route('/start')
def start():
    msg = "already started"
    if global_var["started"] is not True:
        artnet_group.start(True)
        msg = "started"
        global_var["state"] = "free"
        global_var["started"] = True
    return jsonify({'message': msg})


@app.route('/stop')
def stop():
    global current_thread
    msg = "artnet didnt start"
    if global_var["started"]:
        try:
            artnet_group.stop()
            msg = "stopped"
            global_var["started"] = False
        except AttributeError:
            msg = "artnet didnt start"
        with process_pool.mutex:
            process_pool.queue.clear()
        if current_thread[0] is not None:
            current_thread[0].kill()
            current_thread[0] = None
    cube.blackout_cube()
    return jsonify({'message': msg})


@app.route('/reset')
def reset():
    global current_thread
    with process_pool.mutex:
        process_pool.queue.clear()
    current_thread[0].kill()
    current_thread[0] = None
    return jsonify({'message': 'reset'})


@app.route('/state')
def state():
    return jsonify(global_var)


@app.route('/seq', methods=['POST'])
def seq_python():
    msg = "error, data should be text/plain with utf8 encoding"
    if request.content_type == 'text/plain':
        msg = "request saved"
        prog = request.data.decode('utf-8')
        try:
            process_pool.put(ThreadWithTrace(target=perf, args=(prog,)), block=False)
        except queue.Full:
            msg = "Queue is full"
    return jsonify({'message': msg})


@app.route('/stopseq')
def stop_process():
    current_thread[0].kill()
    return jsonify({'message': 'current sequence stop'})
