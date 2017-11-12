import time
import sys
from colorama import *

ENTER_URL = " Paste the url of a Lynda course >>> "

NETSCAPE = '# Netscape HTTP Cookie File\n'

RENAMING_ERROR = "\nError in renaming file !!!"

INFO_FILE_CREATED = "\n-> info.txt file created\n"

COOKIE_NOT_FOUND_ERROR = "\n-> Oops!! Did you forget to put cookies.txt inside Downloads or Desktop folder ??\n"
    
def animate_characters(color, string, speed):
    '''printing ASCII arts line by line'''
    for line in string.splitlines():
        print color + line + Fore.RESET
        time.sleep(speed)

def spinning_cursor():
    '''spinning cursor'''
    flag = True
    while flag:
        for cursor in '\\|/-\\|/-  -':
            time.sleep(0.1)
            # Use '\r' to move cursor back to line beginning
            # Or use '\b' to erase the last character
            sys.stdout.write('\r{}'.format(cursor))
            # Force Python to write data into terminal.
            sys.stdout.flush()
        flag = False

def write(description, value):
    '''prints out any message'''
    sys.stdout.write(str(description) + '\t' + str(value) + '\n')
    sys.stdout.flush()

def print_line(value):
    ''' prints out any string '''
    sys.stdout.write(str(value) + '\n')
    sys.stdout.flush()

def colored_message(color, message):
    print(color + message + Fore.RESET)