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
        downloading_from_cookie = message.return_colored_message(Fore.LIGHTBLUE_EX, 'Downloading videos using cookies.txt')
        message.carriage_return_animate(downloading_from_cookie)
        cookies_not_found = message.return_colored_message(Fore.LIGHTRED_EX, "\
Oops!! Did you forget to put cookies.txt inside Downloads or Desktop folder ??\n")
        message.carriage_return_animate(cookies_not_found)
        sys.exit(message.colored_message(Fore.LIGHTRED_EX,'\nNote: if you wish to download course using username & password combination,\
\n      you should set ->  "use_cookie_for_download": false  in settings.json\n'))
    else:
        latest_cookie = max(cookies, key=os.path.getctime)
        latest_cookie_file = message.return_colored_message(Fore.LIGHTGREEN_EX, 'Using latest cookie file: '+latest_cookie+ '\n')
        message.carriage_return_animate(latest_cookie_file)
        return latest_cookie
