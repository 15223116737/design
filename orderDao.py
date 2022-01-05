# 数据持久化  方法名前缀 insert update select delete

## pymysql 用来做数据库操作的
import  pymysql
import time

# 数据持久化  方法名前缀 insert update select delete

## pymysql 用来做数据库操作的
import  pymysql


##显示菜单
def  showB():
    # 打开数据库连接
    db = pymysql.connect(host="", user="root", password="root", database="test0")
    # 使用cursor()方法获取操作游标
    cursor = db.cursor(cursor = pymysql.cursors.DictCursor)
    # SQL 插入语句
    sql = """SELECT * FROM `OrderForm` WHERE `isFinished` = 'Y'"""
    try:
    # 执行sql语句
        cursor.execute(sql)
        data1 = cursor.fetchall()
    ## 把查询的数据填充到person对象是否可以(要循环这个游标进行数据的填充)
    ## 可以将查询的数据填充(组合)到自定义的模型中
    # 提交到数据库执行
        db.commit()
    except:
    # 如果发生错误则回滚
        db.rollback() 
    # 关闭数据库连接
    db.close()
    return data1
    
def  finishO(num):
    # 打开数据库连接
    db = pymysql.connect(host="101.34.48.210", user="root", password="Wangweijie123", database="lyq")
    # 使用cursor()方法获取操作游标 
    cursor = db.cursor(cursor = pymysql.cursors.DictCursor)
    # SQL 插入语句
    ##想OrderForm表中存入信息
    sql = """UPDATE OrderForm SET isFinished='Y'
WHERE orderNum=%d"""%num
    try:
    # 执行sql语句
        cursor.execute(sql)
    # 提交到数据库执行
        db.commit()
    except:
    #如果发生错误则返回特定的内容
        db.roolback()
    # 关闭数据库连接
        db.close()
    return 0

##显示菜单
def  showO():
    # 打开数据库连接
    db = pymysql.connect(host="101.34.48.210", user="root", password="Wangweijie123", database="lyq")
    # 使用cursor()方法获取操作游标
    cursor = db.cursor(cursor = pymysql.cursors.DictCursor)
    # SQL 插入语句
    sql = """SELECT * FROM `OrderForm`"""
    try:
    # 执行sql语句
        cursor.execute(sql)
        data1 = cursor.fetchall()
    ## 把查询的数据填充到person对象是否可以(要循环这个游标进行数据的填充)
    ## 可以将查询的数据填充(组合)到自定义的模型中
    # 提交到数据库执行
        db.commit()
    except:
    # 如果发生错误则回滚
        db.rollback() 
    # SQL 插入语句
    sql = """SELECT * FROM `MenuOrder`"""
    try:
    # 执行sql语句
        cursor.execute(sql)
        data2 = cursor.fetchall()
    ## 把查询的数据填充到person对象是否可以(要循环这个游标进行数据的填充)
    ## 可以将查询的数据填充(组合)到自定义的模型中
    # 提交到数据库执行
        db.commit()
    except:
    # 如果发生错误则回滚
        db.rollback()
    
    sql = """SELECT * FROM `Menu`"""
    try:
    # 执行sql语句
        cursor.execute(sql)
        data3 = cursor.fetchall()
    ## 把查询的数据填充到person对象是否可以(要循环这个游标进行数据的填充)
    ## 可以将查询的数据填充(组合)到自定义的模型中
    # 提交到数据库执行
        db.commit()
    except:
    # 如果发生错误则回滚
        db.rollback() 
   
    # 关闭数据库连接
    db.close()
    return data1,data2,data3

def  order(uname,tid,tp,list,humidity, temper, dust, dtime, sensor_id):
    curtime=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()) 
    # 打开数据库连接
    db = pymysql.connect(host="101.34.48.210", user="root", password="Wangweijie123", database="lyq")
    # 使用cursor()方法获取操作游标 
    cursor = db.cursor(cursor = pymysql.cursors.DictCursor)
    # SQL 插入语句
    ##想OrderForm表中存入信息
    sql = """INSERT INTO `OrderForm`(`dust`,`humidity`,`temper`,`time`,`sensor_id`)
 VALUES
('%f','%f','%f','%s','%d')"""%(dust,humidity,temper,curtime,sensor_id)
    try:
    # 执行sql语句
        cursor.execute(sql)
    # 提交到数据库执行
        db.commit()
    except:
    #如果发生错误则返回特定的内容
        db.roolback()
        db.close()
    ##得到订单号
    sql = """SELECT `orderNum` FROM `OrderForm` ORDER BY `orderNum` desc LIMIT 1"""
    try:
    # 执行sql语句
        cursor.execute(sql)
        data = cursor.fetchall()
    ## 把查询的数据填充到person对象是否可以(要循环这个游标进行数据的填充)
    ## 可以将查询的数据填充(组合)到自定义的模型中
    # 提交到数据库执行
        db.commit()
    except:
    #如果发生错误则返回特定的内容
        db.roolback()
        db.close()
    ##得到厨师数量
    sql = """SELECT `userId` FROM `User` WHERE `groupId`=3"""
    try:
    # 执行sql语句
        cursor.execute(sql)
        d1 = cursor.fetchall()
    ## 把查询的数据填充到person对象是否可以(要循环这个游标进行数据的填充)
    ## 可以将查询的数据填充(组合)到自定义的模型中
    # 提交到数据库执行
        db.commit()
    except:
    #如果发生错误则返回特定的内容
        db.roolback()
        db.close()
    ##将菜品信息，厨师等信息存入MenuOrder表
    for i in range(0,len(list)):
        list1=list[i].split(":")
        sql = """INSERT INTO `MenuOrder`(`dishNum`,`orderNum`,`dishCount`,`chefNum`,`dishDone`) VALUES ('%d','%d','%d','%d','0')"""%(int(list1[0]),data[0]['orderNum'],int(list1[1]),d1[i%len(d1)]['userId']) 
        try:
    # 执行sql语句
            cursor.execute(sql)
    # 提交到数据库执行
            db.commit()
        except:
    #如果发生错误则返回特定的内容
            db.roolback()
    # 关闭数据库连接
            db.close()
    return 0

def deleteOrder(orderId):
     # 打开数据库连接
    db = pymysql.connect(host="101.34.48.210", user="root", password="Wangweijie123", database="lyq")
    # 使用cursor()方法获取操作游标 
    cursor = db.cursor(cursor = pymysql.cursors.DictCursor)
    # SQL 插入语句
    try:
    # 执行sql语句
        sql = """DELETE FROM `OrderForm` WHERE `orderNum`=%d"""%(orderId)
        cursor.execute(sql)
        db.commit()
    except:
    #如果发生错误则返回特定的内容
        db.rollback()
    # 关闭数据库连接
    finally:
          cursor.close
          db.close()