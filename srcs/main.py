#!/usr/bin/env python3

# from Parsing import Parsing
from Logger import Logger
import os, sys
# from webbot import Browser

from selenium import webdriver

# Opening the website

URL = "https://125.galaxyexperienceparis.com/fr/intro/login"

# web = Browser()

def getEnvVariable(name : str) :
    if os.environ.get(name) :
        return os.environ.get(name)
    raise Exception(f'No env variable found {name}') 
    

def main():
    try :
        logger = Logger()
        EMAIL = getEnvVariable('EMAIL')

        options = webdriver.ChromeOptions()
        webdriver.ChromeService(log_output="selenium.log")
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=options)
        # Here Chrome will be used
        # driver = webdriver.Chrome()

        # web.go_to(URL)
        driver.get(URL)
        logger.Info(f"Web browser go to {URL}")

        # getting the button by class name
        button = driver.find_element_by_class_name("slide-out-btn")

        # clicking on the button
        button.click()
        # web.type(EMAIL, into='email')
        # web.click('Continuez')

        # TODO Faire la verif des politiques 
        # web.click('Politique de confidentialité')
        # web.click('Conditions d’utilisation')


        # web.type
        # agendar = Parsing(URL_FR, logger)
        # agendar.getPage()
        logger.Info("End of script")
    except Exception as error :
        logger.Error(error)
        print(error, file=sys.stderr)
    return

if __name__ == "__main__" :
    main()