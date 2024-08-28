from sqlalchemy.orm import Session

from bot.models.item import Item


class ItemData:
    
    def __init__(self, session: Session) -> None:
        self.session = session
        
        
    def get_item(self, name: str) -> dict:
        
        item = self.session.query(Item).filter_by(name=name).first()
        return item.__dict__ if item else {}
    

    def get_all(self) -> list[Item]:
            
            items = self.session.query(Item).all()
            return [item.__dict__ for item in items]
        
    
    def reset(self) -> None:
            
            self.session.query(Item).delete()
            self.session.commit()
            
        
    def is_item_exist(self, name: str) -> bool:
        
        return bool(self.session.query(Item).filter_by(name=name).first())
    
    
    def add_item(self, name: str, description: str, price: int, type: str="custom") -> None:
        
        item = Item(name, description, price, type)
        self.session.add(item)
        self.session.commit()
        
        
    def remove_item(self, name: str) -> None:
        
        self.session.query(Item).filter_by(name=name).delete()
        self.session.commit()