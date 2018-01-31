''' Rename videos and subtitle, also write content.md '''

import os, re, shutil, sys
import message
from colorama import *

def write(msg):
    '''prints out any message'''
    sys.stdout.write(str(msg) + '\n')
    sys.stdout.flush()

def assign_folder(folder):
    ''' return folder path '''
    os.chdir(folder)
    path = os.getcwd()
    return path   

def hms_string(sec_elapsed):
    ''' format elapsed time '''
    hour = int(sec_elapsed / (60 * 60))
    minutes = int((sec_elapsed % (60 * 60)) / 60)
    seconds = sec_elapsed % 60.
    return "{}:{:>02}:{:>05.2f}".format(hour, minutes, seconds)
