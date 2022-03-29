# AmberHan
# !/usr/bin/env python
# !-*- coding:utf-8 -*-
# !@Time   : 2021/4/26 10:57
# !@File   : zqOperationData.py
#模拟人脸数据

import zqConfig as config
import zqLib
import random
import zqMySQLdb

def funcFacial():
    time = "\"" + zqLib.get_current_time() + "\""
    vals = []
    for i in range(5):
        vals.append(zqLib.zqRandom())

    zqMySQLdb.sp_mysql("proc_facial_tmp", vals)
    print(time,vals)


if __name__ == '__main__':
    zqLib.zqFunTimer(config.INTERVALFacial,funcFacial)
