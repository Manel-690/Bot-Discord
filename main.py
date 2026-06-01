import discord as dc
from discord.ext import commands
import os
from dotenv import load_dotenv

import csv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
MUDAE_CHANNEL = os.getenv("MUDAE_CHANNEL_ID")
AKINATOR_CHANNEL = os.getenv("AKINATOR_CHANNEL_iD")
GARTIC_CHANNEL = os.getenv("GARTIC_CHANNEL_iD")
POKETWO_CHANNEL = os.getenv("POKETWO_CHANNEL_iD")

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
        super().__init__(command_prefix="67", intents=intents, help_command=None)

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
async def setup_recruitment(ctx):
    print("oi")
    embed = dc.Embed(
        title="recrutamento!!",
        description="clique aqui pra se alistar",
    )

    await ctx.send(embed=embed, view=recruitment_panel())
    await ctx.message.delete()

async def handle_mudae(ctx):
    embed = dc.Embed(
        title=":sparkling_heart: **Guia Básico do Mudae**",
        description=":pushpin: **Importante:** O Mudae é um bot de coleção de personagens de animes, jogos, filmes e séries. Seu objetivo é rolar personagens, capturá-los, montar sua coleção e acumular Kakera para desbloquear vantagens.",
        color=dc.Color.pink()
    )

    embed.add_field(name=":game_die: `Rolar personagens`", value="`$m` → Personagem aleatório\n`$wa` → Apenas personagens de anime/mangá\n`$wg` → Apenas personagens de jogos",inline=False)
    embed.add_field(name=":sparkling_heart: `Capturar personagens`", value="Reaja com 💖 quando um personagem aparecer para adicioná-lo à sua coleção.",inline=False)
    embed.add_field(name=":books: `Sua coleção`", value="`$mm` → Exibe sua coleção completa\n`$profile` → Mostra seu perfil\n`$fm` → Define seu personagem favorito",inline=False)
    embed.add_field(name=":mag: `Pesquisar personagens`", value="`$im Nome` → Pesquisa um personagem\nExemplo: `$im Rem`",inline=False)
    embed.add_field(name=":star: `Lista de desejos`", value="`$wish Nome` → Adiciona um personagem à sua wishlist\nExemplo: `$wish Rem`",inline=False)
    embed.add_field(name=":handshake: `Trocas`", value="`$trade @Usuário` → Inicia uma troca\n`$give @Usuário` → Presenteia um personagem",inline=False)
    embed.add_field(name=":broken_heart: `Remover personagens`", value="`$divorce Nome` → Remove um personagem da sua coleção",inline=False)
    embed.add_field(name=":gem: `Kakera`", value="`$kakera` → Mostra seus badges e progresso\n`$dailykakera` → Resgata Kakera diário\n`$kakeratower` → Constrói sua Torre de Kakera",inline=False)
    embed.add_field(name=":alarm_clock: `Temporizadores`", value="`$mu` → Tempo até o próximo claim\n`$rollsup` → Tempo até novas rolagens\n`$timersup` → Mostra todos os temporizadores",inline=False)
    embed.add_field(name=":gift: `Recompensas`", value="`$daily` → Receba rolls extras diariamente\n`$vote` → Vote no Mudae e ganhe benefícios",inline=False)
    embed.set_footer(text="🏆 Comandos essenciais: $m • $wa • $wg • $mm • $profile • $im • $wish • $trade • $kakera • $daily • $mu")
    await ctx.reply(embed=embed)

async def handle_akinator(ctx):
    embed = dc.Embed(
        title=":tophat: **Comandos do Akinator**",
        color = dc.Color.blue()
    )
    
    embed.add_field(name="`/aki`", value="> Inicia uma partida do Akinator", inline=True)
    embed.add_field(name="`/8ball`", value="> Faça uma pergunta e receba uma resposta aleatória da bola 8ball", inline=True)
    embed.add_field(name="`/pat @usuário`", value="> Demonstre carinho dando um cafuné (pat) em outro membro", inline=True)
    await ctx.reply(embed=embed)

async def handle_gartic(ctx):
    embed = dc.Embed(
        title=":art: **Guia Básico do GarticBOT**",
        description=":pushpin: **Importante:** Digite suas respostas diretamente no chat para tentar adivinhar o desenho antes dos outros jogadores.",
        color=dc.Color.green()
    )

    embed.add_field(name="`gartic`", value="> Inicia uma nova partida de Gartic no canal.", inline=True)
    embed.add_field(name="`dica`", value="> Receba uma dica sobre o desenho atual.\n> Máximo de 5 dicas por partida.", inline=True)
    embed.add_field(name="`desenho`", value="> Exibe novamente o desenho atual no chat.", inline=True)
    embed.add_field(name="`record`", value="> Mostra o recorde atual do canal e do tema em jogo.", inline=True)
    embed.add_field(name="`pular`", value="> Pula o desenho atual e inicia um novo.\n> Máximo de 3 pulos por partida.", inline=True)
    embed.set_footer(text="🎯 Adivinhe os desenhos o mais rápido possível para marcar mais pontos! • Qualquer dúvida, abra um ticket.")
    await ctx.reply(embed=embed)

async def handle_poketwo(ctx):
    embed = dc.Embed(
        title=":zap: **Guia Básico do Pokétwo**",
        description="""
        :pushpin: **Importante:** Para usar os comandos, é necessário mencionar o bot antes do comando.
        \nExemplo:\n`@Pokétwo catch Pikachu`  ou  `@Pokétwo pokemon`
        """,
        color=dc.Color.yellow()
    )

    embed.add_field(name="`start`", value="> Inicia sua jornada Pokémon.", inline=True)
    embed.add_field(name="`pick <pokémon>`", value="> Escolha seu Pokémon inicial.", inline=True)
    embed.add_field(name="`catch <pokémon>`", value="> Captura um Pokémon que apareceu no chat.", inline=True)
    embed.add_field(name="`hint`", value="> Receba uma dica sobre o Pokémon atual.", inline=True)
    embed.add_field(name="`pokemon`", value="> Mostra sua coleção de Pokémon", inline=True)
    embed.add_field(name="`info <número>`", value="> Exibe informações detalhadas de um Pokémon.", inline=True)
    embed.add_field(name="`select <número>`", value="> Define um Pokémon como principal.", inline=True)
    embed.add_field(name="`evolve`", value="> Evolui o Pokémon selecionado, se possível.", inline=True)
    embed.add_field(name="`favorite <número>`", value="> Marca um Pokémon como favorito.", inline=True)
    embed.add_field(name="`trade @usuário`", value="> Inicia uma troca com outro treinador.", inline=True)
    embed.add_field(name="`market search <pokémon>`", value="> Procura um Pokémon no mercado.", inline=True)
    embed.add_field(name="`market buy <ID>`", value="> Compra um Pokémon do mercado.", inline=True)
    embed.add_field(name="`market add <número> <preço>`", value="> Coloca um Pokémon à venda.", inline=True)
    embed.add_field(name="`reindex`", value="> Organiza e renumera sua coleção.", inline=True)
    embed.set_footer(text="🎯 Converse no servidor para fazer Pokémons aparecerem no chat e aumente sua coleção!")
    await ctx.reply(embed=embed)

HELP_HANDLERS = {
    MUDAE_CHANNEL: handle_mudae,
    AKINATOR_CHANNEL: handle_akinator,
    GARTIC_CHANNEL: handle_gartic,
    POKETWO_CHANNEL: handle_poketwo
}

@bot.command()
async def help(ctx):
    handler = HELP_HANDLERS.get(str(ctx.channel.id))
    if handler:
        await handler(ctx)
    else:
        print("nada")    

bot.run(TOKEN)