import os
import sys
import install
import cookies
import message

def download_files(url, cookie_path, course_folder):
    ''' This function downloads all the videos in course folder'''
    os.chdir(course_folder)
    print 'course folder path yeh h bhai -' + os.getcwd()
    try:
        # Checking subtitle preferences
        if install.read_settings_json('preferences', 'download_subtitles'):
            subtitles = ' --all-subs '
        else:
            subtitles = ' '

        # Checking cookie preferences
        if  install.read_settings_json('preferences', 'use_cookie_for_download'):
            # Edit cookie file
            cookies.edit_cookie(cookie_path, message.NETSCAPE)
            output = ' -o ' +'"'+ course_folder + "/%(playlist_index)s - %(title)s.%(ext)s" + '"'
            os.system('youtube-dl --cookies '+'"'+cookie_path+'"' + output + subtitles + url)
        else:
            username = ' -u ' + install.read_settings_json('credentials', 'username')
            password = ' -p ' + install.read_settings_json('credentials', 'password')
            output = ' -o ' +'"'+ course_folder + "/%(playlist_index)s - %(title)s.%(ext)s" + '"'
            print ('youtube-dl' + username + password + output + subtitles + url)
            os.system('youtube-dl' + username + password + output + subtitles + url)
    except KeyboardInterrupt:
        sys.exit('Program Interrupted')

def read_bulk_download():
    ''' Read Bulk Download.txt '''
    os.chdir(install.read_settings_json('preferences', 'location'))
    bulk_download = open('Bulk Download.txt', 'r')
    urls = bulk_download.readlines()
    return urls
