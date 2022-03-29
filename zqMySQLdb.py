# AmberHan
# !/usr/bin/env python
# !-*- coding:utf-8 -*-
# !@Time   : 2021/4/26 10:57
# !@File   : zqMySQLdb.py
#数据库操作函数

import zqConfig as config
import MySQLdb  # pip install mysqlclient

def getConnection():
    db = MySQLdb.connect(
        host=config.serverName,
        user=config.userName,
        passwd=config.passWord,
        db=config.dataBase
    )

    return db


def sp_mysql_proc_total_data():
    # 建立连接
    db = getConnection()
    # 创建游标对象
    cursor = db.cursor()
    ret=[[],[],[],[]]
    try:
        # have_sp("proc_total_data", cursor, None)
        cursor.callproc("proc_total_data")
        #for re in cursor.stored_results():
        values = cursor.fetchall() #vocal_tmp
        ret[0] = values;

        # for rs in values:
        #     print(rs)
        # print("-----")
        cursor.nextset()
        values = cursor.fetchall() #facial_tmp
        ret[1]=values;
        # for rs in values:
        #     print(rs)

        # print("-----")
        cursor.nextset()          #vehicle_tmp
        values = cursor.fetchall()
        ret[2]=values;

        # for rs in values:
        #     print(rs)

        # print("-----")
        cursor.nextset()         # total_data
        values = cursor.fetchall()
        ret[3]=values;

        # for rs in values:
        #     print(rs)
            #ret.append(values)
            #print(values)
        cursor.close()
        db.commit()

    except Exception as e:
        print(e)
        cursor.close()
        db.rollback()

    # 关闭数据库连接
    #cursor.close()
    db.close()
    return ret

# 调用存储过程
def have_sp(pcname: str, cursor, vals=None):
    if vals:
        rows = cursor.callproc(procname=pcname, args=vals)
    else:
        rows = cursor.callproc(procname=pcname)
    #print(rows)


# 执行存储过程
def sp_mysql(pcname: str, vals=None):
    # 建立连接
    db = getConnection()
    # 创建游标对象
    cursor = db.cursor()
    try:
        have_sp(pcname, cursor, vals)
        cursor.close()
        db.commit()
    except  Exception as e:
        print(e)
        # 如果发生错误则回滚
        cursor.close()
        db.rollback()

    # 关闭数据库连接

    db.close()

# 执行查询语句
def connect_mysql(sql: str):
    # 建立连接
    db = getConnection()
    # 创建游标对象
    cursor = db.cursor()
    try:
        # 执行sql语句
        # sql = "INSERT INTO vehicle(sharp_turn,speeding, abnormal, time, v_predict) VALUES (1, 1, 1, '2021-4-1', 1)"
        cursor.execute(sql)
        # 提交到数据库执行
        cursor.close()
        db.commit()
        pass
    except Exception as e:
        print(e)
        # 如果发生错误则回滚
        cursor.close()
        db.rollback()

    # 关闭数据库连接
    db.close()


# 插入数据
def insert_sql(db: str, name: list, val: list) -> str:
    # sql = "INSERT INTO " + db + get_str(name) + " VALUES " + get_str(val)
    sql = "INSERT INTO %s%s VALUES %s" % (db, get_str(name), get_str(val))
    return sql


# 批量插入数据
def p_insert_sql(db: str, name: list, val: list) -> str:
    # sql = "INSERT INTO " + db + get_str(name) + " VALUES " + get_str(val)
    sql = "INSERT INTO %s%s VALUES " % (db, get_str(name))
    list1 = []
    for i in range(len(val)):
        list1.append(get_str(val[i]))
    sql += ",".join(list1)
    return sql


# 查找数据
def select_sql(db: str, swhere: str) -> str:
    sql = "select * from %s where 1 = 1" % db
    if str:
        sql += swhere
    return sql


def get_str(name: list) -> str:
    return "(" + ','.join(name) + ")"

#测试
if __name__ == '__main__':
    st1 = "proc_facial_tmp"
    st2 = "proc_vehicle_tmp"
    st3 = "proc_vocal_tmp"
    st4 = "proc_total_data"
    sp_mysql(st1, [0.4, 0.9, 0.8, 0.5, 0.4])
    sp_mysql(st1, [0.5, 0.8, 0.7, 0.6, 0.5])

    sp_mysql(st2, [0.1, 0.2, 0.3, 0.4])
    sp_mysql(st2, [0.13, 0.12, 0.35, 0.34])

    sp_mysql(st3, [0.01, 0.2])
    sp_mysql(st3, [0.2, 0.4])
    print("End")


    sp_mysql_proc_total_data()
    #print(ret)



#ALTER TABLE `vocal_tmp` ADD INDEX IDX_vocal_tmp_ID ( `tag` ) ;
#ALTER TABLE `facial_tmp` ADD INDEX IDX_facial_tmp_ID ( `tag` ) ;
#ALTER TABLE `vehicle_tmp` ADD INDEX IDX_vehicle_tmp_ID ( `tag` ) ;
