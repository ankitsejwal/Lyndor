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

def rename(path):
    ''' Rename files '''

    message.colored_message(Fore.LIGHTYELLOW_EX, '\nRenaming videos to arrange them in correct order:\n')
    # Rename video files
    for vid in os.listdir(path):
        if vid.endswith('.mp4'):
            vid_name, vid_ext = os.path.splitext(vid)
            vid_no = vid_name[-4:]
            vid_title = vid_name[:-7]
            vid_title = re.sub('[^a-zA-Z0-9.,-]', ' ', vid_title)
            new_file = '{}-{}{}'.format(vid_no, vid_title, vid_ext)
            os.rename(vid, new_file)
            write(new_file)

    message.colored_message(Fore.LIGHTYELLOW_EX, '\nRenaming subtitles to match them with videos:\n')    
    # Rename subtitle files
    for sub in os.listdir(path):
        if sub.endswith('.srt'):
            sub_name, sub_ext = os.path.splitext(sub)
            sub_no = sub_name[-7:-3]
            sub_title = sub_name[:-10]
            sub_title = re.sub('[^a-zA-Z0-9.,-]', ' ', sub_title)
            new_file = '{}-{}{}'.format(sub_no, sub_title, sub_ext)
            os.rename(sub, new_file)
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
    '''execute functions'''
    # rename(path)
    write_content_md(path)
