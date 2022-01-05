import sys
import pymysql
import numpy as np
import matplotlib.pyplot as plt
 
plt.rcParams['font.sans-serif']=['SimHei'] #显示中文标签
plt.rcParams['axes.unicode_minus']=False   #这两行需要手动设置

# 1. Import `QApplication` and all the required widgets
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel, QPushButton, QTableWidget, QTableWidgetItem, QLineEdit
from PyQt5.QtWidgets import QWidget, QComboBox, QVBoxLayout, QHBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtCore import QTimer
from matplotlib import patches 


# from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

db = pymysql.connect(host = "localhost", 
                     user = "root",
                     password =  "root",
                     database =  "test0")
cursor = db.cursor()

x_coordinate = [2, 4, 6, 9]  # 监测点横坐标
y_coordinate = [1, 4, 2, 2]  # 监测点纵坐标


def x_coor(i):
    return x_coordinate[i - 1]


def y_coor(i):
    return y_coordinate[i - 1]


def calculate_worker_dust(worker_id):
    dbt = pymysql.connect("localhost", "root", "root", "test0")
    cursort = dbt.cursor()
    # trajectory 轨迹表包含duratioon time location_id worker_id
    # data 数据表包含dust sensor_id
    # 返回轨迹表的持续时间，时间，和数据表的烟尘量 找出数据表和轨迹表时间和位置号与传感器号相同的
    sql = "select trajectory.duration,trajectory.time,data.dust \
    from trajectory inner join data on trajectory.time = data.time \
    and trajectory.location_id = data.sensor_id\
    WHERE worker_id=%s ORDER BY time"
    cursort.execute(sql, worker_id)
    data = cursort.fetchall()
    print("data in calculate:", data)
    dbt.close()
    sum = 0
    dtime = 0
    for row in data:
        sum = sum + row[0] * row[2]
        dtime = row[1]
    return sum, dtime


def establish_workers_dust():
    dbt = pymysql.connect("localhost", "root", "root", "test0")
    cursort = dbt.cursor()
    bar_x = []
    bar_y = []
    # 查询trajectory表中工人个数？
    sql = "SELECT worker_id FROM trajectory GROUP BY worker_id"
    cursort.execute(sql)
    datas = cursort.fetchall()
    print("datas", datas)
    for data in datas:
        print("data[0]", data[0])
        #调用calculate_worker_dust(work_id)计算每个工人的累计受尘量和 时间
        dust_sum, dtime = calculate_worker_dust(int(data[0]))
        bar_x.append(int(data[0]))
        bar_y.append(dust_sum)
        dbt1 = pymysql.connect("localhost", "root", "root", "test0")
        cursort1 = dbt1.cursor()
        #将计算得到的对应worker_id的累计受尘量和dtime插入dusthistory表
        sql1 = """INSERT INTO `dusthistory`(worker_id, dust_sum,time) values(%s, %s, %s)"""
        try:
            cursort1.execute(sql1, (int(data[0]), dust_sum, dtime))
            # 提交到数据库执行
            dbt1.commit()
            dbt1.close()
        except Exception:
            print("数据不需要更新")
            dbt1.close()
    dbt.close()
    # 产生len(bar_y)个100的数组
    bar_ylimit = [100 for i in range(len(bar_y))]
    bar_gap = []
    bar_absgap = []
    for i in range(len(bar_y)):
        bar_gap.append(bar_ylimit[i] - bar_y[i])
    for i in range(len(bar_gap)):
        if bar_gap[i] < 0:
            bar_absgap.append(0)
        else:
            bar_absgap.append(bar_gap[i])
    #matplotlib中的画图函数
    axes4.cla()
    #画对应工人的累计受尘量
    axes4.bar(bar_x, bar_y)
    axes4.bar(bar_x, bar_absgap, bottom=bar_y)
    canvas_bar.draw()


def search_worker_dust(worker_id):
    dbt = pymysql.connect("localhost", "root", "root", "test0")
    cursort = dbt.cursor()
    sql = "SELECT dusthistory.dust_sum FROM dusthistory WHERE worker_id=%s ORDER BY time DESC LIMIT 1"
    cursort.execute(sql, worker_id)
    data = cursort.fetchone()
    # print("搜索到的累积量:",str(data[0]),'mg/m^3')
    dbt.close()
    # dusthistory表的第一表项是dust_sum
    label_dust.setText("搜索到的累积量:" + str(data[0]) + 'mg/m^3')


def plot_worker(worker_id):
    dbt = pymysql.connect("localhost", "root", "root", "test0")
    cursort = dbt.cursor()
    sql_worker = "SELECT * FROM trajectory WHERE worker_id=%s ORDER BY time DESC LIMIT 3"
    cursort.execute(sql_worker, worker_id)
    data = cursort.fetchall()
    dbt.close()
    xnum = []
    ynum = []
    duration = []
    for row in data:
        xnum.append(x_coor(row[0]))
        ynum.append(y_coor(row[0]))
        # trajectory 的第[3]表项为duration
        duration.append(row[3])
    axes3.cla()
    axes3.plot(xnum, ynum)
    #原代码中duration*100
    axes3.scatter(xnum, ynum, marker='o', s=duration, alpha=0.3)
    # 显示图表
    canvas_worker.draw()


def plot_piechart():
    dbt = pymysql.connect("localhost", "root", "root", "test0")
    cursort = dbt.cursor()
    dic = {}
    sql_update = "SELECT * FROM data ORDER BY time DESC LIMIT 2"
    cursort.execute(sql_update)
    data = cursort.fetchall()
    dbt.close()
    # row[0:-1]从第1项截取到倒数第一项（不包含）
    for row in data:
        dic[row[4]] = row[0:-1]
    # rank_dic = sorted(dic.items(), key = lambda kv:kv[1][2])
    axes2.cla()
    print("自动更新piechart:", dic)
    labels = [u'正常', u'超标']
    explode = [0.05, 0]
    num_normal = 0
    num_excede = 0
    for row in dic.items():
        if row[1][2] > 5:
            num_excede = num_excede + 1
        else:
            num_normal = num_normal + 1
    sum_all = num_normal + num_excede
    sizes = [num_normal/sum_all, num_excede/sum_all]
    patches, l_text, p_text = axes2.pie(sizes, explode=explode, labels=labels, normalize=False,
                                        labeldistance=1.1, autopct='%1.1f%%', shadow=False,
                                        startangle=90, pctdistance=0.6)
    # 改变文本的大小
    # 方法是把每一个text遍历。调用set_size方法设置它的属性
    for t in l_text:
        t.set_size = 60
    for t in p_text:
        t.set_size = 60
        # 设置x，y轴刻度一致，这样饼图才能是圆的
    # plt.axis('equal')
    canvas_pie.draw()


def fun1():
    rank_point()
    plot_piechart()
    check_point_history(int(box_plot_dust.currentText()))
    plot_worker(int(box_plot_worker.currentText()))
    selectionchange()
    establish_workers_dust()


def rank_point():
    dbt = pymysql.connect("localhost", "root", "root", "test0")
    cursort = dbt.cursor()
    dic = {}
    sql_update = "SELECT * FROM data ORDER BY time DESC LIMIT 2"
    cursort.execute(sql_update)
    data = cursort.fetchall()
    for row in data:
        dic[row[4]] = row[0:-1]
    rank_dic = sorted(dic.items(), key=lambda kv: kv[1][2])
    print(rank_dic)
    print("自动更新rank:", rank_dic)
    table_rank.setItem(1, 0, QTableWidgetItem(str(rank_dic[0][0])))
    table_rank.setItem(1, 1, QTableWidgetItem(str(rank_dic[0][1][2])))
    table_rank.setItem(2, 0, QTableWidgetItem(str(rank_dic[1][0])))
    table_rank.setItem(2, 1, QTableWidgetItem(str(rank_dic[1][1][2])))
    dbt.close()


def check_point_history(sensor_id):
    dbt = pymysql.connect("localhost", "root", "root", "test0")
    cursort = dbt.cursor()
    sql_check = "SELECT * FROM data WHERE sensor_id=%s ORDER BY time"
    cursort.execute(sql_check, sensor_id)
    data = cursort.fetchall()
    dbt.close()
    xname = []
    ynum = []
    # print(data)
    for row in data:
        xname.append(row[3])
        ynum.append(row[2])

    # 创建一个figure（一个窗口）来显示折线图
    # plt.figure()
    # figure.clear()
    axes1.cla()
    axes1.plot(xname, ynum)
    for x, y in enumerate(ynum):
        axes1.text(x, y, '%s' % y)

    # 显示图表
    canvas.draw()


def selectionchange():
    dbt = pymysql.connect("localhost", "root", "root", "test0")
    cursort = dbt.cursor()
    dic = {}
    sql_update = "SELECT * FROM data ORDER BY time DESC LIMIT 2"
    cursort.execute(sql_update)
    data = cursort.fetchall()
    dbt.close()
    for row in data:
        dic[row[4]] = row[0:-1]
    id = int(box.currentText())
    # print("id:", id)
    # print('dic', dic)
    # print("here", dic[0])
    dust = dic[id][2]
    temper = dic[id][1]
    humidity = dic[id][0]
    dtime = dic[id][3]
    table_point_data.setItem(0, 1, QTableWidgetItem(str(id)))
    table_point_data.setItem(1, 1, QTableWidgetItem(str(dust)))
    table_point_data.setItem(2, 1, QTableWidgetItem(str(temper)))
    table_point_data.setItem(3, 1, QTableWidgetItem(str(humidity)))
    table_point_data.setItem(4, 1, QTableWidgetItem(str(dtime)))

app = QApplication([])

window = QWidget()
window.setWindowTitle('PyQt5 App')
window.setGeometry(50, 50, 1200, 800)  # x,y,width,height
# update_latest_data()

timer = QTimer()
# fun1是监听的函数，如果fun1(x,y)带参，则使用"lambda:fun1(x,y)" 代替下面的“fun1”
timer.timeout.connect(fun1)
timer.start(10000)

box = QComboBox()
box.addItems(['1', '2'])
button_updateRank = QPushButton('更新排名')
table_point_data = QTableWidget()
table_point_data.setRowCount(5)
table_point_data.setColumnCount(2)
table_point_data.setItem(0, 0, QTableWidgetItem("监测点"))
table_point_data.setItem(1, 0, QTableWidgetItem("粉尘"))
table_point_data.setItem(2, 0, QTableWidgetItem("温度"))
table_point_data.setItem(3, 0, QTableWidgetItem("湿度"))
table_point_data.setItem(4, 0, QTableWidgetItem("时间"))
label = QLabel('监测点')
label.setStyleSheet('''QLabel{color:darkGray;background:white;border:2px solid #F3F3F5;border-radius:45px;
                font-size:14pt; font-weight:400;font-family: Roman times;} ''')

# 排行表格
table_rank = QTableWidget()
table_rank.setRowCount(3)
table_rank.setColumnCount(2)
table_rank.setItem(0, 0, QTableWidgetItem("监测点"))
table_rank.setItem(0, 1, QTableWidgetItem("粉尘"))
label44 = QLabel('实时质量排行')
label44.setAlignment(Qt.AlignCenter)

# 折线数据图
labelp = QLabel("粉尘趋势图")
labelp.setAlignment(Qt.AlignCenter)
labelp2 = QLabel("监测点选择")
labelp.setStyleSheet('''QLabel{font-size:20px;font-family:Roman times;}''')
labelp2.setStyleSheet('''QLabel{font-size:20px;font-family:Roman times;}''')
box_plot_dust = QComboBox()
box_plot_dust.addItems(['1', '2'])
figure = plt.figure(1)
axes1 = figure.add_subplot(111)
canvas = FigureCanvas(figure)
check_point_history(1)
# 概况饼图
figure_pie = plt.figure(2)
axes2 = figure_pie.add_subplot(111)
plt.rcParams['font.sans-serif'] = ['SimHei']
canvas_pie = FigureCanvas(figure_pie)
plot_piechart()

# 工人轨迹图
labelw = QLabel("工人轨迹图")
labelw.setAlignment(Qt.AlignCenter)
labelw2 = QLabel("工人选择")
labelw.setStyleSheet('''QLabel{font-size:20px;font-family:Roman times;}''')
labelw2.setStyleSheet('''QLabel{font-size:20px;font-family:Roman times;}''')
box_plot_worker = QComboBox()
box_plot_worker.addItems(['1', '2'])
figure_worker = plt.figure(3)
axes3 = figure_worker.add_subplot(111)
canvas_worker = FigureCanvas(figure_worker)
plot_worker(1)

# 累积接尘量搜索
searchLab = QLineEdit()
searchLab.setPlaceholderText('请输入需要查询的工人ID')
searchButton = QPushButton('点击查询')
label_dust = QLabel('工人接尘量')

# 累计接尘量柱状图
figure_bar = plt.figure(4)
axes4 = figure_bar.add_subplot(111)
canvas_bar = FigureCanvas(figure_bar)

# 右侧布局
RLayout = QVBoxLayout()
RLayout.addWidget(label)
RLayout.addWidget(box)
RLayout.addWidget(table_point_data)
RLayout.addWidget(label44)
RLayout.addWidget(button_updateRank)
RLayout.addWidget(table_rank)

# 中间布局
MLayout = QVBoxLayout()
MLayout.addWidget(canvas)
MLayout.addWidget(labelp)
MLayout.addWidget(labelp2)
MLayout.addWidget(box_plot_dust, 0, Qt.AlignLeft)
MLayout.addWidget(canvas_worker)
MLayout.addWidget(labelw)
MLayout.addWidget(labelw2)
MLayout.addWidget(box_plot_worker, 0, Qt.AlignLeft)
MLayout.addStretch(1)

# 左侧布局
LLayout = QVBoxLayout()
LLayout.addWidget(canvas_pie)
LLayout.addWidget(searchLab)
LLayout.addWidget(searchButton)
LLayout.addWidget(label_dust)
LLayout.addWidget(canvas_bar)
LLayout.addStretch(1)

# 总布局
HLayout = QHBoxLayout()
HLayout.addLayout(LLayout)
HLayout.addLayout(MLayout, 10)
HLayout.addLayout(RLayout)

# slot connect
box.currentIndexChanged.connect(selectionchange)
button_updateRank.clicked.connect(rank_point)
box_plot_dust.currentIndexChanged.connect(lambda: check_point_history(int(box_plot_dust.currentText())))
box_plot_worker.currentIndexChanged.connect(lambda: plot_worker(int(box_plot_worker.currentText())))
searchButton.clicked.connect(lambda: search_worker_dust(int(searchLab.text())))

window.setLayout(HLayout)
# 4. Show your application's GUI
window.setWindowOpacity(0.9)
# window.setWindowFlag(QtCore.Qt.FramelessWindowHint)
pe = QPalette()
window.setAutoFillBackground(True)
pe.setColor(QPalette.Window, Qt.lightGray)  # 设置背景色
# pe.setColor(QPalette.Background,Qt.blue)
window.setPalette(pe)
window.show()

# 5. Run your application's event loop (or main loop)
fun1()
sys.exit(app.exec_())

