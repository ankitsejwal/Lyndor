import os
import re
import sys
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

def list_files(path):
    ''' print all video files in current directory '''
    message.colored_message(Fore.LIGHTYELLOW_EX, '\nRenaming videos to arrange them in correct order:\n')
    for f in os.listdir(path):
        if f.endswith('.mp4'):
            f_name, f_ext = os.path.splitext(f)
            f_no = f_name[-3:]
            f_title = f_name[:-7]
            f_title = re.sub('[^a-zA-Z0-9.,-]', ' ', f_title)
            new_file = '{}-{}{}'.format(f_no, f_title, f_ext)
            write(new_file)

def rename(path):
    ''' Rename all video files '''
    for f in os.listdir(path):
        if f.endswith('.mp4'):
            f_name, f_ext = os.path.splitext(f)
            f_no = f_name[-3:]
            f_title = f_name[:-7]
            f_title = re.sub('[^a-zA-Z0-9.,-]', ' ', f_title)
            new_file = '{}-{}{}'.format(f_no, f_title, f_ext)
            os.rename(f, new_file)
            write(new_file)

def write_content_md(path):
    ''' write the saved videos to content_md files '''
    with open('CONTENT.md', 'a') as content_md:
        for f in os.listdir(path):
            if f.endswith('.mp4'):
                content_md.writelines('* ' + f + '\n')
    content_md.close()
    print("\n-> CONTENT.md is created.")

def hms_string(sec_elapsed):
    ''' format elapsed time '''
    h = int(sec_elapsed / (60 * 60))
    m = int((sec_elapsed % (60 * 60)) / 60)
    s = sec_elapsed % 60.
    return "{}:{:>02}:{:>05.2f}".format(h, m, s)

def execute(path):
    '''lists file to be renamed and rename files'''
    list_files(path)
    rename(path)
    write_content_md(path)
