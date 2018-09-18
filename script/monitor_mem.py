#!/usr/bin/python
# coding=utf-8

from datetime import datetime
import os
import MySQLdb

#  操作数据库


def mysql_opera(sql,flag):
    connection = MySQLdb.connect(host='localhost',user='数据库用户名',passwd='数据库密码',db='Devops',charset='utf8')
    cursor = connection.cursor()
    opera_result = ""

    # 查询数据库
    if flag == 0:
        cursor.excute(sql)
        data = cursor.fetchall()
        connection.close()
        return data
    elif flag == 1:
        try:
            print cursor.execute(sql)
            connection.commit()
            opera_result = "success"
        except:
            connection.rollback()
            opera_result = "failed"
        connection.close()
        return opera_result
    else:
        return "failed"


def monitor_mem():
    now = datetime.now()	
    cmd_mem = "/usr/bin/free -m | grep Mem"
    minion_id = os.popen('hostname').read().splitlines()[0]
    mem_list = os.popen(cmd_mem).read().splitlines()[0].split()
    memory_total = mem_list[1]
    memory_used = mem_list[2]
    memory_free = mem_list[3]
    memory_share = mem_list[4]
    memory_bu_ca = mem_list[5]
    memory_available = mem_list[6]
    memory_time = datetime.strftime(now,('%Y-%m-%d %H:%M:%S'))

    sql_mem = "insert into devops_memory_info(minion_id,memory_total,memory_used,memory_free,"+\
            "memory_share,memory_bu_ca,memory_available,memory_time) values('%s',%s,%s,%s,%s,%s,%s,'%s')"%(minion_id,memory_total,memory_used,memory_free,memory_share,memory_bu_ca,memory_available,memory_time)
    print sql_mem
    result = mysql_opera(sql_mem,1)
    print result


if __name__ == "__main__":
    monitor_mem()
