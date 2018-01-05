''' Lyndor runs from here - contains the main functions '''

import sys
import time
import message
import chapters
import cookies
import download
import rename_files
import install
import draw
from colorama import *

def main():
    ''' Main function '''
    init()
    message.animate_characters(Fore.LIGHTYELLOW_EX, draw.ROCKET, 0.05)
    message.spinning_cursor()
    message.print_line('\r1. Paste course url or\n' +
    '2. Press enter for Bulk Download')
    
    # Prevent name error on python 3.x
    try: 
        url = raw_input()
    except NameError:
        url = input()
    
    print('')
    start_time = time.time() #start time counter begins
    if url == "":
        urls = download.read_bulk_download()
        if not urls:
            sys.exit(message.colored_message(Fore.LIGHTRED_EX, 'Please paste urls in Bulk Download.txt\n'))
        for url in urls:
            schedule_download(url)
    else:
        schedule_download(url)
    try:
        end_time = time.time()
        message.animate_characters(Fore.LIGHTGREEN_EX, draw.COW, 0.1)
        message.colored_message(Fore.LIGHTGREEN_EX, "\nThe whole process took {}\n".format(rename_files.hms_string(end_time - start_time)))
    except KeyboardInterrupt:
        sys.exit(message.colored_message(Fore.LIGHTRED_EX, "\n- Program Interrupted!!\n"))

def schedule_download(url):
    ''' Look for the scheduled time in settings.json '''
    scheduled_time = install.read_settings_json('preferences', 'download_time')
    if scheduled_time == '':
        tip = 'Tip: You can schedule download time in settings.json.'
        message.carriage_return_animate(tip)
        download_course(url)
        return
    else:
        counter = True
        message.colored_message(Fore.LIGHTGREEN_EX, 'Download time set to: ' + scheduled_time + '\
 in settings.json, you can change or remove this time in settings.json\n')
        try:
            while counter:
                if time.strftime("%H:%M") == scheduled_time:
                    download_course(url)
                    return
                print('Download will start at: ' + scheduled_time + ', leave this window open.')
                time.sleep(60)
        except KeyboardInterrupt:
            sys.exit(message.colored_message(Fore.LIGHTRED_EX, "\n- Program Interrupted!!\n"))

def download_course(url):
    ''' download course '''
    #check for a valid url
    if url.find('.html') == -1:
        sys.exit(message.animate_characters(Fore.LIGHTRED_EX, draw.ANONYMOUS, 0.02))

    url = url[:url.find(".html")+5] #strip any extra text after .html in the url

    # Folder/File paths
    lynda_folder_path = install.read_settings_json('preferences', 'location') + '/'
    course_folder_path = chapters.course_path(url, lynda_folder_path)
    desktop_folder_path = install.folder_path("Desktop")
    download_folder_path = install.folder_path("Downloads")
    if install.read_settings_json('credentials', 'use_cookie_for_download'):
        cookie_path = cookies.find_cookie(desktop_folder_path, download_folder_path)
    else:
        cookie_path = ''
        usr_pass_message = message.return_colored_message(Fore.LIGHTGREEN_EX, 'Using username and password combination for download\n')
        message.carriage_return_animate(usr_pass_message)
    #create course folder
    try:
        chapters.save_course(url, lynda_folder_path)
    except KeyboardInterrupt:
        sys.exit(message.colored_message(Fore.LIGHTRED_EX, "\n- Program Interrupted!!\n"))

    #save chapters and videos
    try:
        chapters.gather_info(url, course_folder_path)   # Gather information
        chapters.save_chapters(url, course_folder_path) # Create chapters inside course folder
        download.download_files(url, cookie_path, course_folder_path) # Downloading lynda videos to course folder
    except KeyboardInterrupt:
        sys.exit(message.colored_message(Fore.LIGHTRED_EX, "\n- Program Interrupted!!\n"))

    # Rename files
    try:
        path = rename_files.assign_folder(course_folder_path)
    except KeyboardInterrupt:
        sys.exit(message.colored_message(Fore.LIGHTRED_EX, "\n- Program Interrupted!!\n"))
    except:
        sys.exit('error in assigning path')
    try:
        rename_files.execute(path)
    except KeyboardInterrupt:
        sys.exit(message.colored_message(Fore.LIGHTRED_EX, "\n- Program Interrupted!!\n"))
    except:
        sys.exit(message.RENAMING_ERROR)

if __name__ == '__main__':
    main()
