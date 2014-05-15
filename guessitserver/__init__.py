# -*- coding: utf-8 -*-
import logging

class SimpleFormatter(logging.Formatter):
    def __init__(self):
        self.fmt = '[%(asctime)s] %(levelname)-8s %(module)s:%(funcName)s -- %(message)s'
        logging.Formatter.__init__(self, self.fmt)

ch = logging.StreamHandler()
ch.setFormatter(SimpleFormatter())

logging.getLogger('guessitserver').addHandler(ch)
logging.getLogger('guessitserver').setLevel(logging.DEBUG)
