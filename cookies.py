import os
import sys
import glob
import message
from colorama import *

def add_new_line(cookie, line):
    '''returns cookie file with NETSCAPE line'''
    with file(cookie, 'r') as original: data = original.read()
    with file(cookie, 'w') as modified: modified.write(line + data)
    return modified

def edit_hex_file(cookie):
    '''returns cookie file without carriage return'''
    with file(cookie, 'r') as f:
        newcontent = f.read().replace("\r\n", "\n")

    with file(cookie, 'w') as f:
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
    if not cookies:
        sys.exit(message.colored_message(Fore.LIGHTRED_EX,message.COOKIE_NOT_FOUND_ERROR))
    else:
        latest_cookie = max(cookies, key=os.path.getctime)
        message.colored_message(Fore.LIGHTGREEN_EX, '\nUsing latest cookie file: '+latest_cookie+ '\n')
        return latest_cookie
