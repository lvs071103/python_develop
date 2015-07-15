#!/usr/bin/env python
#coding=utf8

import sys
import os
import redis

class GetRedisStatus():
    def __init__(self):
        self.val = {}
    def check(self, port, db):
        try:
            self.redis = redis.Redis('127.0.0.1', port=port, db=db, password=None)
        except:
            raise Exception, 'Plugin needs the redis module'

    def flushdb(self):
        return self.redis.flushdb()

def main():
    if len(sys.argv) == 3:
        db = int(sys.argv[2])
        port = int(sys.argv[1])
        a = GetRedisStatus()
        a.check(port, db)
        result = a.flushdb()
        if result is True:
            print "fushdb ok"
    else:
        print "Usage: %s port db" %(sys.argv[0])

if __name__ == "__main__":
    main()
