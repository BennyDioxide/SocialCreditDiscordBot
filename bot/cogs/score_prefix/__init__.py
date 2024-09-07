import random
import logging

import discord
from discord.ext import commands

from bot.core import Core
from bot.utils.embed import EmbedMaker
from bot.utils.button import PageButton
from bot.utils.emoji import EmojiManager


log = logging.getLogger(__name__)


class ScorePrefix(commands.Cog):
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
        
    @commands.command(name="addscore", description="增加點數")
    async def add_score_prefix(self, ctx: commands.Context, member: discord.Member, score: int):
        
        if not ctx.author.guild_permissions.administrator:
            await ctx.reply(embed=EmbedMaker(False, "你沒有權限", color="red"), mention_author=False)
            return
        
        Core.score.add_score(member.id, score)
        
        await ctx.reply(embed=EmbedMaker(True, description=f"{ctx.author.mention}使用了大人的卡片，{member.mention}的點數獲得了{score}分的{'提升' if score > 0 else '降低'}"), mention_author=False)
        
        log.info(f"{ctx.author.name} add {score} score to {member.name}")
        log.debug(f"{ctx.author.name} used add_score command")
        
        
    @commands.command(name="setscore")
    async def set_score_prefix(self, ctx: commands.Context, member: discord.Member, score: int):
        
        if not ctx.author.guild_permissions.administrator:
            await ctx.reply(embed=EmbedMaker(False, "你沒有權限", color="red"), mention_author=False)
            return
        
        Core.score.set_score(member.id, score)
        
        await ctx.reply(embed=EmbedMaker(True, description=f"{ctx.author.mention}使用了大人的卡片，{member.mention}的點數被設定為{score}分"), mention_author=False)
        
        log.info(f"{ctx.author.name} set {member.name}'s score to {score}")
        log.debug(f"{ctx.author.name} used set_score command")
        
        
    @commands.command(name="showscore")
    async def show_score_prefix(self, ctx: commands.Context, member: discord.Member | None=None):
        
        if member is None:
            member = ctx.author
        
        score = Core.score.get_score(member.id)
        massages = Core.user.get_messages(member.id)
        
        embed = discord.Embed(title=f"個人資料 - {member.name}", color=discord.Color.green())
        embed.add_field(name="", value=f"訊息量: {massages}")
        embed.add_field(name="", value=f"點數: {score}")
        embed.set_thumbnail(url=member.avatar.url)
        embed.set_footer(text=f"ID: {member.id}")
        embed.timestamp = member.created_at
        
        await ctx.reply(embed=embed, mention_author=False)
        
        log.debug(f"{ctx.author.name} used score command. Show {member.name}'s score")
        
        
    @commands.command(name="rank")
    async def rank_prefix(self, ctx: commands.Context):
        
        limit = 5
        data = Core.score.get_all()
        data = sorted(data, key=lambda x: x["score"], reverse=True)
        list_data = []
        embed = discord.Embed(title="排行榜", color=discord.Color.green())
        
        for i, d in enumerate(data):
            user_id = d["user_id"]
            score = d["score"]
            user = self.bot.get_user(int(user_id))
            if user is None: continue
            list_data.append({
                "name": f"{i+1}. {user.name}",
                "value": f"點數: *{score}*", 
                "inline": False
            })
            
        view = PageButton(ctx=ctx, embed=embed, data=list_data, limit=limit)
            
        await ctx.reply(embed=view.get_embed(), view=view, mention_author=False)
        
        log.debug(f"{ctx.author.name} used ranklist command")
        
        
    @commands.command(name="shop")
    async def shop_prefix(self, ctx: commands.Context):
        
        embed = discord.Embed(title="社會信用商店", color=discord.Color.green())
        
        items = Core.item.get_all()
        
        if len(items) == 0:
            embed.add_field(name="", value="***商店空空如也~***")

        for i, item in enumerate(Core.item.get_all()):
            embed.add_field(name=f'{i+1}. {item["name"]}', value=f'價格: *{item["price"]}*\n說明: *{item["description"]}*\n類型: {item["type"]}', inline=False)
        
        await ctx.reply(embed=embed, mention_author=False)
        
        log.debug(f"{ctx.author.name} used shop command")
        
        
    @commands.command(name="warning")
    async def warning_prefix(self, ctx: commands.Context):

        data = Core.score.get_all()
        
        if len(data) == 0:
            member = ctx.author
        else:
            member = random.choice([self.bot.get_user(int(user)) for user, score in data.items() if score < 100])
        
        embed = discord.Embed(title="警告", color=discord.Color.red())
        embed.add_field(name="", value=f"{member.mention} 您的社會信用點數過低!!! \n目前點數為: {data[str(member.id)]} \n建議多發言以提升您的社會信用點數")
        
        await ctx.reply(embed=embed, mention_author=False)
        
        log.debug(f'{ctx.author.name} warned {member.name}')
        
        
    @commands.command(name="shiroko")
    async def shiroko_prefix(self, ctx: commands.Context):
        
        success = random.choice([True, False])
        if success: value = random.randint(1, 114)
        else: value = random.randint(-114, -1)
        
        Core.score.add_score(ctx.author.id, value)
        
        embed = discord.Embed(title="搶銀行囉", color=discord.Color.green() if success else discord.Color.red())
        embed.set_image(url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTsPASopxuiwUm2auuA8WKKjFyB7Yy13oVMjQ&s")
        embed.add_field(name="成果", value=f'{"成功搶到了" if success else "被抓到了，因此被罰了"}{abs(value)}點社會信用點數')
        
        await ctx.reply(embed=embed, mention_author=False)
        
        log.debug(f'{ctx.author.name} used shiroko command')
        
        
    @commands.command(name="transfer")
    async def transfer(self, ctx: commands.Context, member: discord.Member, score: int):
        
        if Core.score.get_score(ctx.author.id) < score:
            await ctx.reply(embed=EmbedMaker(False, "你的點數不足", color="red"))
            return
        
        Core.score.add_score(ctx.author.id, -score)
        Core.score.add_score(member.id, int(round(score * 0.95)))
        
        embed = discord.Embed(title=EmojiManager("轉帳成功:animation_yes:"), color=discord.Color.green())
        embed.add_field(name="持有者", value=ctx.author.mention, inline=False)
        embed.add_field(name="對象", value=member.mention, inline=False)
        embed.add_field(name="金額", value=f"{score}$", inline=False)
        embed.add_field(name="手續費", value=f"{round(score * 0.05)}$", inline=False) 
        
        await ctx.reply(embed=embed, mention_author=False)
        
        log.debug(f'{ctx.author.name} transfered {score} score to {member.name}')
        
        
    @commands.command(name="item")
    async def item_list(self, ctx: commands.Context, member: discord.Member | None=None):
        
        if member is None:
            member = ctx.author
        
        items = Core.user.get_items(member.id)
        embed = discord.Embed(title=f"{member.name}的物品欄", color=discord.Color.green())
        
        if len(items) == 0:
            embed.add_field(name="", value="***物品欄空空如也~***")
        
        for i, item in enumerate(items):
            embed.add_field(name=f'{i+1}. {item["name"]}', value=f'說明: *{item["description"]}*\n數量: {item["count"]}', inline=False)
        
        await ctx.reply(embed=embed, mention_author=False)
        
        log.debug(f'{ctx.author.name} get item list of {member.name}')

   
            
def setup(bot: commands.Bot):
    bot.add_cog(ScorePrefix(bot))