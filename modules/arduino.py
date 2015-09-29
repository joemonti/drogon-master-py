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
import threading
import traceback
import time

import rcorelib.event as revent

import drogonmodule

SERIAL_PORT = '/dev/ttyAMA0'
SERIAL_BAUD = 9600

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
    .add_byte() \
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


class ArduinoModule(drogonmodule.DrogonModuleRunnable):
    def __init__(self, *args, **kwargs):
        super(ArduinoModule, self).__init__(*args, **kwargs)

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

        self.serialLock = threading.RLock()
        self.ser = serial.Serial(SERIAL_PORT, SERIAL_BAUD, timeout=0)
        self.ser.open()

    def update_arm(self, event):
        reader = event.reader()
        value = reader.read_byte()
        self.serialLock.acquire()
        try:
            self.ser.write(b'A%d\n' % value)
            self.ser.flush()
        except:
            self.logger.error("Error reading/writing serial: %s",
                              traceback.format_exc())
        finally:
            self.serialLock.release()

    def update_motor(self, event):
        reader = event.reader()
        value = reader.read_float()
        self.serialLock.acquire()
        try:
            self.ser.write(b'M%f\n' % value)
            self.ser.flush()
        except:
            self.logger.error("Error reading/writing serial: %s",
                              traceback.format_exc())
        finally:
            self.serialLock.release()

    def update_pid(self, event):
        reader = event.reader()
        ptype = read.read_byte()
        kp = reader.read_float()
        ki = reader.read_float()
        kd = reader.read_float()
        self.serialLock.acquire()
        try:
            self.ser.write(b'M%f\n' % value)
            self.ser.flush()
        except:
            self.logger.error("Error reading/writing serial: %s",
                              traceback.format_exc())
        finally:
            self.serialLock.release()

    def run(self):
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

        self.ser.close()

# THIS EXPOSES THE MODULE CLASS TO THE MODULE LOADER
moduleclass = ArduinoModule
