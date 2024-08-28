import os
from dotenv import load_dotenv


load_dotenv()

BASEDIR = os.path.dirname(__file__)

TOKEN = os.getenv("TOKEN")
SQL_URL = os.getenv("SQL_URL") or "sqlite:///db.sqlite3"

FILENAME = os.path.dirname(__file__).split(f"\\")[-1]
POINT_RADIO = 1
POINT_LIMIT = 2147483647