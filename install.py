''' Install Lyndor software and dependencies '''

import os, sys, shutil
import read, save
import zipfile
import json

def check_os():
    '''Check operating system'''
    if sys.platform.lower() == 'darwin':
        return 'macos'
    elif sys.platform.lower() == 'win32':
        return 'windows'
    elif sys.platform.lower() == 'linux2' or sys.platform.lower() == 'linux':
        return 'linux'
    else:
        print('operating system not supported: ' + sys.platform.lower())
        sys.exit('unknown operating system.')

def set_path():
    '''Set path for saving lynda folder'''
    if check_os() == 'macos':
        os.chdir(os.path.expanduser('~/Movies'))
        return os.getcwd()
    elif check_os() == 'windows' or check_os() == 'linux':
        directory = os.path.expanduser('~/')
        if file_found('Videos', directory):
            os.chdir(os.path.expanduser('~/Videos'))
        else:
            os.mkdir(os.path.expanduser('~/Videos'))
            os.chdir(os.path.expanduser('~/Videos'))
        return os.getcwd()


def get_path(folder):
    '''Set path for desktop folder'''
    if check_os() == 'macos':
        os.chdir(os.path.expanduser('~/' + folder))
        return os.getcwd()
    elif check_os() == 'windows':
        os.chdir(os.path.expanduser('~/' + folder))
        return os.getcwd()
    elif check_os() == 'linux':
        os.chdir(os.path.expanduser('~/' + folder))
        return os.getcwd()


def file_found(folder, directory):
    ''' find a file in a directory '''
    for pointer in os.listdir(directory):
        if pointer == folder:
            return True
    return False


def install_dependencies():
    '''install required softwares'''
    os.chdir(read.LYNDOR_PATH)

    in_file = open('settings.json', 'r')
    requirements = json.load(in_file)
    in_file.close()

    dependencies = requirements['requirements']['dependencies']

    for module in dependencies:
        os.system('pip install ' + module)


if __name__ == '__main__':
    try:
        save.settings_json()
        save.lynda_folder()
        save.aliases_bat()
        save.run_lyndor_bat()
        install_dependencies()
        save.aria2()
        save.webdriver()
    except KeyboardInterrupt:
        print("Program execution cancelled through keyboard!")
        sys.exit(0)
