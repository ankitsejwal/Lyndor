import os
import sys
import message

def write(msg):
    '''prints out any message'''
    sys.stdout.write(str(msg) + '\n')
    sys.stdout.flush()

def ask_continue():
    write(message.IF_CONTINUE)
    answer = raw_input().lower()
    return answer

def assign_folder(tempFolder):
    os.chdir(tempFolder)
    path = os.getcwd()
    return path


def list_files(path):
    for f in os.listdir(path):
        if not (f.endswith('.txt') or f.startswith('.')):
            f_name, f_ext = os.path.splitext(f)
            f_no = f_name[-3:]
            f_title = f_name[:-7]
            new_file = '{}-{}{}'.format(f_no, f_title, f_ext)
            write(new_file)

def rename(path):
    counter = 0
    for f in os.listdir(path):
        if not (f.endswith('.txt') or f.startswith('.')):
            f_name, f_ext = os.path.splitext(f)
            f_no = f_name[-3:]
            f_title = f_name[:-7]
            new_file = '{}-{}{}'.format(f_no, f_title, f_ext)
            os.rename(f, new_file)
            write(new_file)
            counter += 1
    write('\n'+str(counter)+' files renamed !!!\n')

def execute(path):
    '''lists file to be renamed and rename files'''
    list_files(path)
    rename(path)
