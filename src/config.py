from os import getcwd, path
import json

class BadJsonConfig(Exception) : pass

def validateDatabaseConfig(dbConfig: dict) -> bool:
    try:
        dbConfig["host"] and dbConfig["user"] and dbConfig["password"] and dbConfig["database"]
    except KeyError:
        return False
    return True

def readConfig(configPath: str, validateFunction) -> dict:
    with open(configPath, "r") as configJsonFile:
        configJson = json.load(configJsonFile)
        if not validateFunction(configJson):
            raise BadJsonConfig("Invalid JSON config file")
        return configJson

def validateProjectConfig(projConfig: dict) -> bool:
    try:
        projConfig["title"] and projConfig["author"] and projConfig["date"]
    except KeyError:
        return False
    return True

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

def createProjectConfig(pathToWrite: str = "") -> dict:
    title = input("Title: ")
    author = input("Author: ")
    date = input("Date: ")
    config = {
        "title": title,
        "author": author,
        "date": date
    }
    if not pathToWrite == "":
        fileToWrite = open(pathToWrite, "w", encoding="utf-8")
        jsonConfig = json.dumps(config)
        fileToWrite.write(jsonConfig)
    return config