from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
from Logger import Logger
from typing import List
from Sqlite import Sqlite
from enum import Enum

class Langue(Enum):
    FRENCH = 1
    ENGLISH = 2

MONTHS_EN = dict(
    January="01",
    February="02",
    March="03",
    April="04",
    May="05",
    June="06",
    July="07",
    August="08",
    September="09",
    October="10",
    November="11",
    December="12"
    )

MONTHS_FR = dict(
    Janvier="01",
    Février="02",
    Mars="03",
    Avril="04",
    Mai="05",
    Juin="06",
    Juillet="07",
    Août="08",
    Septembre="09",
    Octobre="10",
    Novembre="11",
    Décembre="12"
    )

class Parsing():

    def __init__(self, url, logger: Logger):
        self.logger = logger
        self.url : str = url
        options = webdriver.ChromeOptions()
        webdriver.ChromeService(log_output="selenium.log")
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=options)
        return

    def getPage(self):
        self.logger.Info("request GET on " + self.url)
        self.driver.get(self.url)
        delay = 20 # seconds
        try:
            myElem = WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.ID, '_next-gtm')))
            self.logger.Debug(f"{myElem}")
            self._getEvent(myElem)
        except TimeoutException:
            self.logger.Error(f"Loading took too much time !")
            exit(1)
        # self.driver.find_element("class", "EventMatch")
        self._getEvent(self.driver.page_source)


    def _getEvent(self, response):
        soup = BeautifulSoup(response, 'html.parser')
        if soup.find("div", class_="fr-FR") :
            self.lang : int = Langue.FRENCH
        else :
            self.lang : int = Langue.ENGLISH
        self.logger.Debug(f"{soup}")
        events : str = soup.find_all("div", class_=["EventMatch","EventDate"])
        self._getMatch(events)

    def _getTeam(self, teams : str , name : str) -> str :
        team = teams.find("div", name)
        return team.find("span", "name").text

    def _getTime(self, times : str) -> str:
        hour : str = times.find("span", "hour").text
        minute : str = times.find("span", "minute").text
        return (hour + ":" + minute)

    def _getLeague(self, league : str) -> str :
        result = league.find("div", class_="name")
        if not result:
            return "No Data Found"
        return result.text

    def _logMatch(self, day: str, month : str, teams : List[str], league: str, timeMatch : str) :
        self.logger.Info(day + "-" + month + " " + league + " " + teams[0] + " VS " + teams[1] + " time " + timeMatch)
        return

    def _getDateMatch(self, dateData : str) :
        day = dateData.find("span", "monthday").text
        day, monthStr = day.split(" ")
        if int(day) < 10 :
            day = "0" + str(day)
        monthStr = monthStr.capitalize()
        if self.lang == Langue.FRENCH :
            month = MONTHS_FR[monthStr]
        else :
            month = MONTHS_EN[monthStr]
        values = {
            "day" : day,
            "month" : {"numeric" : month, "str" : monthStr}
        }
        return values

    def _getMatchInfo(self, match : str):
        teams : str = match.find("div", "teams")
        team1 : str = self._getTeam(teams, "team1")
        team2 : str = self._getTeam(teams, "team2")
        if not match.find("span", class_="live-label") :
            timeMatch : str = self._getTime(match.find("div", "time"))
        else :
            timeMatch = "DIRECT"
        league = self._getLeague(match.find("div", class_="league"))
        values = {
            "teams" : [team1, team2],
            "time" : timeMatch,
            "league" : league
            }
        return values

    def _getMatch(self, matchs: str) :
        for match in matchs:
            if not match.find("div", class_="score"):
                if match.find("div", class_="date"):
                    date = self._getDateMatch(match)
                    self.logger.Info("Match of day " + date["day"]+ " " + date["month"]["str"])
                    db = Sqlite(date["day"] + "_" + date["month"]["numeric"] + ".sqlite", self.logger)
                else :
                    dataMatch = self._getMatchInfo(match)
                    self._logMatch(date["day"], date["month"]["str"], [dataMatch["teams"][0], dataMatch["teams"][1]], dataMatch["league"], dataMatch["time"]);
                    db.insertIntoTableMatch(dataMatch)
        if len(matchs) == 0 :
            self.logger.Info("No Match found")

    def __del__(self) :
        self.driver.quit()