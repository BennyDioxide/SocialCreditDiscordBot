import os
import json
from dotenv import load_dotenv


load_dotenv()

BASEDIR = os.path.dirname(__file__)
SETTINGS = json.load(open(os.path.join(BASEDIR, "settings.json"), "r"))

# Environment Variables
TOKEN = os.getenv("TOKEN")
SQL_URL = os.getenv("SQL_URL") or "sqlite:///db.sqlite3"

# Bot Settings
LOCALE = SETTINGS["LOCALE"]
LOG_FILENAME = SETTINGS["LOG_FILENAME"]

# Game Settings
GAME_SETTINGS = SETTINGS["GAME_SETTINGS"]
POINT_RADIO = GAME_SETTINGS["POINT_RADIO"]
POINT_LIMIT = GAME_SETTINGS["POINT_LIMIT"]
ROB_SUCCESS_RATE = GAME_SETTINGS["ROB_SUCCESS_RATE"]
RAPE_SUCCESS_RATE = GAME_SETTINGS["RAPE_SUCCESS_RATE"]
WORK_SUCCESS_RATE = GAME_SETTINGS["WORK_SUCCESS_RATE"]
ROB_COOLDOWN = GAME_SETTINGS["ROB_COOLDOWN"]
RAPE_COOLDOWN = GAME_SETTINGS["RAPE_COOLDOWN"]
WORK_COOLDOWN = GAME_SETTINGS["WORK_COOLDOWN"]
