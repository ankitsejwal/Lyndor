import urllib2
import re
import install
import os
import run
import time
import datetime

def hms_string(sec_elapsed):
    h = int(sec_elapsed / (60 * 60))
    m = int((sec_elapsed % (60 * 60)) / 60)
    s = sec_elapsed % 60.
    return "{}:{:>02}:{:>05.2f}".format(h, m, s)

start_time = time.time()
print 'program running'
end_time = time.time()
print "It took {} to execute this".format(hms_string(end_time - start_time))