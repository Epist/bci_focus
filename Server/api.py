# API

import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, send_from_directory
from openbci_control import OpenBCIControl
from flask_socketio import SocketIO, send, emit
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
# static_location=dir_path+"/Client/bin"
static_location = "/Users/Larry/PycharmProjects/bci_focus/Client/bin"
# print(static_location)
app = Flask(__name__, static_folder=static_location)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
BCI_instance = OpenBCIControl()


# Load default config and override config from an environment variable
"""app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)"""

@app.route('/')
def root():
    print("serving static")
    return app.send_static_file('index.html')

@app.route('/<path:path>')
def send_js(path):
    print("path: " + path)
    return send_from_directory(static_location, path)

@app.route('/start_streaming')
def start_streaming():
    print("Starting Stream")
    BCI_instance.start_streaming()

@app.route('/stop_streaming')
def stop_streaming():
    print("Stopping Stream")
    BCI_instance.stop_streaming()
    stop_logging()


@app.route('/pause_streaming')
def pause_streaming():
    print("Pausing Stream")
    if BCI_instance.get_pause_state() == False:
        BCI_instance.pause_streaming()
        pause_logging()
        return ("Paused")
    else:
        return ("Running")


@app.route('/resume_streaming')
def resume_streaming():
    print("Resuming_Stream")
    if BCI_instance.get_pause_state() == True:
        BCI_instance.resume_streaming()
        resume_logging()
        return ("Running")
    else:
        return ("Paused")


def bci_not_connected():
    # Trigger a client side message to the user telling them that the bci is not connected
    socketio.emit('bci_not_connected', {'error_data': 'bci_not_connected'})

# This is a server-originated socket event
def send_distraction():
    socketio.emit('distraction', {'distraction_data': True})


# This is a response to a client request to the server
@socketio.on('/retrieve_analytics')
def send_analytics(json):
    emit('analytics', json)


def start_logging():
    return


def stop_logging():
    return


def pause_logging():
    return


def resume_logging():
    return


""""@app.teardown_appcontext
def teardown():
    return"""


if __name__ == '__main__':
    socketio.run(app, debug=True)
    # app.run(debug=True)
