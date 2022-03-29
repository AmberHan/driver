# AmberHan
# !/usr/bin/env python
# !-*- coding:utf-8 -*-
# !@Time   : 2021/4/26 10:57
# !@File   : zqAudio.py
# 模拟声音数据

import zqConfig as config
import zqLib
import zqMySQLdb

def gfuncVocal(Queue, Dict):
    zqLib.zqFunTimerEnd(config.INTERVALVocal,Dict, funcVocal)

def funcVocal():
    time = "\"" + zqLib.get_current_time() + "\""
    vals = []
    for i in range(2):
        vals.append(zqLib.zqRandom())
        # vals.append(round(random.random(), 1))

    zqMySQLdb.sp_mysql("proc_vocal_tmp", vals) #写入数据库
    print(time,vals)


if __name__ == '__main__':
    zqLib.zqFunTimerEnd(config.INTERVALVocal,None, funcVocal)
