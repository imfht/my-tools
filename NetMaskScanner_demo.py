#encoding:utf-8
import re

import nmap
import requests

from loggerutil import logger_util


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
        print("Len of hosts_list: %s"%len(hosts_list))
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


########################################################################
if __name__ == '__main__':
    # parser = OptionParser()
    # parser.add_option('-n', '--netmask', default='24', help='子网数量')
    # parser.add_option('-p', '--port', default='80', help='指定端口')
    # (options, args) = parser.parse_args()
    # if not args:
    #     parser.print_usage()
    # else:
    #     An_IP.run(args[0], options.netmask, options.port)
#    print (Util.get_ip_by_netmask('202.194.14.1','80',28)) --> success
    things = ["http://%s/"%i for i in Util.get_ip_by_netmask('202.194.14.1','80',28).keys()]
    print(things)
    print(Util.multi_thread_get_title_by_url(things))
