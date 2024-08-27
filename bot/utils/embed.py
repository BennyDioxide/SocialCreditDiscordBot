import discord
from .emoji import EmojiManager

class EmbedMaker:
    def __new__(self, status: bool=None, description: str=None, title: str=None, color: str=None):
        self.embed = discord.Embed(description=EmojiManager(description))
        
        emojis = EmojiManager.get_emojis()
        
        if "animation_yes" in emojis:
            yes_emoji = emojis["animation_yes"]
        else:
            yes_emoji = "✅"
            
        if "animation_no" in emojis:
            no_emoji = emojis["animation_no"]
        else:
            no_emoji = "❌"
        
        if status is None:
            self.embed.title = EmojiManager(title) if title else None
            self.embed.color = discord.Color.blue()
        elif status:
            self.embed.title = EmojiManager(title) if title else f'**執行成功{yes_emoji}**'
            self.embed.color = discord.Color.green()
        else:
            self.embed.title = EmojiManager(title) if title else f'**執行失敗{no_emoji}**'
            self.embed.color = discord.Color.red()
            
        if color is not None:
            try: self.embed.color = getattr(discord.Color, color)()
            except AttributeError: pass
            
        return self.embed