import sys, os, subprocess

def downloadFiles(url,cookiePath,tempFolderPath):
    os.chdir(tempFolderPath)
    os.system('youtube-dl --cookies '+'"'+cookiePath+'"' +" "+ url)
