import random
import logging
import uuid
from typing import Callable, overload
from datetime import datetime

from bot.core.character import Character


log = logging.getLogger(__name__)


class BattleCharacter:
    
    @overload
    def __init__(self) -> None:
        
        # 角色資訊
        self.name = ...
        self.description = ...
        self.image = ...
        self.price = ...
        
        # 基礎屬性
        self.attack = ...
        self.defense = ...
        self.health = ...
        self.critical = ...
        self.speed = ...
        self.skill = ...
        self.skill_description = ...
        self.skill_func = ...
        self.skill_2 = ...
        self.skill_2_description = ...
        self.skill_2_func = ...
        self.ex_skill = ...
        self.ex_skill_description = ...
        self.ex_skill_func = ...
        
        # 隱藏屬性
        self.ex_attack = 0
        self.ex_defense = 0
        self.ex_health = 0
        self.ex_critical = 0
        self.ex_speed = 0
        
        # 狀態
        self_buff = []
        self_debuff = []
        
        
    def __init__(self, data: dict) -> None:
        self.__dict__.update(data)
        
        
    def __str__(self) -> str:
        return self.name
        

class Battle:
    
    def __init__(self, player1: list[BattleCharacter], player2: list[BattleCharacter]) -> None:
        
        self.battle_id = uuid.uuid4()
        
        self.player1 = player1
        self.player2 = player2
        self.battle_logs = []
        self.turn = 0
        
        
    def battle_log(self, movement: Callable, log_text: str) -> None:
        log_data = {
            "func": movement.__name__,
            "text": log_text,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.battle_logs.append(log_data)
        log.debug(log_text + "BATTLE ID: " + self.battle_id)
        
        
    def attack(self, attacker: BattleCharacter, target: BattleCharacter, damage_radio: int) -> None:
        
        # 基礎傷害
        damage = attacker.attack * damage_radio
        
        # 暴擊
        if critical := random.random() <= attacker.critical / 100: damage *= 2
        
        # 閃避
        if dodge := random.random() <= target.speed / 100: damage = 0
        
        # 防禦
        damage = max(0, damage - target.defense)
        
        # 扣血
        target.health -= damage
        
        self.battle_log(self.attack, f"{attacker.name} 對 {target.name} 造成 {damage} 點傷害 {'(暴擊)' if critical else ''} {'(閃避)' if dodge else ''}")