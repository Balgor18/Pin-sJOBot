#!/usr/bin/env python3

# from Parsing import Parsing
from Logger import Logger
import os, sys, time
# from webbot import Browser

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
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


        # Here Chrome will be used
        options = webdriver.ChromeOptions()
        webdriver.ChromeService(log_output="selenium.log")
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=options)

        driver.get(URL)
        logger.Info(f"Web browser go to {URL}")

        
        # Wait for the page to load
        try :
            WebDriverWait(driver, 10).until(
                expected_conditions.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Inscription')]"))
            )
            try :
                WebDriverWait(driver, 10).until(
                    expected_conditions.text_to_be_present_in_element((By.TAG_NAME, "body"), "Politique de confidentialité")
                )

                # Select Politique
                button = driver.find_element(By.XPATH, "//span[contains(text(), 'Politique de confidentialité')]")
                button.click()

                time.sleep(2)
                # Scroll Down
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                # Accept bouton condition
                accept_button = driver.find_element(By.XPATH, "//p[contains(text(), 'Accepter')]")
                accept_button.click()
            except : 
                logger.Error("Error on politique")
                return

            try :
                WebDriverWait(driver, 10).until(
                    expected_conditions.text_to_be_present_in_element((By.TAG_NAME, "body"), "Conditions d’utilisation")
                )

                # Select Utilisation Condition
                button = driver.find_element(By.XPATH, "//span[contains(text(), 'Conditions d’utilisation')]")
                button.click()
                time.sleep(2)

                # Scroll Down
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                # Accept bouton condition
                accept_button = driver.find_element(By.XPATH, "//p[contains(text(), 'Accepter')]")
                accept_button.click()
            except :
                logger.Error("Error on utilisation condition")
                return

            # Now click on continue
            continue_button = driver.find_element(By.XPATH, "//p[contains(text(), 'Continuez')]")
            continue_button.click()

        except :
            logger.Error("Page is not load")
            return

        # Load email
        try :
            email_input = WebDriverWait(driver, 10).until(
                expected_conditions.element_to_be_clickable((By.XPATH, "//input[@type='email']"))
            )
            email_input = driver.find_element(By.XPATH, "//input[@type='email']")
            email = getEnvVariable('EMAIL')
            email_input.send_keys(email)

            continue_button = driver.find_element(By.XPATH, "//p[contains(text(), 'Continuez')]")
            continue_button.click()
            time.sleep(2)
        except :
            logger.Error("Il ne trouve pas l'input pour l'email")
            return
        logger.Info("Email good")

        try :
            WebDriverWait(driver, 10).until(
                expected_conditions.element_to_be_clickable((By.XPATH, "//input[@type='password']"))
            )

            password_input = driver.find_element(By.XPATH, "//input[@type='password']")
            password = getEnvVariable('PASSWORD')
            password_input.send_keys(password)

            continue_button = driver.find_element(By.XPATH, "//p[contains(text(), 'Suivant')]")
            continue_button.click()

        except :
            logger.Error("Il ne trouve pas l'input pour le password")
            return
        logger.Info('Password good')

        logger.Info("We are connected")


        logger.Info("End of script")
    except Exception as error :
        logger.Error(error)
        print(error, file=sys.stderr)
    return

if __name__ == "__main__" :
    main()