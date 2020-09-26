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
from .utils import NAV, PSWD_HASH_PATH

bp = Blueprint('fs', __name__, url_prefix='/fs')


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
        with open(PSWD_HASH_PATH, 'r') as f:
            h = f.read()
        if check_password_hash(h, request.form['password']):
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
    print(request.form)
    if 'upload' in request.form:
        print(request.files)
        if 'file' not in request.files:
            flash('No file part')
        f = request.files['file']
        if f.filename == '':
            flash('No selected file')
        if f and f.filename:
            filename = secure_filename(f.filename)
            f.save(os.path.join(NAV.full_path(relpath), filename))


@bp.route('/', methods=('GET', 'POST'))
@login_required
def index():
    if request.method == 'POST':
        handle_upload('')
        return redirect(url_for('fs.index'))
    print(session)
    return render_template('index.html', NAV=NAV, relpath='')


@bp.route('/<path:relpath>', methods=('GET', 'POST'))
@login_required
def index_path(relpath):
    if request.method == 'POST':
        handle_upload(relpath)
        return redirect(url_for('fs.index_path', relpath=relpath))
    if NAV.is_folder(relpath):
        return render_template('index.html', NAV=NAV, relpath=relpath)
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
