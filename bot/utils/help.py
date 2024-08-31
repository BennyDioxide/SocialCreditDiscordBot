import logging

import discord
from discord.ext import commands

from bot.utils.embed import EmbedMaker
from bot.data import get_data
from bot.utils.button import PageButton


log = logging.getLogger(__name__)


def need_help(command_name: str, error: discord.ApplicationCommandError) -> discord.Embed:
    return EmbedMaker(status=False, description=f'**在執行{command_name}時發生錯誤，錯誤報告如下:**``` * {error}```')

def comming_soon(command_name: str) -> discord.Embed:
    return discord.Embed(title=f"⚙️ 指令 {command_name} 尚未開放", description="敬請關注更新公告!!!", color=discord.Color.lighter_gray())

class HelpCommandSettings:
    
    @classmethod
    def set_command_list(cls, command_list: list[discord.ApplicationCommand]) -> None:
        cls.command_list = command_list
        
    
    @classmethod
    def set_prefix(cls, prefix: str) -> None:
        cls.prefix = prefix
        
        
    @classmethod
    def help(cls) -> PageButton:
        
        prefix_commands_description = get_data("prefix_commands_description")
        embed = discord.Embed(title=f'指令列表⚙️', color=discord.Color.purple())
        
        if cls.command_list is None: 
            embed.add_field(name=f"_**無法取得指令資訊**_", inline=False)
            
        description_list = []
            
        for cmd in cls.command_list:
            
            if isinstance(cmd, discord.SlashCommand):
                description = cmd.description_localizations or cmd.description
                description_list.append({
                    "name": "", 
                    "value": f"{cmd.mention}\n _{description}_", 
                    "inline": False
                })
                
            elif cls.prefix is not None: 
                
                if cmd.name in prefix_commands_description:
                    description = prefix_commands_description[cmd.name]
                    
                else:
                    log.warning(f"Command {cmd.name} has no description")
                    description = "No description provided"

                description_list.append({
                    "name": "", 
                    "value": f"**{cls.prefix}{cmd.name}**\n _{description}_", 
                    "inline": False
                })
            
        return PageButton(embed=embed, data=description_list, limit=5)