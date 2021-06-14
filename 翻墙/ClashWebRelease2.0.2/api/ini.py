# -*- coding: utf-8 -*-
import configparser
import os
class MyConfigParser(configparser.ConfigParser):
    def __init__(self, defaults=None):
        configparser.ConfigParser.__init__(self, defaults=defaults)

    def optionxform(self, optionstr):
        return optionstr


def getvalue(group,key):
    proDir = os.getcwd()
    configPath = os.path.join(proDir, "api\default.ini")
    conf = MyConfigParser()
    conf.read(configPath, encoding="utf-8")
    return conf.get(group,key)

def setvalue(group,key,value):
    proDir = os.getcwd()
    configPath = os.path.join(proDir, "api\default.ini")
    conf = MyConfigParser()
    conf.read(configPath, encoding="utf-8")
    conf[group][key]=value
    fo = open(configPath, 'w', encoding='UTF-8')  # 重新创建配置文件
    conf.write(fo)  # 数据写入配置文件
    fo.close()
