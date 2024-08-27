from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from bot.models.user import User
from bot.config import SQL_URL


class ScoreData:
    
    @classmethod
    def init(cls) -> None:
        engine = create_engine(SQL_URL)
        db = declarative_base()
        db.metadata.create_all(engine)
        cls.session = sessionmaker(bind=engine)()
        
        
    @classmethod
    def get_score(cls, user_id: int) -> int:
        
        user = cls.session.query(User).filter_by(user_id=user_id).first()
        return user.score if user else 0
    
    
    @classmethod
    def set_score(cls, user_id: int, score: int) -> None:
        
        user = cls.session.query(User).filter_by(user_id=user_id).first()
        if user:
            user.score = score
        else:
            user = User(user_id=user_id, score=score)
            cls.session.add(user)
            
        cls.session.commit()
        
        
    @classmethod
    def add_score(cls, user_id: int, score: int) -> None:
        
        user = cls.session.query(User).filter_by(user_id=user_id).first()
        if user:
            user.score += score
        else:
            user = User(user_id=user_id, score=score)
            cls.session.add(user)
            
        cls.session.commit()
        
        
    @classmethod
    def get_all(cls) -> dict:
        
        users = cls.session.query(User).all()
        return {user.user_id: user.score for user in users}
    
    
    @classmethod
    def reset(cls) -> None:
        
        cls.session.query(User).delete()
        cls.session.commit()
        
        
    @classmethod
    def is_user_exist(cls, user_id: int) -> bool:
        
        return bool(cls.session.query(User).filter_by(user_id=user_id).first())