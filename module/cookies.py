#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' Finds and edits cookie'''

import os, sys, glob
from module import message, read

try:
    from colorama import Fore
except ImportError:
    pass

def add_new_line(cookie, line):
    '''returns cookie file with NETSCAPE line'''
    # fix for python 2.x and 3.x
    try:
        with file(cookie, 'r') as original: data = original.read()
        with file(cookie, 'w') as modified: modified.write(line + data)
    except NameError:
        with open(cookie, 'r') as original: data = original.read()
        with open(cookie, 'w') as modified: modified.write(line + data)
    
    return modified

def edit_hex_file(cookie):
    '''returns cookie file without carriage return'''
    # fix for python 2.x and 3.x
    try:
        with file(cookie, 'r') as f:
            newcontent = f.read().replace("\r\n", "\n")
        with file(cookie, 'w') as f:
            newfile = f.write(newcontent)
    except NameError:
        with open(cookie, 'r') as f:
            newcontent = f.read().replace("\r\n", "\n")
        with open(cookie, 'w') as f:
            newfile = f.write(newcontent)       
    return newfile

def edit_cookie(cookie, line):
    '''this function edits cookie'''
    add_new_line(cookie, line)
    edit_hex_file(cookie)

def find_cookie(desktop_folder, download_folder):
    ''' Find the latest cookie file '''
    down_files = glob.glob(download_folder+'/*.txt')
    desk_files = glob.glob(desktop_folder+'/*.txt')
    files = down_files + desk_files
    cookies = [s for s in files if 'cookies' in s]
    if read.course_download_pref == 'cookies' or read.exfile_download_method == 'aria2':
        forgot_cookie = "Oops!! Did you forget to put 🍪  cookies.txt inside Downloads or Desktop folder ??\n"
        if not cookies:
            cookie_not_found = message.return_colored_message(Fore.LIGHTRED_EX, forgot_cookie)
            message.carriage_return_animate(cookie_not_found)
            sys.exit(message.colored_message(Fore.LIGHTRED_EX,'\nNote:\n\nIf you wish to download course using username & password combination,\
    \nyou should set ->  "course_download_pref": regular-login  in settings.json\n'))
        else:
            latest_cookie = max(cookies, key=os.path.getctime)
            latest_cookie_file = message.return_colored_message(Fore.LIGHTGREEN_EX, '🍪  Using latest cookie file: '+ latest_cookie + '\n')
            message.carriage_return_animate(latest_cookie_file)
            return latest_cookie
