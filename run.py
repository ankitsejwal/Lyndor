import sys
import os
import time
import message
import chapters
import cookies
import download
import renameFiles
import install
import draw
from colorama import *

def main():
    init()
    message.animate_characters(Fore.LIGHTYELLOW_EX, draw.ROCKET, 0.05)
    message.spinning_cursor()
    message.print_line('\n1. Paste course url or\n' +
    '2. Press enter for Bulk Download')
    url = raw_input()

    start_time = time.time() #start time counter begins
    if url == "":
        urls = download.read_bulk_download()
        if not urls:
            sys.exit(message.colored_message(Fore.LIGHTRED_EX, 'Please paste urls in Bulk Download.txt\n'))
        for url in urls:
            download_course(url)
    else:
        download_course(url)
    try:
        end_time = time.time()
        message.animate_characters(Fore.LIGHTGREEN_EX, draw.COW, 0.1)
        message.colored_message(Fore.LIGHTGREEN_EX, "\nThe whole process took {}\n".format(renameFiles.hms_string(end_time - start_time)))
    except KeyboardInterrupt:
        sys.exit(message.colored_message(Fore.LIGHTRED_EX, "\n- Program Interrupted!!\n"))        

def download_course(url):
    #check for a valid url
    if url.find('.html') == -1:
        sys.exit(message.animate_characters(Fore.LIGHTRED_EX, draw.ANONYMOUS, 0.02))

    url = url[:url.find(".html")+5] #strip any extra text after .html in the url

    # Folder/File paths
    lynda_folder_path = install.read_location_file() + '/'
    course_folder_path = chapters.course_path(url, lynda_folder_path)
    desktop_folder_path = install.folder_path("Desktop")
    download_folder_path = install.folder_path("Downloads")
    cookie_path = cookies.find_cookie(desktop_folder_path, download_folder_path)
    
    # Edit cookie file
    cookies.edit_cookie(cookie_path, message.NETSCAPE)

    #create course folder
    try:
        chapters.save_course(url, lynda_folder_path)
    except KeyboardInterrupt:
        sys.exit(message.colored_message(Fore.LIGHTRED_EX, "\n- Program Interrupted!!\n"))
    except:
        sys.exit(message.animate_characters(Fore.LIGHTWHITE_EX, draw.NOPE, 0.02))
    
    #save chapters and videos
    try:
        chapters.gather_info(url, course_folder_path)   # Gather information
        chapters.save_chapters(url, course_folder_path) # Create chapters inside course folder
        download.download_files(url, cookie_path, course_folder_path) # Downloading lynda videos to course folder
    except KeyboardInterrupt:
        sys.exit(message.colored_message(Fore.LIGHTRED_EX, "\n- Program Interrupted!!\n"))

    # Rename files
    try:
        path = renameFiles.assign_folder(course_folder_path)
    except KeyboardInterrupt:
        sys.exit(message.colored_message(Fore.LIGHTRED_EX, "\n- Program Interrupted!!\n"))
    except:
        sys.exit('error in assigning path')
    try:
        renameFiles.execute(path)
    except KeyboardInterrupt:
        sys.exit(message.colored_message(Fore.LIGHTRED_EX, "\n- Program Interrupted!!\n"))
    except:
        sys.exit(message.RENAMING_ERROR)

if __name__ == '__main__':
    main()
