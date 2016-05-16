#!/usr/bin/python
#coding=utf-8
#Copyright (C) RogerPu (espwj@126.com), Plateno Groups Inc

import logging
import get_problem_host
import pexpect
import re
import sys
import time

# logger = logging.getLogger('pexpect_monitor')
# logger.setLevel(logging.DEBUG)
# pexpect_log_handler = logging.FileHandler
# log_format = logging.Formatter('[%(asctime)s] %(name)s:%(levelname)s: %(message)s')

# dir_name = sys.argv[1]

def operation(ip,user,cmd):
    cmd_combine = '/usr/bin/ssh ' + user +'@' + ip + ' "' + cmd + '"'
    print cmd_combine
    child = pexpect.spawn(cmd_combine,timeout=15)
    index = child.expect(["password:",pexpect.TIMEOUT,pexpect.EOF])
    if index == 0:
        child.kill(0)
        r = 'passed without passwd'
        return r
    elif index == 1:
        child.kill(0)
        r = 'passed cause timeout'
        return r
    elif index == 2:
        print('connect OK')
        child = pexpect.spawn(cmd_combine,timeout=15)
        r = child.read()
        return r

def check_dir_avalability(dir_name,ip):
    cmd = 'test -d ' + dir_name + ' && echo \'10001\'||echo \'20001\''
    r = operation(ip,'root',cmd)
    print cmd
    if int(r) == 10001:
        r_code = 10001
        return r_code
    elif int(r) == 20001:
        r_code = 20001
        return r_code


def get_directory_info(dir_name,ip):
    cmd = 'cd ' + dir_name + ';du -sh * 2>/dev/null|sort -rh|head -n 1;'
    r1 = operation(ip,'root',cmd)
    r2 = re.split(r'\t|\r',r1)
    dir_size = r2[0]
    print dir_name
    dir_name = '/' + r2[1]
    return (dir_name,dir_size)

def dir_url_whole(list):
    list1 = []
    list1 = list[:]
    n = len(list1)
    if n > 1:
        del list1[0]
        n = len(list1)
        def l_ops(n):
            if n == 1:
                return (list1[0])
            return (l_ops(n-1)  + list1[n-1])
        r = l_ops(n)
    elif n == 1:
        r = list1[0]
    return r

def get_big_and_last_dir():
    root_dir_name = '/'
    dir_name = root_dir_name
    problem_host_list = get_problem_host.get_problem_host()
    ip_and_dir_dict = {}
    for i in problem_host_list:
        r = 10001
        dir_list = ['/']
        while r != 20001:
            n = len(dir_list)
            if n == 1: ##检查第一个目录
                dir_name2,first_dir_size = get_directory_info(dir_name,i)
                dir_list.append(dir_name2)
                dir_url = dir_url_whole(dir_list)
                r = check_dir_avalability(dir_url,i)
                time.sleep(2)
            elif n > 1: ##进入检查到的目录检查下个目录
                dir_url = dir_url_whole(dir_list)
                dir_name3,dir3_size = get_directory_info(dir_url,i)
                print dir_name3
                dir_list.append(dir_name3)
                dir_name4 = dir_url_whole(dir_list)
                r = check_dir_avalability(dir_name4,i)
        ip_and_dir_dict[i] = dir_url_whole(dir_list)
    return ip_and_dir_dict

if __name__ == "__main__":
    r = get_big_and_last_dir()
    print r;