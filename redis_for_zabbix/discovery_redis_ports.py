#!/usr/bin/env python
#coding=utf-8

import json
import subprocess

if __name__ == '__main__':
    p1 = subprocess.Popen(['netstat', '-lntp'], stdout=subprocess.PIPE)
    p2 = subprocess.Popen(['grep', 'redis-server'], stdin=p1.stdout, stdout=subprocess.PIPE)
    p3 = subprocess.Popen(['awk', '{print $4}'],stdin=p2.stdout,stdout=subprocess.PIPE)
    p4 = subprocess.Popen(['awk', '{{split($0,ports,":");print ports[length(ports)]}}'], stdin=p3.stdout, stdout=subprocess.PIPE)
    p5 = subprocess.Popen(['sort'], stdin=p4.stdout, stdout=subprocess.PIPE)
    p6 = subprocess.Popen(['uniq'], stdin=p5.stdout, stdout=subprocess.PIPE)
    stdout, stderr = p6.communicate()
    data = list()
    for line in stdout.split('\n'):
        if line:
            data.append({"{#REDIS_PORT}": line})
    print(json.dumps({"data": data}, indent=4))
