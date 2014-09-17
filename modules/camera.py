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
import socket
import io
import struct

import drogonmodule

SERVER_IP = "0.0.0.0"
SERVER_PORT = 42112

MAX_FPS=5

class CameraModule(drogonmodule.DrogonModuleRunnable):
    def __init__(self, *args, **kwargs):
        super(CameraModule, self).__init__(*args, **kwargs)
        
        self.logger = self.get_logger()
        self.frame_delay = 1/MAX_FPS
    
    def run(self):
        while self.running:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.bind((SERVER_IP, SERVER_PORT))
                s.listen(1)
                conn, addr = s.accept()
                self.logger.debug('Connection Opened: %s' % ( addr ))
                connfile = conn.makefile('wb')
                with picamera.PiCamera() as camera:
                    camera.resolution = (640, 480)
                    camera.brightness = 60
                    camera.contrast = 15
                    camera.start_preview()
                    time.sleep(2)
                    stream = io.BytesIO()
                    lastFrame = time.time()
                    for foo in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
                        connfile.write(struct.pack('<L', stream.tell()))
                        connfile.flush()
                        stream.seek(0)
                        connfile.write(stream.read())
                        connfile.flush()
                        stream.seek(0)
                        stream.truncate()
                        
                        resp = conn.recv(1)
                        if not self.running or resp == None or len(resp) == 0 or ord(resp[0]) == 0x04:
                            break
                        elif ord(resp[0]) != 0x02:
                            self.logger.warn('Invalid response: %s' % ( resp ))
                        
                        sleepTime = self.frame_delay - ( time.time() - lastFrame )
                        if sleepTime > 0.0:
                            time.sleep(sleepTime)
                        lastFrame = time.time()
                
                self.logger.debug('Connection Closed: %s' % ( addr ))
                conn.close()
            except:
                self.logger.exception("Exception in connection")
                time.sleep(5)


# THIS EXPOSES THE MODULE CLASS TO THE MODULE LOADER
moduleclass = CameraModule

