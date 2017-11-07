import os
import sys
import shutil

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
    path = read_location_file()
    if not os.path.exists(path):
        os.makedirs(path)
        print '-> Lynda folder created at: ' + read_location_file()
    else:
        print '>>> Lynda folder already exists\n'

def create_aliases():
    '''Create aliases file'''
    os.chdir(RESET_PATH)
    if check_os() == 'windows':
        run_path = 'doskey lynda= python "'+os.getcwd()+'/run.py"'
        alias = open('aliases.bat', 'w')
        alias.write(run_path)
        alias.close()
        print '-> aliases.bat file created.\n'

def lynda_folder_files():
    ''' create Run-Lyndor.bat in windows '''
    os.chdir(RESET_PATH)
    bulk_download = open('Bulk Download.txt','w')
    bulk_download.close()
    shutil.move('Bulk Download.txt', read_location_file()+'/Bulk Download.txt')
    print '-> Bulk Download.txt file created successfully.\n'
    if check_os() == 'windows':
        run_path = 'python "'+os.getcwd()+'/run.py"'
        lynda = open('Run-Lyndor.bat', 'a')
        lynda.writelines('@ECHO OFF\n')
        lynda.writelines('REM Batch file to execute run.py\n')
        lynda.writelines('SET PATH=%PATH%;C:\Python27;C:\Python27\Scripts\n')
        lynda.writelines(run_path+'\n')
        lynda.writelines('pause')
        lynda.close()
        try:
            os.rename('Run-Lyndor.bat', read_location_file() + '/Run-Lyndor.bat')
        finally:
            print '-> Run-Lyndor.bat file created.\n'

def create_location_file():
    '''create file that tells the program where to save the new course'''
    os.chdir(RESET_PATH)
    files = os.listdir(os.getcwd())
    try:
        for content in files:
            if content == 'location.txt':
                #Prevent existing location.txt file from overwriting
                print '\n>>> location.txt file already exists, will use the same path inside it.'
                return
        loc_file = open('location.txt', 'w')
        loc_file.write(set_path()+'/Lynda')
        loc_file.close()
        print '-> location.txt file created.\n'
    finally:
        print '>>> (To download videos to a different folder, replace the folder path in location.txt)'
        print '>>> Your Lynda videos will be saved at -> '+ read_location_file() +'\n'
                

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
    print '\n>>> All the required softwares are installed\n'

if __name__ == '__main__':
    try:
        install_dependencies()
        set_path()
        create_location_file()
        create_folder()
        create_aliases()
        lynda_folder_files()
    except KeyboardInterrupt:
        print "Program execution cancelled through keyboard!"
        sys.exit(0)
            