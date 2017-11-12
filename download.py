import os
import sys
import install

def download_files(url, cookie_path, course_folder):
    ''' This function downloads all the videos in course folder'''
    os.chdir(course_folder)
    try:
        os.system('youtube-dl --cookies '+'"'+cookie_path+'"' + ' --all-subs ' + url)
    except KeyboardInterrupt:
        sys.exit('Program Interrupted')

def read_bulk_download():
    os.chdir(install.read_settings_json('preferences', 'location'))
    bulk_download = open('Bulk Download.txt', 'r')
    urls = bulk_download.readlines()
    return urls
