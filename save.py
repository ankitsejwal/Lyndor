#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' Creates course folder/ Saves chapters'''

import os
import install
import sys
import time
import shutil
import requests
import re
from bs4 import BeautifulSoup
import message
from colorama import *

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
    preference = install.read_settings_json('preferences', 'redownload_course')

    answer = None
    for course in courses:
        if (lynda_folder_path + course) == current_course:
            if preference == 'force':
                # delete existing course and re-download
                shutil.rmtree(current_course)
                message.colored_message(Fore.LIGHTRED_EX, "\n✅  Course folder already exists. Current preference -> FORCE redownload")
                message.colored_message(Fore.LIGHTRED_EX, "\n❌  Existing course folder deleted!!")
                time.sleep(2)
                message.colored_message(Fore.LIGHTGREEN_EX, "\n♻️  Re-downloading the course.\n")
                time.sleep(2)
            elif preference == 'skip':
                # skip download process
                message.colored_message(Fore.LIGHTRED_EX, "\n✅  Course folder already exists. Current preference -> SKIP redownload")
                sys.exit(message.colored_message(Fore.LIGHTRED_EX, "\n-> Skipping course download.\n"))    
            elif preference == 'prompt':
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
            content_md.writelines('\n\n## ' + chapters[chapter_count].text + '\n')
            chapter_count += 1
            group = li.find_all('a', class_='video-name')
            for video in group:
                video_count += 1
                try:
                    content_md.writelines("\n* " + str(video_count).zfill(2) + " - " + str(video.text.strip()))
                except:
                    bug = True
                    pass
    content_md.close()                          # close content.md - operation finished
    
    if bug:
        print('🤕  There seems to be an error while writing to content.md, please report the bug on GitHub')
    print("👍🏻  CONTENT.md created.\n")

def videos(url, cookie_path, course_folder):
    ''' This function downloads all the videos in course folder'''
    os.chdir(course_folder)
    COOKIE = install.read_settings_json('credentials', 'use_cookie_for_download')
    SUBTITLE = install.read_settings_json('preferences', 'download_subtitles')
    EXTERNAL_DOWNLOADER = install.read_settings_json('preferences', 'ext-downloader-aria2-installed')
    USERNAME = install.read_settings_json('credentials', 'username')
    PASSWORD = install.read_settings_json('credentials', 'password')
        
    try:
        subtitles = ' --all-subs ' if SUBTITLE else ' '     # Checking subtitle preferences
        # Output name of videos/subtitles
        output = ' -o ' +'"'+ course_folder + "/%(playlist_index)s - %(title)s.%(ext)s" + '"'
        # Extername downloader option
        ext_downloader = ' --external-downloader aria2c' if EXTERNAL_DOWNLOADER else ''
        cookie = ' --cookies ' + '"' + cookie_path + '"'    #cookie
        username = ' -u ' + USERNAME                        #username
        password = ' -p ' + PASSWORD                        #password

        # Checking cookie preferences
        if  COOKIE:
            cookies.edit_cookie(cookie_path, message.NETSCAPE) # Edit cookie file
            os.system('youtube-dl' + cookie + output + subtitles + url + ext_downloader)
        else:
            os.system('youtube-dl' + username + password + output + subtitles + url + ext_downloader)
    except KeyboardInterrupt:
        sys.exit('Program Interrupted')
