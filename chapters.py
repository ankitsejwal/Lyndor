import os
import time
import urllib2
import re
from bs4 import BeautifulSoup
import message
from colorama import *

def create_soup(url):
    ''' create soup object '''
    url = urllib2.urlopen(url)
    pg_content = url.read()
    return BeautifulSoup(pg_content, 'lxml')

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

    release_date = soup.find('span', {"id": "release-date"}).text
    duration = soup.find('div', {"class": "duration"}).find('span').text
    download_date = time.strftime("%d/%m/%y")   # todays date
    if soup.find('span', {"id": "update-date"}) != None:
        update_date = soup.find('span', {"id": "update-date"}).text
    else:
        update_date = release_date

    message.write("Course Name", course_title)
    message.write("Course id", course_id)
    message.write("Author Name", author_name)
    message.write("Topics", topic_tag)
    message.write("Softwares", software_tag)
    message.write("Duration", duration)
    message.write("Release Date", release_date)
    message.write("Updated On", update_date)
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
        info_file.writelines('Updated On' + '\t\t' + update_date + '\n')
        info_file.writelines('Downloaded On' + '\t\t' + download_date + '\n')
        info_file.writelines('Course URL' + '\t\t' + url + '\n')
    info_file.close()

    with open('CONTENT.md','a') as content_md:
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
    course_title = re.sub('[^ a-zA-Z0-9.,-]', '-', course_title)
    course_path = lynda_folder_path + course_title
    return course_path

def save_course(urlink, lynda_folder_path):
    ''' create course folder '''
    course = course_path(urlink, lynda_folder_path)
    os.mkdir(course)

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
 