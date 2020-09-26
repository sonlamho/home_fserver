"""__init__.py"""
import os
from flask import Flask, url_for, redirect
from flask import request, render_template, send_from_directory
from .utils import get_secret_key_hex, NAV
from .route_fs import handle_upload
from typing import Optional, Mapping


def create_app(test_config: Optional[Mapping] = None) -> Flask:
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import route_fs
    app.register_blueprint(route_fs.bp)
    SECRET_PATH = get_secret_key_hex()
    print(f"SECRET_PATH = {SECRET_PATH}")

    @app.route('/')
    def fs():
        return redirect(url_for('fs.index'))

    @app.route(f'/{SECRET_PATH}/', methods=('GET', 'POST'))
    def secret_index():
        if request.method == 'POST':
            pass
        return render_template('index.html', NAV=NAV, relpath='', secret=True)

    @app.route(f'/{SECRET_PATH}/<path:relpath>', methods=('GET', 'POST'))
    def secret_index_path(relpath):
        if request.method == 'POST':
            pass
        if NAV.is_folder(relpath):
            return render_template('index.html', NAV=NAV, relpath=relpath,
                                   secret=True)
        else:
            return send_from_directory(NAV.BASE_DIR, relpath)

    return app


app = create_app()
