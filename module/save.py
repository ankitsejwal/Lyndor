#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' Creates course folder/ Saves chapters'''

import os, io
import sys, zipfile, json
import time
import shutil
import re
import install
from module import message, cookies, read
try:
    from bs4 import BeautifulSoup
    from colorama import Fore
    import requests
except ImportError:
    pass

def utf_encode(string):
    return (string).encode('utf-8')

def utf_decode(string):
    return string.decode('utf-8')

def create_soup(url):
    ''' create soup object '''
    request = requests.get(url)
    page_content = request.content
    return BeautifulSoup(page_content, 'html.parser')

def check_exercise_file(url):
    ''' check if a course has an exercise file '''
    soup = create_soup(url)
    ex_file = soup.find(id='exercise-tab')
    if ex_file is not None:
        return True
    return False

def course_path(url, lynda_folder_path):
    ''' finding course path '''
    soup = create_soup(url)
    course_title = soup.find('h1', {"class": "default-title"}).text
    
    # Check for valid characters
    replacements = [
        ('[?]', ''),
        ('[/]', '_'),
        ('["]', "'"),
        ('[:><\\|*]', ' -')
    ]

    for old, new in replacements:
        course_title = re.sub(old, new, course_title)
    
    course_title = course_title.strip()
    return lynda_folder_path + course_title

def course(url, lynda_folder_path):
    ''' create course folder '''
    current_course = course_path(url, lynda_folder_path)
    courses = os.listdir(lynda_folder_path)

    answer = None
    for course in courses:
        if (lynda_folder_path + course) == current_course:
            if read.redownload_course == 'force':
                # delete existing course and re-download
                shutil.rmtree(current_course)
                message.colored_message(Fore.LIGHTRED_EX, "\n✅  Course folder already exists. Current preference -> FORCE redownload")
                message.colored_message(Fore.LIGHTRED_EX, "\n❌  Existing course folder deleted!!")
                time.sleep(2)
                message.colored_message(Fore.LIGHTGREEN_EX, "\n♻️  Re-downloading the course.\n")
                time.sleep(2)
            elif read.redownload_course == 'skip':
                # skip download process
                message.colored_message(Fore.LIGHTRED_EX, "\n✅  Course folder already exists. Current preference -> SKIP redownload")
                sys.exit(message.colored_message(Fore.LIGHTRED_EX, "\n-> Skipping course download.\n"))    
            elif read.redownload_course == 'prompt':
                # prompt user with available choices
                QUESTION = '\n✅  Course folder already exists: Do you wish to delete it and download again? (Y/N): '
                sys.stdout.write(Fore.LIGHTBLUE_EX + QUESTION + Fore.RESET)
                while answer != 'y':
                    # get user input
                    answer = input().lower()

                    if answer == 'y':
                        shutil.rmtree(current_course)
                        message.colored_message(Fore.LIGHTRED_EX, "\n❌  Existing course folder deleted!!")
                        time.sleep(2)
                        message.colored_message(Fore.LIGHTGREEN_EX, "\n♻️  Re-downloading the course.\n")
                    elif answer == 'n':
                        sys.exit(message.colored_message(Fore.LIGHTRED_EX, "\n-> Program Ended!!\n"))
                    else:
                        sys.stdout.write(Fore.LIGHTRED_EX + "\n- oops!! that's not a valid choice, type Y or N: " + Fore.RESET)
    
    print(f'\ncreating course folder at: {current_course}')
    os.mkdir(current_course)

def info_file(url, course_path):
    ''' gather course information. '''
    soup = create_soup(url)
    course_title = soup.find('h1', {"class": "default-title"}).text
    course_ids = soup.findAll('div', {"data-course-id":True}) # find all course id attributes
    course_id = course_ids[0]['data-course-id'] # select the first course id attribute value
    author_name = soup.find('cite', {"data-ga-label": "author-name"}).text
    #topic tags
    topic_tags = soup.findAll('a', {"data-ga-label": "topic-tag"})
    topic_tag = '\t'
    for tag in topic_tags:
        topic_tag += '#' + tag.text + '\t'
    #software tags
    software_tags = soup.findAll('a', {"data-ga-label": "software-tag"})
    software_tag = ''
    for tag in software_tags:
        software_tag += '#' + tag.text + '\t'
    if software_tag == '':
        software_tag += 'None'
    release_date = soup.find('span', {"id": "release-date"}).text
    duration = soup.find('div', {"class": "duration"}).find('span').text
    download_date = time.strftime("%d/%B/%Y")   # todays date

    message.write("\nCourse Name", course_title)
    message.write("Course id", course_id)
    message.write("Author Name", author_name)
    message.write("Topics", topic_tag)
    message.write("Softwares", software_tag)
    message.write("Duration", duration)
    message.write("Release Date", release_date)
    message.write("Downloaded On", download_date)
    message.write("Course URL", url)

    os.chdir(course_path)   # Jump to course directory to save info.txt

    # write to info.txt
    info_file = io.open('info.txt', mode="a", encoding="utf-8")
    info_file.writelines(u'Course Name' + '\t\t' + course_title + '\n')
    info_file.writelines(u'Course id' + '\t\t' + course_id + '\n')
    info_file.writelines(u'Author Name' + '\t\t' + author_name + '\n')
    info_file.writelines(u'Topics' + '\t\t' + topic_tag + '\n')
    info_file.writelines(u'Softwares' + '\t\t' + software_tag + '\n')
    info_file.writelines(u'Duration' + '\t\t' + duration + '\n')
    info_file.writelines(u'Release Date' + '\t\t' + release_date + '\n')
    info_file.writelines(u'Downloaded On' + '\t\t' + download_date + '\n')
    info_file.writelines(u'Course URL' + '\t\t' + url + '\n')
    info_file.close()

    # write to content.md
    content_md = io.open('CONTENT.md', mode="a", encoding="utf-8")
    content_md.writelines(u"# " + course_title + " with " + author_name + " on lynda.com \n")
    content_md.close()

    # print message
    message.print_line(message.INFO_FILE_CREATED)

def chapters(url, course_folder_path):
    ''' create chapters folder '''
    soup = create_soup(url)
    heading4 = soup.find_all('h4', {"class": "ga"})
    chapter_no = 0

    message.colored_message(Fore.LIGHTYELLOW_EX, "Creating Chapters:\n") # Print message

    
    for h in heading4:
        chapter = h.text
        
        # handle empty named chapters
        if len(chapter) == 0:
            chapter = "Unnamed"
    
        # Check for valid characters
        replacements = [
            ('[?]', ''),
            ('[/]', '_'),
            ('["]', "'"),
            ('[:><\\|*]', ' -')
        ]

        for old, new in replacements:
            chapter = re.sub(old, new, chapter)                

        if chapter[1] == '.':
            chapter = str(chapter_no).zfill(2) + '. ' + chapter[3:]
        elif chapter[2] == '.':
            chapter = str(chapter_no).zfill(2) + '. ' + chapter[4:]
        else:
            chapter = str(chapter_no).zfill(2) + '. ' + chapter
        
        chapter_no += 1
        message.print_line(chapter)

        new_chapter = course_folder_path + "/" + chapter
        new_chapter = new_chapter.strip()
        os.mkdir(new_chapter) # create folders (chapters)
            
    message.colored_message(Fore.LIGHTGREEN_EX, '\n✅  '+str(chapter_no)+' chapters created!!\n')
 
def contentmd(url):
    ''' write chapters and videos information to content.md '''

    soup = create_soup(url)

    chapters = soup.find_all("h4", class_="ga")
    ul_video = soup.find_all('ul', class_="row toc-items")
    
    chapter_count = 0
    video_count = 0


    content_md = io.open('CONTENT.md', mode="a", encoding="utf-8")

    bug = False
    for li in ul_video:
        try:
            chapter = chapters[chapter_count].text
            
            # handle empty named chapters
            if len(chapter) == 0:
                chapter = "Unnamed"
            
            chapter_name = u'\n\n## {}\n'.format(chapter)
            content_md.writelines(chapter_name)
        except Exception:
            bug = True
            break              
        chapter_count += 1
        group = li.find_all('a', class_='video-name')
        for video in group:
            video_count += 1
            try:
                video_name = u"\n* {} - {}".format(str(video_count).zfill(2), video.text.strip())
                content_md.writelines(video_name)
            except Exception:
                bug = True
                break
    if bug:
        print('🤕  There seems to be an error while writing to content.md, please report the bug on GitHub')
    else:
        print("👍🏻  CONTENT.md created.\n")                
    content_md.close()                  # close content.md

def total_videos(url):
    ''' counts total available video files '''

    soup = create_soup(url)
    ul_video = soup.find_all('ul', class_="row toc-items")
    video_count = 0

    for li in ul_video:
        group = li.find_all('a', class_='video-name')
        video_count += len(group)
    return video_count

def videos(url, cookie_path, course_folder):
    ''' Download all the videos in course folder'''
    os.chdir(course_folder)
    download_preference = read.course_download_pref

    try:
        subtitles = ' --all-subs ' if read.download_subtitles else ' ' # Check subtitle preferences
        # Output name of videos/subtitles
        output = ' -o ' +'"'+ course_folder + "/%(playlist_index)s - %(title)s.%(ext)s" + '"'
        # Exter name downloader option
        ext_downloader = ' --external-downloader aria2c' if read.aria2_installed else ''
        cookie = ' --cookies ' + '"' + cookie_path + '"'     # cookie
        uName = read.username

        if "'" in uName:                                     # escaping single quote (') for users with quote in their username
            uName = uName.replace("'", "\\'")
        username = ' -u ' + uName                            # username
        password = ' -p ' + read.password                    # password

        # Checking download preferences
        if  download_preference in ['cookies', 'cookie']:
            cookies.edit_cookie(cookie_path, message.NETSCAPE) # Edit cookie file
            os.system('youtube-dl --no-check-certificate' + cookie + output + subtitles + url + ext_downloader)
        else:
            os.system('youtube-dl --no-check-certificate' + username + password + output + subtitles + url + ext_downloader)
    except KeyboardInterrupt:
        sys.exit('Program Interrupted')

def aria2():
    ''' Download aria2c for windows '''
    try:
        import requests
    except ImportError:
        pass
    os.chdir(install.LYNDOR_PATH)
    if install.check_os() == 'windows':
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
        unzip('aria2c', 'aria2c.zip')
        print('>>> aria2c.zip has been unzipped, copy its path and save to PATH variable.\n')


def unzip(directory, zip_file):
    ''' unzip a file '''
    with zipfile.ZipFile(directory + '/' + zip_file, 'r') as f:
        f.extractall(path=directory)


def settings_json():
    ''' Create settings_json file '''
    os.chdir(install.LYNDOR_PATH)

    settings_dict = {
        "credentials": {
            "regular_login": {
                "username": "",
                "password": ""
            }, 
            "library_login": {
                "card_number": "",
                "card_pin": "",
                "organization_url": ""
            },
            "course_download_pref": "regular-login",
            "exfile_download_pref": "regular-login",
        },
        "preferences": {
            "location": install.set_path() + '/Lynda',
            "download_subtitles": False,
            "download_exercise_file": False,                # feature unavailable for organizational login
            "web_browser_for_exfile": "chrome",             # select chrome or firefox as a web browser
            "aria2_installed": False,                       # set True after installing aria2
            "download_time": "",
            "redownload_course": "prompt",                  # choose between -> prompt, skip & force re-download
            "exfile_download_method": "selenium",           # choose between selenium and aria2
        }
    }

    settings = os.path.join(install.LYNDOR_PATH, 'settings/static/js/settings.json')
    out_file = open(settings, 'w')
    json.dump(settings_dict, out_file, indent=4)
    out_file.close()

    print(f"\n>>> Courses will be saved at -> {read.settings_json('preferences', 'location')} \n")
    print('-> settings.json file created at Lyndor/settings/static/js/settings.json\n')


def lynda_folder():
    ''' Create lynda folder '''
    path = read.settings_json('preferences', 'location')
    if not os.path.exists(path):
        os.makedirs(path)
        print(f'-> Lynda folder created at: {path} \n')
    else:
        print('>>> Lynda folder already exists\n')


def aliases_bat():
    '''Create aliases file'''
    os.chdir(install.LYNDOR_PATH)
    if install.check_os() == 'windows':
        run_path = 'doskey lynda= python "' + os.getcwd() + '/run.py"'
        alias = open('aliases.bat', 'w')
        alias.write(run_path)
        alias.close()
        print('-> aliases.bat file created.\n')


def run_lyndor_bat():
    ''' create Run-Lyndor.bat in windows '''
    os.chdir(install.LYNDOR_PATH)
    bulk_download = open('Bulk Download.txt', 'w')
    bulk_download.close()
    shutil.move('Bulk Download.txt', read.settings_json(
        'preferences', 'location') + '/Bulk Download.txt')
    print('-> Bulk Download.txt file created successfully.\n')
    
    if install.check_os() == 'windows':
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


def webdriver():
    ''' Download web driver '''
    try:
        import requests
    except ImportError:
        pass
    os.chdir(install.LYNDOR_PATH)   # change directory to LYNDOR
    try:
        # create directory webdriver to save platform specific webdrivers
        os.mkdir('webdriver')
    except:
        pass
    print('\n-> Downloading web driver for', install.check_os())

    if install.check_os() == 'windows':
        chrome_url = 'https://chromedriver.storage.googleapis.com/2.35/chromedriver_win32.zip'
        firefox_url = 'https://github.com/mozilla/geckodriver/releases/download/v0.19.1/geckodriver-v0.19.1-win64.zip'
    elif install.check_os() == 'macos':
        chrome_url = 'https://chromedriver.storage.googleapis.com/2.35/chromedriver_mac64.zip'
        firefox_url = 'https://github.com/mozilla/geckodriver/releases/download/v0.19.1/geckodriver-v0.19.1-macos.tar.gz'
    elif install.check_os() == 'linux':
        chrome_url = 'https://chromedriver.storage.googleapis.com/2.35/chromedriver_linux64.zip'
        firefox_url = 'https://github.com/mozilla/geckodriver/releases/download/v0.19.1/geckodriver-v0.19.1-linux64.tar.gz'

    chrome = requests.get(chrome_url)
    firefox = requests.get(firefox_url)

    with open('webdriver/chromedriver.zip', 'wb') as f:
        f.write(chrome.content)

    with open('webdriver/firefoxdriver.zip', 'wb') as f:
        f.write(firefox.content)

    print('\n>>> Web driver downloaded inside "/Lyndor/webdriver" folder, extract the zip file and \
set the webdriver directory path to "PATH" variable, see README.md file for more detail.')
    print('\n>>> Installation complete update your settings by running "python settings/settings.py"')
    print('\nThis will run a local webserver at port 5000, you will see a message like')
    print('* Running on http://127.0.0.1:5000/ visit such URL in web-browser\n')