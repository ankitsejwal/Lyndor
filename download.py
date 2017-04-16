import os

def download_files(url, cookie_path, temp_folder_path):
    ''' This function downloads all the videos in temp folder'''
    os.chdir(temp_folder_path)
    os.system('youtube-dl --cookies '+'"'+cookie_path+'"' +" "+ url)
    