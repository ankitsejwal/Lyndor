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

def gather_info(url, course_path):
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

    os.chdir(course_path)

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
        content_md.writelines("# " + course_title + " with " + author_name + " on lynda.com \n\n")
        content_md.writelines("## Chapters:\n\n") # next heading
    content_md.close()

    # print message
    message.print_line(message.INFO_FILE_CREATED)

def course_path(urlink, lynda_folder_path):
    ''' finding course path '''
    soup = create_soup(urlink)
    course_title = soup.find('h1', {"class": "default-title"}).text
    #remove non-alphanumeric characters
    course_title = re.sub('[^ a-zA-Z0-9.,-]', ' -', course_title)
    return lynda_folder_path + course_title

def save_course(urlink, lynda_folder_path):
    ''' create course folder '''
    current_course = course_path(urlink, lynda_folder_path)
    courses = os.listdir(lynda_folder_path)

    answer = None
    for course in courses:
        if (lynda_folder_path + course) == current_course:

            QUESTION = '\nCourse already exists: Do you wish to delete it and download again? (Y/N): '
            sys.stdout.write(Fore.LIGHTBLUE_EX + QUESTION + Fore.RESET)
            while answer != 'y':
                answer = raw_input().lower()
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

def save_chapters(urlink, course_folder_path):
    ''' create chapters folder '''
    soup = create_soup(urlink)
    heading4 = soup.find_all('h4', {"class": "ga"})
    chapter_no = 0

    message.colored_message(Fore.LIGHTYELLOW_EX, "Creating Chapters:\n") # Print message

    with open('CONTENT.md', 'a') as content_md:
        for h in heading4:
            chapter = h.text
            chapter = re.sub('[^a-zA-Z0-9.,-]', ' ', chapter)

            if chapter[1] == '.':
                chapter_name = chapter[3:]
                chapter = str(chapter_no).zfill(2) + '. ' + chapter_name
                chapter_no += 1
            elif chapter[2] == '.':
                chapter_name = chapter[4:]
                chapter = str(chapter_no).zfill(2) + '. ' + chapter_name
                chapter_no += 1
            else:
                chapter = str(chapter_no).zfill(2) + '. ' + chapter
                chapter_no += 1
            message.print_line(chapter)

            os.mkdir(course_folder_path + "/" + chapter) # create folders (chapters)
            content_md.writelines('* ' + chapter + '\n') # writelines to content_md

        content_md.writelines('\n## Video files:\n\n') # next heading
    content_md.close() # close content_md

    message.colored_message(Fore.LIGHTGREEN_EX, '\n-> '+str(chapter_no)+' chapters created!!\n')
 