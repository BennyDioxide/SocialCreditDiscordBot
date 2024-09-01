import logging
from datetime import datetime
from sqlalchemy.orm import Session

import discord
from discord.ext import commands

from bot.models.data import Data
from bot.models.item import Item as ItemModel
from bot.utils.embed import EmbedMaker
from bot.data import get_data


log = logging.getLogger(__name__)


class Item(Data):
    
    def __init__(self, session: Session) -> None:
        super().__init__(session, ItemModel)
        
        items = get_data("items")
        
        # 初始化物品
        for item in items:
            
            if self.is_exist(name=item["name"]):
                continue
            
            item["type"] = "item"
            
            self.add(**item)
            
            log.info(f"Added item: {item['name']}")
            
            
    @staticmethod
    async def use_ringo(Core, ctx: commands.Context | discord.ApplicationContext, amount: int):
        
        if (cd := Core.remaining_time.get(ctx.author.id, 0) - datetime.now().timestamp()) < 0:
            if isinstance(ctx, commands.Context): await ctx.reply(embed=EmbedMaker(False, "你目前不在古拉格，也沒有被雷普(疑惑)。"), mention_author=False)
            else: await ctx.respond(embed=EmbedMaker(False, "你目前不在古拉格，也沒有被雷普(疑惑)。"))
            return None
        
        ringo_count = 0
        
        for item in Core.user.get_items(ctx.author.id):
            if item["name"] == "林檎":
                ringo_count = item["count"]
                
        if ringo_count <= 0:
            embed = discord.Embed(title="林檎使用結果", color=discord.Color.red())
            embed.add_field(name="林檎使用失敗(絕望)!", value=f"homo特有的零比一大(惱)", inline=False)
        
        elif ringo_count < amount:
            embed = discord.Embed(title="林檎使用結果", color=discord.Color.red())
            embed.add_field(name="林檎使用失敗(絕望)!", value=f"你的林檎不夠用力(大悲)!", inline=False)
        
        else:
            Core.user.add_item(ctx.author.id, Core.item.get(name="林檎"), amount=-amount)
            Core.remaining_time[ctx.author.id] -= amount * 60
            
            embed = discord.Embed(title="林檎使用結果", color=discord.Color.green())
            embed.add_field(name="成功使用林檎！", value=f"你成功使用了一個一個一個林檎，減少了 {amount * 2} 分鐘的古拉格(或雷普)懲罰。", inline=False)
            embed.add_field(name="剩餘林檎數量", value=f"你現在有 {ringo_count - amount} 個林檎。", inline=False)
        
        if isinstance(ctx, commands.Context): await ctx.reply(embed=embed, mention_author=False)
        else: await ctx.respond(embed=embed)