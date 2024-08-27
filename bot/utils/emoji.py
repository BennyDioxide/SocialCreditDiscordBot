import re
import discord

gl_emojis = None

class EmojiManager:
    
    def __new__(self, message: str):
        return self.translation_emoji_string(message)
    
    def translation_emoji_string(message: str):
        """Translate the message including emojis"""
        global gl_emojis
        pattern = re.compile(r':[^:]+:')
        
        for t in re.findall(pattern, message):
            t: str
            if t.strip(":") in gl_emojis:
                message = message.replace(t, gl_emojis[t.strip(":")])
                
        return message
        
    def set_emojis(emojis: dict[str:discord.Emoji]):
        global gl_emojis
        gl_emojis = emojis
        
    def get_emojis():
        global gl_emojis
        return gl_emojis