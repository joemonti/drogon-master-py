"""
drogonmodule.py

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

import threading
import rcorelib


class DrogonModule(object):
    def __init__(self, *args, **kwargs):
        self.name = kwargs['name']
        self.dl = kwargs['dl']
        self.masterConfig = kwargs['masterConfig']
        self.config = kwargs['config']

        self.rcore = None
        self.loggers = {}

    def get_logger(self, name=''):
        """Get Logger
            - name   Optional name of logger"""
        loggerName = self.name
        if len(name) > 0:
            loggerName = '%s-%s' % (loggerName, name)

        return self.dl.get_logger(loggerName)

    def init_rcore(self):
        """Get RobotCore client, creating if not yet created"""
        if self.rcore is None:
            host = self.masterConfig.get('rcore_host')
            self.rcore = rcorelib.RCoreClient(host, self.name)

        return self.rcore

    def shutdown(self):
        """"Shutdown module, including RobotCore client if opened"""
        if self.rcore is not None:
            self.rcore.close()
            self.rcore = None


class DrogonModuleRunnable(DrogonModule):
    def __init__(self, *args, **kwargs):
        super(DrogonModuleRunnable, self).__init__(*args, **kwargs)

        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True
        self.running = False

    def start(self):
        self.running = True
        self.thread.start()

    def isAlive(self):
        return self.thread.isAlive()

    def shutdown(self):
        self.running = False

    def run(self):
        pass
