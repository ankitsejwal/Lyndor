#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' All printing messages and functions '''

import time
import sys
try:
    from colorama import *
except ImportError:
    pass

ENTER_URL = " 🚀 Paste the url of a Lynda course >>> "

NETSCAPE = '# Netscape HTTP Cookie File\n'

RENAMING_ERROR = "\nError in renaming file !!!"

INFO_FILE_CREATED = "\n🌟  info.txt created\n"

def animate_characters(color, string, speed):
    '''printing ASCII arts line by line'''
    # Ignore Unicode errors for systems with different locales
    try:
        for line in string.splitlines():
            print(color + line + Fore.RESET)
            time.sleep(speed)
    except UnicodeEncodeError:
        pass

def spinning_cursor():
    '''spinning cursor'''
    flag = True
    while flag:
        for cursor in '\\|/- ':
            time.sleep(0.2)
            # Use '\r' to move cursor back to line beginning
            # Or use '\b' to erase the last character
            sys.stdout.write('\r{}'.format(cursor))
            # Force Python to write data into terminal.
            sys.stdout.flush()
        flag = False

def write(description, value):
    '''prints out any message'''
    try:
        sys.stdout.write(str(description) + '\t' + str(value) + '\n')
    except UnicodeEncodeError:
        sys.stdout.write((description).encode('utf-8') + '\t' + (value).encode('utf-8') + '\n')

    sys.stdout.flush()

def print_line(value):
    ''' prints out any string '''
    try:
        sys.stdout.write(str(value) + '\n')
    except UnicodeEncodeError:
        sys.stdout.write((value).encode('utf-8'))

    sys.stdout.flush()

def colored_message(color, message):
    ''' print colored line ''' 
    print(color + message + Fore.RESET)

def return_colored_message(color, message):
    ''' return colored line '''
    return color + message + Fore.RESET

def carriage_return_animate(line):
    ''' print running line over an existing line '''
    for char in line:
        sys.stdout.write(char)
        time.sleep(0.01)
        sys.stdout.flush()
    sys.stdout.write('\r')
    time.sleep(0.1)
    sys.stdout.write("\033[K")
    
