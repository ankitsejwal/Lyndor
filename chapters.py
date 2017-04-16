import os
import sys
import urllib2
import shutil
import message
from bs4 import BeautifulSoup

def save_chapters(urlink, lynda_folder_path, temp_folder_path):

    url = urllib2.urlopen(urlink)
    pg_content = url.read()
    soup = BeautifulSoup(pg_content, 'lxml')

    course_title = soup.find('h1', {"class": "default-title"})
    course_title = course_title.text.replace(':', '-').replace('/', '-').replace('\\', '-')
    os.mkdir(lynda_folder_path + course_title)

    heading4 = soup.find_all('h4', {"class": "ga"})
    counter = 0

    for h in heading4:
        files = h.text.replace(':', '-').replace('/', '-').replace('\\', '-')

        print lynda_folder_path + course_title + "/" + files
        os.mkdir(lynda_folder_path + course_title + "/" + files)
        counter += 1
    print '\n'+str(counter)+' chapters created!!!'


    destination_folder = lynda_folder_path + course_title + "/"
    try:
        move_files(temp_folder_path, destination_folder)
    except:
        sys.exit(message.MOVING_ERROR)
    print destination_folder + '\n\n\t**** Happy Downloading :) ****\n'

def move_files(source_folder, destination_folder):
    os.chdir(source_folder)
    path = os.getcwd()

    for content in os.listdir(path):
        if content.endswith('.mp4'):
            shutil.move(content, destination_folder)

    print '\nCourse downloaded successfully, here: '
