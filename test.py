# coding:utf-8

import urllib
import urllib2
import threading
import time
import sys


requests = 1
concurrency_number = 1
#保存文件名
filename = ''
postfile = ''
attribute = ''
url = ''



class Test(object):
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        #print self.kwargs
        
        #self.data = None
        #response info
        self.info = ''
        #锁
        self.mutex = None
        #运行时间
        self.time = []
        #错误次数
        self.err_num = 0
        #包长度
        self.transfered = []
        
    def urlopen(self):
        """
        请求数据
        """
        try:
            if self.kwargs['postfile']:
                postdata = eval(self.kwargs['postfile'])
                postdata = urllib.urlencode(postdata)
                req = urllib2.Request(self.kwargs['url']+"?"+postdata)
            else:
                req = urllib2.Request(self.kwargs['url'],)
            if self.kwargs['attribute']:
                headerdata = eval(self.kwargs['attribute'])
                for i in headerdata:
                    req.add_header(i,headerdata[i])
            
            
            start_time = time.time()
            #req = urllib2.Request(self.kwargs['url'], postdata, headerdata)
            data = urllib2.urlopen(req)
            end_time = time.time()
            
            self.mutex.acquire()
            self.time.append(end_time - start_time)
            self.info = data.info()
            #print self.info['Content-Length'], len(self.data.read())
            self.transfered.append(len(data.read()))
            self.mutex.release()
        except urllib2.URLError, e:
            self.mutex.acquire()
            self.err_num +=1
            self.mutex.release()

    def print_result(self):
        """
        计算结果，打印
        """
        if self.kwargs['filename']:
            f = open(self.kwargs['filename'],'w')
            stdout = sys.stdout
            sys.stdout = f
            print "time:\n",self.time
            print "transferred:\n", self.transfered
            print "response:\n", self.info
            
        print '%-25s\t%s' % ("Complete requests:",self.kwargs['requests'] - self.err_num)
        print '%-25s\t%s' % ("Failed requests:",self.err_num)
        print '%-25s\t%s' % ("Total transferred:",sum(self.transfered))
        total_time = sum(self.time)
        print '%-25s\t%s' % ("Total time:", total_time)
        print '%-25s\t%s' % ("Requests per second:", self.kwargs['requests']/total_time)
        print '%-25s\t%s' % ("Time per request:", total_time/self.kwargs['requests'])

        print 'Percentage of the requests served within a certain time (ms)'
        timelist = sorted(self.time)
        def ctime(timelist,percentage):
            """
            计算百分比对应的时间
            """
            return int(timelist[int(len(timelist)*percentage)-1]*1000)
        print '%-5s\t%s' % ('50%', ctime(timelist,0.5))
        print '%-5s\t%s' % ('60%', ctime(timelist,0.6))
        print '%-5s\t%s' % ('75%', ctime(timelist,0.75))
        #print self.time
        

        
        if self.kwargs['filename']:
            f.close()
            sys.stdout = stdout


    def requesturl(self):
        i = 0
        #这里求需要次数=总请求数/一次请求数
        while i < (self.kwargs['requests']/self.kwargs['concurrency_number']):
            i += 1
            self.urlopen()

    def thread_main(self):
        """
        线程
        """
        print "--start--"
        threads = []
        self.mutex = threading.Lock()
        
        for x in xrange(self.kwargs['concurrency_number']):
            t = threading.Thread(target=self.requesturl,)
            threads.append(t)

        for t in threads:
            t.start()

        for t in threads:
            t.join()

        self.print_result()
        print "--end--"
        



if __name__ == "__main__": 
    a = Test()
    a.urlopen()
