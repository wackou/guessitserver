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

import logging

class SimpleFormatter(logging.Formatter):
    def __init__(self):
        self.fmt = '[%(asctime)s] %(levelname)-8s %(module)s:%(funcName)s -- %(message)s'
        logging.Formatter.__init__(self, self.fmt)

ch = logging.StreamHandler()
ch.setFormatter(SimpleFormatter())

logging.getLogger('guessitserver').addHandler(ch)
logging.getLogger('guessitserver').setLevel(logging.DEBUG)
