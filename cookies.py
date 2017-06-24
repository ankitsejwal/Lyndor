import os
import sys
import message

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
    for f1 in os.listdir(desktop_folder):
        if f1 == 'cookies.txt':
            print message.COOKIE_FOUND_DESKTOP
            return desktop_folder + '/cookies.txt'
    for f2 in os.listdir(download_folder):
        if f2 == 'cookies.txt':
            print message.COOKIE_FOUND_DOWNLOAD
            return download_folder + '/cookies.txt'
    sys.exit(message.COOKIE_NOT_FOUND_ERROR)
