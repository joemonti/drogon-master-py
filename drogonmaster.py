#!/usr/bin/env python
"""
drogonmaster.py

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

# import sys
import time
import importlib

import drogonmodule

import rcorelib

import modules
# from modules import *

from drogonlogger import DrogonLogger
from drogonconfig import DrogonConfigParser


class DrogonModuleManager(object):
    def __init__(self, dl, dcp, masterConfig):
        self.logger = dl.get_logger('module-manager')
        self.dl = dl
        self.dcp = dcp
        self.masterConfig = masterConfig
        self.moduleConfig = dcp.get_config('modules')
        self.modules = {}

    def get_module_list(self):
        return [
            moduleName
            for (moduleName, enabled)
            in self.moduleConfig.items()
            if enabled == 'true']

    def load_module(self, module_name):
        self.logger.debug('Module %s Loading' % (module_name))

        config = self.dcp.get_config(module_name)

        importlib.import_module('modules.%s' % (module_name))
        m = modules.__dict__[module_name] \
            .moduleclass(name=module_name,
                         dl=self.dl,
                         config=config,
                         masterConfig=self.masterConfig)

        if isinstance(m, drogonmodule.DrogonModuleRunnable):
            m.start()

        self.modules[module_name] = m
        self.logger.debug('Module %s Loaded' % (module_name))

    def load_modules(self):
        module_list = self.get_module_list()

        for module_name in module_list:
            self.load_module(module_name)

    def shutdown(self):
        for (name, m) in self.modules.iteritems():
            self.logger.debug('Module %s Shutting Down' % (name))
            m.shutdown()

    def running_modules(self):
        return len([1 for m in self.modules.iteritems()
                    if isinstance(m, drogonmodule.DrogonModuleRunnable) and
                    m.isAlive()])


def main():
    dl = DrogonLogger()

    dcp = DrogonConfigParser()
    masterConfig = dcp.get_config('master')

    mm = DrogonModuleManager(dl, dcp, masterConfig)
    mm.load_modules()

    interrupted = False
    running = True
    interruptTime = None
    while running:
        try:
            if interrupted:
                if (time.time() - interruptTime) > 5.0 or \
                        mm.running_modules() == 0:
                    running = False
                else:
                    time.sleep(0.1)
            else:
                time.sleep(1.0)
        except KeyboardInterrupt:
            print 'Interrupted'
            interrupted = True
            interruptTime = time.time()
            mm.shutdown()
            time.sleep(1)


if __name__ == "__main__":
    main()
