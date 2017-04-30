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

    #change this lyndafolder path on your computer
    video_folder = install.set_path()
    lynda_folder_path = video_folder + '/Lynda/'
    #lynda_folder_path = "/Volumes/750 GB/Movies/Lynda-collection/"

    #temp folder path - the folder should be inside lynda folder
    temp_folder_path = lynda_folder_path + "temp/"

    #don't edit this
    cookie_path = temp_folder_path + 'cookies.txt'
    cookies.edit_cookie(cookie_path, message.NETSCAPE)

    #downloading lynda videos to tempFolder
    download.download_files(url, cookie_path, temp_folder_path)

    #renaming files
    try:
        path = renameFiles.assign_folder(temp_folder_path)
    except:
        sys.exit('error in assigning path')
    try:
        renameFiles.execute(path)
    except:
        sys.exit(message.RENAMING_ERROR)

    #create course folder(with chapters) and move files in course folder
    chapters.save_chapters(url, lynda_folder_path, temp_folder_path)
    