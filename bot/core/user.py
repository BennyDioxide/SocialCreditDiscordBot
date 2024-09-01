import logging
import json

from bot.models.data import Data
from bot.models.user import User as UserModel


log = logging.getLogger(__name__)


class User(Data):
        
    def __init__(self, session) -> None:
        super().__init__(session, UserModel)
        
        
    def add_messages(self, user_id: int) -> None:
        
        user = self.session.query(UserModel).filter_by(user_id=user_id).first()
        user.messages += 1
        self.session.commit()
        
        
    def get_messages(self, user_id: int) -> int:
            
        user = self.session.query(UserModel).filter_by(user_id=user_id).first()
        return user.messages if user else 0
    
    
    def add_item(self, user_id: int, item: dict, amount: int=1) -> None:
        
        user = self.session.query(UserModel).filter_by(user_id=user_id).first()
        items: list[dict] = json.loads(user.items)
        
        for i, it in enumerate(items):
            if it["name"] == item["name"]:
                items[i]["count"] += amount
                user.items = json.dumps(items)
                self.session.commit()
                return None
            
        items.append({
            "name": item["name"],
            "description": item["description"],
            "count": amount
        })
        
        user.items = json.dumps(items)
        
        log.debug(user.items)
        
        self.session.commit()
        
        
    def get_items(self, user_id: int) -> list[dict]:
        
        user = self.session.query(UserModel).filter_by(user_id=user_id).first()
        return json.loads(user.items) if user else []
    
    
    def add_character(self, user_id: int, character: dict) -> None:
        
        user = self.session.query(UserModel).filter_by(user_id=user_id).first()
        
        if not user.characters:
            user.characters = []
            
        for chr in user.characters:
            if chr["name"] == character["name"]:
                return None
            
        characters = json.loads(user.characters)
        characters.append({
            "name": character["name"],
            "level": 1
        })
        user.characters = json.dumps(characters)
        self.session.commit()
        
        
    def character_level_up(self, user_id: int, character_name: str) -> None:
        
        user = self.session.query(UserModel).filter_by(user_id=user_id).first()
        characters = json.loads(user.characters)
        
        for chr in characters:
            if chr["name"] == character_name:
                chr["level"] += 1
                user.characters = json.dumps(characters)
                self.session.commit()
                return None