# -*- coding: utf-8 -*-

# import this module using
# >>> import guessitserver.repl
# to set up a (dummy) flask context to allow you to access the DB

from guessitserver.wsgi import application
ctx = application.app.test_request_context()

from guessitserver.core import db

ctx.push()
