from sqlalchemy.orm import Session

from bot.models.character import Character


class CharacterData:
    
    def __init__(self, session: Session) -> None:
        self.session = session
        
        
    def get_character(self, character_id: int) -> dict:
        
        character = self.session.query(Character).filter_by(id=character_id).first()
        return character.__dict__ if character else {}
    
    
    def get_all(self) -> dict:
        
        characters = self.session.query(Character).all()
        return {character.id: character.__dict__ for character in characters}
    
    
    def reset(self) -> None:
        
        self.session.query(Character).delete()
        self.session.commit()
        
        
    def is_character_exist(self, character_id: int) -> bool:
            
        return bool(self.session.query(Character).filter_by(id=character_id).first())
    
    
    def get_character_by_name(self, name: str) -> dict:
        
        character = self.session.query(Character).filter_by(name=name).first()
        return character.__dict__ if character else {}