"""
modules/dummy.py

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

import drogonmodule

class DummyModule(drogonmodule.DrogonModule):
    def __init__(self, *args, **kwargs):
        super(DummyModule, self).__init__(*args, **kwargs)
        self.logger = self.get_logger()
        self.logger.debug("Dummy Module Loaded")

# THIS EXPOSES THE MODULE CLASS TO THE MODULE LOADER
moduleclass = DummyModule

