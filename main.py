import discord as dc
from discord.ext import commands
import os
from dotenv import load_dotenv

import csv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

class recruitment_form(dc.ui.Modal, title="Clubs Recruitment Form"):
    input_name = dc.ui.Label(
        text="Qual é o seu nome?",
        component=dc.ui.TextInput(
            custom_id="name_form_modal",
            placeholder="Escreva seu nome completo...", 
            style=dc.TextStyle.short,
            min_length=8, max_length=50
        )
    )

    input_id = dc.ui.Label(
        text="Qual é o ID no jogo? (ex.: 9JPJJPUUY)",
        component=dc.ui.TextInput(
            custom_id="id_form_modal",
            placeholder="Digite seu ID do Brawl Stars...", 
            style=dc.TextStyle.short,
            min_length=5, max_length=10
        )
    )

    input_num = dc.ui.Label(
        text="Qual é o seu número de telefone?",
        component=dc.ui.TextInput(
            custom_id="num_form_modal",
            placeholder="Digite seu número de telefone com DDD...",
            style=dc.TextStyle.short,
            min_length=11, max_length=11
        )
    )

    input_reason = dc.ui.Label(
        text="Um motivo para ser aceito (ex.: sei la)",
        component=dc.ui.TextInput(
            custom_id="reason_form_modal",
            placeholder="Escreva um bom motivo...",
            style=dc.TextStyle.long,
            min_length=5, max_length=80
        )
    )

    async def on_submit(self, interaction: dc.Interaction):
        typed_name = self.input_name.component.value
        typed_id = self.input_id.component.value
        typed_num = self.input_num.component.value
        typed_reason = self.input_reason.component.value

        with open("dados.csv", mode="a", encoding="utf-8") as arq:
            arq.write(",".join([typed_name, typed_id, typed_num]) + "\n")

        await interaction.response.send_message(
            "enviado!",
            ephemeral=True
        )


class recruitment_panel(dc.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @dc.ui.button(label="Abrir Formulário", custom_id="form_button")
    async def open_form(self, interaction: dc.Interaction, button: dc.ui.Button):
        await interaction.response.send_modal(recruitment_form())

class Bot(commands.Bot):
    def __init__(self):
        intents = dc.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="67", intents=intents)

    async def setup_hook(self):
        self.add_view(recruitment_panel())
        print("setupado")

bot = Bot()

@bot.event
async def on_ready():
    print("logado eba")

@bot.event
async def on_message(msg):
    if msg.content == "oi":
        if msg.author.name == "felipoz":
            await msg.add_reaction("❤️")
        if msg.author.name == "genebrau":
            await msg.reply("seu cocozao")

    await bot.process_commands(msg)


@bot.command()
async def view_ctx(ctx):
    print("======= ctx attributes =======")
    for key, value in ctx.__dict__.items():
        print(f"{key}: {value} ({type(value)})")

    print("\n======= ctx.message attributes =======")
    attributes = {a: getattr(ctx.message, a) for a in dir(ctx.message) if not a.startswith("_") and a != "interaction"}
    for key, value in attributes.items():
        print(f"{key}: {value} ({type(value)})")


@bot.command()
async def setup_recruitment(ctx):
    print("oi")
    embed = dc.Embed(
        title="recrutamento!!",
        description="clique aqui pra se alistar",
    )

    await ctx.send(embed=embed, view=recruitment_panel())
    await ctx.message.delete()

bot.run(TOKEN)