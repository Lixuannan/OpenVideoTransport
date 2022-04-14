"""Client"""

import socket
import struct
import threading

import cv2
import numpy
import asyncio
from concurrent.futures import ProcessPoolExecutor
executor = ProcessPoolExecutor(1)



class Camera_Connect_Object:
    def __init__(self, D_addr_port=["", 8880]):
        self.executor = ProcessPoolExecutor(1)
        self.resolution = [1920, 1080]
        self.addr_port = D_addr_port
        self.src = 888 + 15
        self.interval = 0
        self.img_fps = 15

    def Set_socket(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def Socket_Connect(self):
        self.Set_socket()
        self.client.connect(self.addr_port)
        print("IP is %s:%d" % (self.addr_port[0], self.addr_port[1]))

    def RT_Image(self):
        self.name = self.addr_port[0] + " Camera"
        self.client.send(struct.pack("lhh", self.src, self.resolution[0], self.resolution[1]))
        while (1):
            info = struct.unpack("lhh", self.client.recv(12))
            buf_size = info[0]
            if buf_size:
                try:
                    self.buf = b""
                    temp_buf = self.buf
                    while (buf_size):
                        temp_buf = self.client.recv(buf_size)
                        buf_size -= len(temp_buf)
                        self.buf += temp_buf
                        data = numpy.frombuffer(self.buf, dtype='uint8')
                        self.image = cv2.imdecode(data, 1)
                        cv2.imshow(self.name, self.image)
                except:
                    pass;
                finally:
                    if (cv2.waitKey(10) == 27):
                        self.client.close()
                        cv2.destroyAllWindows()
                        break


if __name__ == '__main__':
    camera = Camera_Connect_Object()
    camera.addr_port[0] = "localhost"
    camera.addr_port = tuple(camera.addr_port)
    camera.Socket_Connect()
    camera.RT_Image()
