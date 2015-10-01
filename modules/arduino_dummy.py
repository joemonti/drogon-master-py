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

import rcorelib.event as revent

import drogonmodule

EVT_TYPE_ARDUINO_ARM = \
    revent.RCoreEventTypeBuilder('arduino_arm') \
    .add_byte() \
    .build()

EVT_TYPE_ARDUINO_MOTOR = \
    revent.RCoreEventTypeBuilder('arduino_motor') \
    .add_float() \
    .build()

EVT_TYPE_ARDUINO_PID = \
    revent.RCoreEventTypeBuilder('arduino_pid') \
    .add_string() \
    .add_float() \
    .add_float() \
    .add_float() \
    .build()

EVT_TYPE_ARDUINO_LOG = \
    revent.RCoreEventTypeBuilder('arduino_log') \
    .add_int() \
    .add_int() \
    .add_int() \
    .add_float() \
    .add_float() \
    .add_float() \
    .add_float() \
    .add_float() \
    .add_float() \
    .add_float() \
    .add_float() \
    .add_float() \
    .add_float() \
    .add_float() \
    .add_float() \
    .add_float() \
    .add_float() \
    .add_float() \
    .add_float() \
    .build()


class ArduinoDummyModule(drogonmodule.DrogonModuleRunnable):
    def __init__(self, *args, **kwargs):
        super(ArduinoDummyModule, self).__init__(*args, **kwargs)

        self.logger = self.get_logger()
        self.loggerDebug = self.get_logger('debug')
        self.loggerData = self.get_logger('data')
        self.loggerTuner = self.get_logger('tuner')

        self.init_rcore()
        self.rcore.register_event_type(EVT_TYPE_ARDUINO_ARM)
        self.rcore.register_event_type(EVT_TYPE_ARDUINO_MOTOR)
        self.rcore.register_event_type(EVT_TYPE_ARDUINO_PID)
        self.rcore.register_event_type(EVT_TYPE_ARDUINO_LOG)

        self.rcore.register_listener(EVT_TYPE_ARDUINO_ARM.name,
                                     self.update_arm)

        self.rcore.register_listener(EVT_TYPE_ARDUINO_MOTOR.name,
                                     self.update_motor)

        self.rcore.register_listener(EVT_TYPE_ARDUINO_PID.name,
                                     self.update_pid)

    def update_arm(self, event):
        reader = event.reader()
        value = reader.read()
        self.loggerDebug.debug(b'A%d\n' % value)

    def update_pid(self, event):
        reader = event.reader()
        ptype = reader.read()
        kp = reader.read()
        ki = reader.read()
        kd = reader.read()
        self.loggerDebug.debug(b'P\t%s\t%f\t%f\t%f\n' % (ptype, kp, ki, kd))

    def update_motor(self, event):
        reader = event.reader()
        value = reader.read()
        self.loggerDebug.debug(b'M%f\n' % value)

    def run(self):
        # TODO: Generate fake data
        '''
        while self.running:
            self.serialLock.acquire()
            try:
                response = self.ser.readline()
            except:
                self.logger.error("Error reading/writing serial: %s",
                                  traceback.format_exc())
                response = None
            finally:
                self.serialLock.release()

            if response is not None:
                response = response.strip()
                if len(response) > 0:
                    if response[0] == 'D':
                        self.loggerDebug.debug(response)
                    if response[0] == 'L':
                        self.loggerData.debug(response)
                    elif response[0] == 'P':
                        self.loggerTuner.debug(response)
                    else:
                        self.logger.debug(response)
            else:
                time.sleep(0.01)

        '''

# THIS EXPOSES THE MODULE CLASS TO THE MODULE LOADER
moduleclass = ArduinoDummyModule
