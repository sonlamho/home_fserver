"""
route_fs.py
Blue print for '/fs' route
"""
import os
import time
import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,
    send_from_directory
)
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
from .utils import NAV, PSWD_HASH_PATH, get_config

bp = Blueprint('fs', __name__, url_prefix='/fs')
ALLOW_SECRET = get_config().get('ALLOW_SECRET')
ALLOW_DELETE = get_config().get('ALLOW_DELETE')


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('fs.login'))
        return view(**kwargs)
    return wrapped_view


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        print(request.form)
        with open(PSWD_HASH_PATH, 'r') as f:
            h = f.read()
        if check_password_hash(h, request.form['pswd_hash']):
            session.clear()
            session['logged_in'] = 1
            print(session)
            time.sleep(0.5)
            return redirect(url_for('fs.index'))
        else:
            session.clear()
            flash("Incorrect password!")
    print(session)
    return render_template('login.html')


def handle_upload(relpath: str) -> None:
    print(request.files)
    if 'file' not in request.files:
        flash('No file part')
    f = request.files['file']
    if f.filename == '':
        flash('No selected file')
    if f and f.filename:
        filename = secure_filename(f.filename)
        f.save(os.path.join(NAV.full_path(relpath), filename))


def handle_post(relpath: str) -> None:
    print(request.form)
    if 'upload' in request.form:
        handle_upload(relpath)
    elif 'create_folder' in request.form:
        fname = secure_filename(request.form['new_folder_name'])
        NAV.create_folder(relpath, fname)
    elif 'delete' in request.form and ALLOW_DELETE:
        print(f"Request to delete {request.form['filename']}")
        if 'del-confirm' in request.form:
            msg = NAV.attempt_delete(relpath, request.form['filename'])
            flash(msg)
        else:
            flash("No action taken.")


@bp.route('/', methods=('GET', 'POST'))
@login_required
def index():
    if request.method == 'POST':
        handle_post('')
        return redirect(url_for('fs.index'))
    print(session)
    return render_template('index.html', NAV=NAV, relpath='',
                           ALLOW_SECRET=ALLOW_SECRET,
                           ALLOW_DELETE=ALLOW_DELETE)


@bp.route('/<path:relpath>', methods=('GET', 'POST'))
@login_required
def index_path(relpath):
    if request.method == 'POST':
        handle_post(relpath)
        return redirect(url_for('fs.index_path', relpath=relpath))
    if NAV.is_folder(relpath):
        print(session)
        return render_template('index.html', NAV=NAV, relpath=relpath,
                               ALLOW_SECRET=ALLOW_SECRET,
                               ALLOW_DELETE=ALLOW_DELETE)
    else:
        return send_from_directory(NAV.BASE_DIR, relpath)


@bp.before_app_request
def load_logged_in_user():
    g.user = session.get('logged_in')


@bp.route('/logout')
def logout():
    session.clear()
    print(session)
    return redirect(url_for('fs.index'))
