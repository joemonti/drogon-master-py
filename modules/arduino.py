"""
modules/arduino.py

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

import serial

import drogonmodule

SERIAL_PORT='/dev/ttyAMA0'
SERIAL_BAUD=9600

class ArduinoModule(drogonmodule.DrogonModuleRunnable):
    def __init__(self, *args, **kwargs):
        super(ArduinoModule, self).__init__(*args, **kwargs)
        
        self.logger = self.get_logger()
        self.loggerDebug = self.get_logger('debug')
        self.loggerTuner = self.get_logger('tuner')
    
    def run(self):
        ser = serial.Serial(SERIAL_PORT, SERIAL_BAUD, timeout=1)
        ser.open()
        
        try:
            while True:
                response = ser.readline()
                if response is not None:
                    response = response.strip()
                    if len(response) > 0:
                        if response[0] == 'D':
                            self.loggerDebug.debug(response)
                        elif response[0] == 'P':
                            self.loggerTuner.debug(response)
                        else:
                            self.logger.debug(response)
        except KeyboardInterrupt:
            ser.close()

# THIS EXPOSES THE MODULE CLASS TO THE MODULE LOADER
moduleclass = ArduinoModule

