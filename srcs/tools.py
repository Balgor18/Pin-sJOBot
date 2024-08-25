
import os

def getEnvVariable(name : str) :
    if os.environ.get(name) :
        return os.environ.get(name)
    raise Exception(f'No env variable found {name}') 
