# -*- coding:UTF-8 -*-
#py2
'''
OpenSSL受戒礼和Freak漏洞检测脚本
2016.07
'''

import paramiko
import os

import sys
server = []
sjl_sign = "Server certificate\n"
freak_sign = "Server certificate\n"

ip = raw_input("Please Input Plart IP:")
username = raw_input("Username:")
pwd = raw_input("Password:")

def scan(ip):
    # for line in read.readlines():
    #     server.append(line)
    # for i in server:
    #     i = i.strip("\n")  # 去掉行末换行符
    cmd_sjl = "openssl s_client -connect" + " " + ip + ":443 -cipher RC4"
    cmd_freak = "openssl s_client -connect" + " " + ip + ":443 -cipher EXPORT"
    print "\nScanning %s..." % ip
    scanbody(ip, username, pwd, cmd_sjl, cmd_freak)

    print "\nAll Done"
    print "SSH"

def scanbody(ip, username, pwd, cmd_sjl, cmd_freak):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, 22, username, pwd)
        stdin, stdout, stderr = ssh.exec_command(cmd_sjl)
        sjl = stdout.readlines()
        stdin, stdout, stderr = ssh.exec_command(cmd_freak)
        freak = stdout.readlines()
        ssh.close()

        list_sjl = []
        list_freak = []

        for k in sjl:
            list_sjl.append(k)

        for j in freak:
            list_freak.append(j)

        if sjl_sign in list_sjl:
            if freak_sign in list_freak:
                print "[-]：存在OpenSSL受戒礼漏洞和Freak漏洞"
            else:
                print "[-]：存在OpenSSL受戒礼漏洞"
        else:
            if freak_sign in list_freak:
                print "[+]：不存在OpenSSLFreak漏洞"
            else:
                print "[+]：不存在OpenSSL受戒礼漏洞和Freak漏洞"
    except paramiko.AuthenticationException, e:
        print 'Error'
        print 'Error Detail', e


# GUI Program
if __name__ == '__main__':
    print("OpenSSL受戒礼和Freak漏洞检测程序")
    scan(sys.argv[1])
# 获取文件内容




