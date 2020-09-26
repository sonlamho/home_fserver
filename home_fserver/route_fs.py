"""
route_datachecks.py
Blue print for '/datachecks' route
"""
import os
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,
    send_from_directory
)
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from .utils import NAV

bp = Blueprint('fs', __name__, url_prefix='/fs')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        pass
    return 'fs.login under construction'


@bp.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        pass
    return render_template('index.html', NAV=NAV, relpath='')


@bp.route('/<path:relpath>', methods=('GET', 'POST'))
def index_path(relpath):
    if request.method == 'POST':
        pass
    if NAV.is_folder(relpath):
        return render_template('index.html', NAV=NAV, relpath=relpath)
    else:
        return send_from_directory(NAV.BASE_DIR, relpath)
