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

from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware
from guessitserver import frontend
from guessitserver.config import get_current_environment_config
import logging
log = logging.getLogger(__name__)

settings = get_current_environment_config()
log.critical('** Running in %s mode **'% settings.SERVER_ID)

frontend_app = frontend.create_app(settings=settings)

application = DispatcherMiddleware(frontend_app)


def main():
    print('-'*100)
    print('Registered frontend routes:')
    print(frontend_app.url_map)

    run_simple('0.0.0.0', 5000, application, use_reloader=settings.DEBUG,
               use_debugger=settings.DEBUG)

if __name__ == "__main__":
    main()
