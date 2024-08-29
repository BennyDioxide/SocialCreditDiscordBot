import logging
from sqlalchemy.orm import Session

from bot.models.data import Data
from bot.models.user import User
from bot.config import POINT_LIMIT


log = logging.getLogger(__name__)


class Score(Data):
    
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