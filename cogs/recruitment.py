import discord as dc
from discord.ext import commands
from views.form_button import FormButton
from views.recruitment_panel import RecruitmentPanel

class Recruitment(commands.Cog):
    """
    Cog responsável pelos comandos de recrutamento.
    Registra as views e cria o comando de setup do painel de recrutamento.
    """
    def __init__(self, bot, service):
        self.bot = bot
        self.service = service

    async def cog_load(self):
        self.bot.add_view(FormButton(self.service))
        self.bot.add_view(RecruitmentPanel(self.service))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setup_recruitment(self, ctx):
        embed = dc.Embed(
            title="😝 Recrutamento",
            description="etc etc etc"
        )
        await ctx.send(embed=embed, view=RecruitmentPanel(self.service))
        await ctx.message.delete()

async def setup(bot):
    service = RecruitmentService(
        validator=FormValidator(),
        brawl=BrawlStarsService(),
        candidates=CandidatesRepository(),
        members=MembersRepository()
    )
    await bot.add_cog(Recruitment(bot, service))