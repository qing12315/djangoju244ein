# 负责读取配置文件，获取数据库相关配置信息
#coding:utf-8
__author__ = "qing12315"
from configparser import ConfigParser

# 从指定的配置文件中读取数据库相关配置信息
# :param filePath: 配置文件的路径，类型为字符串
# :return: 若配置文件中存在 'sql' 部分，则返回数据库类型、主机地址、端口号、用户名、密码、数据库名、字符集和是否有Hadoop的信息；
#          若不存在 'sql' 部分，则返回多个 None
def config_read(filePath:str):
    # 创建一个 ConfigParser 对象，用于解析配置文件
    cfg=ConfigParser()
    cfg.read(filePath, encoding="utf-8-sig")
    if "sql" in cfg.sections():
        dbType=cfg.get('sql','type')
        host=cfg.get('sql','host')
        port=cfg.getint('sql','port')
        user=cfg.get('sql','user')
        passwd=cfg.get('sql','passwd')
        dbName=cfg.get('sql','db')
        charset=cfg.get('sql','charset')
        hasHadoop=cfg.get('sql','hasHadoop')
        return dbType,host,port,user,passwd,dbName,charset,hasHadoop
    else:
        return None,None,None,None,None,None,None,None