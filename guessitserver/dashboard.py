from collections import defaultdict
import json
import datetime
import logging

from flask import Blueprint, render_template, redirect, url_for, abort, \
    request, send_from_directory, flash, current_app
from guessitserver.core import db
from guessitserver.models import Submission
import guessit

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
    subs = Submission.query.all()

    def guess_popover(filename):
        g = guessit.guess_video_info(filename)
        return ', '.join('%s: <b>%s</b>' % (k, v) for k, v in g.items())

    subs = [(sub, guess_popover(sub.filename)) for sub in subs]
    return render_template('buglist.html',
                           title='Guessit bugs',
                           fields=['filename', 'guess', 'submit_date'],
                           submissions=subs,
                           guessitversion=guessit.__version__)




