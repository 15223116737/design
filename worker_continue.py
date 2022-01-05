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
import pymysql

HOST = 'localhost'
PORT = 3306
ADDR = (HOST, PORT)
BUFSIZE = 1024
worker_id = 1
dtime = 0
duration = 0
db = pymysql.connect(host = "localhost", 
                     user = "root",
                     password =  "root",
                     database =  "test0")

cursor = db.cursor(cursor = pymysql.cursors.DictCursor)

#写入trajectory表 写入数据location_id, worker_id, time，数据duration待定！！！！！
while True:
    location_id = random.randint(1, 4)
    # 包含四个数据 位置点编号 员工编号 dtime duration
    col = [location_id, worker_id, dtime, duration]
    dtime=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    duration = duration + 1
    sql = """INSERT INTO `trajectory`(location_id, worker_id, time, duration) values(%s, %s, %s, %s)"""
    try:
        cursor.execute(sql,(location_id, worker_id, dtime, duration))       
        # 提交到数据库执行
        db.commit()
        time.sleep(10)
    except:
        db.roolback()
        db.close()
