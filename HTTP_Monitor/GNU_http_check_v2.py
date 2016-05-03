#!/usr/bin/python
#coding=utf-8

try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO
import httplib
import json
import pycurl
import time
import threading
import traceback

conf_file = '/home/roger/api_info.conf'

def send_sms(phone,body1,body2):
    try:
        requrl=##msg_send_url
        post_data = ##Post data here
        post_data_encode = json.dumps(post_data,skipkeys=True)
        headerdata = ##header data here
        conn = httplib.HTTPConnection('##host here')
        conn.request(method="POST", url=requrl, body=post_data_encode, headers=headerdata)

        response = conn.getresponse()

        res = response.read()

        print res
    except:
        print('Error Occurred when send message')

def send_message_all(body1='Http监控异常',body2='未获取到IP信息'):
    for phone_number in [1852013xxxx]:
        print('正在发送短息')
        print('短信内容:[铂涛会]%s%s web访问失败故障!' % (body1,body2))
        #send_sms(phone_number, body1, body2)
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
        print('Error at pycurl process')
        res_code = 'None'
        res_time_ms = 'None'
        return (res_code,res_time_ms)
    except:
        traceback.print_exc()
        print('Error occurrd when get response')
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
        print('index error')

def Web_check(api_name,channel_name,host,port,location):
    location_simple = location[0:11]
    msg_body1 = api_name + '在' + channel_name + '线:' + host + ':' + port + location_simple
    url = 'http://' + host + ':' + port + location
    #while 1:
    Error_count = 0
    while Error_count < 1000:
        res_code,res_time = get_response(url)
        msg_body2 = '状态码:' + str(res_code) + ' ' + '响应时间:' + str(res_time) + ' ms'
        if res_code == 'None':
            msg_body2 = '接口端口异常'
            send_message_all(msg_body1,msg_body2)
            time.sleep(10)
            Error_count = Error_count + 1
        elif res_code != 200:
            if Error_count == 2:
                    print(msg_body1)
                    print(msg_body2)
                    send_message_all(msg_body1,msg_body2)
            elif Error_count > 2:
                if (Error_count % 10) == 0:
                    print(msg_body1)
                    print(msg_body2)
                    send_message_all(msg_body1,msg_body2)
                else:
                    print(msg_body1)
                    print(msg_body2)
            time.sleep(10)
            Error_count = Error_count + 1
        else:
            if res_time > 1000 :
                print(msg_body1)
                print(msg_body2)
                send_message_all(msg_body1,msg_body2)
            print(msg_body1)
            print(msg_body2)
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
        Thread =  api_name + '[监控 Thread]' + str(i) + 'start'
        print Thread
        Thread = myThread(api_name,channel_name,host,port,location)
        Thread.start()
        time.sleep(2)

if __name__ == "__main__":
    multi_monitor(6)