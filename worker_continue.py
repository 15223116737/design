# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 16:41:44 2021

@author: huangao
"""

import json
import random
import socket
import sys
import time

HOST = 'localhost'
PORT = 8961
ADDR = (HOST, PORT)
BUFSIZE = 1024
worker_id = 1

dtime = 0
while True:
    sock = socket.socket()
    location_id = random.randint(1, 4)
    duration = 1
    col = [location_id, worker_id, dtime, duration]
    data = json.dumps({"a": None, "b": col})
    dtime = dtime + duration
    try:
        sock.connect(ADDR)
        print('have connected with server')
        if len(data) > 0:
            sock.sendall(data.encode())  # 不要用send()
            recv_data = sock.recv(BUFSIZE)
            print('receive:', recv_data.decode('utf-8'))
            sock.close()
        else:
            sock.close()

    except Exception:
        print('error')
        sock.close()
        sys.exit()
    time.sleep(5)
