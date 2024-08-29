from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from bot.config import SQL_URL
from bot.models import db


class DataBase:
      
    def __init__(self) -> None:
        self.engine = create_engine(SQL_URL)
        self.session = sessionmaker(bind=self.engine)()
        db.metadata.create_all(self.engine)
        
        
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