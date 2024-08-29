from bot.models.data import DataBase
from bot.core.character import Character
from bot.core.item import Item
from bot.core.score import Score
from bot.core.user import User


class Core:
    
    @classmethod
    def init(cls) -> None:
        cls.db = DataBase()
        
        cls.character = Character(cls.db.session)
        cls.item = Item(cls.db.session)
        cls.score = Score(cls.db.session)
        cls.user = User(cls.db.session)
        
        cls.add_characters_to_items()
        
        
    @classmethod
    def add_characters_to_items(cls) -> None:
        items = [i["name"] for i in cls.item.get_all()]
        
        for chr in cls.character.get_all():
            if not chr["name"] in items:
                cls.item.add(name=chr["name"], description=chr["description"], price=chr["price"], type="character")