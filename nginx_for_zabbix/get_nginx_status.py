#!/usr/bin/env python

import urllib2
import re
import sys

def Usage():
    print "Usage: %s [Active connections|accepts|handled|requests|request_time|Reading|Writing|Waiting]" %(sys.argv[0])
    sys.exit(2)

def main():
    url = 'http://127.0.0.1:61709'
    data = urllib2.urlopen(url)
    result = data.read()
    #print result
    DICT = {}
    a = re.findall(r'\d{1,8}', result)

    DICT['Active'] = a[0]
    DICT['accepts'] = a[1]
    DICT['handled'] = a[2]
    DICT['requests'] = a[3]
    DICT['request_time'] = a[4]
    DICT['Reading'] = a[5]
    DICT['Writing'] = a[6]
    DICT['Waiting'] = a[7]

    if len(sys.argv) != 2:
        Usage()
    
    if sys.argv[1] in DICT:
        print DICT[sys.argv[1]]
    else:
        print "unknown key!!"

if __name__ == "__main__":
    main()
