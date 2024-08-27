import discord
from discord.ext import commands

from bot.utils.help import HelpCommandSettings


class Help(commands.MinimalHelpCommand):
    async def send_bot_help(self, mapping):
        destination = self.get_destination()
        await destination.send(embed=HelpCommandSettings.help())