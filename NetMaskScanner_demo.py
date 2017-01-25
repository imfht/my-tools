import requests
import re
from bs4 import BeautifulSoup
import ipaddress
import socket
import threading
import queue
import os
import nmap
from optparse import OptionParser
########################################################################
class An_IP():
    """"""
    #----------------------------------------------------------------------
    def __init__(self,ip,netmask=24,thread_num=255):
        """Constructor"""
        self.ip = ip
        self.netmask = netmask
        self.thread_num = thread_num
        self.alive_ip = []
    #----------------------------------------------------------------------
    def format_ip(ip):
        """format an IP"""
        return ip[0:ip.rfind('.')]+'.'+'0'
    
    def get_title(ip):
        """给定网址返回title值"""
        try:
            req = requests.get('http://%s'%ip,timeout=3)
            if req.status_code !=200:
                pass
            req.encoding = req.apparent_encoding
            pattern = re.compile('<title>(.*?)</title>')
            i = re.findall(pattern,req.text)
            if i:
                return i[0]
        except Exception as e:
            #print(e)
            pass
    #----------------------------------------------------------------------
    def my_thread(a_queue):
        """找title的线程驱动工具"""
        while(not a_queue.empty()):
            ip = a_queue.get()
            title = An_IP.get_title(ip)
            if title:
                print(ip,title)
    #----------------------------------------------------------------------
    def get_ip_list(ip,netmask=24):
        """给一个端口,以list的方式返回C段80的主机"""
        # print('正在扫描%s'%ip)
        nm = nmap.PortScanner()
        nm.scan(hosts='%s/%s'%(ip,netmask),ports='80',arguments='')
        hosts_list = [x for x in nm.all_hosts()]
        return hosts_list
    #----------------------------------------------------------------------
    def run(ip,netmask=24):
        """run test bt python nmap"""
        print('Scaning')
        nm = nmap.PortScanner()
        nm.scan(hosts='%s/%s'%(ip,netmask),ports='80',arguments='')
        print(nm.command_line())
        hosts_list = [(x, nm[x]['status'],['state']) for x in nm.all_hosts()]
        myqueue = queue.Queue()
        for i in hosts_list:
            myqueue.put(i[0])
            #GetUrl(i[0])
        print('端口扫描结束')
        threads = [threading.Thread(target=An_IP.my_thread(myqueue)) for i in range(0,10)]
        for i in threads:
            i.start()
            i.join()
#An_IP.get_ip_list('121.250.223.41',netmask=26)
########################################################################
if __name__=='__main1__':
    parser = OptionParser()
    parser.add_option('-n','--netmask',default='24',help='子网数量')
    (options,args) = parser.parse_args()
    if not args:
        parser.print_usage()
    else:
        An_IP.run(args[0],options.netmask)
#An_IP.run("47.90.0.106",netmask=24)
#From_Stack().return_thing()
