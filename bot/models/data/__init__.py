from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from bot.config import SQL_URL
from bot.models import db
from bot.models.data.character import CharacterData
from bot.models.data.score import ScoreData
from bot.models.data.item import ItemData


class DataStorage:
      
    @classmethod
    def init(cls) -> None:
        engine = create_engine(SQL_URL)
        session = sessionmaker(bind=engine)()
        db.metadata.create_all(engine)
        
        cls.score_data = ScoreData(session)
        cls.character_data = CharacterData(session)
        cls.item_data = ItemData(session)