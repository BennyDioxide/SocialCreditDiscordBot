import logging

import discord
from discord.ext import commands

from bot.utils.help import comming_soon


log = logging.getLogger(__name__)


class ThunderDragonScore(commands.Cog):
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
        
    @commands.command(name="rob")
    async def rob(self, ctx: commands.Context):
        await ctx.reply(embed=comming_soon(self.rob.name))
        
    
    @commands.command(name="rape")
    async def rape(self, ctx: commands.Context):
        await ctx.reply(embed=comming_soon(self.rape.name))
    
    
    @commands.command(name="work")
    async def work(self, ctx: commands.Context):
        await ctx.reply(embed=comming_soon(self.work.name))
    
    
    @commands.command(name="useringo")
    async def useringo(self, ctx: commands.Context):
        await ctx.reply(embed=comming_soon(self.useringo.name))

            
def setup(bot: commands.Bot):
    bot.add_cog(ThunderDragonScore(bot))