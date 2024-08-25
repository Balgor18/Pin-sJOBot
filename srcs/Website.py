
from Logger import Logger
from tools import getEnvVariable
import time, os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

SAVE_FOLDERS = "LOG_SCREEN"
class Website():
    """docstring for Website."""

    # Here Chrome will be used
    def __init__(self, url : str, logger: Logger, debug : bool = False):
        self.url = url
        self.logger = logger
        self.debug = debug
        options = webdriver.ChromeOptions()
        webdriver.ChromeService(log_output="selenium.log")
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=options)

        if debug :
            self.logger.Info(f"Debug value is turn ON. Information in {SAVE_FOLDERS}")
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
        self.driver.get("https://125.galaxyexperienceparis.com/fr/pin-board/phryges")
        time.sleep(2)
        if (self.debug) :
            self.driver.save_screenshot(f"{SAVE_FOLDERS}/phryges_page.png")


    def __del__(self) :
        self.driver.quit()
