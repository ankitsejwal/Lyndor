import os

def download_files(url, cookie_path, course_folder):
    ''' This function downloads all the videos in temp folder'''
    os.chdir(course_folder)
    os.system('youtube-dl --cookies '+'"'+cookie_path+'"' +" "+ url)
    