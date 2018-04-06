''' Install Lyndor software and dependencies '''

import os, sys, shutil
import read
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
        if find_a_file('Videos'):
            os.chdir(os.path.expanduser('~/Videos'))
        else:
            os.mkdir(os.path.expanduser('~/Videos'))
            os.chdir(os.path.expanduser('~/Videos'))
        return os.getcwd()


def folder_path(folder):
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


def find_a_file(folder):
    ''' find a file in a directory '''
    directory = os.path.expanduser('~/')
    for fil in os.listdir(directory):
        if fil == folder:
            return True
    return False


def create_folder():
    ''' Create lynda folder '''
    path = read.settings_json('preferences', 'location')
    if not os.path.exists(path):
        os.makedirs(path)
        print('-> Lynda folder created at: ' +
              read.settings_json('preferences', 'location') + '\n')
    else:
        print('>>> Lynda folder already exists\n')


def create_aliases():
    '''Create aliases file'''
    os.chdir(read.LYNDOR_PATH)
    if check_os() == 'windows':
        run_path = 'doskey lynda= python "' + os.getcwd() + '/run.py"'
        alias = open('aliases.bat', 'w')
        alias.write(run_path)
        alias.close()
        print('-> aliases.bat file created.\n')


def lynda_folder_files():
    ''' create Run-Lyndor.bat in windows '''
    os.chdir(read.LYNDOR_PATH)
    bulk_download = open('Bulk Download.txt', 'w')
    bulk_download.close()
    shutil.move('Bulk Download.txt', read.settings_json(
        'preferences', 'location') + '/Bulk Download.txt')
    print('-> Bulk Download.txt file created successfully.\n')
    if check_os() == 'windows':
        run_path = 'python "' + os.getcwd() + '/run.py"'
        lynda = open('Run-Lyndor.bat', 'a')
        lynda.writelines('@ECHO OFF\n')
        lynda.writelines('REM Batch file to execute run.py\n')
        lynda.writelines('SET PATH=%PATH%;C:\Python27;C:\Python27\Scripts\n')
        lynda.writelines(run_path + '\n')
        lynda.writelines('pause')
        lynda.close()
        try:
            os.rename('Run-Lyndor.bat', read.settings_json('preferences',
                                                           'location') + '/Run-Lyndor.bat')
        except:
            pass
        finally:
            print('-> Run-Lyndor.bat file created.\n')


def create_settings_json():
    ''' Create settings_json file '''
    os.chdir(read.LYNDOR_PATH)

    settings_dict = {
        "credentials": {
            "username": "",                             # use cookie for organizational login-
            "password": "",                             # instead of username & password
            "use_cookie_for_download": True,            # if false, username & password will be used
        },
        "preferences": {
            "location": set_path() + '/Lynda',
            "download_subtitles": True,
            "download_exercise_file": False,            # feature unavailable for organizational login
            "web_browser_for_exfile": 'chrome',         # select chrome or firefox as a web browser
            "ext-downloader-aria2-installed": False,    # set True after installing aria2
            "download_time": "",
            "redownload_course": "prompt"            # choose between -> prompt, skip and force re-download
        },
        "requirements": {
            "dependencies": ['youtube-dl', 'requests', 'beautifulsoup4', 'colorama', 'selenium']
        }
    }
    out_file = open(read.LYNDOR_PATH + '/settings.json', 'w')
    json.dump(settings_dict, out_file, indent=4)
    out_file.close()

    print('\n>>> Courses will be saved at -> ' +
          read.settings_json('preferences', 'location') + '\n')
    print('-> settings.json file created in Lyndor folder.\
 (Have a look at this file, you can edit settings here.)\n')

def install_dependencies():
    '''install required softwares'''
    os.chdir(read.LYNDOR_PATH)

    in_file = open('settings.json', 'r')
    requirements = json.load(in_file)
    in_file.close()

    dependencies = requirements['requirements']['dependencies']

    for module in dependencies:
        os.system('pip install ' + module)


def download_webdriver():
    ''' Download web driver '''
    import requests
    os.chdir(read.LYNDOR_PATH)   # change directory to LYNDOR
    try:
        # create directory webdriver to save platform specific webdrivers
        os.mkdir('webdriver')
    except:
        pass
    print('\n-> Downloading web driver for ' + check_os())

    if check_os() == 'windows':
        chrome_url = 'https://chromedriver.storage.googleapis.com/2.35/chromedriver_win32.zip'
        firefox_url = 'https://github.com/mozilla/geckodriver/releases/download/v0.19.1/geckodriver-v0.19.1-win64.zip'
    elif check_os() == 'macos':
        chrome_url = 'https://chromedriver.storage.googleapis.com/2.35/chromedriver_mac64.zip'
        firefox_url = 'https://github.com/mozilla/geckodriver/releases/download/v0.19.1/geckodriver-v0.19.1-macos.tar.gz'
    elif check_os() == 'linux':
        chrome_url = 'https://chromedriver.storage.googleapis.com/2.35/chromedriver_linux64.zip'
        firefox_url = 'https://github.com/mozilla/geckodriver/releases/download/v0.19.1/geckodriver-v0.19.1-linux64.tar.gz'

    chrome = requests.get(chrome_url)
    firefox = requests.get(firefox_url)

    with open('webdriver/chromedriver.zip', 'wb') as f:
        f.write(chrome.content)

    with open('webdriver/firefoxdriver.zip', 'wb') as f:
        f.write(firefox.content)

    print('\n>>> Web driver downloaded inside "/Lyndor/webdriver" folder, extract the zip file and\
set the webdriver directory path to "PATH" variable, see README.md file for more detail.\n')

    print('\n>>> Installation complete, Don\'t forget to have a look at settings.json\n')


def download_aria2():
    ''' Download aria2c for windows '''
    import requests
    os.chdir(read.LYNDOR_PATH)
    if check_os() == 'windows':
        try:
            os.mkdir('aria2c')
        except:
            pass
        aria = requests.get(
            'https://github.com/aria2/aria2/releases/download/release-1.33.1/aria2-1.33.1-win-64bit-build1.zip')
        print('\n-> Downloading aria2c for windows')
        with open('./aria2c/aria2c.zip', 'wb') as f:
            f.write(aria.content)
        print('\n>>> aria2c.zip has been downloaded inside "Lyndor/aria2c" folder')
        print('>>> unzipping aria2c.zip')
        unzip('aria2c', 'aria2c.zip')
        print(
            '>>> aria2c.zip has been unzipped, copy its path and save to PATH variable.\n')


def unzip(directory, zip_file):
    ''' unzip a file '''
    with zipfile.ZipFile(directory + '/' + zip_file, 'r') as f:
        f.extractall(path=directory)


if __name__ == '__main__':
    try:
        create_settings_json()
        create_folder()
        create_aliases()
        lynda_folder_files()
        install_dependencies()
        download_aria2()
        download_webdriver()
    except KeyboardInterrupt:
        print("Program execution cancelled through keyboard!")
        sys.exit(0)
