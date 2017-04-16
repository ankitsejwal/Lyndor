import os, sys, message

def write(msg):
    sys.stdout.write(str(msg) + '\n')
    sys.stdout.flush()

def askContinue():
    write(message.ifcontinue)
    answer = raw_input().lower()
    return answer

def assignFolder(tempFolder):
    os.chdir(tempFolder)
    path = os.getcwd()
    return path


def listFiles(path):
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
    listFiles(path)
    rename(path)
