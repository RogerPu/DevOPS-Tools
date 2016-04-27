# -*- coding: utf-8 -*-
import pexpect
import sys

ip = sys.argv[1]
user = sys.argv[2]
cmd = sys.argv[3]

def operation(ip,user,cmd):

    cmd_combie = 'ssh ' + user +'@' + ip

    child = pexpect.spawn(cmd_combie,timeout=2)
    i = child.expect(["password:",pexpect.TIMEOUT])
    if i == 0:
        child.kill(0)
    elif i == 1:
        child.kill(0)

    cmd_final = cmd_combie + " " + '"' + cmd + '"'
    child = pexpect.spawn(cmd_final)
    r = child.read()
    #print r
    return (r,cmd_final)


def multi_command(ip,user,cmd1,cmd2):

    (r2,r2_cmd_final) = operation(ip,user,cmd1)
    print r2_cmd_final
    print r2
    if r2.find("redis-server"):
        (r3,r3_cmd_final) = operation(ip,user,cmd2)
        print r3_cmd_final
        print r3

multi_command(ip,user,cmd,cmd2="free -m")

#if __main___ == "__main__":
#    multi_command()



