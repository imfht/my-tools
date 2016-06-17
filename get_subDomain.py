#!/usr/bin/env python
#coding:utf-8
"""
  Author:  fiht --<fiht@qq.com>
  Purpose: 查找subDomain
  Created: 2016年06月16日
"""
import requests
from bs4 import BeautifulSoup
import time
try:
    from queue import Queue
except:
    from Queue import Queue
import threading
from termcolor import colored
import os
import sys
from optparse import OptionParser
banner = '''\
| |__   ___| | | ___   \ \      / /__  _ __| | __| |
| '_ \ / _ \ | |/ _ \   \ \ /\ / / _ \| '__| |/ _` |
| | | |  __/ | | (_) |   \ V  V / (_) | |  | | (_| |
|_| |_|\___|_|_|\___/     \_/\_/ \___/|_|  |_|\__,_|

Usage: python get_subDomain filename 
the result will save as {filename}_subDomains
'''
#----------------------------------------------------------------------
"""return None 有点问题,但是不想折腾了"""
def get_subDomain(url):
    """返回子域名list"""
    try:
        req =requests.post('http://i.links.cn/subdomain/',data='domain=%s&b2=1&b3=1&b4=1'%url,headers={'Content-Type': 'application/x-www-form-urlencoded'},timeout=10)
    except Exception as e:
        print(e)
        return None
    return_value = []
    sub_domains = BeautifulSoup(req.text,'lxml').findAll(rel='nofollow')
    if len(sub_domains)==2:
        return_value.append(url)
        return return_value
    for i in sub_domains:
        return_value.append(i.string)
    return return_value
que = Queue()
target = ''
#----------------------------------------------------------------------
def run_thread():
    """"""
    while(not que.empty()):
        url = que.get()
        sub_domains = get_subDomain(url)
        if not sub_domains: # 返回None
            print('[-]%s 获取超时,重新推回队列'%url)
            que.put(url)
        else:
            print(colored('[+] %s寻找完毕'%url,'green'))
            for i in sub_domains:
                target.writelines(i+'\n')
#----------------------------------------------------------------------
if __name__=='__main__':
    """"""
    parser = OptionParser()
    print(banner)
    if len(sys.argv) < 2:
        print(colored('[ERROR] Please input a filename!','red'))
        sys.exit(0)
    an_loney_list = []
    target = open(sys.argv[1]+'_subDomain','w+')
    with open(sys.argv[1]) as e:
        for i in e.readlines():
            i = i.strip('\n')
            if i not in an_loney_list: # 主要是去重
                an_loney_list.append(i)
            else:
                pass
    for i in an_loney_list:
        que.put(i)
    threads = [threading.Thread(target=run_thread) for i in range(0,50)]
    for i in threads:
        i.start()
        i.join()

