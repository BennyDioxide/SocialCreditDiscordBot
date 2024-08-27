from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from bot.config import SQL_URL


engine = create_engine(SQL_URL, echo=True)
db = declarative_base()
session = sessionmaker(bind=engine)()