# -*- coding=utf-8 -*-
# Zhaijiahui    https://github.com/zhaijiahui

import requests
import re
import os,sys,time
import threadpool
import random

from requests.packages.urllib3.exceptions import InsecureRequestWarning,InsecurePlatformWarning   # 屏蔽错误提示的一般方法，配合下面两个disable
import requests.packages.urllib3.util.ssl_                   # 解决部分ssl证书版本不正确的问题
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'


requests.packages.urllib3.disable_warnings(InsecureRequestWarning) # 移除ssl错误告警
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)
base = [str(x) for x in range(10)] + [ chr(x) for x in range(ord('A'),ord('A')+6)]

#十进制0~255转化为二进制,补0到8位
def dec2bin80(string_num):
    num = int(string_num)
    mid = []
    while True:
        if num == 0: break
        num,rem = divmod(num, 2)
        mid.append(base[rem])

    result = ''.join([str(x) for x in mid[::-1]])
    length = len(result)
    if length < 8:
        result = '0' * (8 - length) + result
    return result


#十进制0~255转化为二进制,补0到32位
def dec2bin320(string_num):
    num = int(string_num)
    mid = []
    while True:
        if num == 0: break
        num,rem = divmod(num, 2)
        mid.append(base[rem])

    result = ''.join([str(x) for x in mid[::-1]])
    length = len(result)
    if length < 32:
        result = '0' * (32 - length) + result
    return result


#十进制0~255转化为二进制，不补零
def dec2bin(string_num):
    num = int(string_num)
    mid = []
    while True:
        if num == 0: break
        num,rem = divmod(num, 2)
        mid.append(base[rem])

    return ''.join([str(x) for x in mid[::-1]])


#二进制转换为十进制
def bin2dec(string_num):
    return str(int(string_num, 2))

#ip列表生成
def iplist(string_startip,string_endip):

    #分割IP，然后将其转化为8位的二进制代码
    start = string_startip.split('.')
    start_a = dec2bin80(start[0])
    start_b = dec2bin80(start[1])
    start_c = dec2bin80(start[2])
    start_d = dec2bin80(start[3])
    start_bin = start_a + start_b + start_c + start_d
    #将二进制代码转化为十进制
    start_dec = bin2dec(start_bin)

    end = string_endip.split('.')
    end_a = dec2bin80(end[0])
    end_b = dec2bin80(end[1])
    end_c = dec2bin80(end[2])
    end_d = dec2bin80(end[3])
    end_bin = end_a + end_b + end_c + end_d
    #将二进制代码转化为十进制
    end_dec = bin2dec(end_bin)

    #十进制相减，获取两个IP之间有多少个IP
    count = int(end_dec) - int(start_dec)

    ip_list = []
    #生成IP列表
    for i in range(0,count + 1):
        #将十进制IP加一，再转化为二进制（32位补齐）
        plusone_dec = int(start_dec) + i
        plusone_dec = str(plusone_dec)
        address_bin = dec2bin320(plusone_dec)
        #分割IP，转化为十进制
        address_a = bin2dec(address_bin[0:8])
        address_b = bin2dec(address_bin[8:16])
        address_c = bin2dec(address_bin[16:24])
        address_d = bin2dec(address_bin[24:32])
        address = address_a + '.'+ address_b +'.'+ address_c +'.'+ address_d
        ip_list.append(address)
    return ip_list


def checkip(ip):
    p = re.compile(r'^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)')
    if p.match(ip):
        return True
    else:
        return False

def request(ip):
    headers_list = ['Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0',
'Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7A341 Safari/528.16',
'Mozilla/5.0 (iPhone; CPU iPhone OS 10_2_1 like Mac OS X) AppleWebKit/602.4.6 (KHTML, like Gecko) Version/10.0 Mobile/14D27 Safari/602.1',
'Mozilla/5.0 (iPhone; CPU iPhone OS 10_2_1 like Mac OS X; zh-CN) AppleWebKit/537.51.1 (KHTML, like Gecko) Mobile/14D27 UCBrowser/11.6.1.1003 Mobile  AliApp(TUnionSDK/0.1.20)']
    headers = { 'User-Agent': headers_list[random.randint(0,4)] }
    disclosure = {'/.svn/entries':'dir','/.git/config':'[core]','/.DS_Store':'','/WEB-INF/web.xml':'','/crossdomin.xml':'',
    '/icons/':'Index of'} # 敏感信息设置
    for u,j in disclosure.items():
        try:
            r = requests.get('http://'+ ip + u,headers=headers,timeout=3,verify=False)
            html = r.text
            if r.status_code == 200:
                if j in html:
                    print('Find: ' + 'http://'+ip + u +' is Leak !!!')
                else:
                    print('Find: ' + 'http://'+ip + u +' is Exist !!!')
        except Exception as e:
            try:
                r = requests.get('https://'+ ip + u,headers=headers,timeout=3,verify=False)
                html = r.text
                if r.status_code == 200:
                    if j in html:
                        print('Find: ' + 'https://'+ip + u +' is Leak !!!')
                    else:
                        print('Find: ' + 'https://'+ip + u +' is Exist !!!')
            except Exception as e:
                pass
    

def main():
    print('*'*35+'''\nIDscan V1.0 By Zhaijiahui\n
Information disclosure Check.\n'''+'*'*35)
    with open('url_list.txt','r') as f:
        url_list = f.readlines()
    pool = threadpool.ThreadPool(255)
    ipl = []
    for i in url_list:
        if 'http' in i:
            temp = i.split('://')
            ipl.append(temp[1].strip())
        elif '-' in i:
            start_ip,end_ip = i.split('-')
            ipl = iplist(start_ip,end_ip)
        elif checkip(i):
            ipl.append(i.strip())
        else:
            print('未知形式IP：'+i)
    # print(ipl)
    print('Start...')
    requests = threadpool.makeRequests(request, ipl)
    [pool.putRequest(req) for req in requests]
    pool.wait()

    print('End...')



if __name__ == '__main__':
    main()