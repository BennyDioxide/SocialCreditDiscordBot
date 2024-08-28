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
        
        if self.index + self.limit >= len(self.data):
            for child in self.children:
                if child.custom_id == "next": child.disabled = True
                
        if self.index - self.limit < 0:
            for child in self.children:
                if child.custom_id == "previous": child.disabled = True
            
        
    def on_timeout(self) -> discord.Coroutine[discord.Any, discord.Any, None]:
        self.disable_all_items()
        
        
    @discord.ui.button(label="上一頁", style=discord.ButtonStyle.primary, custom_id="previous")
    async def previous(self, button: discord.ui.Button, interaction: discord.Interaction):
        
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("我剛剛查排行榜的時候...你偷看了罷...", ephemeral=True)
            return
        
        embed = discord.Embed(title="排行榜", color=discord.Color.green())
        
        self.index -= self.limit
        for field in self.data[self.index:self.index + self.limit]:
            embed.add_field(**field)
            
        for child in self.children:
            if child.custom_id == "next": child.disabled = False
            
        button.disabled = self.index - self.limit < 0
            
        await interaction.message.edit(embed=embed, view=self)
        await interaction.response.defer()
        
        log.debug(f"index: {self.index} limit: {self.limit} data: {len(self.data)}")
        

    @discord.ui.button(label="下一頁", style=discord.ButtonStyle.primary, custom_id="next")
    async def next(self, button: discord.ui.Button, interaction: discord.Interaction):
        
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("我剛剛查排行榜的時候...你偷看了罷...", ephemeral=True)
            return
        
        embed = discord.Embed(title="排行榜", color=discord.Color.green())
        
        self.index += self.limit
        for field in self.data[self.index:self.index + self.limit]:
            embed.add_field(**field)
        
        for child in self.children:
            if child.custom_id == "previous": child.disabled = False
                
        button.disabled = self.index + self.limit >= len(self.data)
            
        await interaction.message.edit(embed=embed, view=self)
        await interaction.response.defer()
        
        log.debug(f"index: {self.index} limit: {self.limit} data: {len(self.data)}")
        