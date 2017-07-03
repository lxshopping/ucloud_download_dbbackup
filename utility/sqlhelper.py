#!/usr/bin/env python
#coding:utf-8

import MySQLdb
import conf

class MysqlHelper(object):
    
    def __init__(self):
        self.__sql_conf = conf.conn_conf
        
    
    def get_all_data(self,sql,params):
        conn = MySQLdb.connect(**self.__sql_conf) 
        cur = conn.cursor()
#         cur = conn.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        
        reCount = cur.execute(sql,params)  # 通过光标，执行sql语句显示影响数据的条数    数目
        data = cur.fetchall() # 元组的形式显示上面被影响的具体数据
        
        cur.close()
        conn.close()
        return data
    
    def get_one_data(self,sql,params):
        conn = MySQLdb.connect(**self.__sql_conf)
        cur = conn.cursor()
        
        reCount = cur.execute(sql,params)
        data = cur.fetchone()
        
        cur.close()
        conn.close()
        return data
        
        
    def insert_one_data(self,sql,params):
        conn = MySQLdb.connect(**self.__sql_conf)
        cur = conn.cursor()
        #插入一行
        reCount = cur.execute(sql,params)
        if not reCount == 1:
            return False
        
        conn.commit()
        cur.close()
        conn.close()
        return True
    
    
    def insert_multiterm_data(self,sql,params):
        conn = MySQLdb.connect(**self.__sql_conf)
        cur = conn.cursor()
        
        reCount = cur.executemany(sql,params)
        
        conn.commit()
        cur.close()
        conn.close()
        return True
    

    def update_one_data(self,sql,params):
        conn = MySQLdb.connect(**self.__sql_conf)
        cur = conn.cursor()
        #更新一行
        reCount = cur.execute(sql,params)
        if not reCount == 1:
            return False

        conn.commit()
        cur.close()
        conn.close()
        return True
    