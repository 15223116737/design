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
sensor_id = 2
duration = 1

db = pymysql.connect(host = "localhost", 
                     user = "root",
                     password =  "root",
                     database =  "test0")

cursor = db.cursor(cursor = pymysql.cursors.DictCursor)

dtime = 0
while True:
    humidity = format(random.uniform(50, 70), '.1f')  #湿度
    temper = format(random.uniform(30, 43), '.1f')    #温度
    dust = format(random.uniform(2, 7), '.1f')        #颗粒物浓度
    col = [humidity, temper, dust, dtime, sensor_id]
    data = json.dumps({"a": col, "b": None})
    dtime = dtime + duration
    #dtime=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())      
    #sql1 = """INSERT INTO `dusthistory`(worker_id, dust_sum,time) values(%s, %s, %s)"""
    sql = """INSERT INTO `data`(humidity, temper, dust, time, sensor_id) values(%s, %s, %s,%s, %s)"""
    try:
        cursor.execute(sql,(humidity, temper, dust, dtime, sensor_id))       
        # 提交到数据库执行
        db.commit()
        time.sleep(10)
    except:
        db.roolback()
        db.close()
    


