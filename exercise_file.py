''' Download exercise file '''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import install, message, read
import os, sys, time, shutil
from colorama import *
from pathlib import Path
import logging

def download(url, course_folder):
    ''' Download exercise file '''
    if read.web_browser_for_exfile.lower() == 'firefox': 
        #Edu
        message.colored_message(Fore.LIGHTCYAN_EX, "Usando Firefox ;)" )
        fp = webdriver.FirefoxProfile("C:\\Users\\edu\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\2rz525o1.edu-1531359955209")
        driver = webdriver.Firefox(firefox_profile=fp)
    else:
        driver = webdriver.Chrome()

    if read.exfile_download_pref == 'regular-login':
        regular_login(url, course_folder, driver)
    elif read.exfile_download_pref == 'library-login':
        lib_login(url, course_folder, driver)
    else:
        sys.exit('Please choose between -> regular-login / library-login in settings.json')
    
    # move to the course page
    print('launching desired course page ....')
    driver.get(url)
    #Edu - time.sleep(4)
    time.sleep(2)
    
    # Maximize Window if exercise-tab element not visible
    try:
        driver.find_element_by_css_selector('#exercise-tab').click()
    except:
        driver.maximize_window()
        time.sleep(2)
        driver.find_element_by_css_selector('#exercise-tab').click()


    #Edu - ¿Cuandos ficheros zip de ejericios hay?
    selector = '#tab-exercise-files .exercise-name' 
    ficheros = driver.find_elements_by_css_selector(selector)
    n = len(ficheros)
    print('URL del curso en Lynda.com: ' + url)

    if n>1:
        message.colored_message(Fore.LIGHTGREEN_EX, 'o' * 100)
        message.colored_message(Fore.LIGHTGREEN_EX, 'Número de ficheros de EJERCICIOS (zip): ' + str(n) + ' <------- CURSO CON MAS DE UN FICHERO DE EJERCICIOS !!!')   
        message.colored_message(Fore.LIGHTGREEN_EX, 'o' * 100)
    else:
        print('Número de ficheros de EJERCICIOS (zip) = ' + str(n))

    print("-" * 100)
    print("EJERCICIOS (RESUMEN)")
    i=1
    for fichero in ficheros:
        message.colored_message(str(i) + ') ' + Fore.LIGHTYELLOW_EX, fichero.text )
        i+=1
    print("-" * 100)

    i=1
    for fichero in ficheros:
        message.colored_message(Fore.LIGHTYELLOW_EX, fichero.text + ' (' + str(i) + ' de ' + str(n) + ')')
        print("-" * 100)
        individual(driver, fichero, course_folder)
        time.sleep(2)
        i+=1

    driver.close()


def individual(driver, fichero, course_folder):
    # Descarga de un fichero de ejercicios
  
    ex_file_name = fichero.text
    logging.info('individual: ex_file_name=' + ex_file_name)

    # Compruebo si ya existe y por tanto ya se ha descargado el fichero para evitar descargarlo de nuevo
    downloads_folder = install.get_path("Downloads")
    origen = downloads_folder +'/'+ ex_file_name
    destino = course_folder+'/'+ex_file_name

    if Path(destino).is_file():
        message.carriage_return_animate('Se omite la descarga del fichero ' + origen)
        message.colored_message(Fore.LIGHTGREEN_EX, 'Ya existe: ' + destino + ' ---> Ahorro de ancho de banda :)' )
        return
    else:

        if Path(origen).is_file():
            message.colored_message(Fore.LIGHTRED_EX, 'Ya existe el fichero en el directorio de descargas: ' + origen) 
            message.colored_message(Fore.LIGHTRED_EX, 'Se borrará y volverá a descargar ya que tuvo que quedarse a medias') 
            try:
                os.remove(origen)
                message.colored_message(Fore.LIGHTGREEN_EX, 'Fichero borrado: ' + origen)
            except: 
                message.colored_message(Fore.LIGHTRED_EX, 'Error al borrar el fichero: ' + origen)
                logging.error('Al borrar el fichero %s', origen)
                return

        # Make sure page is more fully loaded before finding the element
        try:
            action=ActionChains(driver)
            action.move_to_element(fichero).click().perform()
        except:
            WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, "html.no-touch.member.loaded")))
            driver.find_element_by_css_selector('#exercise-tab').click()
            fichero.click()
           
        print('DESCARGANDO: ' + ex_file_name)
        
        file_not_found = True
        while file_not_found:
            message.spinning_cursor()
            os.chdir(downloads_folder)
            for folder in os.listdir(downloads_folder):
                if folder == ex_file_name:
                    print("\r{0}".format(' Descargando...'), end='')
                    if os.path.getsize(folder) > 0: # if file downloaded completely.
                        print('Descarga completada a ' + downloads_folder)
                        file_not_found = False
            time.sleep(2)

        try:
            print('Moviendo: '+  origen + ' a ' + destino)
            shutil.move(origen, destino )
            print('Fichero de ejercicios: ' + origen + ' movido a ' + destino + ' con EXITO')
        except:
            message.colored_message(Fore.LIGHTRED_EX, 'Error al mover el fichero!!!') 
            logging.error('Al mover el fichero %s a %s', origen, destino)


def lib_login(url, course_folder, driver):
    driver.get("https://www.lynda.com/portal/sip?org=" + read.organization_url)  # launch lynda.com/signin

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
    time.sleep(2)


def regular_login(url, course_folder, driver):
    driver.get("https://www.lynda.com/signin/")  # launch lynda.com/signin

    # enter username
    email = driver.find_element_by_css_selector("#email-address")
    email.clear()
    email.send_keys(read.username)
    driver.find_element_by_css_selector('#username-submit').click()
    print('\nusername successfully entered ....')
    time.sleep(2)

    # enter password
    passwrd = driver.find_element_by_css_selector('#password-input')
    passwrd.send_keys(read.password)
    driver.find_element_by_css_selector('#password-submit').click()
    print('password successfully entered ....')
    time.sleep(2)
