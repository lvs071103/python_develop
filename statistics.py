#!/usr/bin/python
# -*- coding:utf-8 -*-
# author: Jack

import sys
import os
import subprocess
import logging
import time


def daemon():
    try:
        pid = os.fork()
        if pid > 0:
            # exit first parent
            sys.exit(0)
    except OSError as err:
        sys.stderr.write('_Fork #1 failed: {0}\n'.format(err))
        sys.exit(1)
    # decouple from parent environment
    os.chdir('/')
    os.setsid()
    os.umask(0)
    # do second fork
    try:
        pid = os.fork()
        if pid > 0:
            # exit from second parent
            sys.exit(0)
    except OSError as err:
        sys.stderr.write('_Fork #2 failed: {0}\n'.format(err))
        sys.exit(1)
    # redirect standard file descriptors
    sys.stdout.flush()
    sys.stderr.flush()
    si = open(os.devnull, 'r')
    so = open(os.devnull, 'w')
    se = open(os.devnull, 'w')
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())


def statistics():
    command = "netstat -ant | grep -i '2001' | grep ESTABLISHED | wc -l"
    number = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).communicate()[0].split('\n')[0]
    message = 'port 2001 tcp ESTABLISHED number: %s' % number
    return message

if __name__ == '__main__':
    daemon()
    while True:
        time.sleep(300)
        logging.basicConfig(level=logging.INFO, filename="/tmp/statistics.log", filemode="a+",
                            format="%(asctime)-15s %(levelname)-8s %(message)s")
        logging.info(statistics())
