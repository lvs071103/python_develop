#!/usr/bin/env python
#coding=utf8

import MySQLdb
import MySQLdb.cursors

class MySQL_Privilege_Manage():
    def __init__(self):
        self.sql = ''
    def check(self):
        try:
            self.db = MySQLdb.connect(user="root", passwd="...",
                                      host="192.168.1.60", port=3306,
                                      cursorclass=MySQLdb.cursors.DictCursor)
        except Exception, e:
            raise Exception, "Cannot interface with MySQL server, %s" % e

    def extract(self):
        try:
            c = self.db.cursor()
            #print(self.sql)
            c.execute(self.sql)
            c.execute("flush privileges")
            self.db.commit()
            c.close()
            self.db.close()
            print("complete")
        except Exception, e:
            print e

    def authorize(self, dbname, user, host, passwd):
        self.sql = "grant all privileges on %s.* to %s@'%s' identified by '%s';" % (dbname, user, host, passwd)
        return self.extract()

    def delautorize(self, user, host):
        self.sql = "drop user '%s'@'%s'" % (user, host)
        return self.extract()

    def modify_pass(self, user, newpasswd):
        self.sql = "UPDATE mysql.user SET Password = PASSWORD('%s') WHERE user = '%s'" % (newpasswd, user)
        return self.extract()

class main():
    def showmenu(self):
        prompt = """
         (A)uthorize MySQL user
         (D)elete MySQL user
         (M)odify password
         (Q)uit
         Enter choice: """

        while True:
            while True:
                try:
                    choice = raw_input(prompt).strip()[0].lower()
                except (EOFError, KeyboardInterrupt):
                    choice = 'q'

                print '\nYou picked: [%s]' % choice
                if choice not in 'admq':
                    print 'invalid option... try again'
                else:
                    break

            if choice == 'q':
                break

            if choice == 'a':
                try:
                    dbname = raw_input("Authorize database name: ")
                    user = raw_input("Authorize user name: ")
                    host = raw_input("Authorize remote host: ")
                    passwd = raw_input("Authorize password: ")
                    print "\ndbname is :%s, user is: %s, host: %s, password: %s" \
                          % (dbname, user, host, passwd)
                    opt = raw_input('Are you sure？[y or n]').lower()
                    if opt and opt[0] == 'y':
                        new = MySQL_Privilege_Manage()
                        new.check()
                        new.authorize(dbname, user, host, passwd)
                except (KeyboardInterrupt, EOFError):
                    break

            if choice == 'd':
                try:
                    user = raw_input("delete Authorize user: ")
                    host = raw_input("delete Authorize host: ")
                    print "\ndelete user name: %s, host: %s" % (user, host)
                    opt = raw_input('Are you Sure? [y or n]').lower()
                    if opt and opt[0] == 'y':
                        new = MySQL_Privilege_Manage()
                        new.check()
                        new.delautorize(user, host)
                except(KeyboardInterrupt, EOFError):
                    break

            if choice == 'm':
                try:
                    user = raw_input("Modfy password user name: ")
                    newpasswd = raw_input("new password: ")
                    print "\nModfy user name: %s, password: %s" % (user, newpasswd)
                    opt = raw_input('Are you Sure?[y or n]').lower()
                    if opt and opt[0] == 'y':
                        new = MySQL_Privilege_Manage()
                        new.check()
                        new.modify_pass(user, newpasswd)
                except(KeyboardInterrupt, EOFError):
                    break

if __name__ == '__main__':
    main().showmenu()
