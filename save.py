#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' Creates course folder/ Saves chapters'''

import os
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

            QUESTION = '\nCourse already exists: Do you wish to delete it and download again? (Y/N): '
            sys.stdout.write(Fore.LIGHTBLUE_EX + QUESTION + Fore.RESET)
            while answer != 'y':
                # fix for python 2.x and 3.x
                try: answer = raw_input().lower()
                except NameError: answer = input().lower() 

                if answer == 'y':
                    shutil.rmtree(current_course)
                    message.colored_message(Fore.LIGHTRED_EX, "\nx- Existing course folder deleted!!\n")
                    time.sleep(2)
                    message.colored_message(Fore.LIGHTGREEN_EX, "\n-> re-downloading the course.\n")
                elif answer == 'n':
                    sys.exit(message.colored_message(Fore.LIGHTRED_EX, "\n-> Program Ended!!\n"))
                else:
                    sys.stdout.write(Fore.LIGHTRED_EX + "\n- oops!! that's not a valid choice, type Y or N: " + Fore.RESET)
    os.mkdir(current_course)

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
            
    chapters_and_videos_to_contentmd(url)
    message.colored_message(Fore.LIGHTGREEN_EX, '\n-> '+str(chapter_no)+' chapters created!!\n')
 
 
def chapters_and_videos_to_contentmd(url):
    ''' write chapters and videos info. to content.md '''

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
        print('🤕 There seems to be an error while writing to content.md, please report the bug on GitHub')
    print("\n👍🏻 CONTENT.md is created.")