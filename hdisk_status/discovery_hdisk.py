#!/usr/bin/env python
#coding=utf-8

import json
import subprocess

if __name__ == '__main__':
    p1 = subprocess.Popen(['cat', '/proc/diskstats'], stdout=subprocess.PIPE)
    p2 = subprocess.Popen(['awk', '{print $3}'],stdin=p1.stdout,stdout=subprocess.PIPE)
    p3 = subprocess.Popen(['grep', '-v',  'ram\|loop\|sr\|sda[0-9]\{1\}\|sdb[0-9]\{1\}\|dm-[0-9]\{1\}'], stdin=p2.stdout, stdout=subprocess.PIPE)
    stdout, stderr = p3.communicate()
    data = list()
    for line in stdout.split('\n'):
        if line:
            data.append({"{#DEVICE}": line, "{#DEVICENAME}": line.replace("/dev/", "")})
    print(json.dumps({"data": data}, indent=4))
