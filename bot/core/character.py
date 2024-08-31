import logging
from sqlalchemy.orm import Session

from bot.models.data import Data
from bot.models.character import Character as CharacterModel
from bot.data import get_assets, get_data, get_skill_func


log = logging.getLogger(__name__)


class Character(Data):
    
    def __init__(self, session: Session) -> None:
        super().__init__(session, CharacterModel)
        
        characters = get_data("characters")
        
        # 初始化角色
        for chr in characters:
            
            if self.is_exist(name=chr["name"]):
                continue
            
            # 設定角色技能
            chr_skill = get_skill_func(chr["name"])
            chr["skill_func"] = chr_skill[0]
            chr["skill_2_func"] = chr_skill[1]
            chr["ex_skill_func"] = chr_skill[2]
            
            # 設定角色圖片
            chr["image"] = get_assets(chr["name"])
            
            self.add(**chr)
            
            log.info(f"Added character: {chr['name']}")