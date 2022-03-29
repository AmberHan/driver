# AmberHan
# !/usr/bin/env python
# !-*- coding:utf-8 -*-
# !@Time   : 2021/4/26 10:57
# !@File   : zqLib.py
#统用库函数

import threading
import time
import random

gDict={'run':True}

def zqRandom(n=5):
    iret=1
    for i in range(n):
        iret*=random.random()
    return round(iret,1)

def zqFunTimerEnd(interval:int ,Dict, func):
    global gDict
    gDict=Dict
    if not (gDict and gDict['run']):
        return

    func()
    global timer
    timer = threading.Timer(interval, zqFunTimer,(interval,func))
    timer.start()

def zqFunTimer(interval:int , func):
    global gDict
    if not (gDict and gDict['run']):
        return

    func()
    global timer
    timer = threading.Timer(interval, zqFunTimer,(interval,func))
    timer.start()

# 获取当前时间
def get_current_time():
    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    return current_time

