#!/usr/bin/env python
#coding:utf-8

# #断言
# assert(1==1)

import MySQLdb

conn = MySQLdb.connect(host='192.168.8.222',user='root',passwd='111111',db='08day05')
cur = conn.cursor()

'''
查询  原始SQL
reCount = cur.execute('select * from admin')  # 执行sql语句所影响表admin的行数
data = cur.fetchall() # 以元组的形式显示表中所有的数据，每行数据一个元组    只有查询需要，其他的都不需要

插入
sql = "insert into admin (name,address) values (%s,%s)" # 注意所有数据类型都用%s来表示，在数据库中都用%s来表示占位符
params = ('alex_1','usa')

删除
sql = "delete from admin where id = %s"
params = ('1')
params = (3,)

更新
sql = "update admin set name = %s where id = 7"
params = ('sb',)


reCount = cur.execute(sql,params) #reCount值    执行这条sql语句所影响的行数


#批量插入
li =[
     ('alex','usa'),
     ('sb','usa'),
]
reCount = cur.executemany('insert into admin(name,address) values(%s,%s)',li)

conn.commit()
cur.close()
conn.close()

print reCount


conn.commit()  #增删改需要commit，select查询不需要commit
# conn.rollback()

cur.close()
conn.close()

print reCount # 执行sql语句所影响表admin的行数
#print data


#mysql的事务操作 、 回滚              sql操作完后commit提交，会自动验证提交前的sql语句是否都执行成功！执行成功，才会commit提交一次事务

sql = "update admin set name = %s where id = 6 "
params = (0)

sql = "update admin set name = %s where id = 7 "
params = (200)

conn.commit()
cur.close()
conn.close()
事务  :以上2条sql语句都执行成功，commit才能提交成功，修改对应的字段
'''


# 以字典的形式显示列表名
cur = conn.cursor(cursorclass = MySQLdb.cursors.DictCursor)
reCount = cur.execute('select * from admin')  #执行这条sql语句所影响的表行数
data = cur.fetchall()    # 获取上面查询出来的所有数据，并用字典的方式打印出来

data = cur.fetchone()
print data
cur.scroll(0,mode='absolute')
data = cur.fetchone()
print data

#相对定位  指针
cur.scroll(-1,mode='relative')

#绝对定位  类似文件操作seek(0)
cur.scroll(0,mode='absolute')

print reCount
print data
conn.commit()
cur.close()
conn.close()


# 获取自增id，用于2张表之间的关联id  外键id   先commit 才能获取到自增id，插入失败，也就没有自增id，lastrowid自然就获取不到自增id
# 案例就是文章表和附件表，之间要建立关联，需要附件表的自增id 作为外键id插入到文章表中，从而2张表建立关系
sql = "insert into media (address) values %s"
params = ('/usr/bin/a.txt',)
reCount = cur.execute(sql,params)  # 执行sql语句所影响的数据库行数
conn.commit()
new_id = cur.lastrowid  # 插入数据的自增id
print new_id

cur.close()
conn.close()

'''
#对于三层架构模型，使用面向过程实现如下：  

这样做的坏处是无法扩展，如果数据库有10张表，那么就要写40个增删改查的方法，而且每次都要打开和关闭连接，非常不合理，而且后期也很难维护和扩展，
比如一个表结构改变了，要按照业务逻辑来查找所有跟这张表有关的函数，修改起来很不方便，三层架构就很好的解决了这些问题，
1.减少了重复代码，2.后期表结构也方便修改和维护

import MySQLdb
user = raw_input('username')
pwd = raw_input('password')
sql = 'xxx'
params = (user,pwd)

conn = MySQLdb.connect()
cur = conn.cursor()
reCount = cur.execute()
data = cur.fetchone()

cur.close()
conn.close()
print data

'''









