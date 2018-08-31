#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' Install Lyndor software and dependencies '''

import os, sys, shutil, json, zipfile

real_path = os.path.realpath(__file__)
LYNDOR_PATH = real_path[:real_path.find('install.py')]

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
    os.chdir(LYNDOR_PATH)
    print('lyndor path:', LYNDOR_PATH)
    requirements = os.path.join(LYNDOR_PATH, 'requirements.txt')
    os.system('pip install -r ' + requirements)


if __name__ == '__main__':
    try:
        from module import save
        install_dependencies()
        save.settings_json()
        save.lynda_folder()
        save.aliases_bat()
        save.run_lyndor_bat()
        save.aria2()
        save.webdriver()
    except KeyboardInterrupt:
        print("Program execution cancelled through keyboard!")
        sys.exit(0)
