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

from .core import db
import logging

log = logging.getLogger(__name__)


class Submission(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    filename = db.Column(db.String(1000), nullable=False)
    submit_date = db.Column(db.DateTime(), nullable=False)
    guessit_version = db.Column(db.String(20))
    options = db.Column(db.String())
    resolved = db.Column(db.Boolean(), nullable=False)
    active = db.Column(db.Boolean(), nullable=False)

    def __repr__(self):
        return '<Filename: %s>' % self.filename
