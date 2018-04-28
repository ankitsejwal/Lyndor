#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' Lyndor runs from here - contains the main functions '''

import sys, time
import message, save, cookies, read, install, move, draw, rename, exercise_file
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
        urls = read.bulk_download()
        if not urls:
            sys.exit(message.colored_message(Fore.LIGHTRED_EX, 'Please paste urls in Bulk Download.txt\n'))
        for url in urls:
            schedule_download(url)
    else:
        schedule_download(url)
    try:
        end_time = time.time()
        message.animate_characters(Fore.LIGHTGREEN_EX, draw.COW, 0.1)
        message.colored_message(Fore.LIGHTGREEN_EX, "\nThe whole process took {}\n".format(move.hms_string(end_time - start_time)))
    except KeyboardInterrupt:
        sys.exit(message.colored_message(Fore.LIGHTRED_EX, "\n- Program Interrupted!!\n"))

def schedule_download(url):
    ''' Look for the scheduled time in settings.json '''
    
    if not read.external_downloader:
        tip = '☝🏻  Tip: Install aria2c for faster downloads, read README.md to learn more.'
        message.carriage_return_animate(tip)
    if read.download_time == '':
        # If download time not set, begin download
        download_course(url)
        return
    else:
        counter = True
        message.colored_message(Fore.LIGHTGREEN_EX, 'Download time set to: ' + read.download_time + '\
 in settings.json, you can change or remove this time in settings.json\n')
        try:
            while counter:
                if time.strftime("%H:%M") == read.download_time:
                    download_course(url)
                    return
                print('Download will start at: ' + read.download_time + ', leave this window open.')
                time.sleep(60)
        except KeyboardInterrupt:
            sys.exit(message.colored_message(Fore.LIGHTRED_EX, "\n- Program Interrupted!!\n"))

def download_course(url):
    ''' download course '''
    # Check for a valid url
    if url.find('.html') == -1:
        sys.exit(message.animate_characters(Fore.LIGHTRED_EX, draw.ANONYMOUS, 0.02))

    url = url[:url.find(".html")+5] #strip any extra text after .html in the url

    # Folder/File paths
    lynda_folder_path = read.settings_json('preferences', 'location') + '/'
    course_folder_path = save.course_path(url, lynda_folder_path)
    desktop_folder_path = install.get_path("Desktop")
    download_folder_path = install.get_path("Downloads")
    
    # Read preferences
    use_cookie_for_download = read.course_download_pref

    if use_cookie_for_download in ['cookies', 'cookie']:
        cookie_path = cookies.find_cookie(desktop_folder_path, download_folder_path)
    else:
        cookie_path = ''
        usr_pass_message = message.return_colored_message(Fore.LIGHTGREEN_EX, 'Using username and password combination for download\n')
        message.carriage_return_animate(usr_pass_message)

    try:
        # main operations ->
        save.course(url, lynda_folder_path)                 # Create course folder
        save.info_file(url, course_folder_path)             # Gather information
        save.chapters(url, course_folder_path)              # Create chapter folders
        save.contentmd(url)                                 # Create content.md
        save.videos(url, cookie_path, course_folder_path)   # Download videos
        rename.videos(course_folder_path)                   # rename videos
        rename.subtitles(course_folder_path)                # rename subtitles
        move.vid_srt_to_chapter(url, course_folder_path)    # Move videos and subtitles to chapter folders

        # Download exercise files
        if save.check_exercise_file(url):
            print('\nExercise file is available to download')
            if not read.download_exercise_file:
                # if user do not want to download ex-file
                print("settings.json says you do not want to download ex-file -> 'download_exercise_file': false")
            else:
                # if user wants to download ex-file
                if read.course_download_pref == 'regular-login':
                    exercise_file.download(url, course_folder_path)
                elif read.exfile_download_pref == 'library-login':
                    if read.card_number == '':
                        print('\nTo download ex-file via library login -> Please save library card details in settings.json')
                    else:
                        exercise_file.download(url, course_folder_path)
                else:
                    print('\nThe exercise file can only be downloaded through one of the below combinations:')
                    print('~ Regular login: username + password or')
                    print('~ Library login: card number, pin and org. url\n')
        else:   # if exercise file not present
            print('This course do not include the Exercise files.')

    except KeyboardInterrupt:
        sys.exit(message.colored_message(Fore.LIGHTRED_EX, "\n- Program Interrupted!!\n"))


if __name__ == '__main__':
    main()
