# coding:utf-8
from configparser import ConfigParser
import logging, sys, os
import pymysql

from util.configread import config_read

# 定义数据库创建和表创建的类，并用于初始化数据库结构
class Create(object):
    """
       该类用于创建数据库和数据表，封装了数据库连接、数据库创建、数据表创建以及连接关闭等操作。
       """
    def __init__(self, dbtype, host, port, user, passwd, dbName, charset):
        """
        初始化数据库连接。
        Args:
            dbtype (str): 数据库类型。
            host (str): 数据库主机地址。
            port (int): 数据库端口号。
            user (str): 数据库用户名。
            passwd (str): 数据库密码。
            dbName (str): 数据库名称。
            charset (str): 数据库字符集。
        """
        self.dbtype, self.host, self.port, self.user, self.passwd, self.dbName, self.charset = dbtype, host, port, user, passwd, dbName, charset
        self.conn = pymysql.connect(host=self.host, user=self.user, passwd=self.passwd, port=self.port,
                                    charset=self.charset)
        self.cur = self.conn.cursor()

    def create_db(self, sql):
        self.cur.execute(sql)
        self.conn.commit()

    def create_tables(self, sqls):
        use_sql = '''use `{}`;'''.format(self.dbName)
        self.cur.execute(use_sql)

        for sql in sqls:
            try:
                self.cur.execute(sql)
                self.conn.commit()
            except Exception as e:
                print(e)

    def conn_close(self):
        self.cur.close()
        self.conn.close()
