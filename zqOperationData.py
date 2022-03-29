# AmberHan
# !/usr/bin/env python
# !-*- coding:utf-8 -*-
# !@Time   : 2021/4/26 10:57
# !@File   : zqOperationData.py
#模拟操作数据

import zqConfig as config
import zqLib
import zqMySQLdb

def gfuncVehicle(Queue, Dict):
    zqLib.zqFunTimerEnd(config.INTERVALVocal,Dict, funcVehicle)

def funcVehicle():
    time = "\"" + zqLib.get_current_time() + "\""
    vals = []
    for i in range(4):
        vals.append(zqLib.zqRandom())

    zqMySQLdb.sp_mysql("proc_vehicle_tmp", vals) #写入数据库
    print(time,vals)


if __name__ == '__main__':
    zqLib.zqFunTimerEnd(config.INTERVALVehicle,None, funcVehicle)
