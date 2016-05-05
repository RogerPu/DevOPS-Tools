#!/usr/bin/python
#coding=utf-8
#Copyright (C) RogerPu (espwj@126.com), Plateno Groups Inc.

try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO
import httplib
import json,sys
import pycurl
import time,logging
import threading

api_nums = int(sys.argv[1])
conf_file = '/home/roger/HTTP_Monitor/api_info.conf'
#conf_file = '/home/roger/DevOPS-Tools/HTTP_Monitor/api_info.conf'

log_file = 'api_monitor.log'

logger = logging.getLogger('日志')
logger.setLevel(logging.DEBUG)

hdr = logging.FileHandler(log_file)
formatter = logging.Formatter('[%(asctime)s] %(name)s:%(levelname)s: %(message)s')
hdr.setFormatter(formatter)

logger.addHandler(hdr)

def send_sms(phone,body1,body2):
    #define your send_sms function here

def send_message_all(body1='Http监控异常',body2='未获取到IP信息'):
    for phone_number in [185--------]:
        logger.debug('正在发送短息')
        logger.debug('短信内容:[铂涛会]%s%s web访问失败故障!' % (body1,body2))
        send_sms(phone_number, body1, body2)
        break

def get_response(url):
    buffer = BytesIO()
    try:
        c = pycurl.Curl()
        c.setopt(c.URL,url)
        c.setopt(c.FOLLOWLOCATION,True)
        c.setopt(c.WRITEFUNCTION,buffer.write)
        c.perform()
        res_code = c.getinfo(c.RESPONSE_CODE)
        res_time = c.getinfo(c.TOTAL_TIME)
        c.close()
        res_time_ms = res_time * 1000
        return  (res_code,res_time_ms)
    except pycurl.error:
        logger.debug('Error at pycurl process')
        res_code = 'None'
        res_time_ms = 'None'
        return (res_code,res_time_ms)
    except:
        logger.debug('Error occurrd when get response')
        res_code = 'None'
        res_time_ms = 'None'
        return (res_code,res_time_ms)

def get_api_info(line_number):
    file = open(conf_file)
    lines = file.readlines(10)
    line_number = line_number - 1
    try:
        line = lines[line_number].split('--')
        api_name = line[0]
        channel_name = line[1]
        host = line[2]
        port = line[3]
        location = line[4]
        file.close()
        return (api_name,channel_name,host,port,location)
    except:
        file.close()
        logger.debug('index error')

def Web_check(api_name,channel_name,host,port,location):
    location_simple = location[0:11]
    msg_body1 = api_name + '在' + channel_name + '线:' + host + ':' + port + location_simple
    msg_body1_whole = api_name + '在' + channel_name + '线:' + host + ':' + port + location
    url = 'http://' + host + ':' + port + location
    #while 1:
    Error_count = 0
    while Error_count < 1000:
        res_code,res_time = get_response(url)
        msg_body2 = '状态码:' + str(res_code) + ' ' + '响应时间:' + str(res_time) + ' ms'
        if res_code == 'None':
            msg_body2 = '接口端口异常'
            send_message_all(msg_body1_whole,msg_body2)
            time.sleep(10)
            Error_count = Error_count + 1
        elif res_code != 200:
            if Error_count == 2:
                    logger.debug(msg_body1_whole)
                    logger.debug(msg_body2)
                    send_message_all(msg_body1,msg_body2)
            elif Error_count > 2:
                if (Error_count % 30) == 0:
                    logger.debug(msg_body1_whole)
                    logger.debug(msg_body2)
                    send_message_all(msg_body1,msg_body2)
                else:
                    logger.debug(msg_body1_whole)
                    logger.debug(msg_body2)
            time.sleep(10)
            Error_count = Error_count + 1
        else:
            if res_time > 1000 :
                msg_body2 = '状态码:' + str(res_code) + ' ' + '响应时间:' + str(res_time / 1000) + ' s'
                logger.debug(msg_body1_whole)
                logger.debug(msg_body2)
                send_message_all(msg_body1,msg_body2)
            logger.debug(msg_body1_whole)
            logger.debug(msg_body2)
            time.sleep(10)
            Error_count = 1

class myThread(threading.Thread):
    def __init__(self,api_name,channel_name,host,port,location):
        threading.Thread.__init__(self)
        self.api_name = api_name
        self.channel_name = channel_name
        self.host = host
        self.port = port
        self.location = location
    def run(self):
        Web_check(self.api_name,self.channel_name,self.host,self.port,self.location)

def multi_monitor(api_nums):
    for i in range(2,api_nums):
        api_name,channel_name,host,port,location = get_api_info(i)
        Thread =  api_name + '[监控Thread:' + str(i) + '] start'
        logger.debug(Thread)
        Thread = myThread(api_name,channel_name,host,port,location)
        logger.debug(Thread)
        Thread.start()
        time.sleep(0.1)

if __name__ == "__main__":
    multi_monitor(api_nums)