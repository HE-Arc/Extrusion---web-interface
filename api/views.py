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
api.add_resource(resources.Fps, '/fps')
api.add_resource(resources.Network, '/network')


@app.route('/start')
@jwt_required
@mode_superuser
def start():
    """function for /start

    Start to send ArtNet data

    :return information of request
    """
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
    """function for /stop

    Stop to send ArtNet data

    :return information of request
    """
    stop_cube = False
    try:
        stop_cube = artnet_group.stop()
        if stop_cube:
            msg = "stopped"
            # reset global variables
            global_var["started"] = False
            global_var["mode"] = "direct"
            global_var["sequence"] = False
            # erase all sequence in the queue
            queue_manager.delete_all()
        else:
            msg = "error when stopping"
    except AttributeError:
        msg = "artnet didnt start"
    cube.blackout_cube()
    return jsonify({'message': msg, 'state': stop_cube})


@app.route('/state')
@jwt_required
def state():
    """function for route /state

    give api information

    :return all information of api status
    """
    info = deepcopy(global_var)
    info['nb_seq_in_queue'] = queue_manager.nb_seq_in_queue()
    info['fps'] = artnet_group.get_fps()
    info['net'] = {'ip1': artnet_group.ip1, 'ip2': artnet_group.ip2, 'port1': artnet_group.port1,
                   'port2': artnet_group.port2}
    return jsonify(info)


@app.route('/reset')
@jwt_required
@mode_superuser
def reset():
    """function for /reset

    erase the sequence queue and stop current sequence


    all information of api status
    """
    try:
        queue_manager.delete_all()
        return jsonify({'message': 'reset', 'state': True})
    except:
        return jsonify({'message': 'An error occured', 'state': False})


@app.route('/stopseq')
@jwt_required
@mode_superuser
def stopseq():
    """function for /stopseq

    stop current sequence running on the cube

    all information of api status
    """
    try:
        msg = queue_manager.kill_current_seq()
        return jsonify({'message': msg, 'state': True})
    except:
        return jsonify({'message': 'An error occured', 'state': False})


@app.route('/admin')
def admin():
    """function for /admin

    return the template admin.html if connected user ask it

    :return: template of admin.html
    """
    if session.get('logged_admin', False):
        return render_template('admin.html')
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """function for /login

    create session for user
    if already login go to /admin

    :return: template of login.html
    """
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
    """function for /logout
     disconnect a user
    :return: go to login page
    """
    session.pop('logged_admin', False)
    return redirect(url_for('login'))
