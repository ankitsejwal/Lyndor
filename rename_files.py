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

def hms_string(sec_elapsed):
    ''' format elapsed time '''
    hour = int(sec_elapsed / (60 * 60))
    minutes = int((sec_elapsed % (60 * 60)) / 60)
    seconds = sec_elapsed % 60.
    return "{}:{:>02}:{:>05.2f}".format(hour, minutes, seconds)
