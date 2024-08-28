import discord
from discord.ext import commands
import logging

from bot.models.data import DataStorage

log = logging.getLogger(__name__)


class Battle(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="character", description="查看角色資訊")
    async def character(self, ctx: discord.ApplicationContext, name: discord.Option(
        str,
        name="角色名稱",
        choices=[discord.OptionChoice(name=char["name"], value=char["name"]) for char in DataStorage.character_data.get_all()]
        )): # type: ignore
        
        character = DataStorage.character_data.get_character_by_name(name)
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
        embed.add_field(name="技能", value=character["skill_description"], inline=False)
        embed.add_field(name="被動技能", value=character["skill_2_description"], inline=False)
        embed.add_field(name="EX技能", value=character["ex_skill_description"], inline=False)
        
        await ctx.respond(embed=embed)
    
            
def setup(bot: commands.Bot):
    bot.add_cog(Battle(bot))