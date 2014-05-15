# -*- coding: utf-8 -*-

from functools import wraps
import logging

from flask import render_template, Flask
from flask_security import login_required

from .core import db
from guessitserver import dashboard


log = logging.getLogger(__name__)



# Jinja filter for dates
def format_datetime(value, fmt='full'):
    if fmt == 'full':
        result = value.strftime('%Y-%m-%d %H:%M:%S')
        tzinfo = value.strftime('%Z')
        if tzinfo:
            result = result + ' ' + tzinfo
        return result
    return value.strftime(fmt)



def create_app(settings_override=None):
    """Returns the GuessitServer dashboard application instance"""

    print('creating Flask app guessitserver')
    app = Flask('guessitserver', instance_relative_config=True)

    app.config.from_object(settings_override)

    db.init_app(app)

    app.register_blueprint(dashboard.bp)

    # Register custom error handlers
    for e in [500, 404]:
        app.errorhandler(e)(handle_error)

    # custom filter for showing dates
    app.jinja_env.filters['datetime'] = format_datetime

    return app


def handle_error(e):
    return render_template('errors/%s.html' % e.code), e.code


def authenticated_route(bp, *args, **kwargs):
    def decorator(f):
        @bp.route(*args, **kwargs)
        @login_required
        @wraps(f)
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)
        return f

    return decorator


