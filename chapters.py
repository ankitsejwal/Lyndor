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

def save_chapters(urlink, lynda_folder_path, temp_folder_path):
    soup = create_soup(urlink)

    course_title = soup.find('h1', {"class": "default-title"})
    course_title = course_title.text
    #remove non-alphanumeric characters
    course_title = re.sub('[^a-zA-Z0-9.]', ' ', course_title)
    os.mkdir(lynda_folder_path + course_title)

    heading4 = soup.find_all('h4', {"class": "ga"})
    chapter_no = 0

    for h in heading4:
        chapter = h.text
        chapter = re.sub('[^a-zA-Z0-9.]', ' ', chapter)

        if chapter[1] == '.' or chapter[2] == '.':
            for c in range(len(chapter)):
                if chapter[c] == '.':
                    chapter_name = chapter[c+2:]
                    chapter = str(chapter_no) + '. ' + chapter_name
                    chapter_no += 1
        else:
            chapter = str(chapter_no) + '. ' + chapter
            chapter_no += 1

        print lynda_folder_path + course_title + "/" + chapter
        os.mkdir(lynda_folder_path + course_title + "/" + chapter)

    print '\n'+str(chapter_no)+' chapters created!!!'

    destination_folder = lynda_folder_path + course_title + "/"
    try:
        move_files(temp_folder_path, destination_folder)
    except:
        sys.exit('Error in moving files from temp folder - move your self' + message.MOVING_ERROR)
    print destination_folder + '\n\n\t**** Happy Downloading :) ****\n'

def move_files(source_folder, destination_folder):
    os.chdir(source_folder)
    path = os.getcwd()

    for content in os.listdir(path):
        if content.endswith('.mp4'):
            shutil.move(content, destination_folder)

    print '\nCourse downloaded successfully, here: '
