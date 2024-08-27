import discord
from discord.ext import commands
from .embed import EmbedMaker
from .data import prefix_commands_description


gl_command_list = None
gl_prefix = None

def need_help(command_name: str, error: discord.ApplicationCommandError) -> discord.Embed:
    return EmbedMaker(status=False, description=f'**在執行{command_name}時發生錯誤，錯誤報告如下:**``` * {error}```')

class HelpCommandSettings:
    
    def set_command_list(command_list: list[discord.ApplicationCommand]) -> None:
        global gl_command_list
        gl_command_list = command_list
        
    def set_prefix(prefix: str) -> None:
        global gl_prefix
        gl_prefix = prefix
        
    def help() -> discord.Embed:
        
        global gl_prefix
        global gl_command_list
        command_list = gl_command_list
        prefix = gl_prefix
        
        embed = discord.Embed(title=f'指令列表⚙️', color=discord.Color.purple())
        
        if command_list is None: 
            embed.add_field(name=f"_**無法取得指令資訊**_", inline=False)
            
        for cmd in command_list:
            
            if isinstance(cmd, discord.SlashCommand):
                description = cmd.description_localizations if cmd.description_localizations else cmd.description
                embed.add_field(name="", value=f"{cmd.mention}\n _{description}_", inline=False)
                
            elif prefix is not None: 
                
                if cmd.name in prefix_commands_description:
                    description = prefix_commands_description[cmd.name]
                    
                else:
                    description = "No description provided"
                    
                embed.add_field(name="", value=f"**{prefix}{cmd.name}**\n _{description}_", inline=False)
            
        return embed