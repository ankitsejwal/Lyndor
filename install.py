import os
import sys

def check_os():
    '''Check operating system'''
    if sys.platform.lower() == 'darwin':
        return 'macos'
    elif sys.platform.lower() == 'win32':
        return 'windows'
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

def create_folder():
    ''' Create lynda folder '''
    if not os.path.exists('Lynda'):
        os.makedirs('Lynda/temp')
        print '\n\t >>> Your Lynda videos will be saved at -> '+set_path()+'Lynda (folder)'
    else:
        print 'Lynda folder already exists'

def install_dependencies():
    '''install required softwares'''
    os.system('pip install youtube-dl')
    os.system('pip install lxml')
    os.system('pip install beautifulsoup4')
    print '\n\t >>> All the required softwares are installed '

if __name__ == '__main__':
    set_path()
    create_folder()
    install_dependencies()
    