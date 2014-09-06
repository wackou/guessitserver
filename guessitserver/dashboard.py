from collections import defaultdict
import json
import datetime
import logging

from flask import Blueprint, render_template, jsonify, request, redirect
from guessitserver.core import db
from guessitserver.models import Submission
import guessit
import babelfish

log = logging.getLogger(__name__)

bp = Blueprint('web', __name__, static_folder='static', template_folder='templates')


def guessit_to_json(o):
    if isinstance(o, (guessit.Language, babelfish.Language)):
        return o.alpha2
    raise TypeError(repr(o) + ' is not JSON serializable')


@bp.route('/robots.txt')
#@bp.route('/sitemap.xml')
def static_from_root():
    """Allows to serve static files directly from the root url instead of the
    static folder. Files still need to be put inside the static folder."""
    return send_from_directory(bp.static_folder, request.path[1:])

@bp.route('/')
def homepage():
    return redirect('http://guessit.readthedocs.org/')

@bp.route('/bugs', methods=['POST'])
def post_bug_submission():
    """
    @api {post} /bugs Submit new test case / wrong detection
    @apiName SubmitBug
    @apiGroup Submit bug

    @apiParam {String} filename Filename which guessit doesn't analyze correctly.

    @apiSuccess {String} &nbsp The submitted filename.
    """
    filename = request.form['filename']
    log.info('Posting bug submission: %s' % filename)
    s = Submission(filename=filename, submit_date=datetime.datetime.utcnow(),
                   guessit_version=request.form.get('version'),
                   options=request.form.get('options'),
                   active=False, resolved=False)
    db.session.add(s)
    db.session.commit()
    return filename

@bp.route('/bugs')
def view_bugs():
    subs = Submission.query.all()

    def guess_popover(filename):
        try:
            g = guessit.guess_video_info(filename)
            return ', '.join('%s: <b>%s</b>' % (k, v) for k, v in g.items())

        except Exception as e:
            return 'Exception occurred: %s' % e

    subs = [(sub, guess_popover(sub.filename)) for sub in subs]
    return render_template('buglist.html',
                           title='Guessit bugs',
                           fields=['filename', 'guess', 'options', 'guessit_version', 'submit_date'],
                           sort_order='[[ 4, "desc" ], [ 0, "asc" ]]',
                           submissions=subs,
                           guessitversion=guessit.__version__)


@bp.route('/guess', methods=['POST'])
def guess_file_info_post():
    """
    @api {post} /guess Detect properties for a given filename
    @apiName GuessFileInfoPost
    @apiGroup Guess

    @apiParam {String} filename Filename out of which to guess information.

    @apiSuccess {Object} &nbsp Object containing all detected fields.
                               For a list of detected properties see <a href="https://guessit.readthedocs.org/en/latest/#features">here</a>

    @apiSuccessExample Success-Response:
HTTP/1.1 200 OK
{
    "audioChannels": "5.1",
    "audioCodec": "DolbyDigital",
    "container": "mkv",
    "episodeNumber": 3,
    "format": "WEBRip",
    "mimetype": "video/x-matroska",
    "releaseGroup": "NTb",
    "screenSize": "1080p",
    "season": 2,
    "series": "House of Cards",
    "title": "NF",
    "type": "episode",
    "videoCodec": "h264",
    "year": 2013
}
    """
    filename = request.form['filename']
    filetype = request.form.get('type', None)

    log.info('[POST] Guess request: %s' % filename)

    # TODO: store request in DB
    # TODO: if exception, store in list of bugs
    g = guessit.guess_file_info(filename, type=filetype)

    return json.dumps(g, default=guessit_to_json)


@bp.route('/guess', methods=['GET'])
def guess_file_info_get():
    """
    @api {get} /guess Detect properties for a given filename
    @apiName GuessFileInfoGet
    @apiGroup Guess

    @apiParam {String} filename Filename out of which to guess information.

    @apiSuccess {Object} &nbsp Object containing all detected fields.
                               For a list of detected properties see <a href="https://guessit.readthedocs.org/en/latest/#features">here</a>

    @apiExample Example usage:
curl "http://guessit.io/guess?filename=House.of.Cards.2013.S02E03.1080p.NF.WEBRip.DD5.1.x264-NTb.mkv"

    @apiSuccessExample Success-Response:
HTTP/1.1 200 OK
{
    "audioChannels": "5.1",
    "audioCodec": "DolbyDigital",
    "container": "mkv",
    "episodeNumber": 3,
    "format": "WEBRip",
    "mimetype": "video/x-matroska",
    "releaseGroup": "NTb",
    "screenSize": "1080p",
    "season": 2,
    "series": "House of Cards",
    "title": "NF",
    "type": "episode",
    "videoCodec": "h264",
    "year": 2013
}

    """
    filename = request.args['filename']
    filetype = request.args.get('type', None)

    log.info('[GET] Guess request: %s' % filename)

    # TODO: store request in DB
    # TODO: if exception, store in list of bugs
    g = guessit.guess_file_info(filename, type=filetype)

    return json.dumps(g, default=guessit_to_json)


@bp.route('/guessit_version')
def guessit_version():
    """
    @api {get} /guessit_version Return guessit version
    @apiName GuessitVersion
    @apiGroup General

    @apiSuccess {String} version Version of GuessIt used for the detection on the server.

    @apiSuccessExample Success-Response:
    HTTP/1.1 200 OK
    {
        "version": "0.7.1"
    }
    """
    return jsonify(version=guessit.__version__)
