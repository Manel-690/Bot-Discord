from discord.ext import commands

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("logado eba")

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.bot:
            return
            
        if msg.content == "oi":
            if msg.author.name == "felipoz":
                await msg.add_reaction("❤️")
            if msg.author.name == "genebrau":
                await msg.reply("seu cocozao")

        await self.bot.process_commands(msg)

async def setup(bot):
    await bot.add_cog(Events(bot))