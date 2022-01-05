# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 16:41:44 2021

@author: huangao
"""

import socket
import sys
import json
import random
import time
import pymysql

HOST = 'localhost'
PORT = 3306
ADDR = (HOST, PORT)
BUFSIZE = 1024
sensor_id = 1
duration = 1
dtime = 0
db = pymysql.connect(host = "localhost", 
                     user = "root",
                     password =  "root",
                     database =  "test0")

cursor = db.cursor(cursor = pymysql.cursors.DictCursor)


while True:
    humidity = format(random.uniform(50, 70), '.1f')
    temper = format(random.uniform(30, 43), '.1f')
    dust = format(random.uniform(2, 7), '.1f')
    # 包含五个数据 湿度 温度 颗粒物 持续时间 传感器编号
    col = [humidity, temper, dust, dtime, sensor_id]
    data = json.dumps({"a": col, "b": None})
    #dtime=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    dtime = dtime + duration
    sql = """INSERT INTO `data`(humidity, temper, dust, time, sensor_id) values(%s, %s, %s,%s, %s)"""
    try:
        cursor.execute(sql,(humidity, temper, dust, dtime, sensor_id))       
        # 提交到数据库执行
        db.commit()
        time.sleep(10)
    except:
        db.roolback()
        db.close()
