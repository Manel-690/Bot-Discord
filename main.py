import discord as dc
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="67", 
            intents=self._intents(), 
            help_command=None
        )

    def _intents(self):
        intents = dc.Intents.default()
        intents.message_content = True
        return intents

    async def setup_hook(self):
        await self.load_extension("cogs.recruitment")
        await self.load_extension("cogs.help")
        await self.load_extension("cogs.events")

bot = Bot()
bot.run(TOKEN)
