# -*- coding: utf-8 -*-
import pexpect
import sys

# ip = '10.100.112.88'
# user = 'roger'
# cmd = '/sbin/ip a'

ip = sys.argv[1]
user = sys.argv[2]
cmd = sys.argv[3]

def operation(ip,user,cmd):

    cmd_combine = '/usr/bin/ssh ' + user +'@' + ip + ' "' + cmd + '"'
    #print cmd_combine
    child = pexpect.spawn(cmd_combine,timeout=2)
    index = child.expect(["password:",pexpect.TIMEOUT,pexpect.EOF])
    if index == 0:
        child.kill(0)
        r = 'passed without passwd'
        return (r,cmd_combine)
    elif index == 1:
        child.kill(0)
        r = 'passed cause timeout'
        return (r,cmd_combine)
    elif index == 2:
        child = pexpect.spawn(cmd_combine,timeout=2)
        r = child.read()
        #print r
        return (r,cmd_combine)
    #    child.kill(0)
    # else:
    #     r = child.read()
    #     #print r
    #     return (r,cmd_combine)

# operation(ip,user,cmd)

def multi_command(ip,user,cmd1,cmd2="free -m"):

    (r2,r2_cmd_combine) = operation(ip,user,cmd1)
    print r2_cmd_combine
    print r2
    if r2.find('redis-server') != -1 :
        (r3,r3_cmd_combine) = operation(ip,user,cmd2)
        print r3_cmd_combine
        print r3
        return r3
    else:
        print('Cannot find redis-server')
        print('Cannot find redis-server')
multi_command(ip,user,cmd)

#if __main___ == "__main__":
#    multi_command()



