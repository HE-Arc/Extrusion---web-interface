from run import app, api, global_var
import resources
from flask import jsonify, render_template, session, request, flash, redirect, url_for
from package.global_variable.variables import *
from copy import deepcopy
from flask_jwt_extended import jwt_required
from package.security.decorators import mode_superuser
from passlib.hash import pbkdf2_sha256 as sha256

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
api.add_resource(resources.StartSequence, '/startseq')


@app.route('/start')
@jwt_required
@mode_superuser
def start():
    msg = "already started"
    if global_var["started"] is not True:
        artnet_group.start(True)
        msg = "started"
        global_var["started"] = True
    return jsonify({'message': msg, 'state': True})


@app.route('/stop')
@jwt_required
@mode_superuser
def stop():
    stop_cube = False
    try:
        stop_cube = artnet_group.stop()
        if stop_cube:
            msg = "stopped"
            global_var["started"] = False
            global_var["mode"] = "direct"
            global_var["sequence"] = False
            queue_manager.delete_all()
        else:
            msg = "error when stopping"
    except AttributeError:
        msg = "artnet didnt start"
    cube.blackout_cube()
    return jsonify({'message': msg, 'state': stop_cube})


@app.route('/state')
def state():
    info = deepcopy(global_var)
    info['nb_seq_in_queue'] = queue_manager.nb_seq_in_queue()
    return jsonify(info)


@app.route('/reset')
def reset():
    queue_manager.delete_all()
    return jsonify({'message': 'reset'})


@app.route('/stopseq')
def stopseq():
    msg = queue_manager.kill_current_seq()
    return jsonify({'message': msg})


@app.route('/admin')
def admin():
    if session.get('logged_admin', False):
        return render_template('admin.html')
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if session.get('logged_admin', False):
            return admin()
        else:
            return render_template('login.html')
    if request.method == 'POST':
        if request.form['username'] == app.config['admin_user'] and sha256.verify(request.form['password'],
                                                                                  app.config['admin_pwd']):
            session['logged_admin'] = True
            return redirect(url_for('admin'))
        flash('wrong username or password')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('logged_admin', False)
    return redirect(url_for('login'))
