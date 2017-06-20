import sys
import os
import message
import chapters
import cookies
import download
import renameFiles
import install
import time

if __name__ == '__main__':

    print message.ENTER_URL
    url = raw_input()

    #strip any extra text after .html in the url
    url = url[:url.find(".html")+5]
    
    #start time counter begins
    start_time = time.time()

    #lynda folder path
    lynda_folder_path = install.read_location_file() + '/'

    course_folder_path = chapters.course_path(url, lynda_folder_path)
    desktop_folder_path = install.folder_path("Desktop")
    download_folder_path = install.folder_path("Downloads")
    cookie_path = cookies.find_cookie(desktop_folder_path, download_folder_path)
    cookies.edit_cookie(cookie_path, message.NETSCAPE)

    #create course folder
    try:
        chapters.save_course(url, lynda_folder_path)
    except:
        sys.exit("\n-> Oops! Course folder already exists\n")

    #create chapters inside course folder
    chapters.save_chapters(url, course_folder_path)

    #downloading lynda videos to tempFolder
    download.download_files(url, cookie_path, course_folder_path)

    #renaming files
    try:
        path = renameFiles.assign_folder(course_folder_path)
    except:
        sys.exit('error in assigning path')
    try:
        renameFiles.execute(path)
        end_time = time.time()
        print "\n>>> Awesome!! Your course is downloaded, the whole process took {}\n".format(renameFiles.hms_string(end_time - start_time))
    except:
        sys.exit(message.RENAMING_ERROR)
