from sqlalchemy import Column, Integer, String, PickleType
from bot.models import db


class Character(db):
    __tablename__ = "characters"
    
    # General
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    description = Column(String)
    image = Column(PickleType())
    price = Column(Integer)
    
    # Ability
    health = Column(Integer)
    attack = Column(Integer)
    defense = Column(Integer)
    critical = Column(Integer)
    speed = Column(Integer)
    
    # Skill
    skill = Column(PickleType())
    skill_description = Column(String)
    skill_func = Column(PickleType())
    
    skill_2 = Column(PickleType())
    skill_2_description = Column(String)
    skill_2_func = Column(PickleType())
    
    ex_skill = Column(PickleType())
    ex_skill_description = Column(String)
    ex_skill_func = Column(PickleType())
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    
    def __repr__(self):
        return f"<Character(name={self.name})>"