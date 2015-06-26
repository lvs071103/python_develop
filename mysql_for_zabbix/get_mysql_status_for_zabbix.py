#!/usr/bin/env python
#coding=utf8

import sys
import os
#import inspect
import MySQLdb
import MySQLdb.cursors

class GetMysqlStatus():
    def __init__(self):
        self.result = ''
        self.dict = {}
    def check(self, port):
        try:
            self.db = MySQLdb.connect(user="root", passwd="...",
                                      host="127.0.0.1", port=port,
                                      cursorclass=MySQLdb.cursors.DictCursor)
        except Exception, e:
            raise Exception, 'Cannot interface with MySQL server, %s' % e

    def extract(self):
        try:
            c = self.db.cursor()
            c.execute("""show global status;""")
            self.result = c.fetchall()
            for i in self.result:
                self.dict[i['Variable_name']] = i['Value']
            return self.dict
            c.close()
            self.db.close()
        except Exception, e:
            print e
    
    def get_val(self):
        return self.dict
    def dict_init(self):
        self.dict['TPS'] = int(self.dict['Com_commit']) + int(self.dict['Com_rollback'])
        self.dict['QPS'] = int(self.dict['Com_insert']) + int(self.dict['Com_delete']) + int(self.dict['Com_select']) + int(self.dict['Com_update'])

        if self.dict['Key_read_requests'] != "0":
            self.dict['Key_read_hit_ratio'] = (1 - float(self.dict['Key_reads'])  / float(self.dict['Key_read_requests'])) * 100
        else:
            self.dict['Key_read_hit_ratio'] = 0

        if self.dict['Key_blocks_used'] != "0" or self.dict['Key_blocks_unused'] != "0":
            self.dict['Key_usage_ratio'] = float(self.dict['Key_blocks_used']) / (float(self.dict['Key_blocks_used']) + float(self.dict['Key_blocks_unused']))
        else:
            self.dict['Key_usage_ratio'] = 0
        
        if self.dict['Key_write_requests'] != "0":
            self.dict['Key_write_hit_ratio'] = (1 - float(self.dict['Key_writes']) / float(self.dict['Key_write_requests'])) * 100
        else:
            self.dict['Key_write_hit_ratio'] = 0

        if self.dict['Innodb_buffer_pool_read_requests'] != "0":
            self.dict['Innodb_buffer_read_hit_ratio'] = (1 - float(self.dict['Innodb_buffer_pool_reads']) / float(self.dict['Innodb_buffer_pool_read_requests'])) * 100
        else:
            self.dict['Innodb_buffer_read_hit_ratio'] = 0

        if self.dict['Innodb_buffer_pool_pages_total'] != "0":
            self.dict['Innodb_buffer_usage'] = (1 - float(self.dict['Innodb_buffer_pool_pages_free']) / float(self.dict['Innodb_buffer_pool_pages_total'])) * 100
        else:
            self.dict['Innodb_buffer_usage'] = 0

        if self.dict['Innodb_buffer_pool_pages_total'] != "0":
            self.dict['Innodb_buffer_pool_dirty_ratio'] = (float(self.dict['Innodb_buffer_pool_pages_dirty']) / float(self.dict['Innodb_buffer_pool_pages_total'])) * 100
        else:
            self.dict['Innodb_buffer_pool_dirty_ratio'] = 0

class ErrorOut():
    def error_print(self):
        """输出错误信息"""
        print
        print 'Usage: ' + sys.argv[0] + ' ' + ' MySQL_Status_Key '
        print
        sys.exit(1)

class Main():
    def main(self):
        error = ErrorOut()
        if len(sys.argv) == 1:
            error.error_print()
        elif len(sys.argv) == 2:
            error.error_print()
        elif len(sys.argv) == 3:
            port = int(sys.argv[1])
            key = sys.argv[2]
            a = GetMysqlStatus()
            a.check(port)
            a.extract()
            a.dict_init()
	    new_dict = a.get_val()
            print new_dict[key]

if __name__ == "__main__":
     run = Main()
     run.main()
