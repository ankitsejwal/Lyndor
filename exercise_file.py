''' Download exercise file '''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import install, message
import os, sys, time, shutil

username = install.read_settings_json('credentials', 'username')
password = install.read_settings_json('credentials', 'password')
web_browser = install.read_settings_json('preferences', 'web_browser_for_exfile')

def download(url, course_folder):
    ''' Download exercise file '''
    if web_browser.lower() == 'firefox': 
        driver = webdriver.Firefox()
    else:
        driver = webdriver.Chrome()
    driver.get("https://www.lynda.com/signin/")  # launch lynda.com/signin

    # enter username
    email = driver.find_element_by_css_selector("#email-address")
    email.clear()
    email.send_keys(username)
    driver.find_element_by_css_selector('#username-submit').click()
    print('\nusername successfully entered ....')
    time.sleep(2)

    # enter password
    passwrd = driver.find_element_by_css_selector('#password-input')
    passwrd.send_keys(password)
    driver.find_element_by_css_selector('#password-submit').click()
    print('password successfully entered ....')
    time.sleep(2)

    # move to the course page
    print('launching desired course page ....')
    driver.get(url)
    time.sleep(4)
    driver.find_element_by_css_selector('#exercise-tab').click()
    driver.find_element_by_css_selector('a > .exercise-name').click()
    ex_file_name = driver.find_element_by_css_selector('.exercise-name').text
    ex_file_size = driver.find_element_by_css_selector('.file-size').text
    print('Downloading ' + ex_file_name)
    
    file_not_found = True
    while file_not_found:
        message.spinning_cursor()
        os.chdir(install.folder_path("Downloads"))
        for folder in os.listdir():
            if folder == ex_file_name:
                print('\r{}'.format('Download in progress ...'))
                if os.path.getsize(folder) > 0: # if file downloaded completely.
                    print('Download completed.')
                    file_not_found = False
        time.sleep(2)
    try:
        shutil.move(ex_file_name, course_folder)
        print('File Moved to Course Folder successfully.')
    except:
        print('Moving error.')

    
if __name__ == '__main__':
    download('https://www.lynda.com/Python-tutorials/Programming-Fundamentals-Real-World/418249-2.html')