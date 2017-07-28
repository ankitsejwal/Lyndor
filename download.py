import os
import sys

def download_files(url, cookie_path, course_folder):
    ''' This function downloads all the videos in course folder'''
    os.chdir(course_folder)
    try:
        os.system('youtube-dl --cookies '+'"'+cookie_path+'"' +" "+ url)
    except KeyboardInterrupt:
        sys.exit('Program Interrupted')