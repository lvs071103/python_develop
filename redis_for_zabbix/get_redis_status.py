#!/usr/bin/env python
#coding=utf8

import sys
import os
import redis

class GetRedisStatus():
    def __init__(self):
        self.val = {}
    def check(self, port):
        try:
            self.redis = redis.Redis('127.0.0.1', port=port, password=None)
        except:
            raise Exception, 'Plugin needs the redis module'

    def extract(self, key):
        info = self.redis.info()
        try:
            if key in info:
                self.val[key] = info[key]
            return self.val[key]
        except:
            raise Exception, 'ERROR info not include this key!'


def main():
    if len(sys.argv) == 1:
        print "ERROR! Please enter a parameter"
    if len(sys.argv) == 2:
        print "ERROR! Please enter a parameter"
    elif len(sys.argv) == 3:
        key = sys.argv[2]
        port= int(sys.argv[1])
        a = GetRedisStatus()
        a.check(port)
        print a.extract(key)

if __name__ == "__main__":
    main()
