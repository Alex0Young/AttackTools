import os
import time
#py2
filename = time.strftime('%Y%m%d_%H%M%S', time.localtime())+'seninfo.txt'
fileObj = open(filename)

def baseInfo():
    #all system info
    fileObj.writelines('\n+++++++Basic Info+++++++++++ \n')
    cmd = 'uname -a'
    fileObj.writelines('  ******'+cmd + '********* : \n')
    textlist = os.popen(cmd).readlines()
    for line in textlist:
        fileObj.writelines(line)

    #kernel version
    cmd = 'cat /proc/version'
    fileObj.writelines('  ********'+cmd + '*********** : \n')
    textlist = os.popen(cmd).readlines()
    for line in textlist:
        fileObj.writelines(line)
    #relese info
    cmd = 'cat /etc/*-release'
    fileObj.writelines('  ********'+cmd + '*********** : \n')
    textlist = os.popen(cmd).readlines()
    for line in textlist:
        fileObj.writelines(line)
    #cpu info
    cmd = 'cat /proc/cpuinfo'
    fileObj.writelines('  ********'+cmd + '*********** : \n')
    textlist = os.popen(cmd).readlines()
    for line in textlist:
        fileObj.writelines(line)
    #document info
    cmd = 'df -a'
    fileObj.writelines('  ********'+cmd + '*********** : \n')
    textlist = os.popen(cmd).readlines()
    for line in textlist:
        fileObj.writelines(line)

def UserInfo():
    #all user
    fileObj.writelines('\n +++User Info \n')
    cmd = 'cat /etc/passwd'
    fileObj.writelines('  ********'+cmd + '*********** : \n')
    textlist = os.popen(cmd).readlines()
    for line in textlist:
        fileObj.writelines(line)
    #all group
    cmd = 'cat /etc/group'
    fileObj.writelines('  ********'+cmd + '*********** : \n')
    textlist = os.popen(cmd).readlines()
    for line in textlist:
        fileObj.writelines(line)
    #all user hash
    cmd = 'cat /etc/shadow'
    fileObj.writelines('  ********'+cmd + '*********** : \n')
    textlist = os.popen(cmd).readlines()
    for line in textlist:
        fileObj.writelines(line)
    #now login
    cmd = 'who -a'
    fileObj.writelines('  ********'+cmd + '*********** : \n')
    textlist = os.popen(cmd).readlines()
    for line in textlist:
        fileObj.writelines(line)
    #now logined user and the process
    cmd = 'w'
    fileObj.writelines('  ********'+cmd + '*********** : \n')
    textlist = os.popen(cmd).readlines()
    for line in textlist:
        fileObj.writelines(line)
    #the uses logined
    cmd = 'last'
    fileObj.writelines('  ********'+cmd + '*********** : \n')
    textlist = os.popen(cmd).readlines()
    for line in textlist:
        fileObj.writelines(line)
    #the users last login
    cmd = 'lastlog'
    fileObj.writelines('  ********'+cmd + '*********** : \n')
    textlist = os.popen(cmd).readlines()
    for line in textlist:
        fileObj.writelines(line)

def SysInfo():
    #history command
    fileObj.writelines('\n +++System Info \n')
    cmd = 'history'
    fileObj.writelines('  ********'+cmd + '*********** : \n')
    textlist = os.popen(cmd).readlines()
    for line in textlist:
        fileObj.writelines(line)
    #useful shell
    cmd = 'cat /etc/shells'
    fileObj.writelines('  ********'+cmd + '*********** : \n')
    textlist = os.popen(cmd).readlines()
    for line in textlist:
        fileObj.writelines(line)

def FileInfo():
    fileObj.writelines('\n +++File Info \n')
    #find SUID file
    cmd = 'find / -perm -4000 -type f'
    fileObj.writelines('  ********'+cmd + '*********** : \n')
    textlist = os.popen(cmd).readlines()
    for line in textlist:
        fileObj.writelines(line)
    #find root  SUID file
    cmd = 'find / -uid 0 -perm -4000 -type f'
    fileObj.writelines('  ********'+cmd + '*********** : \n')
    textlist = os.popen(cmd).readlines()
    for line in textlist:
        fileObj.writelines(line)
    #find pass log
    cmd = ' grep -l -i pass /var/log/*.log'
    fileObj.writelines('  ********'+cmd + '*********** : \n')
    textlist = os.popen(cmd).readlines()
    for line in textlist:
        fileObj.writelines(line)
    #apache info
    cmd = 'apache2 -v'
    fileObj.writelines('  ********'+cmd + '*********** : \n')
    textlist = os.popen(cmd).readlines()
    for line in textlist:
        fileObj.writelines(line)
    #mysql info
    cmd = 'mysql --version'
    fileObj.writelines('  ********'+cmd + '*********** : \n')
    textlist = os.popen(cmd).readlines()
    for line in textlist:
        fileObj.writelines(line)
    #perl version
    cmd = 'perl -v'
    fileObj.writelines('  ********'+cmd + '*********** : \n')
    textlist = os.popen(cmd).readlines()
    for line in textlist:
        fileObj.writelines(line)
    #iptables info
    cmd = 'iptables -L'
    fileObj.writelines('  ********'+cmd + '*********** : \n')
    textlist = os.popen(cmd).readlines()
    for line in textlist:
        fileObj.writelines(line)
    #port info
    cmd = 'netstat -an'
    fileObj.writelines('  ********'+cmd + '*********** : \n')
    textlist = os.popen(cmd).readlines()
    for line in textlist:
        fileObj.writelines(line)
    #service info
    cmd = 'cat /etc/services'
    fileObj.writelines('  ********'+cmd + '*********** : \n')
    textlist = os.popen(cmd).readlines()
    for line in textlist:
        fileObj.writelines(line)


if __name__ == '__main__':
    baseInfo()
    UserInfo()
    SysInfo()
    FileInfo()