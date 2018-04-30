#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' Creates course folder/ Saves chapters'''

import os
import install, cookies
import sys, zipfile, json
import time
import shutil
import re
import message, read
try:
    from bs4 import BeautifulSoup
    from colorama import *
    import requests
except ImportError:
    pass

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
    course_title = re.sub('[,:?.><"/\\|*]', ' -', course_title)
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
                    # fix for python 2.x and 3.x
                    try: answer = raw_input().lower()
                    except NameError: answer = input().lower() 

                    if answer == 'y':
                        shutil.rmtree(current_course)
                        message.colored_message(Fore.LIGHTRED_EX, "\n❌  Existing course folder deleted!!")
                        time.sleep(2)
                        message.colored_message(Fore.LIGHTGREEN_EX, "\n♻️  Re-downloading the course.\n")
                    elif answer == 'n':
                        sys.exit(message.colored_message(Fore.LIGHTRED_EX, "\n-> Program Ended!!\n"))
                    else:
                        sys.stdout.write(Fore.LIGHTRED_EX + "\n- oops!! that's not a valid choice, type Y or N: " + Fore.RESET)
    
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

    with open('info.txt', 'a') as info_file:
        info_file.writelines('Course Name' + '\t\t' + course_title + '\n')
        info_file.writelines('Course id' + '\t\t' + course_id + '\n')
        info_file.writelines('Author Name' + '\t\t' + author_name + '\n')
        info_file.writelines('Topics' + '\t\t' + topic_tag + '\n')
        info_file.writelines('Softwares' + '\t\t' + software_tag + '\n')
        info_file.writelines('Duration' + '\t\t' + duration + '\n')
        info_file.writelines('Release Date' + '\t\t' + release_date + '\n')
        info_file.writelines('Downloaded On' + '\t\t' + download_date + '\n')
        info_file.writelines('Course URL' + '\t\t' + url + '\n')
    info_file.close()

    with open('CONTENT.md', 'a') as content_md:
        content_md.writelines("# " + course_title + " with " + author_name + " on lynda.com \n")
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
        chapter = re.sub('[,:?><"/\\|*]', ' ', chapter)

        if chapter[1] == '.':
            chapter = str(chapter_no).zfill(2) + '. ' + chapter[3:]
        elif chapter[2] == '.':
            chapter = str(chapter_no).zfill(2) + '. ' + chapter[4:]
        else:
            chapter = str(chapter_no).zfill(2) + '. ' + chapter
        
        chapter_no += 1
        message.print_line(chapter)

        os.mkdir(course_folder_path + "/" + chapter) # create folders (chapters)
            
    message.colored_message(Fore.LIGHTGREEN_EX, '\n✅  '+str(chapter_no)+' chapters created!!\n')
 
def contentmd(url):
    ''' write chapters and videos information to content.md '''

    soup = create_soup(url)

    chapters = soup.find_all("h4", class_="ga")
    ul_video = soup.find_all('ul', class_="row toc-items")
    
    chapter_count = 0
    video_count = 0

    with open('CONTENT.md', 'a') as content_md:
        bug = False
        for li in ul_video:
            try:
                content_md.writelines('\n\n## ' + (chapters[chapter_count].text).encode('utf-8') + '\n')
            except TypeError:
                content_md.writelines('\n\n## ' + str((chapters[chapter_count].text).encode('utf-8')) + '\n')
            except Exception:
                bug = True
                break              
            chapter_count += 1
            group = li.find_all('a', class_='video-name')
            for video in group:
                video_count += 1
                try:
                    content_md.writelines("\n* " + str(video_count).zfill(2) + " - " + (video.text.strip()).encode('utf-8'))
                except TypeError:
                    content_md.writelines("\n* " + str(video_count).zfill(2) + " - " + str((video.text.strip()).encode('utf-8')))
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
        for video in group:
            video_count += 1
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
        ext_downloader = ' --external-downloader aria2c' if read.external_downloader else ''
        cookie = ' --cookies ' + '"' + cookie_path + '"'     # cookie
        username = ' -u ' + read.username                    # username
        password = ' -p ' + read.password                    # password

        # Checking download preferences
        if  download_preference in ['cookies', 'cookie']:
            cookies.edit_cookie(cookie_path, message.NETSCAPE) # Edit cookie file
            os.system('youtube-dl' + cookie + output + subtitles + url + ext_downloader)
        else:
            os.system('youtube-dl' + username + password + output + subtitles + url + ext_downloader)
    except KeyboardInterrupt:
        sys.exit('Program Interrupted')

def aria2():
    ''' Download aria2c for windows '''
    import requests
    os.chdir(read.LYNDOR_PATH)
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
        print('>>> unzipping aria2c.zip')
        unzip('aria2c', 'aria2c.zip')
        print(
            '>>> aria2c.zip has been unzipped, copy its path and save to PATH variable.\n')


def unzip(directory, zip_file):
    ''' unzip a file '''
    with zipfile.ZipFile(directory + '/' + zip_file, 'r') as f:
        f.extractall(path=directory)


def settings_json():
    ''' Create settings_json file '''
    os.chdir(read.LYNDOR_PATH)

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
            "course_download_pref": ["regular-login", "cookies"],
            "exfile_download_pref": ["regular-login", "library-login"]
        },
        "preferences": {
            "location": install.set_path() + '/Lynda',
            "download_subtitles": True,
            "download_exercise_file": True,                    # feature unavailable for organizational login
            "web_browser_for_exfile": ["chrome", "firefox"],    # select chrome or firefox as a web browser
            "ext-downloader-aria2-installed": False,            # set True after installing aria2
            "download_time": "",
            "redownload_course": ["prompt", "skip", "force" ]   # choose between -> prompt, skip & force re-download
        }
    }

    out_file = open(read.LYNDOR_PATH + '/settings.json', 'w')
    json.dump(settings_dict, out_file, indent=4)
    out_file.close()

    print('\n>>> Courses will be saved at -> ' +
          read.settings_json('preferences', 'location') + '\n')
    print('-> settings.json file created in Lyndor folder.\
 (Have a look at this file, you can edit settings here.)\n')


def lynda_folder():
    ''' Create lynda folder '''
    path = read.settings_json('preferences', 'location')
    if not os.path.exists(path):
        os.makedirs(path)
        print('-> Lynda folder created at: ' +
              read.settings_json('preferences', 'location') + '\n')
    else:
        print('>>> Lynda folder already exists\n')


def aliases_bat():
    '''Create aliases file'''
    os.chdir(read.LYNDOR_PATH)
    if install.check_os() == 'windows':
        run_path = 'doskey lynda= python "' + os.getcwd() + '/run.py"'
        alias = open('aliases.bat', 'w')
        alias.write(run_path)
        alias.close()
        print('-> aliases.bat file created.\n')


def run_lyndor_bat():
    ''' create Run-Lyndor.bat in windows '''
    os.chdir(read.LYNDOR_PATH)
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
    import requests
    os.chdir(read.LYNDOR_PATH)   # change directory to LYNDOR
    try:
        # create directory webdriver to save platform specific webdrivers
        os.mkdir('webdriver')
    except:
        pass
    print('\n-> Downloading web driver for ' + install.check_os())

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

    print('\n>>> Web driver downloaded inside "/Lyndor/webdriver" folder, extract the zip file and\
set the webdriver directory path to "PATH" variable, see README.md file for more detail.\n')

    print('\n>>> Installation complete, Don\'t forget to have a look at settings.json\n')
