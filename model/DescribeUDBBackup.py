#!/usr/bin/env python
# --*-- coding:utf-8 --*--

from utility.sqlhelper import MysqlHelper


class DescribeUDBBackup(object):

    def __init__(self):
        self.__sqlhelper = MysqlHelper()

    def get_one(self,BackupId):
        sql = "select * from DescribeUDBBackup where BackupId = %s"
        params = (BackupId,)
        return self.__sqlhelper.get_one_data(sql, params)

    def get_download_id(self,is_download):
        sql = "select * from DescribeUDBBackup where is_download = %s"
        params = (is_download,)
        return self.__sqlhelper.get_one_data(sql,params)

    def get_all(self):
        sql = "select * from DescribeUDBBackup"
        params = ()
        return self.__sqlhelper.get_all_data(sql, params)

    # def get_user_all(self,user):
    #     sql = "select user,content from DescribeUDBBackup where user = %s"
    #     params = (user,)
    #     return self.__sqlhelper.get_all_data(sql, params)

    def insert_one(self,BackupId,BackupName,BackupTime,BackupSize,BackupType,State,DBId,DBName,Zone,BackupZone):
        sql = "insert into DescribeUDBBackup (BackupId,BackupName,BackupTime,BackupSize,BackupType,State,DBId,DBName,Zone,BackupZone) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        params = (BackupId,BackupName,BackupTime,BackupSize,BackupType,State,DBId,DBName,Zone,BackupZone)
        # 返回True or False
        return self.__sqlhelper.insert_one_data(sql, params)


    def insert_many(self,BackupId,BackupName,BackupTime,BackupSize,BackupType,State,DBId,DBName,Zone,BackupZone):
        sql = "insert into DescribeUDBBackup (BackupId,BackupName,BackupTime,BackupSize,BackupType,State,DBId,DBName,Zone,BackupZone) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        params = [(BackupId,BackupName,BackupTime,BackupSize,BackupType,State,DBId,DBName,Zone,BackupZone),(BackupId,BackupName,BackupTime,BackupSize,BackupType,State,DBId,DBName,Zone,BackupZone)]
        # 返回True or False
        return self.__sqlhelper.insert_multiterm_data(sql, params)

    def update_one(self,BackupId):
        # UPDATE Person SET FirstName = 'Fred' WHERE LastName = 'Wilson'
        sql = "UPDATE DescribeUDBBackup SET is_download = 1 WHERE BackupId = %s"
        params = (BackupId,)
        return self.__sqlhelper.update_one_data(sql,params)


