import os
import json

from ..config import BASEDIR


PATH = os.path.join(BASEDIR, "core", "data")
        
class ItemData:
    
    @classmethod
    def init(cls) -> None:
        
        if not os.path.exists(PATH):
            os.makedirs(PATH)
            
        if not os.path.exists(os.path.join(PATH, "item.json")):
            with open(os.path.join(PATH, "item.json"), "w") as f:
                json.dump([], f)
                
                
    @classmethod
    def get_items(cls) -> list:
            
        with open(os.path.join(PATH, "item.json"), "r", encoding="utf-8") as f:
            return json.load(f)
        
        
    @classmethod
    def add_item(cls, name: str, price: int, description: str) -> None:
        
        with open(os.path.join(PATH, "item.json"), "r", encoding="utf-8") as f:
            data: list = json.load(f)
            data.append({"name": name, "price": price, "description": description})
            
        with open(os.path.join(PATH, "item.json"), "w", encoding="utf-8") as f:
            json.dump(data, f)
            
            
    @classmethod
    def remove_item(cls, name: str) -> None:
        
        with open(os.path.join(PATH, "item.json"), "r", encoding="utf-8") as f:
            data: list = json.load(f)
            data = [item for item in data if item["name"] != name]
            
        with open(os.path.join(PATH, "item.json"), "w", encoding="utf-8") as f:
            json.dump(data, f)