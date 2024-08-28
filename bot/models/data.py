from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from bot.config import SQL_URL, POINT_LIMIT
from bot.models import db
from bot.models.user import User
from bot.models.character import Character
from bot.models.item import Item


class DataStorage:
      
    @classmethod
    def init(cls) -> None:
        engine = create_engine(SQL_URL)
        session = sessionmaker(bind=engine)()
        db.metadata.create_all(engine)
        
        cls.score_data = ScoreData(session)
        cls.character_data = CharacterData(session)
        cls.item_data = ItemData(session)
        
        
class Data:
    
    def __init__(self, session: Session, database) -> None:
        self.session = session
        self.database = database
        
        
    def get(self, *args, **kwargs) -> dict:
        
        data = self.session.query(self.database).filter_by(*args, **kwargs).first()
        return data.__dict__ if data else {}


    def get_all(self) -> list[dict]:
        
        data = self.session.query(self.database).all()
        return [d.__dict__ for d in data]
    
    
    def reset(self) -> None:
        
        self.session.query(self.database).delete()
        self.session.commit()
        
        
    def is_exist(self, *args, **kwargs) -> bool:
            
        return bool(self.session.query(self.database).filter_by(*args, **kwargs).first())
    
    
    def add(self, *args, **kwargs) -> None:
        
        data = self.database(*args, **kwargs)
        self.session.add(data)
        self.session.commit()
        
        
    def remove(self, *args, **kwargs) -> None:
            
        self.session.query(self.database).filter_by(*args, **kwargs).delete()
        self.session.commit()
        
        
class ItemData(Data):
    
    def __init__(self, session: Session) -> None:
        super().__init__(session, Item)
        
        
class CharacterData(Data):
    
    def __init__(self, session: Session) -> None:
        super().__init__(session, Character)
        
        
class ScoreData(Data):
    
    def __init__(self, session: Session) -> None:
        super().__init__(session, User)
        
        
    def get_score(self, user_id: int) -> int:
        
        user = self.session.query(User).filter_by(user_id=user_id).first()
        return user.score if user else 0
    
    
    def set_score(self, user_id: int, score: int) -> None:
        
        user = self.session.query(User).filter_by(user_id=user_id).first()
        
        if user is None:
            user = User(user_id=user_id, score=0)
            self.session.add(user)
            
        if score >= POINT_LIMIT:
            user.score = POINT_LIMIT
            
        elif score < -POINT_LIMIT:
            user.score = -POINT_LIMIT
            
        else: user.score = score
            
        self.session.commit()
        
        
    def add_score(self, user_id: int, score: int) -> None:
        
        user = self.session.query(User).filter_by(user_id=user_id).first()
        
        if user is None:
            user = User(user_id=user_id, score=0)
            self.session.add(user)

        if user.score + score >= POINT_LIMIT: 
            user.score = POINT_LIMIT
            
        elif user.score + score < -POINT_LIMIT: 
            user.score = -POINT_LIMIT
            
        else: user.score += score
            
        self.session.commit()