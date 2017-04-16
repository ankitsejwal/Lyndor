from bs4 import BeautifulSoup
import os, urllib2, shutil
import message

def saveChapters(urlink, lyndaFolderPath, tempFolderPath):

    url = urllib2.urlopen(urlink)
    pgContent = url.read()
    soup = BeautifulSoup(pgContent,'lxml')

    courseTitle = soup.find('h1', {"class": "default-title"})
    courseTitle = courseTitle.text.replace(':', '-').replace('/', '-').replace('\\','-')
    os.mkdir(lyndaFolderPath + courseTitle)

    heading4 = soup.find_all('h4',{"class": "ga"})
    counter = 0

    for h in heading4:
        files = h.text.replace(':', '-').replace('/', '-').replace('\\','-')

        print (lyndaFolderPath + courseTitle + "/" + files)
        os.mkdir(lyndaFolderPath + courseTitle + "/" + files)
        counter+=1
    print '\n'+str(counter)+' chapters created!!!'


    destinationFolder = lyndaFolderPath + courseTitle + "/"
    moveFiles(tempFolderPath, destinationFolder)
    print destinationFolder + '\n\n\t**** Happy Downloading :) ****\n'

def moveFiles(sourceFolder, destinationFolder):
    os.chdir(sourceFolder)
    path = os.getcwd()

    for f in os.listdir(path):
        if f.endswith('.mp4'):
            shutil.move(f,destinationFolder)

    print '\nCourse downloaded successfully, here: '
