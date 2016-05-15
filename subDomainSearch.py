import requests
from bs4 import BeautifulSoup
from socket import getaddrinfo
from optparse import OptionParser
import sys
#----------------------------------------------------------------------
def get_subDomain(url):
    """返回子域名list"""
    req =requests.post('http://i.links.cn/subdomain/',data='domain=%s&b2=1&b3=1&b4=1'%url,headers={'Content-Type': 'application/x-www-form-urlencoded'},timeout=5)
    return_value = []
    for i in BeautifulSoup(req.text,'lxml').findAll(rel='nofollow'):
        return_value.append(i.string)
    return return_value
#----------------------------------------------------------------------
def getIPSet(url):
    """给定url找所有子域名对应的IP"""
    my_set = set()
    for i in get_subDomain(url):
        try:
            #print(i.strip('http://'))
            i = i.strip('http://')
            a,b,c,d = getaddrinfo(i,80)[2][4][0].split('.')
            my_set.add('%s.%s.%s.1'%(a,b,c))
        except Exception as e:
            #print(e,i)
            pass
    return my_set
if __name__=='__main__':
    parse = OptionParser('加入-c表示你想找C段的IP')
    parse.add_option('-c',dest='C',help='打印子域名的IP,用来寻找C段')
    (options, args) = parse.parse_args()
    print(options,'--->',args)
    if options.C: # 需要打印C段
        printIP(options.C)    
    elif len(args)<1:
        parse.print_usage()
        sys.exit(0)
    else:
        for i in get_subDomain(args[0]):
            print(i)