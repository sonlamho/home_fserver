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
    return render_template('index.html', NAV=NAV, path='')


@bp.route('/<path:fpath>', methods=('GET', 'POST'))
def index_path(fpath):
    if request.method == 'POST':
        pass
    return render_template('index.html', NAV=NAV, path=fpath)
