# -*- coding: utf-8 -*-
import pexpect
import sys

ip = sys.argv[1]
user = sys.argv[2]
cmd = sys.argv[3]

cmd_combie = 'ssh ' + user +'@' + ip
#print cmd_combie

child = pexpect.spawn(cmd_combie,timeout=2)
i = child.expect(["password:","[roger@localhost ~]$",pexpect.TIMEOUT])
if i == 0:
    child.kill(0)
elif i == 1:
    cmd_final = cmd_combie + " " + '"' + cmd + '"'
    child = pexpect.spawn(cmd_final)
    print cmd_final
    r = child.read()
    print r
elif i == 2:
    child.kill(0)

