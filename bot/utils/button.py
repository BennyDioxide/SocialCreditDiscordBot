import logging

import discord
from discord.ext import commands


log = logging.getLogger(__name__)

class PageButton(discord.ui.View):
    
    def __init__(self, ctx: discord.ApplicationContext, data: list, limit: int):
        super().__init__()
        self.ctx = ctx
        self.index = 0
        self.data = data
        self.limit = limit
            
        
    def on_timeout(self) -> discord.Coroutine[discord.Any, discord.Any, None]:
        self.disable_all_items()
        
        
    @discord.ui.button(label="上一頁", style=discord.ButtonStyle.primary)
    async def previous(self, button: discord.ui.Button, interaction: discord.Interaction):
        
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("我剛剛查排行榜的時候...你偷看了罷...", ephemeral=True)
            return
        
        embed = discord.Embed(title="排行榜", color=discord.Color.green())
        
        if self.index - self.limit < 0:
            await interaction.response.send_message("已經是第一頁了", ephemeral=True)
            return
        
        self.index -= self.limit
        for field in self.data[self.index:self.index + self.limit]:
            embed.add_field(**field)
            
        
        await interaction.message.edit(embed=embed)
        await interaction.response.defer()
        

    @discord.ui.button(label="下一頁", style=discord.ButtonStyle.primary)
    async def next(self, button: discord.ui.Button, interaction: discord.Interaction):
        
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("我剛剛查排行榜的時候...你偷看了罷...", ephemeral=True)
            return
        
        embed = discord.Embed(title="排行榜", color=discord.Color.green())
        limit = self.limit
        
        if self.index + self.limit >= len(self.data) + self.limit:
            await interaction.response.send_message("已經是最後一頁了", ephemeral=True)
            return
        
        if self.index + self.limit > len(self.data):
            limit = len(self.data) - self.index
        
        self.index += limit
        for field in self.data[self.index:self.index + limit]:
            embed.add_field(**field)
            
        
        await interaction.message.edit(embed=embed)
        await interaction.response.defer()