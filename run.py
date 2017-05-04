import sys
import message
import chapters
import cookies
import download
import renameFiles
import install


if __name__ == '__main__':

    print message.ENTER_URL
    url = raw_input()

    #strip any extra text after .html in the url
    url = url[:url.find(".html")+5]

    #change this lyndafolder path on your computer to save video at some other place
    video_folder = install.set_path()
    lynda_folder_path = video_folder + '/Lynda/'
    #lynda_folder_path = "/Volumes/750 GB/Movies/Lynda-collection/"

    course_folder_path = chapters.course_path(url, lynda_folder_path)
    desktop_folder_path = install.desktop_path()
    cookie_path = desktop_folder_path + '/cookies.txt'
    cookies.edit_cookie(cookie_path, message.NETSCAPE)

    #create course folder
    chapters.save_course(url, lynda_folder_path)

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
    except:
        sys.exit(message.RENAMING_ERROR)

    