from sqlalchemy.orm import Session

from bot.models.data import Data
from bot.models.item import Item as ItemModel


class Item(Data):
    
    def __init__(self, session: Session) -> None:
        super().__init__(session, ItemModel)