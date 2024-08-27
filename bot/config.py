import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
BASEDIR = os.path.dirname(__file__)
FILENAME = os.path.dirname(__file__).split(f"\\")[-1]
POINT_RADIO = 1