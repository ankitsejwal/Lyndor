import os
import sys

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
        print '>>> Your Lynda videos will be saved at -> '+set_path()+'Lynda (folder)\n'
    else:
        print '\nLynda folder already exists\n'

def create_aliases():
    '''Create aliases file'''
    os.chdir(RESET_PATH)
    if check_os() == 'windows':
        run_path = 'doskey lynda= python "'+os.getcwd()+'/run.py"'
        alias = open('aliases.bat', 'w')
        alias.write(run_path)
        alias.close()
        print '-> aliases.bat file created.\n'

def create_lynda_bat():
    ''' create lynda.bat in windows '''
    os.chdir(RESET_PATH)
    if check_os() == 'windows':
        run_path = 'python "'+os.getcwd()+'/run.py"'
        lynda = open('Lynda.bat', 'a')
        lynda.writelines('@ECHO OFF\n')
        lynda.writelines('REM Batch file to execute run.py\n')
        lynda.writelines('SET PATH=%PATH%;C:\Python27;C:\Python27\Scripts\n')
        lynda.writelines(run_path+'\n')
        lynda.writelines('pause')
        lynda.close()
        print '-> Lynda.bat file created.\n'
        os.rename('Lynda.bat', read_location_file() + '/Lynda.bat')

def create_location_file():
    '''create file that tells the program where to save the new course'''
    os.chdir(RESET_PATH)
    loc_file = open('location.txt', 'w')
    loc_file.write(set_path()+'/Lynda')
    loc_file.close()
    print '-> location.txt file created.\n'

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
    set_path()
    create_folder()
    create_aliases()
    create_location_file()
    create_lynda_bat()
    install_dependencies()
    