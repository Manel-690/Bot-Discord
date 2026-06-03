import discord as dc
from discord.ext import commands
from dotenv import load_dotenv
from utils.constants import *
import os
import csv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

class form_button(dc.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @staticmethod
    def get_cache(interaction: dc.Interaction):
        result = None
        with open("cache.csv", mode="r", encoding="utf-8") as arq:
            linhas = arq.readlines()
            for index, linha in enumerate(linhas):
                col = linha.strip().split(",")
                if col[0] == str(interaction.message.id):
                    linhas.pop(index)
                    result = col[1], col[2], col[3]
                    break
            
        with open("cache.csv", mode="w", encoding="utf-8") as arq:
            arq.writelines(linhas)
                
        return result

    @staticmethod
    def save_csv(name: str, game_id: str, number: str):
        with open("dados.csv", mode="a", encoding="utf-8") as arq:
            arq.write(",".join([name, game_id, number]) + "\n")
    
    @dc.ui.button(style=dc.ButtonStyle.green, emoji="✅", custom_id="fzxbtn_accept_form")
    async def accept(self, interaction: dc.Interaction, button=dc.ui.Button):
        embed = interaction.message.embeds[0]

        desc = embed.description
        embed.description = desc.replace("Aguardando análise...", f"Aprovado por {interaction.user.mention}!")
        embed.color = dc.Color.green()

        for item in self.children:
            item.disabled = True

        cached = self.get_cache(interaction)
        self.save_csv(*cached)

        await interaction.response.edit_message(embed=embed, view=self)

    @dc.ui.button(style=dc.ButtonStyle.green, emoji="❌", custom_id="fzxbtn_decline_form")
    async def decline(self, interaction: dc.Interaction, button=dc.ui.Button):
        embed = interaction.message.embeds[0]

        desc = embed.description
        embed.description = desc.replace("Aguardando análise...", f"Recusado por {interaction.user.mention}!")
        embed.color = dc.Color.red()

        for item in self.children:
            item.disabled = True

        cached = self.get_cache(interaction)
        self.save_csv(*cached)

        await interaction.response.edit_message(embed=embed, view=self)

class recruitment_form(dc.ui.Modal, title="Clubs Recruitment Form"):
    input_name = dc.ui.Label(
        text="Qual é o seu nome?",
        component=dc.ui.TextInput(
            custom_id="fzxname_form_modal",
            placeholder="Escreva seu nome completo...", 
            style=dc.TextStyle.short,
            min_length=8, max_length=50
        )
    )

    input_id = dc.ui.Label(
        text="Qual é o seu ID no jogo? (ex.: 9JPJJPUUY)",
        component=dc.ui.TextInput(
            custom_id="fzxid_form_modal",
            placeholder="Digite seu ID do Brawl Stars...", 
            style=dc.TextStyle.short,
            min_length=5, max_length=10
        )
    )

    input_num = dc.ui.Label(
        text="Qual é o seu número de telefone?",
        component=dc.ui.TextInput(
            custom_id="fzxnum_form_modal",
            placeholder="Digite seu número de telefone com DDD...",
            style=dc.TextStyle.short,
            min_length=11, max_length=11
        )
    )

    input_reason = dc.ui.Label(
        text="Um motivo para ser aceito (ex.: sei la)",
        component=dc.ui.TextInput(
            custom_id="fzxreason_form_modal",
            placeholder="Escreva um bom motivo...",
            style=dc.TextStyle.long,
            min_length=5, max_length=80
        )
    )

    def clean_form(self, game_id: str, number: str):
        if game_id.startswith("#"):
            game_id = game_id[1:]
            
        number = "".join(char for char in number if char.isdigit())

        return game_id, number

    async def validate_num(self, interaction: dc.Interaction, number: str):
        if len(number) != 11:
            await interaction.response.send_message(
                "O telefone deve conter 8 dígitos: DDD + 9 + NUM"
            )
            return False
        return True

    async def verify_duplicate(self, interaction: dc.Interaction, name: str, game_id: str, number: str):
        with open("dados.csv", mode="r", encoding="utf-8") as arq:
            for linha in arq:
                col = linha.strip().split(",")
                if col[1] == game_id:
                    await interaction.response.send_message(
                        "O ID informado já está cadastrado.",
                        ephemeral=True
                    )
                    return False
                elif col[2] == number:
                    await interaction.response.send_message(
                        "O número de telefone informado já está cadastrado.",
                        ephemeral=True
                    )
                    return False

        with open("cache.csv", mode="r", encoding="utf-8") as arq:
            for linha in arq:
                col = linha.strip().split(",")
                if col[2] == game_id or col[3] == number:
                    await interaction.response.send_message(
                        "Você já enviou o formulário, aguarde o resultado.",
                        ephemeral=True
                    )
                    return False
        return True

    def save_cache(self, message_id: int, name: str, game_id: str, number: str):
        with open("cache.csv", mode="a", encoding="utf-8") as arq:
            arq.write(",".join([str(message_id), name, game_id, number]) + "\n") 

    async def send_form(self, interaction: dc.Interaction, name: str, game_id: str, number: str, reason: str):
        channel = interaction.client.get_channel(FORMS_CHANNEL_ID)
        if channel is None:
            try:
                channel = await interaction.client.fetch_channel(FORMS_CHANNEL_ID)
            except Exception as e:
                print(f"Erro ao buscar o canal de formulários: {e}")
                return False

        embed = dc.Embed(
            title="📝 Formulário de Recrutamento", 
            color=dc.Color.default(), 
            timestamp=interaction.created_at,
            description=(
                f"**Usuário:** {interaction.user.mention}\n"
                f"**Status:** Aguardando análise...\n"
                f"--------------------------\n"
                f"```yaml\n"
                f"Nickname: {name}\n"
                f"ID: #{game_id}\n"
                f"Telefone: {number}\n"
                f"```\n"
                f"**Motivo:**\n"
                f"> {reason}\n"
                f"--------------------------\n"
            )
        )
        embed.set_thumbnail(url=interaction.user.display_avatar.url)

        mensagem = await channel.send(embed=embed, view=form_button())
        self.save_cache(mensagem.id, name, game_id, number)
        return True

    async def on_submit(self, interaction: dc.Interaction):
        typed_name = self.input_name.component.value
        typed_id = self.input_id.component.value
        typed_num = self.input_num.component.value
        typed_reason = self.input_reason.component.value

        typed_id, typed_num = self.clean_form(typed_id, typed_num)

        if not await self.validate_num(interaction, typed_num): 
            return
        if not await self.verify_duplicate(interaction, typed_name, typed_id, typed_num): 
            return

        await interaction.response.send_message("enviado!", ephemeral=True)
        await self.send_form(interaction, typed_name, typed_id, typed_num, typed_reason)

class recruitment_panel(dc.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @dc.ui.button(label="Abrir Formulário", custom_id="fzxform_button")
    async def open_form(self, interaction: dc.Interaction, button: dc.ui.Button):
        await interaction.response.send_modal(recruitment_form())

class Bot(commands.Bot):
    def __init__(self):
        intents = dc.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="69", intents=intents, help_command=None)

    async def setup_hook(self):
        self.add_view(recruitment_panel())
        self.add_view(form_button())
        await self.load_extension("cogs.help")
        await self.load_extension("cogs.events")

bot = Bot()

# ============= commands =============

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
@commands.has_permissions(administrator=True)
async def setup_recruitment(ctx):
    embed = dc.Embed(
        title="recrutamento!!",
        description="clique aqui pra se alistar",
    )

    await ctx.send(embed=embed, view=recruitment_panel())
    await ctx.message.delete()

bot.run(TOKEN)