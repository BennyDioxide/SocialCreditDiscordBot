import os
from dotenv import load_dotenv


load_dotenv()

BASEDIR = os.path.dirname(__file__)
FILENAME = os.path.split(os.path.dirname(__file__))[-1]

# Environment Variables
TOKEN = os.getenv("TOKEN")
SQL_URL = os.getenv("SQL_URL") or "sqlite:///db.sqlite3"

# Bot Settings
LOCALE = "zh-TW"

# Game Settings
POINT_RADIO = 1
POINT_LIMIT = 2147483647
ROB_SUCCESS_RATE = [0.5, 0.4, 0.1] # 成功, 失敗, 被抓
RAPE_SUCCESS_RATE = [0.5, 0.5] # 成功, 失敗
ROB_COOLDOWN = 2
RAPE_COOLDOWN = 15
WORK_COOLDOWN = 30