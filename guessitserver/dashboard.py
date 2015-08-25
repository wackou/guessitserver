#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# GuessItServer - Providing http access points to GuessIt
# Copyright (c) 2014 Nicolas Wack <wackou@gmail.com>
#
# GuessItServer is free software; you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# GuessItServer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from collections import defaultdict
import json
import datetime
import logging

from flask import Blueprint, render_template, request, redirect, current_app, send_from_directory
from guessitserver.core import db, crossdomain
from guessitserver.models import Submission
import guessit
import babelfish

log = logging.getLogger(__name__)

bp = Blueprint('web', __name__, static_folder='static', template_folder='templates')


def guessit_to_json(o):
    if isinstance(o, (guessit.Language, babelfish.Language, babelfish.Country)):
        return str(o)
    raise TypeError(repr(o) + ' is not JSON serializable')


def jsonify(o):
    return current_app.response_class(json.dumps(o, default=guessit_to_json),
                                      mimetype='application/json')

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


def parse_opt(v):
    # parse a boolean
    if v.lower() in {'true', 'yes'}:
        return True
    if v.lower() in {'false', 'no'}:
        return False

    # parse an int
    try:
        return int(v)
    except ValueError:
        pass
    # TODO: parse list of objects

    return v


def parse_options_dict(d):
    return {k: parse_opt(v) for k, v in d.items()}


@bp.route('/guess', methods=['POST'])
@crossdomain(origin='*')
def guess_file_info_post():
    """
    @api {post} /guess Detect properties for a given filename
    @apiName GuessFileInfoPost
    @apiGroup Guess

    @apiParam {String} filename Filename out of which to guess information.

    @apiParam {String} * Other fields you pass will be forwarded as options to the guesser.

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

    args = parse_options_dict(request.form)
    filename = args.pop('filename')
    filetype = args.pop('type', None)
    options = args

    log.info('[POST] Guess request: %s  --  options: %s' % (filename, options))

    # TODO: store request in DB
    # TODO: if exception, store in list of bugs
    g = guessit.guess_file_info(filename, type=filetype, options=options)

    return jsonify(g)


@bp.route('/guess', methods=['GET'])
@crossdomain(origin='*')
def guess_file_info_get():
    """
    @api {get} /guess Detect properties for a given filename
    @apiName GuessFileInfoGet
    @apiGroup Guess

    @apiParam {String} filename Filename out of which to guess information.

    @apiParam {String} * Other fields you pass will be forwarded as options to the guesser.

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
    args = parse_options_dict(request.args)
    filename = args.pop('filename')
    filetype = args.pop('type', None)
    options = args

    log.info('[GET] Guess request: %s  --  options: %s' % (filename, options))


    # TODO: store request in DB
    # TODO: if exception, store in list of bugs
    g = guessit.guess_file_info(filename, type=filetype, options=options)

    return jsonify(g)


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
    return jsonify({'version': guessit.__version__})
