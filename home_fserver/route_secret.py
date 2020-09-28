
import os
from flask import (
    Blueprint, render_template, request,
    send_from_directory
)
from .utils import NAV, get_config

SECRET_PATH = os.urandom(16).hex()
bp = Blueprint('secret', __name__, url_prefix='/' + SECRET_PATH)
ALLOW_SECRET = get_config().get('ALLOW_SECRET')


@bp.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        pass
    return render_template('index.html', NAV=NAV, relpath='',
                           secret=True, ALLOW_SECRET=ALLOW_SECRET)


@bp.route('/<path:relpath>', methods=('GET', 'POST'))
def index_path(relpath):
    if request.method == 'POST':
        pass
    if NAV.is_folder(relpath):
        return render_template('index.html', NAV=NAV, relpath=relpath,
                               secret=True, ALLOW_SECRET=ALLOW_SECRET)
    else:
        return send_from_directory(NAV.BASE_DIR, relpath)
