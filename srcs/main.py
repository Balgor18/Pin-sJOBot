#!/usr/bin/env python3

from Logger import Logger
from Website import Website
import sys, signal
from functools import partial

# Opening the website

URL = "https://125.galaxyexperienceparis.com/fr/intro/login"

def signal_handler(logger : Logger, sig : signal, frame) -> None:
    logger.Error("Programme stop by CTRL+C")
    Logger.WRITE_LOG = False
    sys.exit(1)

def main() -> None:
    try :
        logger = Logger()
        logger.Info("Start the code")
        signal.signal(signal.SIGINT, partial(signal_handler, logger))

        website = Website(URL, logger, debug=False)

        website.connect()
        website.goToPhrygesPage()

        website.getPhryges()

    except Exception as error :
        logger.Error(error)
        print(error, file=sys.stderr)

    return

if __name__ == "__main__" :
    main()