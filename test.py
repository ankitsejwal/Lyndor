import urllib2
import re
import install
import os
import run

desktop_path = install.folder_path("Desktop")
download_path = install.folder_path("Download")

cookie_found = False

def find_cookie(desktop_path, download_path):
    for f in os.listdir(download_path):
        if f == "cookies.txt":
            cookie_found = True
            print "Cookie file found at Desktop"


    for f in os.listdir(desktop_path):
        if f == "cookies.txt":
            cookie_found = True
            print "Cookie file found at Download"
   
