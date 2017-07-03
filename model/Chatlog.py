#!/usr/bin/env python
#coding:utf-8
from utility.sqlhelper import MysqlHelper


class ChatLog(object):
    
    def __init__(self):
        self.__sqlhelper = MysqlHelper()
        
    def get_one(self,id):
        sql = "select * from Chatlog where id = %s"
        params = (id,)
        return self.__sqlhelper.get_one_data(sql, params)
    
    def get_all(self):
        sql = "select * from Chatlog"
        params = ()
        return self.__sqlhelper.get_all_data(sql, params)
    
    def get_user_all(self,user):
        sql = "select user,content from Chatlog where user = %s"
        params = (user,)
        return self.__sqlhelper.get_all_data(sql, params)
    
    def insert_one(self,user,content):
        sql = "insert into Chatlog (user,content) values (%s,%s)"
        params = (user,content)
        # 返回True or False
        return self.__sqlhelper.insert_one_data(sql, params)
    
        
    def insert_many(self,user,content):
        sql = "insert into Chatlog (user,content) values (%s,%s)"
        params = [(user),(content)]
        # 返回True or False
        return self.__sqlhelper.insert_multiterm_data(sql, params)