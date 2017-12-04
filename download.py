import os
import sys
import install
import cookies
import message

def download_files(url, cookie_path, course_folder):
    ''' This function downloads all the videos in course folder'''
    os.chdir(course_folder)
    COOKIE = install.read_settings_json('credentials', 'use_cookie_for_download')
    SUBTITLE = install.read_settings_json('preferences', 'download_subtitles')
    EXTERNAL_DOWNLOADER = install.read_settings_json('preferences', 'ext-downloader-aria2-installed')
    USERNAME = install.read_settings_json('credentials', 'username')
    PASSWORD = install.read_settings_json('credentials', 'password')
        
    try:
        subtitles = ' --all-subs ' if SUBTITLE else ' '     # Checking subtitle preferences
        # Output name of videos/subtitles
        output = ' -o ' +'"'+ course_folder + "/%(playlist_index)s - %(title)s.%(ext)s" + '"'
        # Extername downloader option
        ext_downloader = ' --external-downloader aria2c' if EXTERNAL_DOWNLOADER else ''
        cookie = ' --cookies ' + '"' + cookie_path + '"'    #cookie
        username = ' -u ' + USERNAME                        #username
        password = ' -p ' + PASSWORD                        #password

        # Checking cookie preferences
        if  COOKIE:
            cookies.edit_cookie(cookie_path, message.NETSCAPE) # Edit cookie file
            os.system('youtube-dl' + cookie + output + subtitles + url + ext_downloader)
        else:
            os.system('youtube-dl' + username + password + output + subtitles + url + ext_downloader)
    except KeyboardInterrupt:
        sys.exit('Program Interrupted')

def read_bulk_download():
    ''' Read Bulk Download.txt '''
    os.chdir(install.read_settings_json('preferences', 'location'))
    bulk_download = open('Bulk Download.txt', 'r')
    urls = bulk_download.readlines()
    return urls
