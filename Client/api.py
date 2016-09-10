import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash

# create our little application :)
app = Flask(__name__, static_folder='Client/static', template_folder='Client/template')

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
def test():
    return render_template('test.html')

@app.route('/start_streaming')
def start_streaming():


@app.route('/stop_streaming')
def stop_streaming():
    stop_logging()


@app.route('/pause_streaming')


pause_logging()


def send_distraction():


def send_analytics():


def start_logging():


def stop_logging():


def pause_logging():


@app.teardown_appcontext
