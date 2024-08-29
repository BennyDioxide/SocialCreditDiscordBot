import os
import json
import logging


log = logging.getLogger(__name__)


def get_data(filename: str) -> dict:
    
    if not filename.endswith(".json"):
        filename += ".json"

    path = os.path.join(os.path.dirname(__file__), "json", filename)
    
    if not os.path.exists(path):
        
        log.error(f"File not found: {path}")
        return {}
    
    with open(path, "r", encoding="utf-8") as f:
    
        log.debug(f"Loaded {filename}")
        return json.load(f)
    
    
def get_skill_func(name: str) -> dict:
    
    try:
        import importlib
        importlib.invalidate_caches()
        
        character = importlib.import_module(f"bot.skills.{name}")
        
        log.debug(character)
        
        log.debug(f"Loaded skill function: {name}")
        return [character.skill, character.skill_2, character.ex_skill]
    
    except ImportError as e:
        log.error(f"Skill function not found: {name}", exc_info=e)
        return {}