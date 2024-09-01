import discord
from discord.ext import commands
import logging

from bot.core import Core
from bot.utils.help import comming_soon


log = logging.getLogger(__name__)


class Battle(commands.Cog):
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        

    @commands.slash_command(name="角色資訊", description="查看角色資訊")
    async def character(self, ctx: discord.ApplicationContext, name: discord.Option(
        str,
        name="角色名稱",
        choices=[discord.OptionChoice(name=chr["name"], value=chr["name"]) for chr in Core.character.get_all()]
        )): # type: ignore
        
        character = Core.character.get(name=name)
        embed = discord.Embed(
            title=character["name"],
            description=character["description"],
            color=discord.Color.blurple()
        )
        
        embed.set_thumbnail(url=character["image"])
        embed.add_field(name="價格", value=character["price"], inline=False)
        embed.add_field(name="生命", value=character["health"], inline=True)
        embed.add_field(name="攻擊", value=character["attack"], inline=True)
        embed.add_field(name="防禦", value=character["defense"], inline=True)
        embed.add_field(name="暴擊", value=character["critical"], inline=True)
        embed.add_field(name="速度", value=character["speed"], inline=True)
        embed.add_field(name=f"技能-{character['skill']}", value=character["skill_description"], inline=False)
        embed.add_field(name=f"被動技能-{character['skill_2']}", value=character["skill_2_description"], inline=False)
        embed.add_field(name=f"EX技能-{character['ex_skill']}", value=character["ex_skill_description"], inline=False)
        
        # TODO: 持有狀態 + 等級
        
        await ctx.respond(embed=embed)
        
        
    @commands.slash_command(name="發起戰鬥", description="Yo Battle!!!")
    async def battle(self, ctx: discord.ApplicationContext):
        await ctx.respond(embed=comming_soon(self.battle.name))
    
            
def setup(bot: commands.Bot):
    bot.add_cog(Battle(bot))