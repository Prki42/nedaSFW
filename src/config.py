from os import getcwd, path
import json

class BadJsonConfig(Exception) : pass

def validateDatabaseConfig(dbConfig: dict) -> bool:
    try:
        dbConfig["host"] and dbConfig["user"] and dbConfig["password"] and dbConfig["database"]
    except KeyError as err:
        return False
    return True

def readConfig(configPath: str) -> dict:
    with open(configPath, "r") as configJsonFile:
        configJson = json.load(configJsonFile)
        if not validateDatabaseConfig(configJson):
            raise BadJsonConfig("Invalid database config file")
        return configJson;

def createDatabaseConfig(pathToWrite: str = "") -> dict:
    host = input("Host: ")
    user = input("User: ")
    password = input("Password: ")
    database = input("Database: ")
    config = {
        "host": host,
        "user": user,
        "password": password,
        "database": database
    }
    if not pathToWrite == "":
        fileToWrite = open(pathToWrite, "w", encoding="utf-8")
        jsonConfig = json.dumps(config)
        fileToWrite.write(jsonConfig)
    return config