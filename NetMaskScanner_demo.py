# encoding:utf-8
import re
from optparse import OptionParser

import nmap
import requests
from loggerutil import logger_util
import json

########################################################################
class Util:
    """Util Of Scanpy."""

    @staticmethod
    # ----------------------------------------------------------------------
    def get_ip_by_netmask(ip, port, netmask):
        """return {ip:product}, which port is open from ip's netmask"""
        print('Scaning')
        return_value = {}
        nm = nmap.PortScanner()
        nm.scan(hosts='%s/%s' % (ip, netmask), ports=port, arguments='')
        print(nm.command_line())
        hosts_list = [(x, nm[x]['tcp'][int(port)]['product']) for x in nm.all_hosts()]
        print("Len of hosts_list: %s" % len(hosts_list))
        for i in hosts_list:
            if 1:
                return_value[i[0]] = i[1]
            else:
                print("I pass")
        return return_value

    # ----------------------------------------------------------------------
    @staticmethod
    def get_title_by_url(url, timeout=5, pattern='<title>(.*?)</title>'):
        """return {url:title}, if title do not find we return{url:None}"""
        try:
            raw_http = requests.get(url, timeout=timeout)
        except requests.ConnectionError or requests.ConnectTimeout:
            logger_util.log_warning('Connect failed to %s ' % url)
            return None
        title = re.findall(pattern, raw_http.text)
        if not title:
            logger_util.log_debug('This page do not have title %s' % url)
            return {url: None}
        else:
            return {url: title[0]}

    # ----------------------------------------------------------------------
    @staticmethod
    def multi_thread_get_title_by_url(urllist, threads_num=50):
        """a commom spider frame, default use 50 threads"""
        from multiprocessing.dummy import Pool as TheadPool
        pool = TheadPool(processes=threads_num)
        things = pool.map(Util.get_title_by_url, urllist)  # @todo need add timeout and pattern to finish the frame
        pool.close()
        pool.join()
        return things

    @staticmethod
    def url_maker(iplist, port, scheme):
        '''return a list of url use ip,port and scheme
        example:
            url_maker(['1.1.1.1','2.2.2.2'],'8080','http')
        will return:
            ['http://1.1.1.1:8080/','http://2.2.2.2:8080/']
        '''
        return ['%s://%s:%s' % (scheme,i,port) for i in iplist]
    @staticmethod
    def run(ip, port, netmask):
        hosts = Util.get_ip_by_netmask(ip, port, netmask).keys() # @todo 接收这个函数返回的banner信息
        titles = Util.get_title_by_url(Util.url_maker(hosts,port,'http'))
        return titles
########################################################################
if __name__ == '__main__':
    parser = OptionParser()
    parser.usage='''
        example: python NetMaskScanner_demo.py -p 8080 -n 24 202.194.14.166
    '''
    parser.add_option('-n', '--netmask', default='24', help='子网数量')
    parser.add_option('-p', '--port', default='80', help='指定端口')
    parser.add_option('-f','--file',help='将结果写入文件')
    (options, args) = parser.parse_args()
    if not args:
        parser.print_usage()
    else:
        results = Util.run(args[0], options.netmask, options.port)
        print('报告小主，找到了 %s 个目标' % len(results))
        if options.file:
            with open(options.file,'w+') as f:

                json.dump(results,f,ensure_ascii=False)
        else:
            import sys
            json.dump(results,fp=sys.stdout,ensure_ascii=False)
    #    print (Util.get_ip_by_netmask('202.194.14.1','80',28)) --> success
