
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

WAIT_1_MINUTE = 60

RETRY_MAX = 0

LOCATIONS_PHYRGE_PINS : Tuple[dict] = [
    {"name" : "Opéra Garnier", "latitude" : 48.872028,"longitude" : 2.331785},
    {"name" : "Exposition Versaille", "latitude" : 48.828522,"longitude" : 2.289897},
    {"name" : "Exposition Versaille 2", "latitude" : 48.82853,"longitude" : 2.289871},
    {"name" : "Entrance Versaille exposition", "latitude" : 48.831011,"longitude" : 2.287623},
    {"name" : "Roland Garros", "latitude" : 48.846867,"longitude" : 2.250618},
    {"name" : "Champs de mars ecole militaire", "latitude" : 48.852716,"longitude" : 2.301034},
    {"name" : "Eiffel Tower", "latitude" : 48.857513,"longitude" : 2.296488},
    {"name" : "Quai Anatole France", "latitude" : 48.862244,"longitude" : 2.320151},
    {"name" : "Gare de l'Est", "latitude" : 48.874317,"longitude" : 2.358361},
    {"name" : "Near Chatelet", "latitude" : 48.862597,"longitude" : 2.341484},
    {"name" : "Pyramides", "latitude" : 48.864483,"longitude" : 2.332753},
    {"name" : "Concorde Stadium", "latitude" : 48.865621,"longitude" : 2.324362},
    {"name" : "Rue royale", "latitude" : 48.867838,"longitude" : 2.322569},
    {"name" : "Champs-Elysees 1", "latitude" : 48.873329,"longitude" : 2.298051},
    {"name" : "Champs-Elysees 2", "latitude" : 48.873327,"longitude" : 2.298274},
    {"name" : "Champs-Elysees 3", "latitude" : 48.872235,"longitude" : 2.298298},
    {"name" : "Champs-Elysees 4", "latitude" : 48.872461,"longitude" : 2.300274},
    {"name" : "Champs-Elysees 5", "latitude" : 48.872297,"longitude" : 2.299724},
    {"name" : "Champs-Elysees 6", "latitude" : 48.872302,"longitude" : 2.299734},
    {"name" : "Champs-Elysees 7", "latitude" : 48.871546,"longitude" : 2.300453},
    {"name" : "Champs-Elysees 8", "latitude" : 48.871901,"longitude" : 2.300807},
    {"name" : "Champs-Elysees 9", "latitude" : 48.870895,"longitude" : 2.302781},
    {"name" : "Champs-Elysees 10", "latitude" : 48.871499,"longitude" : 2.305449},
    {"name" : "Champs-Elysees 11", "latitude" : 48.870420,"longitude" : 2.304580},
    {"name" : "Champs-Elysees 12", "latitude" : 48.871074,"longitude" : 2.305854},
    {"name" : "Champs-Elysees 13", "latitude" : 48.870411,"longitude" : 2.306893},
    {"name" : "Champs-Elysees 14", "latitude" : 48.870121,"longitude" : 2.308167},
    {"name" : "Champs-Elysees 15", "latitude" : 48.869297,"longitude" : 2.307707},
    {"name" : "Champs-Elysees 16", "latitude" : 48.869653,"longitude" : 2.308656},
    {"name" : "Champs-Elysees 17", "latitude" : 48.868333,"longitude" : 2.309426},
    {"name" : "Place de la Défense 1", "latitude" : 48.892531,"longitude" : 2.237661},
    {"name" : "Place de la Défense 2", "latitude" : 48.891762,"longitude" : 2.237174},
    {"name" : "Place de la Défense 3", "latitude" : 48.891774,"longitude" : 2.236158},
    {"name" : "Place de la Défense 4", "latitude" : 48.891905,"longitude" : 2.234358},

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
]

LOCATIONS_K_POP_PINS : Tuple[dict] = [
    {"name" : "CE125", "latitude" : 48.872505,"longitude" : 2.297884},
    {"name" : "OLP", "latitude" : 48.868674,"longitude" : 2.31139},
    {"name" : "SES Rosny", "latitude" : 48.881054,"longitude" : 2.476764},
    {"name" : "SES Velizy", "latitude" : 48.78017,"longitude" : 2.220484},
    {"name" : "SES Madeleine", "latitude" : 48.870209,"longitude" : 2.322898},
    {"name" : "SES La Défense", "latitude" : 48.89198,"longitude" : 2.23881},
    {"name" : "Fnac Ternes", "latitude" : 48.879065,"longitude" : 2.294935},
    {"name" : "Fnac Beaugrenelle", "latitude" : 48.848462,"longitude" : 2.282393},
    {"name" : "Fnac Montparnasse", "latitude" : 48.84586,"longitude" : 2.325508},
    {"name" : "Fnac St Lazare", "latitude" : 48.875348,"longitude" : 2.326998},
    {"name" : "Fnac Forum", "latitude" : 48.861546,"longitude" : 2.346947},
    {"name" : "Fnac Champs Elysées", "latitude" : 48.87128,"longitude" : 2.304682},
    {"name" : "Arc de triomphe", "latitude" : 48.873779,"longitude" : 2.295037},
    {"name" : "Notre-Dame", "latitude" : 48.852937,"longitude" : 2.35005},
    {"name" : "The Louvre", "latitude" : 48.861033,"longitude" : 2.335834},
    {"name" : "Opéra Garnier", "latitude" : 48.872028,"longitude" : 2.331785}
]

class Website():
    """docstring for Website."""

    def __init__(self, url : str, logger: Logger, debug : bool = False):
        self.url : str = url
        self.logger : Logger = logger
        self.debug : bool = debug
        self.currentVirtualPins : int = 0
        self.retry : int = 0
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

            time.sleep(2)
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
        time.sleep(3)

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
            time.sleep(10)

            # DEBUG
            # print(self.driver.page_source)
            self.driver.save_screenshot(f"Phryges_Status_{name}.png")

            status_pins = WebDriverWait(self.driver, 10).until(
                expected_conditions.presence_of_element_located((By.XPATH, "//*[contains(@class, 'GPSMainSection_text_')]"))# GPSMainSection_text_found
            )

            
            if (status_pins.text == "Aucun pin n‘a été trouvé.") : # J'ai pas trouvée 
                self.logger.Warning(f"Error pin's not found need to retry {name} retry {self.retry}/{RETRY_MAX}")
                self.logger.Warning(f"if the error still appear verify coord GPS of \"{name}\"")
                retryPins = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Vers le tableau de pins')]")
                retryPins.click()
                if (self.retry == RETRY_MAX) :
                    self.logger.Warning("Skip maximum retry")
                    self.retry = 0
                    return
                self.retry += 1
                time.sleep(5)
                self._collectPhryges(name)
            elif (status_pins.text == "Un pin a été trouvé !") :
                self.driver.save_screenshot(f"Status_{name}.png")
                self.logger.Info("Congrats new pin's Add")
                getPins = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Recevoir le pin')]")
                getPins.click()
                
            else :
                statusPinsPlace = WebDriverWait(self.driver, 10).until(
                    expected_conditions.presence_of_element_located((By.XPATH, "//*[contains(@class, 'GPSMainSection_timer')]"))
                )
                self.logger.Info(f"I already have it {name} need to wait {statusPinsPlace.text}")
                getPins = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Vers le tableau de pins')]")
                getPins.click()

            self.retry = 0
            time.sleep(2)
        except Exception as error :
            self.logger.Error(f"Error on _collectPhryges {error}")
        return

    def _statusKpop(self) -> None :
        try :
            virtualPins = WebDriverWait(self.driver, 10).until(
                expected_conditions.presence_of_element_located((By.XPATH, "//*[contains(@class, 'KDigitalPinBoard_currentstamp__')]"))
            )
            currentVirtualPins = virtualPins.text
            self.logger.Info(f" Status Pin's virtual : {currentVirtualPins}/36")

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

    def _collectKpop(self, name : str) -> None :
        # TODO Go to Kpop Page and launch the collect
        try : 
            self.logger.Info(f"Try to get the K-POP pin's locate at {name}")
            buttonGetPins = WebDriverWait(self.driver, 10).until(
                expected_conditions.presence_of_element_located((By.XPATH, "//*[contains(@class, 'KDigitalPinSection_link_title')]"))
            )
            buttonGetPins.click()
            time.sleep(10)

            # DEBUG
            # print(self.driver.page_source)
            self.driver.save_screenshot(f"K-POP_Status_{name}.png")

            status_pins = WebDriverWait(self.driver, 10).until(
                expected_conditions.presence_of_element_located((By.XPATH, "//*[contains(@class, 'GPSMainSection_text_')]"))# GPSMainSection_text_found
            )

            
            if (status_pins.text == "Aucun pin n‘a été trouvé.") : # J'ai pas trouvée 
                self.logger.Warning(f"Error K-POP pin's not found need to retry {name} retry {self.retry}/{RETRY_MAX}")
                self.logger.Warning(f"if the error still appear verify coord GPS of \"{name}\"")
                retryPins = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Vers le tableau de pins')]")
                retryPins.click()
                if (self.retry == RETRY_MAX) :
                    self.logger.Warning("Skip maximum retry")
                    self.retry = 0
                    return
                self.retry += 1
                time.sleep(5)
                self._collectKpop(name)
            elif (status_pins.text == "Un pin a été trouvé !") :
                self.driver.save_screenshot(f"K-POP_Status_{name}.png")
                self.logger.Info("Congrats new KPop pin's Add")
                getPins = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Recevoir le pin')]")
                getPins.click()
                
            else :
                statusPinsPlace = WebDriverWait(self.driver, 10).until(
                    expected_conditions.presence_of_element_located((By.XPATH, "//*[contains(@class, 'GPSMainSection_timer')]"))
                )
                self.logger.Info(f"I already have it {name} need to wait {statusPinsPlace.text}")
                getPins = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Vers le tableau de pins')]")
                getPins.click()

            self.retry = 0
            time.sleep(2)
        except Exception as error :
            self.logger.Error(f"Error on _collectKpop {error}")
        return

    def getPhryges(self) -> None :
        while True :

            # Virtual Phryges 
            URL = "https://125.galaxyexperienceparis.com/fr/pin-board/phryges"
            self.logger.Info(f"Web browser go to {URL}")
            self.driver.get(URL)
            time.sleep(2)
            if (self.debug) :
                self.driver.save_screenshot(f"{SAVE_FOLDERS}/phryges_page.png")
            self._statusPhryges()
            for location in LOCATIONS_PHYRGE_PINS :

                if (int(self.currentVirtualPins) == MAX_PINS_VIRUTAL) :
                    self.logger.Warning("ATTENTION Max pin's virtuel reached")
                    time.sleep(WAIT_1_MINUTE * 30)
                    break

                self.driver.execute_cdp_cmd("Emulation.setGeolocationOverride", {
                    "latitude": location['latitude'],
                    "longitude": location['longitude'],
                    "accuracy": 1
                })

                self._collectPhryges(location['name'])
                time.sleep(WAIT_1_MINUTE * 5)

            self.logger.Info("End of phryges location")
            self._statusPhryges()

            # K-POP Pins
            URL = "https://125.galaxyexperienceparis.com/fr/pin-board/k-digital"
            self.logger.Info(f"Web browser go to {URL}")
            self.driver.get(URL)
            time.sleep(2)
            if (self.debug) :
                self.driver.save_screenshot(f"{SAVE_FOLDERS}/K-POP_page.png")
            self._statusKpop()
            for location in LOCATIONS_K_POP_PINS :

                self.driver.execute_cdp_cmd("Emulation.setGeolocationOverride", {
                    "latitude": location['latitude'],
                    "longitude": location['longitude'],
                    "accuracy": 1
                })

                self._collectKpop(location['name'])
                time.sleep(WAIT_1_MINUTE * 5)

            self.logger.Info("End of K-POP location")
            self._statusKpop()

            time.sleep(WAIT_1_MINUTE * 30)


    def __del__(self) :
        self.driver.quit()
