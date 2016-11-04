#!/usr/bin/python
# -*- coding: utf8 -*-
# author: Jack

import os
import sys
import subprocess
import time
from subprocess import CalledProcessError
from subprocess import check_output
import logging
import json


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


def check_process_exists(name):
    zone_list = []
    command = "ps aux | grep %s | grep -v grep | grep -v '/bin/sh'| awk '{print $12}'" % name
    stdout = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True).communicate()[0]
    for line in stdout.split('\n'):
        if line:
            zone_list.append(line)
    return zone_list

def get_pid(name):
    try:
        command = "pidof %s" % name
        return map(int, check_output(command, shell=True, stderr=subprocess.STDOUT).split())        
    except subprocess.CalledProcessError as e:
        # raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
        return False

def reset_service(name, number):
    command = "cd /data/Server/Release/Bin && nohup ./%s %d 2>&1 > /data/logs/%s_%d.log &" % (name, number, name, number)
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        process.wait()
        message =  process.returncode
    except subprocess.CalledProcessError as e:
        message = e.returncode
    return message

def logging_out(message):
    logging.basicConfig(level=logging.INFO, filename="/tmp/Automatic_pull_up.log", filemode="a+",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")
    logging.info(message)


def run():
    p_name = 'FightServer2'
    while True:
        time.sleep(30)
        if not get_pid(p_name):
            for item in ['1', '2', '3']:
                if reset_service(p_name, int(item)) == 0:
                    logging_out(json.dumps("%s %d进程启动成功" % (p_name, int(item)), ensure_ascii=False, encoding='UTF-8'))
                else:
                    logging_out(json.dumps("%s %d进程启动成功" % (p_name, int(item)), ensure_ascii=False, encoding='UTF-8'))
        if len(get_pid(p_name)) == 3:
            messages = "FightServer2进程ID列表: %s" % get_pid(p_name)
            logging_out(json.dumps(messages, ensure_ascii=False, encoding='UTF-8'))

        elif len(get_pid(p_name)) > 0 and len(get_pid(p_name)) < 3:
            logging_out(json.dumps("进程数量异常,3秒后自动拉起", ensure_ascii=False, encoding='UTF-8'))
            for item in ['1', '2', '3']:
                if item not in check_process_exists(p_name):
                    if reset_service(p_name, int(item)) == 0:
                        logging_out(json.dumps("自动拉起%s %d进程成功" % (p_name, int(item)), ensure_ascii=False, encoding='UTF-8'))
                    else:
                        logging_out(json.dumps("自动拉起%s %d进程失败" % (p_name, int(item)), ensure_ascii=False, encoding='UTF-8'))
        else:
            logging_out(json.dumps("进程数大于3，有可能重复启动" % (p_name, int(item)), ensure_ascii=False, encoding='UTF-8'))

if __name__ == '__main__':
    daemon()
    run()
