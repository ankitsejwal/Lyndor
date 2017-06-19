import os
import sys
import message

found = False

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
    '''check to see if cookie exist in desktop or download folder'''
    found = False
    for f1 in os.listdir(desktop_folder):
        if f1 == "cookies.txt":
            found = True
        if found:
            print "\ncookie file found at Desktop folder\n"
            return desktop_folder + '/cookies.txt'
        else:
            for f2 in os.listdir(download_folder):
                if f2 == "cookies.txt":
                    found = True
                if found:
                    print "\ncookie file found at Download folder\n"
                    return download_folder + '/cookies.txt'
                # else:
                #     print "cookie not found"
                #    # sys.exit(message.COOKIE_NOT_FOUND_ERROR)
