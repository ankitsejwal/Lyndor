import os
import re
import sys
import message

def write(msg):
    '''prints out any message'''
    sys.stdout.write(str(msg) + '\n')
    sys.stdout.flush()

def assign_folder(folder):
    os.chdir(folder)
    path = os.getcwd()
    return path

def list_files(path):
    print '\n-> Renaming videos to arrange them beautifully:\n'
    for f in os.listdir(path):
        if f.endswith('.mp4'):
            f_name, f_ext = os.path.splitext(f)
            f_no = f_name[-3:]
            f_title = f_name[:-7]
            f_title = re.sub('[^a-zA-Z0-9.,-]', ' ', f_title)
            new_file = '{}-{}{}'.format(f_no, f_title, f_ext)
            write(new_file)

def rename(path):
    counter = 0
    for f in os.listdir(path):
        if f.endswith('.mp4'):
            f_name, f_ext = os.path.splitext(f)
            f_no = f_name[-3:]
            f_title = f_name[:-7]
            f_title = re.sub('[^a-zA-Z0-9.,-]', ' ', f_title)
            new_file = '{}-{}{}'.format(f_no, f_title, f_ext)
            os.rename(f, new_file)
            write(new_file)
            counter += 1
    write('\n-> '+str(counter)+' files downloaded and renamed to course folder !!')

def hms_string(sec_elapsed):
    h = int(sec_elapsed / (60 * 60))
    m = int((sec_elapsed % (60 * 60)) / 60)
    s = sec_elapsed % 60.
    return "{}:{:>02}:{:>05.2f}".format(h, m, s)

def execute(path):
    '''lists file to be renamed and rename files'''
    list_files(path)
    rename(path)
