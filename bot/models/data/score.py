from sqlalchemy.orm import Session

from bot.models.user import User


class ScoreData:
    
    def __init__(self, session: Session) -> None:
        self.session = session
        
        
    def get_score(self, user_id: int) -> int:
        
        user = self.session.query(User).filter_by(user_id=user_id).first()
        return user.score if user else 0
    
    
    def set_score(self, user_id: int, score: int) -> None:
        
        user = self.session.query(User).filter_by(user_id=user_id).first()
        if user:
            user.score = score
        else:
            user = User(user_id=user_id, score=score)
            self.session.add(user)
            
        self.session.commit()
        
        
    def add_score(self, user_id: int, score: int) -> None:
        
        user = self.session.query(User).filter_by(user_id=user_id).first()
        if user:
            user.score += score
        else:
            user = User(user_id=user_id, score=score)
            self.session.add(user)
            
        self.session.commit()
        
        
    def get_all(self) -> dict:
        
        users = self.session.query(User).all()
        return {user.user_id: user.score for user in users}
    
    
    def reset(self) -> None:
        
        self.session.query(User).delete()
        self.session.commit()
        
        
    def is_user_exist(self, user_id: int) -> bool:
        
        return bool(self.session.query(User).filter_by(user_id=user_id).first())