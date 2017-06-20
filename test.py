import urllib2
import re
import install
import os
import run

real_path = os.path.realpath(__file__)
real_path = real_path[:real_path.find('test.py')]
print real_path