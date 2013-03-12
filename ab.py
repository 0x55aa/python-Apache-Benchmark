# coding:utf-8

import sys
import getopt
import re

import test

VERSION = '0.0.1'
ARG = {'-n requests':'Number of requests to perform',
       '-h':'Display usage information (this message)',
       '-V':'Print version number and exit',
       '-c concurrency':'Number of multiple requests to make',
       '-e filename':'Output CSV file with percentages served',
       '-p postfile':' File containing data to POST. Remember also to set -T',
       '-H attributefile':"Add Arbitrary header line, eg.{'Accept-Encoding': \
'gzip'}Inserted after all normal header lines. (repeatable)",


       }




def usage():
    """
    帮助信息
    """
    print 'Usage: ab.py [options] [http://]hostname/path'
    print 'Options are:'

    for i in ARG:
        print '\t%-12s\t%s' % (i,ARG[i])


def deal_argv():
    """
    参数处理
    """
    if len(sys.argv) < 2:
        print 'ab.py: wrong number of arguments'
        usage()
        sys.exit()
    try:
        opts, args = getopt.getopt(sys.argv[1:], "Vhn:c:e:p:H:", ["help",])
    except getopt.GetoptError as err:
        print str(err)
        usage()
        sys.exit(2)
    for o,a in opts:
        if o == "-n":
            test.requests = int(a)
        elif o == "-c":
            test.concurrency_number = int(a)
        elif o == "-e":
            test.filename = a
        elif o == "-p":
            f = open(a,'r')
            test.postfile = f.read()
            f.close()
        elif o == "-H":
            f = open(a,'r')
            test.attribute = f.read()
            f.close()
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o == "-V":
            print "this is ab.py,Version %s" % VERSION
            sys.exit()
            
        else:
            assert False, "unhandled option"

    #url匹配 ^http://[\d\-a-zA-Z]+(\.[\d\-a-zA-Z]+)*/?$
    p = re.compile('^http://[\d\-a-zA-Z]+(\.[\d\-a-zA-Z]+)*/?$')
    if args and p.match(args[0]):
        test.url = args[0]
        #print args[0],url
    else:
        print 'ab.py: invalid URL.try again'
        usage()
        sys.exit()
        

if __name__ == "__main__": 
    deal_argv()
    t = test.Test(requests = test.requests,
             concurrency_number = test.concurrency_number,
             filename = test.filename,
             postfile = test.postfile,
             attribute = test.attribute,
             url = test.url,
             )
    t.thread_main()
