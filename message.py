import time
import sys

ENTER_URL = "\n***** Paste the url of Lynda course >>>\n"

NETSCAPE = '# Netscape HTTP Cookie File\n'

RENAMING_ERROR = "\nError in renaming file !!!"

COOKIE_FOUND_DESKTOP = "\n-> Great!! cookies.txt file found inside DESKTOP folder\n"

COOKIE_FOUND_DOWNLOAD = "\n-> Great!! cookies.txt file found inside DOWNLOADS folder\n"

COOKIE_NOT_FOUND_ERROR = "\n-> Oops!! Did you forget to put cookies.txt \
file inside Desktop or Downloads folder ??\n"

def animate_characters(string, speed):
    '''printing ASCII arts line by line'''
    for line in string.splitlines():
        print line
        time.sleep(speed)

def spinning_cursor():
    '''spinning cursor'''
    flag = True
    while flag:
        for cursor in '\\|/-\\|/-  -':
            time.sleep(0.1)
            # Use '\r' to move cursor back to line beginning
            # Or use '\b' to erase the last character
            sys.stdout.write('\r{}'.format(cursor))
            # Force Python to write data into terminal.
            sys.stdout.flush()
        flag = False

