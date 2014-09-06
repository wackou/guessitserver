# -*- coding: utf-8 -*-
"""
    overholt.users.models
    ~~~~~~~~~~~~~~~~~~~~~

    User models
"""

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
