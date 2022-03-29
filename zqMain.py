# AmberHan
# !/usr/bin/env python
# !-*- coding:utf-8 -*-
# !@Time   : 2021/4/26 10:57
# !@File   : zqMain.py
#GUI主程序
#如果各模块在同一台电脑运行,可用多进程通信,否则可用数据库共享数据

import random
from tkinter import *
from tkinter import ttk
import time
import numpy as np
import multiprocessing
from tkinter import messagebox

# import zqFacial
import zqAudio
import zqOperationData
import zqConfig as config
import zqLib
import zqMySQLdb
import zqDecisionTree


LOG_LINE_NUM = 0


#用户界面
class MY_GUI():

    def __init__(self, init_window_name, gManager):
        self.init_window_name = init_window_name
        self.itag = 0
        self.qQueue = gManager.Queue()
        self.qQueueAudio = gManager.Queue()
        self.qQueueOperationData = gManager.Queue()

        self.gDict = gManager.dict()
        self.gDict['run'] = True
        self.clearList()

    #表格组件
    def myTree(self,
               headings,     #表头
               irow,         #在窗体中位置 行
               icolumn,      #在窗体中位置 列
               irowspan,     #在窗体中位置 跨行
               icolumnspan   #在窗体中位置 跨列
               ):

        iColumnCount = len(headings)
        if iColumnCount == 10:  #total_data
            mytree = ttk.Treeview(self.init_window_name,
                                  columns=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11'],
                                  show='headings')
            for i in range(1,iColumnCount+1):
                id=str(i)
                if i==1:
                    mytree.column(id, width=138, anchor='center')
                else:
                    mytree.column(id, width=100, anchor='center')

                mytree.heading(id, text=headings[i-1])
        elif iColumnCount == 3:
            mytree = ttk.Treeview(self.init_window_name, columns=['1', '2', '3'], show='headings')

            for i in range(1, iColumnCount+1):
                id = str(i)
                mytree.column(id, width=100, anchor='center')
                mytree.heading(id, text=headings[i - 1])

        elif iColumnCount == 1:
            mytree = ttk.Treeview(self.init_window_name, columns=['1'], show='headings')
            mytree.column('1', width=100, anchor='center')
            mytree.heading('1', text=headings[0])

        else:
            return None

        mytree.grid(row=irow, column=icolumn, rowspan=irowspan, columnspan=icolumnspan, sticky="NSEW")
        myvbar = ttk.Scrollbar(self.init_window_name, orient="vertical", command=mytree.yview)
        mytree.configure(yscrollcommand=myvbar.set)
        myvbar.grid(row=irow, column=icolumn + icolumnspan, rowspan=irowspan, sticky="NS")
        return mytree

    # 设置窗口
    def set_init_window(self):
        self.init_window_name.title("Intelligent Platform for Fleet Operations v1.0, 2021, ASTRI, Zhiqiang Li")  # 窗口名

        # 设置窗口大小
        winWidth = 1238
        winHeight = 691

        screenWidth = self.init_window_name.winfo_screenwidth()
        screenHeight = self.init_window_name.winfo_screenheight()

        x = int((screenWidth - winWidth) / 2)
        y = int((screenHeight - winHeight) / 2)

        # 设置窗口初始位置在屏幕居中
        self.init_window_name.geometry("%sx%s+%s+%s" % (winWidth, winHeight, x, y))

        # self.init_window_name.iconbitmap("./astri.png")
        # self.init_window_name.resizable(0, 0)
        # self.init_window_name.geometry('1068x681+10+10')

        # self.init_window_name["bg"] = "pink"
        # #窗口背景色，其他背景色见：blog.csdn.net/chl0000/article/details/7657887
        # self.init_window_name.attributes("-alpha",0.9)
        # #虚化，值越小虚化程度越高

        self.init_data_label = Label(self.init_window_name, text="  ")
        self.init_data_label.grid(row=0, column=0)

        # 按钮
        self.run_button = Button(self.init_window_name, text="Run", bg="lightblue", width=10,
                                 command=self.simulate)  # 调用内部方法  加()为直接调用
        self.run_button.grid(row=1, column=1)

        self.init_data_label = Label(self.init_window_name, text="")
        self.init_data_label.grid(row=2, column=0)
        # 标签
        self.init_data_label = Label(self.init_window_name, text="Vehicle operation(speeding,sharp turn,abnormal)")
        self.init_data_label.grid(row=3, column=1, columnspan=2)

        self.result_data_label = Label(self.init_window_name, text="Facial(distracted,yawn,blink)")
        self.result_data_label.grid(row=3, column=8, columnspan=1)

        self.result_data_label = Label(self.init_window_name, text="Vocal(Abnormal)")
        self.result_data_label.grid(row=3, column=15, columnspan=1)

        self.treeVehicle = self.myTree(
            ['speeding', 'sharp turn', 'abnormal'],
            irow=4, icolumn=1, irowspan=6, icolumnspan=5)

        self.init_data_label = Label(self.init_window_name, text="  ")
        self.init_data_label.grid(row=4, column=7)

        self.treeFacial = self.myTree(
            ['distracted', 'yawn', 'blink'],
            irow=4, icolumn=8, irowspan=6, icolumnspan=5)

        self.init_data_label = Label(self.init_window_name, text="  ")
        self.init_data_label.grid(row=4, column=14)

        self.treeVocal = self.myTree(
            ['Abnormal'],
            irow=4, icolumn=15, irowspan=6, icolumnspan=6)

        self.init_data_label = Label(self.init_window_name, text="  ")
        self.init_data_label.grid(row=11, column=1)

        self.log_label = Label(self.init_window_name, text="Result")
        self.log_label.grid(row=12, column=1)
        # self.textResult = Text(self.init_window_name, width=143, height=10)  # 日志框
        # self.textResult.grid(row=13, column=1, columnspan=20)
        self.treeRisk = self.myTree(
            ['time', 'speeding', 'sharp turn', 'Vehicle abnormal', 'distracted',
             'yawn', 'blink', 'VocalAbnormal', 'dtPredict', 'manualPredict'
            ],
            irow=13, icolumn=1, irowspan=6, icolumnspan=20)

        # self.init_data_label = Label(self.init_window_name, text="  ")
        # self.init_data_label.grid(row=14, column=0)

    def clearList(self):
        pass

    def clearData(self):
        self.clearList()
        self.delButton(self.treeVehicle)
        self.delButton(self.treeFacial)
        self.delButton(self.treeVocal)

    def funcIntegrator(self): #集成
        self.clearData()     #清空三个表格
        ret=zqMySQLdb.sp_mysql_proc_total_data()
        for rs in ret[0]:
            self.treeVocal.insert('', 'end', values=rs[2:3])

        for rs in ret[1]:
            self.treeFacial.insert('', 'end', values=(rs[2],rs[4],rs[5]))

        for rs in ret[2]:
            self.treeVehicle.insert('', 'end', values=rs[2:5])


        for rs in ret[3]:
            # rs is tuple, can't be changed
            ret= zqDecisionTree.riskMode(
                [ float(rs[2]), float(rs[3]), float(rs[4])],
                [float(rs[5]), float(rs[6]), float(rs[7])],
                [float(rs[8])]
            )
            ret2=''
            self.treeRisk.insert('', 0, values=(rs[1:9]+(ret,ret2)))
            # print(ret)

        #显示在表格中

    def simulate(self):
        if self.itag == 1:
            self.itag = 2
            self.run_button['text'] = 'Run'
            self.gDict['run'] = False
        else:
            self.gDict['run'] = True

            p1 = multiprocessing.Process(target=zqFacial.gfuncFacial, args=(self.qQueue, self.gDict))
            if not p1.is_alive():
                p1.start()

            p2 = multiprocessing.Process(target=zqAudio.gfuncVocal, args=(self.qQueueAudio, self.gDict))
            if not p2.is_alive():
                p2.start()

            p3 = multiprocessing.Process(target=zqOperationData.gfuncVehicle, args=(self.qQueueOperationData, self.gDict))
            if not p3.is_alive():
                p3.start()

            zqLib.zqFunTimerEnd(config.INTERVALRisk, self.gDict, self.funcIntegrator)

            if self.itag == 0:
                pass
            else:
                self.clearData()
            self.itag = 1

            self.run_button['text'] = 'Stop'

    # 获取当前时间
    def get_current_time(self):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        return current_time

    # 日志动态打印
    def write_log_to_Text(self, logmsg):
        global LOG_LINE_NUM
        current_time = self.get_current_time()
        logmsg_in = str(current_time) + " " + str(logmsg) + "\n"  # 换行
        if LOG_LINE_NUM <= 7:
            self.log_data_Text.insert(END, logmsg_in)
            LOG_LINE_NUM = LOG_LINE_NUM + 1
        else:
            self.log_data_Text.delete(1.0, 2.0)
            self.log_data_Text.insert(END, logmsg_in)

    def delButton(self, tree):  # 清空列表
        x = tree.get_children()
        for item in x:
            tree.delete(item)


ZMJ_PORTAL = None


def gui_start():
    global ZMJ_PORTAL
    init_window = Tk()  # 实例化出一个父窗口
    gManager = multiprocessing.Manager()
    ZMJ_PORTAL = MY_GUI(init_window,gManager)
    # 设置根窗口默认属性
    ZMJ_PORTAL.set_init_window()

    # p1 = multiprocessing.Process(target=GUICV.GUICV, args= (changetitle, ))
    # p1 = multiprocessing.Process(target=main1, args=(ZMJ_PORTAL.qQueue, ZMJ_PORTAL.gDict))
    init_window.protocol("WM_DELETE_WINDOW", on_closing)
    init_window.mainloop()  # 父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示


def on_closing():
    global ZMJ_PORTAL
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        ZMJ_PORTAL.gDict['run'] = False
        ZMJ_PORTAL.init_window_name.destroy()

if __name__ == '__main__':
    gui_start()
