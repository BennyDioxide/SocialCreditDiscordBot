import logging
from typing import Callable, overload

from bot.core.character import Character


log = logging.getLogger(__name__)


class Skill:
    
    def __init__(self, name: str, description: str, func: Callable) -> None:
        self.name = name
        self.description = description
        self.func = func
        
        self.character: Character = None
        self.target: Character = None
        
    
    @overload
    def func(character: Character, target: Character, *args, **kwargs): ...
    
    
    def __call__(self, *args, **kwargs):
        log.debug(f"Skill: {self.name} called")
        return self.func(character=self.character, target=self.target, *args, **kwargs)