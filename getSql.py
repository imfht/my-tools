import requests
from bs4 import BeautifulSoup
#----------------------------------------------------------------------
def get_url(url):
    """从给定的url中找打自己的网站的带有参数的链接(只返回一条)"""
    try:
        req = requests.get(url,timeout=5)
        soup = BeautifulSoup(req.text,'lxml')
        for i in soup.findAll('a'):
            if i.has_attr('href'):
                #print('+',i['href'])
                if 'http' not in i['href'] and '=' in i['href']:
                    #print('-',i['href'])
                    return url+'/'+i['href']
    except Exception as e:
        #print(e)
        return None
if __name__=='__main__':
    print('GetSql')
    print(get_url('http://www.hnfnu.edu.cn'))