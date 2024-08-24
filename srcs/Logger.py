import sys, style, datetime, os
from enum import Enum
from colorama import Fore, Style

FOLDERNAME = "Log/"

class Logger():
    
    COLORS = {
        'DEBUG': Fore.BLUE,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.RED + Style.BRIGHT,
    }

    def __init__(self):
        self.closeFile : bool= True
        path = os.path.join(os.environ.get('PWD'), FOLDERNAME)
        filename : str = path + "Pin's_" + datetime.datetime.today().strftime('%B_%d') + ".log"
        if self._existFolder(path)is False :
            self._createFolder(path)
        try :
            self.file = open(filename, 'w')
            self.Info("File create " + filename)
        except Exception as e: 
            print(f"[{style.red('ERROR')}] Creation file {filename} exception {e}", file=sys.stderr)
            exit(1)

    # TODO Check if this class have to create the folder of log
    def _createFolder(self, path : str) -> bool :
        try : 
            os.mkdir(path)
        except Exception as e :
            print(f"[{style.red('ERROR')}] Creation folder {path} exception {e}", file=sys.stderr)
            self.closeFile = False
            exit(1)

    def _existFolder(self, name : str) -> bool :
        if os.path.isdir(name) :
            return True
        return False

        

    def Info(self, logInfo: str):
        time = datetime.datetime.today().strftime('%Hh%M:%S')
        print(f"[{self.COLORS.get('INFO')}INFO{Style.RESET_ALL}] {str(time)} {logInfo}", file=self.file)

    def Debug(self, logInfo : str):
        time = datetime.datetime.today().strftime('%Hh%M:%S')
        print(f"[{self.COLORS.get('DEBUG')}DEBUG{Style.RESET_ALL}] {str(time)} {logInfo}", file=self.file)

    def Error(self, logInfo : str) :
        time = datetime.datetime.today().strftime('%Hh%M:%S')
        print(f"[{self.COLORS.get('ERROR')}ERROR{Style.RESET_ALL}] {str(time)} {logInfo}", file=self.file)

    def Warning(self, logInfo : str) :
        time = datetime.datetime.today().strftime('%Hh%M:%S')
        print(f"[{self.COLORS.get('WARNING')}WARNING{Style.RESET_ALL}] {str(time)} {logInfo}", file=self.file)

    def Critical(self, logInfo : str) :
        time = datetime.datetime.today().strftime('%Hh%M:%S')
        print(f"[{self.COLORS.get('CRITICAL')}CRITICAL{Style.RESET_ALL}] {str(time)} {logInfo}", file=self.file)

    def __del__(self) -> None:
        if self.closeFile :
            self.file.close()
        return