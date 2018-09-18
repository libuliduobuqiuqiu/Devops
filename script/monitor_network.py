#!/usr/bin/python
# coding=utf8

from datetime import datetime
import os
import re
import MySQLdb
import time


try:
    import psutil
except ImortError:
    os.popen("yum install -y python-devel")
    f = os.popen("pip install psutil").read()
    if re.search('error',f,re.IGNORECASE):
        print("安装 psutil 模块失败，请手动安装")
    else:
        import psutil
        print("安装 psutil模块成功")


# 处理网络流量
class NetworkTraffic(object):
    network_keys = []

    old_sent, old_receive = {}, {}
    new_sent, new_receive = {}, {}

    def __init__(self):
        pass

    # 获取网络发包和收包
    def get_network_counters(self):
        sent = {}
        receive = {}
        network_counters = psutil.net_io_counters(pernic=True)
        self.network_keys = network_counters.keys()

        for key in self.network_keys:
            sent[key] = network_counters.get(key).bytes_sent
            receive[key] = network_counters.get(key).bytes_recv
        return sent, receive

    # 处理统计5分钟内的网络流量
    def handle_network_counters(self):

        network_times = {}
        net_input, net_output = {}, {}

        self.old_sent, self.old_receive = self.get_network_counters()
        network_times['old'] = datetime.strftime(datetime.now(), ('%Y-%m-%d %H:%M:%S'))

        time.sleep(300)
        self.new_sent, self.new_receive = self.get_network_counters()
        network_times['new'] = datetime.strftime(datetime.now(), ('%Y-%m-%d %H:%M:%S'))

        for key in self.network_keys:
            net_output[key] = (self.new_sent[key]-self.old_sent[key])/1024
            net_input[key] = (self.new_receive[key]-self.old_receive[key])/1024

        return net_output, net_input, network_times


# 处理数据库
class MysqlOpera(object):
    host = ""
    user = ""
    password = ""
    db = ""
    charset = ""

    def __init__(self,password, db, host='localhost', user='root', charset='utf8'):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.charset = charset

    def connect_mysql(self):
        connection = MySQLdb.connect(host=self.host, user=self.user, passwd=self.password, db=self.db, charset=self.charset)
        return connection

    def query_mysql(self,sql):
        connection = self.connect_mysql()
        cursor = connection.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        connection.close()
        return data

    def insert_mysql(self,sql):
        connection = self.connect_mysql()
        cursor = connection.cursor()
        try:
            cursor.execute(sql)
            connection.commit()
        except Exception as e:
            connection.rollback()
            print e.message
        connection.close()


if __name__ == "__main__":
    net_out, net_in = {}, {}
    network_time = {}
    monitor_hostname = os.popen('hostname').read().splitlines()[0]

    monitor_network = NetworkTraffic()
    mysql_opera = MysqlOpera('数据库密码','Devops')

    net_out,net_in,network_time = monitor_network.handle_network_counters()

    sql_network = "insert into devops_network_info(minion_id,network_key,network_in,network_out,network_time)" +\
        " values('"+monitor_hostname+"','%s',%s,%s,'%s')"
    # print sql_network

    for key in net_out.keys():
        sql_cmd = sql_network % (key, net_in[key], net_out[key], network_time['old'])
        mysql_opera.insert_mysql(sql_cmd)
        # print sql_cmd




