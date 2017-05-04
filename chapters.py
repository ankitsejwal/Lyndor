import os
import sys
import urllib2
import shutil
import re
import message
from bs4 import BeautifulSoup

def create_soup(urlink):
    url = urllib2.urlopen(urlink)
    pg_content = url.read()
    return BeautifulSoup(pg_content, 'lxml')

def course_path(urlink, lynda_folder_path):
    soup = create_soup(urlink)
    course_title = soup.find('h1', {"class": "default-title"})
    course_title = course_title.text
    #remove non-alphanumeric characters
    course_title = re.sub('[^a-zA-Z0-9.,-]', ' ', course_title)
    course_path = lynda_folder_path + course_title
    return course_path

def save_course(urlink, lynda_folder_path):
    course = course_path(urlink, lynda_folder_path)
    os.mkdir(course)

def save_chapters(urlink, course_folder_path):
    soup = create_soup(urlink)
    heading4 = soup.find_all('h4', {"class": "ga"})
    chapter_no = 0

    for h in heading4:
        chapter = h.text
        chapter = re.sub('[^a-zA-Z0-9.,-]', ' ', chapter)

        if chapter[1] == '.':
            chapter_name = chapter[3:]
            chapter = str(chapter_no) + '. ' + chapter_name
            chapter_no += 1
        elif chapter[2] == '.':
            chapter_name = chapter[4:]
            chapter = str(chapter_no) + '. ' + chapter_name
            chapter_no += 1
        else:
            chapter = str(chapter_no) + '. ' + chapter
            chapter_no += 1
        print course_folder_path + "/" + chapter
        os.mkdir(course_folder_path + "/" + chapter)

    print '\n'+str(chapter_no)+' chapters created!!!'
