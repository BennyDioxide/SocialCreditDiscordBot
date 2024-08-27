from sqlalchemy import Column, Integer, PickleType
from bot.models import db


class Character(db):
    __tablename__ = "characters"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(PickleType())
    description = Column(PickleType())
    price = Column(Integer)
    health = Column(Integer)
    attack = Column(Integer)
    defense = Column(Integer)
    # Todo: 暴擊率、閃避率等等
    
    image = Column(PickleType())
    skill = Column(PickleType())
    
    def __init__():
        pass
        
    
    def __repr__(self):
        return f"<Character(name={self.name}, price={self.price})>"