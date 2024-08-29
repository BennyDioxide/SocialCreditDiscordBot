from sqlalchemy import Column, Integer, PickleType, String
from bot.models import db


class User(db):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, unique=True, nullable=False)
    score = Column(Integer)
    messages = Column(Integer)
    level = Column(Integer)
    items = Column(String)
    characters = Column(String)
    
    def __init__(self, user_id: str, score: int=0, messages: int=0, level: int=0):
        self.user_id = user_id
        self.score = score
        self.messages = messages
        self.level = level
        
        self.items = "[]"
        self.characters = "[]"
        
    
    def __repr__(self):
        return f"<User(user_id={self.user_id}, score={self.score})>"