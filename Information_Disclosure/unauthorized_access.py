#!/usr/bin/env python  
# -*- coding: utf-8 -*-

import MySQLdb
import pymongo
import socket
import ftplib
import optparse
import requests
from kazoo.client import KazooClient
from threading import Thread


MongoDB_unauthhost = []
Redis_unauthhost = []
MySQL_unauthhost = []
FTP_unauthhost = []
Memcached_unauthhost = []
ZooKeeper_unauthhost = []
Elasticsearch_unauthhost = []
CouchDB_unauthhost = []
Rsync_unauthhost = []
Docker_unauthhost = []
GitLab_unauthhost = []
solr_unauthhost = []
Hadoop_unauthhost = []
Dubbo_unauthhost = []
Jenkins_unauthhost = []
LDAP_unauthhost = []
Samba_unauthhost = []

def portFind(hosts, port, timeout=3):
    connCon = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connCon.settimeout(timeout)
    try:
        connCon.connect((hosts, port))
        connCon.close()
        return True
    except:
        return False


def connMySQL(hosts):
    for host in hosts:
        try:
            conn = MySQLdb.connect(host=host, user="root", passwd="")
            MySQL_unauthhost.append(host)
            conn.close()
        except:
            pass
    return MySQL_unauthhost


def connFtp(hosts):
    for host in hosts:
        try:
            ftp = ftplib.FTP(host)
            ftp.login('anonymous','anonymous')
            FTP_unauthhost.append(host)
        except:
            pass
    return FTP_unauthhost


def connMongoDB(hosts,port = 27017):
    for host in hosts:
        try:
            conn = pymongo.MongoClient(host,port,socketTimeoutMS=300)
            dbname = conn.database_names()
            if dbname:
                MongoDB_unauthhost.append(host)
                conn.close()
        except:
            pass
    return MongoDB_unauthhost


def connRedis(hosts,port = 6379):
    payload = '\x2a\x31\x0d\x0a\x24\x34\x0d\x0a\x69\x6e\x66\x6f\x0d\x0a'
    s = socket.socket()
    socket.setdefaulttimeout(10)
    for host in hosts:
        try:
            s.connect((host, port))
            s.send(payload)
            recvdata = s.recv(1024)
            if recvdata and 'redis_version' in recvdata:
                Redis_unauthhost.append(host)
        except:
            pass
    return Redis_unauthhost

def connMemcached(hosts,port = 11211):
    for host in hosts:
        payload = '\x73\x74\x61\x74\x73\x0a'
        s = socket.socket()
        socket.setdefaulttimeout(10)
        try:
            s.connect((host, port))
            s.send(payload)
            recvdata = s.recv(2048)
            s.close()
            if recvdata and 'STAT version' in recvdata:
                Memcached_unauthhost.append(host)
        except:
            pass
        return Memcached_unauthhost

def connZookeeper(hosts,port = 2181):
    for host in hosts:
        try:
            connZK = KazooClient(hosts="%s:2181" % host,timeout=10)
            connZK.start()
            if connZK:
                ZooKeeper_unauthhost.append(host)
        except:
            pass
    return ZooKeeper_unauthhost

def connElasticsearch(hosts,port = 9200):
    Dic = ['_nodes','_rive','_cat']
    for host in hosts:
        try:
            for Dir in Dic:
                url = 'http://%s:%s/%s/' % (host,port,Dir)
                content = requests.get(url,timeout=5,allow_redirects=True,verify=False).content
                if '_river' in content:
                    Elasticsearch_unauthhost.append(host)
        except:
            pass
    return Elasticsearch_unauthhost

def connJenkins(hosts,port = 8080):
    Dic = ['manage','script']
    for host in hosts:
        try:
            for Dir in Dic:
                url = 'http://%s:%s/%s/' % (host,port,Dir)
                res_code = requests.get(url, timeout=5, allow_redirects=True, verify=False).status_code
                if res_code == 200:
                    Jenkins_unauthhost.append(host)
        except:
            pass
    return Jenkins_unauthhost

def connHadoop(hosts,port = 50070):
    for host in hosts:
        try:
            url = 'http://%s:%s/' % (host,port)
            res_code = requests.get(url, timeout=5, allow_redirects=True, verify=False).status_code
            if res_code == 200:
                Hadoop_unauthhost.append(host)
        except:
            pass
    return Hadoop_unauthhost

def connCouchDB(hosts,port = 5984):
    for host in hosts:
        try:
            url = 'http://%s:%s/_config/' % (host,port)
            res_code = requests.get(url, timeout=5, allow_redirects=True, verify=False).status_code
            if res_code == 200:
                CouchDB_unauthhost.append(host)
        except:
            pass
    return CouchDB_unauthhost

def connDocker(hosts,port = 2375):
    Dic = ['/containers/json','/api/','/v1','/v2','']
    for host in hosts:
        try:
            for Dir in Dic:
                url = 'http://%s:%s/%s' % (host,port,Dir)
                res_code = requests.get(url, timeout=5, allow_redirects=True, verify=False).status_code
                if res_code == 200:
                    Docker_unauthhost.append(host)
        except:
            pass
    return Docker_unauthhost


def vul_Check(hosts):
    if portFind(hosts, 27017):
        connMongoDB(hosts)
    elif portFind(hosts, 6397):
        connRedis(hosts)
    elif portFind(hosts,11211):
        connMemcached(hosts)
    elif portFind(hosts,21):
        connFtp(hosts)
    elif portFind(hosts,2181):
        connZookeeper(hosts)
    elif portFind(hosts,9200):
        connElasticsearch(hosts)
    elif portFind(hosts,8080):
        connJenkins(hosts)
    elif portFind(hosts,6984):
        connMySQL(hosts)
    elif portFind(hosts,2375):
        connDocker(hosts)
    elif portFind(hosts,5984):
        connCouchDB(hosts)
    elif portFind(hosts,50070):
        connHadoop(hosts)


def parseInputAndvulCheck():
    parser = optparse.OptionParser("usage%prog " + "--host <target host> -f <ip_file>")
    parser.add_option('-f', action="store",dest='filename',help='the targets of file')
    parser.add_option('--host', dest='target', type='string', help='the targets of ip')
    (options, args) = parser.parse_args()
    targetHosts = str(options.targetHost).split(',')
    filename = options.filename
    if filename != None:
        f = open(filename)
        hosts = f.readlines()
        thread_list = []
        for i in xrange(10):
            t = Thread(target=vul_Check, args=hosts)
            thread_list.append(t)
        for t in thread_list:
            t.start()
        for t in thread_list:
            t.join()
    else:
        thread_list = []
        for i in xrange(10):
            t = Thread(target=vul_Check, args=targetHosts)
            thread_list.append(t)
        for t in thread_list:
            t.start()
        for t in thread_list:
            t.join()
    f.close()


def printResults():
    while len(FTP_unauthhost) > 0:
        print FTP_unauthhost.pop() + ' : ' + 'FTP Unauthorized Access Succeeded'
    while len(MongoDB_unauthhost) > 0:
        print MongoDB_unauthhost.pop() + ' : ' + 'MongoDB Unauthorized Access Succeeded'
    while len(Redis_unauthhost) > 0:
        print Redis_unauthhost.pop() + ' : ' + 'Redis Unauthorized Access Succeeded'
    while len(Memcached_unauthhost) > 0:
        print Memcached_unauthhost.pop() + ' : ' + 'Memcached Unauthorized Access Succeeded'
    while len(MySQL_unauthhost) > 0:
        print MySQL_unauthhost.pop() + ' : ' + 'MySQL Unauthorized Access Succeeded'
    while len(ZooKeeper_unauthhost) > 0:
        print ZooKeeper_unauthhost.pop() + ' : ' + 'ZooKeeper Unauthorized Access Succeeded'
    while len(Elasticsearch_unauthhost) > 0:
        print Elasticsearch_unauthhost.pop() + ' : ' + 'Elasticsearch Unauthorized Access Succeeded'
    while len(Jenkins_unauthhost) > 0:
        print Jenkins_unauthhost.pop() + ' : ' + 'Jenkins Unauthorized Access Succeeded'
    while len(Docker_unauthhost) > 0:
        print Docker_unauthhost.pop() + ' : ' + 'Docker Unauthorized Access Succeeded'
    while len(CouchDB_unauthhost) > 0:
        print CouchDB_unauthhost.pop() + ' : ' + 'CouchDB Unauthorized Access Succeeded'
    while len(Hadoop_unauthhost) > 0:
        print Hadoop_unauthhost.pop() + ' : ' + 'Hadoop Unauthorized Access Succeeded'


if __name__ == ' __main__ ':
    parseInputAndvulCheck()
    printResults()