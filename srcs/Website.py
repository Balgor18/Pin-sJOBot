
from Logger import Logger
from tools import getEnvVariable
import time, os
from typing import Tuple

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

SAVE_FOLDERS = "LOG_SCREEN"

MAX_PINS_VIRUTAL = 48

WAIT_1_HOUR = 3600

LOCATIONS_PINS : Tuple[dict] = [
    {"name" : "Middle Stade de France", "latitude" : 48.924542,"longitude" : 2.360169},
    {"name" : "Stade de France Porte X", "latitude" : 48.923055,"longitude" : 2.357934},
    {"name" : "West of Stade de France", "latitude" : 48.924112,"longitude" : 2.351847},
    {"name" : "Carrefour Near of Stade de France", "latitude" : 48.920204,"longitude" : 2.345034},
    {"name" : "Plaine Saint Denis near N1", "latitude" : 48.90371, "longitude" :2.35894},
    {"name" : "Colombes Tennis", "latitude" : 48.93072, "longitude" :2.250156},
    {"name" : "Middle of Paris near 3 subway station", "latitude" : 48.85254, "longitude" :2.333281},
    {"name" : "Porte D'Orleans", "latitude" : 48.819966,"longitude" : 2.324762},
    {"name" : "Vaire sur Marne", "latitude" : 48.865491,"longitude" : 2.62689},
    {"name" : "Guyancourt Golf", "latitude" : 48.750457,"longitude" : 2.072079},
    {"name" : "Versaille", "latitude" : 48.813259,"longitude" : 2.083915}
    # TODO Create other point
]

class Website():
    """docstring for Website."""

    def __init__(self, url : str, logger: Logger, debug : bool = False):
        self.url : str = url
        self.logger : Logger = logger
        self.debug : bool = debug
        self.currentVirtualPins : int = 0
        options = webdriver.ChromeOptions()
        webdriver.ChromeService(log_output="selenium.log")
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.geolocation": 1
        })
        options.add_argument("--disable-geolocation")
        self.driver = webdriver.Chrome(options=options)

        if debug :
            self.logger.Debug(f"Debug value is turn ON. Information in {SAVE_FOLDERS}")
            if not os.path.exists(SAVE_FOLDERS):
                os.makedirs(SAVE_FOLDERS)

    def _legalNotice(self, name : str) -> None :
        WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located((By.XPATH, "//p[contains(text(), 'Politique de confidentialité')]"))
        )
        try :
            if (self.debug) :
                self.driver.save_screenshot(f"{SAVE_FOLDERS}/{name}_0.png")
            WebDriverWait(self.driver, 10).until(
                expected_conditions.text_to_be_present_in_element((By.TAG_NAME, "body"), f"{name}")
            )
            if (self.debug) :
                self.driver.save_screenshot(f"{SAVE_FOLDERS}/{name}_1.png")

            # Select Politique
            button = self.driver.find_element(By.XPATH, f"//span[contains(text(), '{name}')]")
            button.click()

            if (self.debug) :
                self.driver.save_screenshot(f"{SAVE_FOLDERS}/{name}_2.png")

            time.sleep(2)

            # Scroll Down
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Accept bouton condition
            accept_button = self.driver.find_element(By.XPATH, "//p[contains(text(), 'Accepter')]")
            accept_button.click()

            if (self.debug) :
                self.driver.save_screenshot(f"{SAVE_FOLDERS}/{name}_3.png")

        except : 
            self.logger.Critical(f"Error on accept {name}")
            exit(1)
        return

    def _inputEmail(self) -> None :
        try :
            email_input = WebDriverWait(self.driver, 10).until(
                expected_conditions.element_to_be_clickable((By.XPATH, "//input[@type='email']"))
            )
            if (self.debug) :
                self.driver.save_screenshot(f"{SAVE_FOLDERS}/email_page.png")
            email_input = self.driver.find_element(By.XPATH, "//input[@type='email']")
            email = getEnvVariable('EMAIL')
            email_input.send_keys(email)
            if (self.debug) :
                self.driver.save_screenshot(f"{SAVE_FOLDERS}/input_email.png")

            continue_button = self.driver.find_element(By.XPATH, "//p[contains(text(), 'Continuez')]")
            continue_button.click()
            if (self.debug) :
                self.driver.save_screenshot(f"{SAVE_FOLDERS}/click_button_email.png")
            time.sleep(2)
        except Exception as error:
            self.logger.Critical(f"Mail block {error}")
            exit (1)
        return

    def _inputPassword(self) -> None :
        try :
            WebDriverWait(self.driver, 10).until(
                expected_conditions.element_to_be_clickable((By.XPATH, "//input[@type='password']"))
            )

            password_input = self.driver.find_element(By.XPATH, "//input[@type='password']")
            password = getEnvVariable('PASSWORD')
            password_input.send_keys(password)

            continue_button = self.driver.find_element(By.XPATH, "//p[contains(text(), 'Suivant')]")
            continue_button.click()

        except Exception as error :
            self.logger.Critical(f"Password block {error}")
            exit (1)
        return

    def connect(self) :
        self.driver.get(self.url)
        self.logger.Info(f"Web browser go to {self.url}")
        time.sleep(4)

        if (self.debug) :
            self.driver.save_screenshot(f"{SAVE_FOLDERS}/Connect_1.png")
        try :
            WebDriverWait(self.driver, 10).until(
                expected_conditions.presence_of_element_located((By.XPATH, "//p[contains(text(), 'Rejoindre')]"))
            )
            if (self.debug) :
                self.driver.save_screenshot(f"{SAVE_FOLDERS}/Connect_2.png")
        except :
            self.goToConnectionPage()

        if (self.debug) :
            self.driver.save_screenshot(f"{SAVE_FOLDERS}/Connect_3.png")
        self.connection()

    def connection(self) -> None :

        self.logger.Info("Start Authentification")

        self._inputEmail()
        if (self.debug) :
            self.driver.save_screenshot(f"{SAVE_FOLDERS}/email.png")
        self._inputPassword()
        if (self.debug) :
            self.driver.save_screenshot(f"{SAVE_FOLDERS}/password.png")

        self.logger.Info("End Authentification")

        time.sleep(2)
        if (self.debug) :
            self.driver.save_screenshot(f"{SAVE_FOLDERS}/Connected.png")
        self.logger.Info("Connection OK")

    def goToConnectionPage(self) -> None :
        try :
            self.logger.Info("Start Legal notice")
            self._legalNotice("Politique de confidentialité")
            self._legalNotice("Conditions d’utilisation")
            self.logger.Info("Finish Legal notice")

            # Now click on continue
            continue_button = self.driver.find_element(By.XPATH, "//p[contains(text(), 'Continuez')]")
            continue_button.click()

        except Exception as error :
            self.logger.Critical(f"Error goToConnectionPage {error}")
            return
        return

    def goToPhrygesPage(self) -> None :
        URL = "https://125.galaxyexperienceparis.com/fr/pin-board/phryges"
        self.logger.Info(f"Web browser go to {URL}")
        self.driver.get(URL)
        time.sleep(2)
        if (self.debug) :
            self.driver.save_screenshot(f"{SAVE_FOLDERS}/phryges_page.png")

    def _statusPhryges(self) -> None :
        try :
            virtualPins = WebDriverWait(self.driver, 10).until(
                expected_conditions.presence_of_element_located((By.XPATH, "//*[contains(@class, 'PhrygesBoard_currentstamp__')]"))
            )
            self.currentVirtualPins = virtualPins.text
            self.logger.Info(f" Status Pin's virtual : {self.currentVirtualPins}/{MAX_PINS_VIRUTAL}")

            button_qrcode = WebDriverWait(self.driver, 10).until(
                expected_conditions.presence_of_element_located((By.XPATH, "//img[@alt='qr icon']"))
            )
            button_qrcode.click()
            time.sleep(2)


            collectablePins = WebDriverWait(self.driver, 10).until(
                expected_conditions.presence_of_element_located((By.XPATH, "//div[contains(@class, 'QrOperationImageBox_count')]"))
            )
            self.logger.Info(f" Status collectable Pin's : {collectablePins.text} !")

            closeModal = WebDriverWait(self.driver, 10).until(
                expected_conditions.presence_of_element_located((By.XPATH, "//div[contains(@class, 'CircleButton_circlebtn_innercontainer')]"))
            )
            closeModal.click()

        except Exception as error: 
            self.driver.save_screenshot("error_screenshot.png")
            self.logger.Critical(f"Error on _statusPhryges {error}")
            exit(1)
        return

    def _collectPhryges(self, name : str) -> None :
        try : 
            self.logger.Info(f"Try to get the pin's locate at {name}")
            buttonGetPins = WebDriverWait(self.driver, 10).until(
                expected_conditions.presence_of_element_located((By.XPATH, "//*[contains(@class, 'PhrygesPinSection_link_title')]"))
            )
            buttonGetPins.click()
            # TODO Left the page
            time.sleep(2)

            # self.driver.save_screenshot("Status.png")

            # if () : # J'ai pas trouvée 
            # TODO MESSAGE ERROR VERIF COORD GPS || RETRY
            #     self.logger.Warning(f"Error pin's not found need to retry {name}")
            #     self.logger.Warning(f"if the error still appear verify coord GPS of \"{name}\"")
            #     self._collectPhryges(name)
            
            self.logger.Info("Congrats new pin's Add")
        except Exception as error :
            self.logger.Error(f"Error on _collectPhryges {error}")
        return

    def getPhryges(self) -> None :
        while True :
            for location in LOCATIONS_PINS :

                self._statusPhryges()

                if (self.currentVirtualPins == MAX_PINS_VIRUTAL) :
                    self.logger.Warning("ATTENTION Max pin's virtuel reached")
                    time.sleep(11 * WAIT_1_HOUR)
                    continue

                self.driver.execute_cdp_cmd("Emulation.setGeolocationOverride", {
                    "latitude": location['latitude'],
                    "longitude": location['longitude'],
                    "accuracy": 1
                })

                # DEBUG ================================================
                # self.driver.get("https://www.google.com/maps")

                # self.driver.execute_cdp_cmd("Emulation.setGeolocationOverride", {
                #     "latitude": 48.8720949,
                #     "longitude": 2.3323339,
                #     "accuracy": 1
                # })

                # self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                # continue_button = self.driver.find_element(By.XPATH, "//span[contains(text(), 'Tout accepter')]")
                # continue_button.click()
                # DEBUG ================================================

                self._collectPhryges(location['name'])

                time.sleep(30)
            time.sleep(WAIT_1_HOUR * 6)
            return 


    def __del__(self) :
        self.driver.quit()
