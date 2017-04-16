import urllib2, os, sys
import message, chapters, cookies, download, renameFiles
from bs4 import BeautifulSoup


if __name__ == '__main__':

    print message.enterUrl
    url = raw_input()

    #strip any extra text after .html in the url
    url = url[:url.find(".html")+5]

    #change this lyndafolder path on your computer
    lyndaFolderPath = "/Volumes/750 GB/Movies/Lynda-collection/"

    #temp folder path - the folder should be inside lynda folder
    tempFolderPath = lyndaFolderPath + "temp/"

    #don't edit this
    cookiePath = tempFolderPath + 'cookies.txt'
    cookies.editCookie(cookiePath,message.netscapeLine)

    #downloading lynda videos to tempFolder
    download.downloadFiles(url,cookiePath,tempFolderPath)

    #renaming files
    try:
        path = renameFiles.assignFolder(tempFolderPath)
    except:
        sys.exit('error in assigning path')
    try:
        renameFiles.execute(path)
    except:
        sys.exit(message.error)

    #create course folder(with chapters) and move files in course folder
    chapters.saveChapters(url, lyndaFolderPath, tempFolderPath)
