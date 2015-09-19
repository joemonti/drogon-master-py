
import ConfigParser as configparser

import os.path

CONF_FNAME = 'drogon.cfg'


class DrogonConfigParser(object):
    def __init__(self, baseDir):
        self.cp = configparser.ConfigParser()

        conffile = os.path.join(baseDir, CONF_FNAME)

        self.cp.read([conffile])

    def get_config(self, name):
        return DrogonConfig(self.cp, name)


class DrogonConfig(object):
    def __init__(self, cp, name):
        self.cp = cp
        self.name = name

    def get(self, option):
        return self.cp.get(self.name, option)

    def getint(self, option):
        return self.cp.getint(self.name, option)

    def getfloat(self, option):
        return self.cp.getfloat(self.name, option)

    def getboolean(self, option):
        return self.cp.getboolean(self.name, option)

    def items(self):
        return self.cp.items(self.name)
