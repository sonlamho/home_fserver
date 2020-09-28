"""__init__.py"""
import os
from flask import Flask, url_for, redirect
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

    ALLOW_SECRET = app.config.get('ALLOW_SECRET')
    print(app.config)

    @app.route('/')
    def fs():
        return redirect(url_for('fs.index'))

    if ALLOW_SECRET:
        from . import route_secret
        app.register_blueprint(route_secret.bp)

    return app


app = create_app()
