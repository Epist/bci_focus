# API

import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from openbci_control import OpenBCIAdapter
# create our little application :)
app = Flask(__name__)
BCI_instance = OpenBCIAdapter()




# Load default config and override config from an environment variable
"""app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)"""


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


def send_distraction():
    return

def send_analytics():
    return


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
    app.run(debug=True)
