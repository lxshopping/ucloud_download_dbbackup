#!/usr/bin/env python
# --*-- coding:utf-8 --*--

import sys
import urlparse
import urllib
import requests
import json
import urllib2
import time
import hashlib
from model import DescribeUDBBackup
import commands
import os, random
from multiprocessing import Pool,TimeoutError
import logging



base_url = 'http://api.ucloud.cn'
public_key = 'ucloudcaihy@qq.com13960596782016582545'
private_key = '688e3228c34528a5e9388134ade8632347a9c7dd'

"""
http(s)://api.ucloud.cn/?Action=DescribeUDBBackup
&Region=cn-gd
&Offset=0
&Limit=100

http://api.ucloud.cn/?Action=DescribeUDBBackup&Region=cn-gd&Offset=0&Limit=100
"""

params = {
    "Action" : "DescribeUDBBackup",
    "Region" : "cn-gd",
    "Offset" : 0,
    "Limit" : 100,
    "PublicKey" : 'ucloudcaihy@qq.com13960596782016582545',

}


class BaseResponse():
    def __init__(self):
        self.status = False
        self.data = None
        self.error = ''


class server_conn(object):

    def __init__(self,url):
        self.url = url

    def get_assetid(self):
        pass


    def request_url(self):
        logging.info( self.url)
        req = urllib2.urlopen(self.url)
        result = req.read()
        return result

    def request(self,url):
        if self.port is not None:
            url_str = "http://%s:%s%s" %(self.host,self.port,url)

        else:
            url_str = "http://%s%s" %(self.host,url)
        logging.info( url_str)
        req = urllib2.urlopen(url_str)
        result = req.read()
        return result



# post、get类

class http_method(object):

    def __init__(self):
        pass

        # self.message = message


    def inform_post(self,mess_infom):
        # post的组接口
        # url = 'https://oapi.dingtalk.com/robot/send?access_token=6e7583cdcb89f266026a21723e52aedd63dd21e8aa2e2c061b35e734759cf920'
        url = 'https://oapi.dingtalk.com/robot/send?access_token=51f2b40d112daaaf3d972395c3afde7e8b60c3b8a00b9121b66883ceb1db341c'
        # payload = {'some': 'data'}
        headers = {'content-type': 'application/json'}

        ret = requests.post(url, data=json.dumps(mess_infom), headers=headers)

        return ret.text
        # print ret.cookies


    def inform_get(self):

        pass


def _verfy_ac(private_key, params):
    items=params.items()
    # 请求参数串
    items.sort()
    # 将参数串排序

    params_data = "";
    for key, value in items:
        params_data = params_data + str(key) + str(value)
    params_data = params_data + private_key

    sign = hashlib.sha1()
    sign.update(params_data)
    signature = sign.hexdigest()

    return signature
    # 生成的Signature值


def get_backup_all(public_key,private_key,params):

    # print _verfy_ac(private_key,params)
    ucloud_get_backupid = server_conn('http://api.ucloud.cn/?Action=DescribeUDBBackup&Region=cn-gd&Offset=0&Limit=100&PublicKey=%s&Signature=%s'  %(public_key,_verfy_ac(private_key,params)))
    return ucloud_get_backupid.request_url()



def get_download_url(public_key,private_key):

    download_list = []

    sql = DescribeUDBBackup.DescribeUDBBackup()
    # 获取没有下载过的url连接,is_download == 0 的url下载连接
    # is_download = 0
    # for url in sql.get_download_id(is_download):
    for url in sql.get_all():
        if url[11] == 0:
            DBId = url[7]
            BackupId = url[1]
        # print type(url)
        # print type(json.dumps(url))

            download_params = {

            "Action" : "DescribeUDBInstanceBackupURL",
            "Region" : "cn-gd",
            "Zone" : "cn-gd-02",
            "DBId" : DBId,
            "BackupId" : BackupId,
            "PublicKey" : 'ucloudcaihy@qq.com13960596782016582545',

            }

            ucloud_get_download_url = server_conn('http://api.ucloud.cn/?Action=DescribeUDBInstanceBackupURL&Region=cn-gd&Zone=cn-gd-02&DBId=%s&BackupId=%d&PublicKey=%s&Signature=%s'  %(DBId,BackupId,public_key,_verfy_ac(private_key,download_params)))
            # # a获取result返回值
            # a = ucloud_get_download_url.request_url()
            # print a
            # print download_list

            last_download_url = json.loads(ucloud_get_download_url.request_url())

            last_download_url["BackupId"] = BackupId

            download_list.append(last_download_url)

            # print len(download_list)
    # print len(download_list)
    # print download_list
    # 没有下载连接 download_list = [] 测试

    # logging.info(type(download_list[0]))
    # logging.info(download_list)
    # 多线程下载
    if len(download_list) == 0:
        logging.info("没有可下载的备份文件")

    else:
        '''
        print download_list
        print len(download_list)
        # 3、实现多进程同时下载所有的备份文件
        '''
        with open('/tmp/db.dd', 'ab+') as write_file_dd:
            write_file_dd.write("Ucloud广州B区db全备:\n\n数据库实例名称            备份时间            备份大小        下载成功url\n")

        pool = Pool(processes=len(download_list))
        # i 代表list index,item内容
        for i, item in enumerate(download_list):

            '''
            print type(item)
            print item

            print type(json.loads(item))
            print json.loads(item)

            print type(json.loads(item)["BackupPath"])
            print json.loads(item)["BackupPath"]

            '''

            logging.info( 'Parent process %s.' % os.getpid())

            # 看cpu的核数，一般是cpu的2倍，过多会产生僵尸进程，父进程和子进程失联,父进程会变为1.

            pool.apply_async(many_process_download,[item["BackupPath"],item["BackupId"], i])
            res_list = []
            '''
            # 2、 把创建进程放在循环里面发现创建了2个进程去下载同一个地址，最后后完成下载的进程覆盖掉新下载好的文件，相当于2个进程去下载同一个文件，最后只能看到一个文件，
            #     启用了2个进程去下载同一个地址，后面会覆盖前面进程下载好的，下载完一个在下载下一个也是开2个进程去下载同一个下载地址
            # pool = Pool(processes=2)
            # for i in range(2):
                # pool.apply_async(many_process_download,[item["BackupPath"],item["BackupId"], i])
                # pool.apply_async(many_process_download,[json.loads(item)["BackupPath"],backupid,i])
                # res = pool.apply_async(get_download_url,[public_key,private_key,i]) # 这里使用 pool.apply 可以串行输出，也就是阻塞，等待进程输出
                # res = Process(target=f,args=[,i])
                # res.get()  这里跟上面使用pool.apply的效果一样，也是串行输出
                # print '-----:', i
                # res_list.append(res)
                # print res_list


            # for r in res_list:
            #     try:
            #         # 设置进程挂死的超时时间，防止如果进程挂起，永远get不到数据时就会抛出异常！设置每个进程的超时时间
            #         print r.get(timeout=1)
            #     # except Exception as e:
            #     except TimeoutError:
            #         print "We lacked patience and got a multiprocessing.TimeoutError"
            '''
        logging.info( 'Waiting for all subprocesses done...')
        pool.close()
        pool.join()
        logging.info( 'All subprocesses done.')
        infor_dd()
        # return True
        # return download_list



def many_process_download(download_url,backupid,name):

    sql = DescribeUDBBackup.DescribeUDBBackup()

    logging.info( 'Run task %s (%s)...' % (name, os.getpid()))
    start = time.time()
    # time.sleep(random.random() * 3)
    url_download_staus = commands.getstatusoutput('wget -c -P /data/dbbackup %s &> /tmp/db_download.log'  % (download_url, ))
    logging.info( url_download_staus)
    # url_download_staus = commands.getstatusoutput('wget -c -P /data/dbbackup %s &> /tmp/db_download.log'  % (str(json.loads(item)["BackupPath"]),) )
    # url_download_staus = commands.getstatusoutput('wget -c -P /data/dbbackup %s &> /tmp/db_download.log')  % (item["BackupPath"])
    if url_download_staus[0] == 0:
        logging.info( "%s:download url success:  %s" % (time.strftime('%Y-%m-%d %H:%M:%S'),download_url))
        download_id = sql.get_one(backupid)
        with open('/tmp/db.dd', 'ab+') as write_file_dd:
            try:
                value = round(float(download_id[4])/1024/1024,4)
                line =  "\n%s       %s       %sM        %s\n" %(download_id[8],time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(download_id[3])),value,download_url)
            except Exception as e:
                logging.info(e)
            write_file_dd.write(line)

        # 将db中is_download修改为1,下次不再下载
        try:
            sql.update_one(backupid)
        except Exception as e:
            logging.info( "更新数据库报错:%s,更新BackupId失败:%d" % (e,backupid))

    else:
        logging.info( "download url failed: %s, Next time automatically download" % (download_url))

    end = time.time()
    logging.info( 'Many process Task %s runs %0.2f seconds.' % (name, (end - start)))



def bakparams_write_db(public_key,private_key,params):
    # 获取json数据处理
    '''
    json.dumps/loads 使用方法
    # print get_data_dict
    # print type(get_data_dict)
    # get_data_str = json.dumps(get_data)  字典 -> 字符串
    # print type(get_data_str)
    # print get_data_str
    # print json.loads(get_data_str)  字符串 -> 字典
    '''
    sql = DescribeUDBBackup.DescribeUDBBackup()
    get_data = get_backup_all(public_key,private_key,params)
    # print type(get_data)
    get_data_dict = json.loads(get_data)
    for infor in get_data_dict['DataSet']:
        try:
            # print sql.get_one(infor['BackupId'])
            if not sql.get_one(infor['BackupId']):
                '''
                报错:插入数据库报错:(1264, "Out of range value for column 'BackupSize' at row 1"),请检查BackupId:275273,BackupSize:19183846971
                # 这里得到的就是整型和字符串，可以直接存入mysql，无需再转换成字符串存入mysql，如果是字典或者list需要json.dumps进行格式转换成字符串后再存入mysql,能得到可以存入mysql的类型(int,varchar,char等)就可以直接存入mysql
                # 把表结构的BackupSize字段int(80)改为varchar(255)类型解决
                print type(infor['BackupId'])
                print infor['BackupId']
                print type(infor['BackupSize'])
                print type(json.dumps(infor['BackupSize']))
                print json.dumps(infor['BackupSize'])
                '''
                sql.insert_one(infor['BackupId'],infor['BackupName'],infor['BackupTime'],infor['BackupSize'],infor['BackupType'],infor['State'],infor['DBId'],infor['DBName'],infor['Zone'],infor['BackupZone'])
        except Exception as e:
            logging.info( "插入数据库报错:%s,请检查BackupId:%s,BackupSize:%s" % (e,infor['BackupId'],infor['BackupSize']))

    return True



def infor_dd():

    '''
    sql = DescribeUDBBackup.DescribeUDBBackup()

    is_download = 1

    download_success_url = []

    for url in sql.get_all_download_id(is_download):
        # print type(url)
        download_success_url.append(url)

    logging.info( download_success_url)

    for item in download_success_url:
        with open('/tmp/db.dd', 'ab+') as write_file_dd:
            try:
                value = round(float(item[4])/1024/1024,4)
                line =  "\n%s       %s       %sM\n" %(item[8],time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(item[3])),value)
            except Exception as e:
                logging.info(e)
            write_file_dd.write(line)
    '''
    
    dd_infor = http_method()

    with open('/tmp/db.dd', 'ab+') as write_file_dd:
        write_file_dd.seek(0)
        message_dd = write_file_dd.read()
        # message_dd.encode('utf-8')

        if len(message_dd) > 0:
            values = { "msgtype": "text","text": {"content": message_dd}, "at": {"atMobiles": ["18607169123","13986238346","18627051621"], } }
            dd_infor.inform_post(values)

        else:
            logging.info("已下载的url等于0:%s" % message_dd)

    with open('/tmp/db.dd', 'w+') as write_file_dd:
        clear_file_dd = ''
        write_file_dd.write(clear_file_dd)

    # print "Sleep 14400s..."
    # time.sleep(14400)


if __name__=='__main__':
    logging.basicConfig(filename='db_script.log',level=logging.DEBUG)
    bakparams_write_db(public_key,private_key,params)
    get_download_url(public_key,private_key)



    '''
    1、在这里使用多进程发现多个进程去下载不同的文件，但是文件内容是一样的，每次访问url的下载地址都会变，启动2个进程去下载同一个url返回的不同下载地址，其实下载的备份文件是同一个文件
    #这里使用多进程调用上面的get_download_url函数会出现多个进程下载一个文件的情况，也就是无法实现多进程同时下载多个备份文件的需求，只是把一个文件使用多进程去下载了多次而已，并不能实现需求
    print 'Parent process %s.' % os.getpid()

    # 看cpu的核数，一般是cpu的2倍，过多会产生僵尸进程，父进程和子进程失联,父进程会变为1.
    pool = Pool(processes=2)

    res_list = []
    for i in range(2):
        pool.apply_async(get_download_url,[public_key,private_key,i])
        # res = pool.apply_async(get_download_url,[public_key,private_key,i]) # 这里使用 pool.apply 可以串行输出，也就是阻塞，等待进程输出
        # res = Process(target=f,args=[,i])
        # res.get()  这里跟上面使用pool.apply的效果一样，也是串行输出
        # print '-----:', i
        # res_list.append(res)
        # print res_list
    print 'Waiting for all subprocesses done...'
    pool.close()
    pool.join()

    print 'All subprocesses done.'

    # 设置进程超时时间
    # for r in res_list:
    #     try:
    #         # 设置进程挂死的超时时间，防止如果进程挂起，永远get不到数据时就会抛出异常！设置每个进程的超时时间
    #         print r.get(timeout=1)
    #     # except Exception as e:
    #     except TimeoutError:
    #         print "We lacked patience and got a multiprocessing.TimeoutError"

    '''
