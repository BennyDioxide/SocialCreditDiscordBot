import logging
import random
from datetime import datetime

import discord
from discord.ext import bridge, commands

from bot.core import Core
from bot.config import ROB_SUCCESS_RATE, RAPE_SUCCESS_RATE, ROB_COOLDOWN, RAPE_COOLDOWN, WORK_COOLDOWN


log = logging.getLogger(__name__)


class ThunderDragonScore(commands.Cog):
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        Core.command_cooldown.update({func.name: {} for func in self.get_commands()})
        
        
    @bridge.bridge_command(
        name="rob",
        name_localizations={"zh-TW": "搶劫"},
        description="Rob someone's score.",
        description_localizations={"zh-TW": "搶劫他人的社會信用點數"},
    )
    async def rob(self, ctx: discord.ApplicationContext, member: bridge.BridgeOption(discord.Member, name="成員")): # type: ignore
        
        if (cd := Core.command_cooldown.get(self.rob.name, {}).get(ctx.author.id, 0) - datetime.now().timestamp()) > 0:
            embed = discord.Embed(title="收拾中", color=discord.Color.red())
            embed.add_field(name="嗯、嘛、啊...", value=f"你剛剛已經搶劫過別人了，請等待 {round(cd)} 秒後再試。", inline=False)
            await ctx.respond(embed=embed)
            return None
        
        if (cd := Core.remaining_time.get(ctx.author.id, 0) - datetime.now().timestamp()) > 0:
            await ctx.respond(f"十分不幸的，同志，你被遣送古拉格（或是被雷普了）！請等待 {round(cd)} 秒後再試。")
            return None
        
        robber: discord.Member = ctx.author
        target: discord.Member = member
        robber_score = Core.score.get_score(robber.id)
        target_score = Core.score.get_score(target.id)
        
        if robber.id == target.id:
            embed = discord.Embed(title="搶劫失敗！", color=discord.Color.red())
            embed.add_field(name="出現錯誤", value=f"{robber.mention}，請不要搶劫你自己！", inline=False)

        elif target_score <= 0:
            embed = discord.Embed(title="搶劫失敗！", color=discord.Color.red())
            embed.add_field(name="", value="百姓成窮鬼啦，沒油水可搶啦!", inline=False)
        
        elif robber_score > target_score:
            embed = discord.Embed(title="搶劫失敗！", color=discord.Color.red())
            embed.add_field(name="", value="請不要對無產者出手，同志!", inline=False)
            
        elif random.random() <= ROB_SUCCESS_RATE[0]:
            max_score = robber_score * pow(ROB_SUCCESS_RATE[0], 2)
            min_score = max(max_score - robber_score // 2, 0)
            score = random.randint(int(min_score), int(max_score))
            Core.score.add_score(robber.id, score)
            Core.score.add_score(target.id, -score)
            
            embed = discord.Embed(title="搶劫結果", color=discord.Color.green())
            embed.add_field(name="搶劫成功！", value=f"{robber.mention} 搶劫了 {target.mention} 並獲得了 {score} 點社會信用。", inline=False)
            embed.add_field(name=f"{robber.display_name} 的新社會信用點數", value=f"{Core.score.get_score(robber.id)} 點", inline=True)
            embed.add_field(name=f"{target.display_name} 的新社會信用點數", value=f"{Core.score.get_score(target.id)} 點", inline=True)
            
        elif random.random() <= RAPE_SUCCESS_RATE[1] / (ROB_SUCCESS_RATE[1] + ROB_SUCCESS_RATE[2]):
            score = random.randint(robber_score // 20, robber_score // 3)
            Core.score.add_score(robber.id, -score)
            
            embed = discord.Embed(title="搶劫失敗！", color=discord.Color.red())
            embed.add_field(name="結果", value=f"你失敗了！你被公安罰款 {score} 點。", inline=False)
            
        else:
            Core.score.set_score(robber.id, 0)
            Core.remaining_time[robber.id] = datetime.now().timestamp() + 60
            
            embed = discord.Embed(title="搶劫失敗！", color=discord.Color.red())
            embed.add_field(name="結果", value="你被秘密警察逮了個正著，被送往古拉格! 除了社會信用歸零外，1 分鐘內無法使用 `?rob` 和 `?gamble`。", inline=False)
                
        await ctx.respond(embed=embed)
        
        Core.command_cooldown[self.rob.name][ctx.author.id] = datetime.now().timestamp() + ROB_COOLDOWN
        
        log.debug(f"{ctx.author.name} used rob command. target: {member.name}")
        
    
    @bridge.bridge_command(
        name="rape",
        name_localizations={"zh-TW": "雷普"},
        description="Success will reward you, but failure will punish you.",
        description_localizations={"zh-TW": "雷普，成功了有獎勵，失敗了有懲罰"},
    )
    async def rape(self, ctx: discord.ApplicationContext, member: bridge.BridgeOption(discord.Member, name="成員")): # type: ignore
        
        if (cd := Core.command_cooldown.get(self.rape.name, {}).get(ctx.author.id, 0) - datetime.now().timestamp()) > 0:
            embed = discord.Embed(title="脫出中", color=discord.Color.red())
            embed.add_field(name="嗯、嘛、啊...", value=f"你剛剛已經雷普過別人了，請等待 {round(cd)} 秒後再試。", inline=False)
            await ctx.respond(embed=embed)
            return None
        
        if (cd := Core.remaining_time.get(ctx.author.id, 0) - datetime.now().timestamp()) > 0:
            await ctx.respond(f"十分不幸的，同志，你被遣送古拉格（或是被雷普了）！請等待 {round(cd)} 秒後再試。")
            return None
        
        author: discord.Member = ctx.author
        target: discord.Member = member
        
        if author.id == target.id:
            embed = discord.Embed(title="我撅我自己(難視)", color=discord.Color.red())
            embed.add_field(name="出現錯誤", value=f"{author.mention}，請不要雷普你自己(困惑)", inline=False)

        elif random.random() <= RAPE_SUCCESS_RATE[0]:
            Core.remaining_time[target.id] = datetime.now().timestamp() + 300
            
            embed = discord.Embed(title="雷普結果", color=discord.Color.red())
            embed.add_field(name="雷普成功！", value=f"{author.mention} 成功雷普了一個一個一個 {target.mention}。{target.mention} 將因為過於疲憊而無法使用 `?rob` 和 `?gamble` 5 分鐘。", inline=False)
            
        else:
            Core.remaining_time[author.id] = datetime.now().timestamp() + 600
            
            embed = discord.Embed(title="雷普結果", color=discord.Color.red())
            embed.add_field(name="雷普失敗！（絕望）", value=f"{author.mention} 遭到一轉攻勢，將無法使用 `?rob` 和 `?gamble` 10 分鐘。", inline=False)
            
            if random.random() <= 0.1:
                Core.user.add_item(author.id, Core.item.get(name="林檎"))
                embed.add_field(name="哦？（察覺）", value=f"...你在被一轉攻勢時，意外發現了一個一個一個林檎。", inline=False)
                
        await ctx.respond(embed=embed)
        
        Core.command_cooldown[self.rape.name][ctx.author.id] = datetime.now().timestamp() + RAPE_COOLDOWN
        
        log.debug(f"{ctx.author.name} used rape command. target: {member.name}")
    
    
    @bridge.bridge_command(
        name="work",
        name_localizations={"zh-TW": "工作"},
        description="Work for the society.",
        description_localizations={"zh-TW": "廉價勞工模擬器"},
    )
    async def work(self, ctx: discord.ApplicationContext):
        
        if (cd := Core.command_cooldown.get(self.work.name, {}).get(ctx.author.id, 0) - datetime.now().timestamp()) > 0:
            embed = discord.Embed(title="冷卻中", color=discord.Color.red())
            embed.add_field(name="請稍等，同志！", value=f"你已經勞動過了，請等待 {round(cd)} 秒後再試。", inline=False)
            await ctx.respond(embed=embed)
            return None
        
        if random.random() <= 0.3:
            score = 250
            Core.score.add_score(ctx.author.id, score)
            embed = discord.Embed(title="工作結果", color=discord.Color.green())
            embed.add_field(name="史達林同志的餽贈!", value=f"{ctx.author.mention} 史達林同志看見你如此辛勤勞動，便決定獎賞你 {score} 點社會信用點數。", inline=False)
            embed.add_field(name="當前社會信用點數", value=f"{Core.score.get_score(ctx.author.id)} 點", inline=False)
        
        else:
            score = 10
            Core.score.add_score(ctx.author.id, score)
            embed = discord.Embed(title="工作結果", color=discord.Color.green())
            embed.add_field(name="辛苦了，同志！", value=f"{ctx.author.mention} 你已經成功勞動並獲得了 {score} 點社會信用。", inline=False)
            embed.add_field(name="當前社會信用點數", value=f"{Core.score.get_score(ctx.author.id)} 點", inline=False)
        
        await ctx.respond(embed=embed)
        
        Core.command_cooldown[self.work.name][ctx.author.id] = datetime.now().timestamp() + WORK_COOLDOWN
        
        log.debug(f"{ctx.author.name} used work command.")
    
    
    @bridge.bridge_command(
        name="useringo",
        name_localizations={"zh-TW": "使用林檎"},
        description="Use an apple to recover 1 minute.",
        description_localizations={"zh-TW": "一個林檎可以舒緩一分鐘"},
    )
    async def use_ringo(self, ctx: discord.ApplicationContext, amount: bridge.BridgeOption(int, name="數量", default=1)): # type: ignore
        
        await Core.item.use_ringo(Core, ctx, amount)
        
        log.debug(f"{ctx.author.name} used use_ringo command. amount: {amount}")


            
def setup(bot: commands.Bot):
    bot.add_cog(ThunderDragonScore(bot))