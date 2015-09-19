"""
camera.py

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

import time
import picamera
import io
import threading

import rcorelib.event as revent

import drogonmodule

SERVER_IP = "0.0.0.0"
SERVER_PORT = 42112

MAX_FPS = 5

EVT_TYPE_CAMERA_TRIGGER = \
    revent.RCoreEventTypeBuilder('camera_trigger') \
    .build()

EVT_TYPE_CAMERA_IMAGE = \
    revent.RCoreEventTypeBuilder('camera_image') \
    .add_bytea() \
    .build()


class CameraModule(drogonmodule.DrogonModuleRunnable):
    def __init__(self, *args, **kwargs):
        super(CameraModule, self).__init__(*args, **kwargs)

        self.logger = self.get_logger()
        self.trigger_condition = threading.Condition()

        self.init_rcore()
        self.rcore.register_event_type(EVT_TYPE_CAMERA_TRIGGER)
        self.rcore.register_event_type(EVT_TYPE_CAMERA_IMAGE)

        self.rcore.register_listener(EVT_TYPE_CAMERA_TRIGGER.name,
                                     self.trigger)

    def trigger(self):
        self.trigger_condition.acquire()
        self.trigger_condition.notify()
        self.trigger_condition.release()

    def run(self):
        while self.running:
            try:
                self.trigger_condition.acquire()
                self.trigger_condition.wait()
                self.trigger_condition.release()

                with picamera.PiCamera() as camera:
                    camera.resolution = (640, 480)
                    camera.brightness = 60
                    camera.contrast = 15
                    camera.start_preview()
                    time.sleep(2)
                    stream = io.BytesIO()

                    for foo in camera.capture_continuous(stream,
                                                         'jpeg',
                                                         use_video_port=True):
                        image_data = stream.read()
                        e = revent.RCoreEventBuilder(EVT_TYPE_CAMERA_IMAGE) \
                            .add_bytea(image_data) \
                            .build()

                        self.rcore.send(e)

                        stream.seek(0)
                        stream.truncate()

                        self.trigger_condition.acquire()
                        self.trigger_condition.wait()
                        self.trigger_condition.release()
            except:
                self.logger.exception("Exception in connection")
                time.sleep(5)


# THIS EXPOSES THE MODULE CLASS TO THE MODULE LOADER
moduleclass = CameraModule
