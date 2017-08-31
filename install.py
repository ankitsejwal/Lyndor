import os
import sys
import message
import shutil
from colorama import *

real_path = os.path.realpath(__file__)
real_path = real_path[:real_path.find('install.py')]
RESET_PATH = real_path

def check_os():
    '''Check operating system'''
    if sys.platform.lower() == 'darwin':
        return 'macos'
    elif sys.platform.lower() == 'win32':
        return 'windows'
    elif sys.platform.lower() == 'linux2':
        return 'linux'
    else:
        sys.exit('unknown operating system.')

def set_path():
    '''Set path for saving lynda folder'''
    if check_os() == 'macos':
        os.chdir(os.path.expanduser('~/Movies'))
        return os.getcwd()
    elif check_os() == 'windows':
        os.chdir(os.path.expanduser('~/Videos'))
        return os.getcwd()

def folder_path(folder):
    '''Set path for desktop folder'''
    if check_os() == 'macos':
        os.chdir(os.path.expanduser('~/'+folder))
        return os.getcwd()
    elif check_os() == 'windows':
        os.chdir(os.path.expanduser('~/'+folder))
        return os.getcwd()

def create_folder():
    ''' Create lynda folder '''
    if not os.path.exists('Lynda'):
        os.makedirs('Lynda')
        message.print_line('>>> Your Lynda videos will be saved at -> '+ set_path() +'/Lynda (folder)\n')
    else:
        message.print_line('\nLynda folder already exists\n')

def create_aliases():
    '''Create aliases file'''
    os.chdir(RESET_PATH)
    if check_os() == 'windows':
        run_path = 'doskey lynda= python "'+os.getcwd()+'/run.py"'
        alias = open('aliases.bat', 'w')
        alias.write(run_path)
        alias.close()
        message.print_line('-> aliases.bat file created.\n')

def lynda_folder_files():
    ''' create lynda.bat in windows '''
    os.chdir(RESET_PATH)
    bulk_download = open('Bulk Download.txt','w')
    bulk_download.close()
    shutil.move('Bulk Download.txt', read_location_file()+'/Bulk Download.txt')
    message.print_line('-> Bulk Download.txt file created successfully.\n')
    if check_os() == 'windows':
        run_path = 'python "'+os.getcwd()+'/run.py"'
        lynda = open('Lynda.bat', 'a')
        lynda.writelines('@ECHO OFF\n')
        lynda.writelines('REM Batch file to execute run.py\n')
        lynda.writelines('SET PATH=%PATH%;C:\Python27;C:\Python27\Scripts\n')
        lynda.writelines(run_path+'\n')
        lynda.writelines('pause')
        lynda.close()
        message.print_line('-> Lynda.bat file created.\n')
        os.rename('Lynda.bat', read_location_file() + '/Lynda.bat')

def create_location_file():
    '''create file that tells the program where to save the new course'''
    os.chdir(RESET_PATH)
    files = os.listdir(os.getcwd())
    for content in files:
        if content == 'location.txt':
            #Prevent existing location.txt file from overwriting
            message.print_line('location.txt file already exists, will use the same path inside it for downloads\n')
            return
    loc_file = open('location.txt', 'w')
    loc_file.write(set_path()+'/Lynda')
    loc_file.close()
    message.print_line('-> location.txt file created.\n')

def read_location_file():
    '''read the content of location.txt'''
    os.chdir(RESET_PATH)
    loc_file = open('location.txt')
    content = loc_file.read()
    loc_file.close()
    return content

def install_dependencies():
    '''install required softwares'''
    os.chdir(RESET_PATH)
    requirements = open('requirements.txt')
    line = requirements.readline()
    for module in requirements:
        os.system('pip install '+ module)
    requirements.close()
    message.print_line('\n>>> All the required softwares are installed\n')
    message.colored_message(Fore.LIGHTGREEN_EX, 'If you wish to download your courses to some other FOLDER,'+
    ' paste the folder path in location.txt file\n')

if __name__ == '__main__':
    try:
        set_path()
        create_folder()
        create_aliases()
        create_location_file()
        lynda_folder_files()
        install_dependencies()
    except KeyboardInterrupt:
        message.print_line("Program execution cancelled through keyboard!")
        try:
            sys.exit(0)
        except:
            os._exit(0)
            