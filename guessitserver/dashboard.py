from collections import defaultdict
import json
import datetime
import logging

from flask import Blueprint, render_template, redirect, url_for, abort, \
    request, send_from_directory, flash, current_app
from guessitserver.core import db
from guessitserver.models import Submission

log = logging.getLogger(__name__)

bp = Blueprint('web', __name__, static_folder='static', template_folder='templates')

@bp.route('/robots.txt')
#@bp.route('/sitemap.xml')
def static_from_root():
    """Allows to serve static files directly from the root url instead of the
    static folder. Files still need to be put inside the static folder."""
    return send_from_directory(bp.static_folder, request.path[1:])

@bp.route('/', methods=['POST'])
def post_bug_submission():
    filename = request.form['filename']
    s = Submission(filename=filename, submit_date=datetime.datetime.utcnow(),
                   active=False, resolved=False)
    db.session.add(s)
    db.session.commit()
    return filename

@bp.route('/')
def view_bugs():
    return render_template('buglist.html',
                           title='Guessit bugs',
                           fields=['filename', 'submit_date'],
                           submissions=Submission.query.all())




