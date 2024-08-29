import logging
from sqlalchemy.orm import Session

from bot.models.data import Data
from bot.models.character import Character as CharacterModel
from bot.data import get_data, get_skill_func


log = logging.getLogger(__name__)


class Character(Data):
    
    def __init__(self, session: Session) -> None:
        super().__init__(session, CharacterModel)
        
        characters = get_data("characters")
        
        log.debug(characters)
        
        for chr in characters:
            if not self.is_exist(name=chr["name"]):
                
                chr_skill = get_skill_func(chr["name"])
                
                chr["skill_func"] = chr_skill[0]
                chr["skill_2_func"] = chr_skill[1]
                chr["ex_skill_func"] = chr_skill[2]
                
                self.add(**chr)
                
                log.info(f"Added character: {chr['name']}")