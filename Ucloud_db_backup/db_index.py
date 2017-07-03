#!/usr/bin/env python
#coding:utf-8

import MySQLdb
import SocketServer

class Myserver(SocketServer.BaseRequestHandler):
    
    def setup(self):
        pass

    def handle(self):
        conn = self.request
        client = str(self.client_address)
        content = 'hello.Welcome intelligent chat robot'
        conn.send(content)
        sql_conn = MySQLdb.connect(host='192.168.8.222',user='root',passwd='111111',db='08day05')
        #         cur = conn.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        cur = sql_conn.cursor()
        #对Chatlog表的操作
        sql = 'insert into Chatlog (user,content) values (%s,%s)'
        params = ('server',content)
        reCount = cur.execute(sql,params)
        if not reCount == 1:
            return False
        sql_conn.commit()

        
        flag = True
        while flag:
            data = conn.recv(1024)
            client_params = (client,data)
            reCount = cur.execute(sql,client_params)
            if not reCount == 1:
                return False
            sql_conn.commit()
            if data == 'exit':
                flag = False
            elif 'hello' in data:
                hello_answer = 'hello,how are you!'
                conn.send(hello_answer)
                hello_params = ('server', hello_answer)
                reCount = cur.execute(sql,hello_params)
                sql_conn.commit()
            elif 'who' in data:
                who_answer = "I'm a smart chat robot"
                conn.send(who_answer)
                who_params = ('server', who_answer)
                reCount = cur.execute(sql,who_params)
                sql_conn.commit()
            elif 'thank' in data:
                thank_answer = 'thank you!'
                conn.send(thank_answer)
                thank_params = ('server', thank_answer)
                reCount = cur.execute(sql,thank_params)
                sql_conn.commit()
            elif 'love' in data:
                love_answer = 'Love your sister'
                conn.send(love_answer)
                love_params = ('server', love_answer)
                reCount = cur.execute(sql,love_params)
                sql_conn.commit()

            else:
                last_answer = "I'm sorry, I don't understand your answer. What's more, please."
                conn.send(last_answer)
                last_params = ('server', last_answer)
                reCount = cur.execute(sql,last_params)
                sql_conn.commit()
                
        
#         print self.__sql_data.get_all()
#         print self.__sql_data.get_user_all(client)
        query_sql = "select user,content from Chatlog where user = %s"
        query_params = (client,)
        reCount = cur.execute(query_sql,query_params)
        data = cur.fetchall()
        print data
        
        cur.close()
        sql_conn.close()
        conn.close()



    def finish(self):
        pass



if __name__ == '__main__':
    server = SocketServer.ThreadingTCPServer(('127.0.0.1',9999),Myserver)
    server.serve_forever()
    

'''

1.params可以使用一个，不需要query_params、hello_params。。这些变量，只写一个params应该可以   因为每次都会对params重新赋值，sql仍然执行以前的变量，params带入重新赋值后的参数，执行的结果也是重新赋值后新变量的值，所以可以都使用params
sql不变，参数params改变，最后执行完毕，查询并展现数据

2，开始想到每插入一次数据都需要连接和断开数据库，太影响性能了，每次插入都连接一次数据库然后关闭一次，但是实际只需要打开一次，然后开始插入数据，全部插入完成后在关闭连接，这样对数据库影响较小
但是仍然有很多重复代码， 而且每次都需要写查询语句并赋值，目前只有一张表，看不出来有什么问题，如果现在有10张不同的表，那么就要写40个增删改查，会出现大量重复代码，没有意义，所以需要采用上面的2层架构。

1024字节  1KB

import MySQLdb
user = raw_input('username')
pwd = raw_input('password')
sql = 'xxx'
params = (user,pwd)

conn = MySQLdb.connect()
cur = conn.cursor()
reCount = cur.execute(sql,params)
data = cur.fetchone()

cur.close()
conn.close()
print data

''' 
    



