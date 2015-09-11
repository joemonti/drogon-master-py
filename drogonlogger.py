"""
drogonlogger.py

This file is part of Drogon.

Drogon is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Drogon is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Drogon.  If not, see <http://www.gnu.org/licenses/>.

@author: Joseph Monti <joe.monti@gmail.com>
@copyright: 2014 Joseph Monti All Rights Reserved, http://joemonti.org/
"""

import logging

FORMAT = '%(asctime)s %(levelname)-6s %(message)s'

LOGDIR = 'log'


class DrogonLogger(object):
    def __init__(self):
        self.loggers = {}

    def get_logger(self, name):
        if name in self.loggers:
            return self.loggers[name]

        logger = logging.getLogger(name)
        handler = logging.FileHandler('%s/%s.log' % (LOGDIR, name))
        handler.setFormatter(logging.Formatter(FORMAT))
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)

        self.loggers[name] = logger

        return logger
