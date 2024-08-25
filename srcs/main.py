#!/usr/bin/env python3

from Logger import Logger
from Website import Website
# from tools import getEnvVariable
import sys

# Opening the website

URL = "https://125.galaxyexperienceparis.com/fr/intro/login"

def main():
    try :
        logger = Logger()
        website = Website(URL, logger)

        website.connect()
        website.goToPhrygesPage()

    except Exception as error :
        logger.Error(error)
        print(error, file=sys.stderr)

    return

if __name__ == "__main__" :
    main()