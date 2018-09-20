#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' Download exercise file '''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import install
from module import message, read, save
import os, sys, time, shutil, requests
from colorama import Fore

# function list ->> download(), lib_login(), regular_login(), use_selenium(), use_aria2()


def download(url, course_folder, cookie_path):
    ''' Download exercise file '''
    if read.web_browser_for_exfile.lower() == 'firefox': 
        driver = webdriver.Firefox()
    elif read.web_browser_for_exfile.lower() == 'chrome':
        options = webdriver.ChromeOptions()

        # if downloading with aria2, launch chrome in headless mode
        if read.exfile_download_method == "aria2":
            options.add_argument('headless')
        
        options.add_argument("--window-size=1300x744")
        driver = webdriver.Chrome(chrome_options=options)
    else:
        sys.exit('Choose either chrome or firefox in settings.json to download exercise file')

    if read.exfile_download_pref == 'regular-login':
        regular_login(url, course_folder, driver)
    elif read.exfile_download_pref == 'library-login':
        lib_login(url, course_folder, driver)
    else:
        sys.exit('Please choose between -> regular-login / library-login in settings.json')

    time.sleep(3)   # wait request/response to happen after login
    
    # move to the course page
    print('launching desired course page ....')
    driver.get(url)
    
    if read.exfile_download_method == 'aria2':
        if read.aria2_installed: print('') 
        else: sys.exit('Aria2 not installed. Check preferences in settings')
        use_aria2(url, course_folder, cookie_path, driver)

    elif read.exfile_download_method == 'selenium':
        use_selenium(url, course_folder, driver)

    else:
        sys.exit('settings.json: exfile_download = should be selenium or aria2')

def use_selenium(url, course_folder, driver):
    ''' use just selenium to download files '''

    # injecting jquery
    jquery = requests.get(url="https://code.jquery.com/jquery-3.3.1.min.js")
    driver.execute_script(jquery.text)
    
    # delete .exercise-tab max-height:320px so that all the ex_files can be seen
    driver.execute_script("$('.exercise-tab .content').css('max-height', 'none');")

    # Maximize Window if exercise-tab element not visible
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#exercise-tab")))
    driver.find_element_by_css_selector('#exercise-tab').click()

    # Make sure page is more fully loaded before finding the element
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "html.no-touch.member.loaded")))

    exercises = driver.find_elements_by_css_selector('a > .exercise-name')

    try:
        for exercise in exercises:
                print(f"Downloading: {exercise.text}")
                exercise.click()
    except Exception as e:
        sys.exit(e)

    time.sleep(4)                                       # Give some heads up time to downloads

    downloads_folder = install.get_path("Downloads")
    os.chdir(downloads_folder)

    while len(exercises) > 0:                           # until exercises[] gets empty
        message.spinning_cursor()
        for folder in os.listdir(downloads_folder):

            try: folder = folder.decode('utf-8')        # python 2.x
            except AttributeError: pass                 # python 3.x

            sys.stdout.write("\033[K")                  # Clear to the end of line
            sys.stdout.write("\rFinding Ex_file in Downloads folder ---> " + message.return_colored_message(Fore.LIGHTYELLOW_EX,folder))
            sys.stdout.flush()                          # Force Python to write data into terminal.

            for exercise in exercises:
                if folder == exercise.text:
                    if os.path.getsize(folder) > 0:     # if file downloaded completely.
                        try:
                            shutil.move(exercise.text, course_folder)
                            print(f'\nMoved to course folder: {exercise.text}')
                        except:
                            print('\nMoving error: File already exists.')
                        
                        exercises.remove(exercise)      # pop out moved exercise file from exercises list
                        break                           # break inner for-loop when ex-file downloaded
            
            if(len(exercises) == 0):                    # if all exercises downloaded successfully
                break                                   # break outer for-loop and stop scanning Downloads folder

            time.sleep(0.02)                            # delay to print which file is being scanned

    driver.close()                                      # close web browser



def use_aria2(url, course_folder, cookie_path, driver):
    ''' user aria2 to download exercise files '''
    # jump to course_folder
    os.chdir(course_folder)

    # To be filled with all exercise file links /ajax/....
    exercise_file_urls = []
    files = driver.find_elements_by_css_selector('.course-file')

    for file in files:
        url = file.get_attribute('href')
        exercise_file_urls.append(url)

    driver.find_element_by_css_selector('#exercise-tab').click()
    exercises = driver.find_elements_by_css_selector('a > .exercise-name')

    for exercise in exercises:
        exercise_message = message.return_colored_message(Fore.LIGHTYELLOW_EX, exercise.text)
        print(f"To be Downloaded: {exercise_message}")


    total_ex_files = len(exercise_file_urls)
    counter = 1
    for url in exercise_file_urls:
        print(message.return_colored_message(Fore.LIGHTYELLOW_EX, f"\nDownloading {counter} of {total_ex_files}"))
        counter += 1
        os.system("aria2c --load-cookie='{}' {}".format(cookie_path, url))
    


def lib_login(url, course_folder, driver):
    driver.get("https://www.lynda.com/portal/patron?org=" + read.organization_url)  # launch lynda.com/signin

    # enter username
    card_number = driver.find_element_by_css_selector("#card-number")
    card_number.clear()
    card_number.send_keys(read.card_number)

    # enter password
    card_pin = driver.find_element_by_css_selector('#card-pin')
    card_pin.clear()
    card_pin.send_keys(read.card_pin)

    driver.find_element_by_css_selector('#library-login-login').click()
    print('\nlibrary card no. and card pin. entered successfully....')



def regular_login(url, course_folder, driver):
    driver.get("https://www.lynda.com/signin/")          # launch lynda.com/signin

    # enter username
    email = driver.find_element_by_css_selector("#email-address")
    email.clear()
    email.send_keys(read.username)
    driver.find_element_by_css_selector('#username-submit').click()
    print('\nusername successfully entered ....')
    # wait for password field to appear
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#password-input")))
    # enter password
    passwrd = driver.find_element_by_css_selector('#password-input')
    passwrd.send_keys(read.password)
    driver.find_element_by_css_selector('#password-submit').click()
    print('password successfully entered ....')
