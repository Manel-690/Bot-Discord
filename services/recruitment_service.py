import discord as dc
from dataclasses import dataclass
from services.form_validator import FormValidator
from services.brawlstars import BrawlStarsService
from repositories.csv_candidates import CandidatesRepository
from repositories.csv_members import MembersRepository
from utils.constants import FORMS_CHANNEL_ID

@dataclass
class SubmitResult:
    """Resultado do envio de um formulário."""
    ok: bool
    error: str = ""

class RecruitmentService:
    """
    Serviço responsável por organizar o fluxo do recrutamento.
    Valida dados, checa duplicatas, busca troféus e organiza o envio e avaliação de formulários.
    """
    def __init__(self, validator, brawl, members, candidates):
        """
        Parameters
        ----------
        validator : FormValidator
        brawl : BrawlStarsService
        members : MembersRepository
        candidates : CandidatesRepository
        """
        self.validator = validator
        self.brawl = brawl
        self.members = members
        self.candidates = candidates

    async def submit(self, interaction: dc.Interaction, name: str, game_id: str, phone: str, reason: str):
        """
        Realiza o envio um formulário de recrutamento no canal de recrutamento e aguarda aprovação.

        Parameters
        ----------
        interaction : discord.Interaction
            Interação do discord que originou o envio do formulário.
        name : str
            Nome do candidato.
        game_id : str
            ID do jogador.
        phone : str
            Telefone do candidato.
        reason : str
            Motivo para entrar na comunidade.

        Returns
        -------
        SubmitResult
            Resultado com ok=True, ou ok=False e mensagem de erro.
        """
        game_id, phone = self.validator.clean(game_id, phone)

        error = self.validator.validate(phone)
        if error:
            return SubmitResult(ok=False, error=error)

        if self.members.exists(game_id=game_id):
            return SubmitResult(ok=False, error="ID já cadastrado.")

        if self.members.exists(phone=phone):
            return SubmitResult(ok=False, error="Telefone já cadastrado.")

        if self.candidates.exists(game_id=game_id, phone=phone):
            return SubmitResult(ok=False, error="Você já enviou o formulário, aguarde.")

        trophies = await self.brawl.get_trophies(game_id)
        embed = self._build_embed(interaction, name, game_id, phone, reason, trophies)

        channel = await self._get_channel(interaction)

        if channel is None:
            return SubmitResult(ok=False, error="Canal de formulários não encontrado.")

        from views.form_button import FormButton
        message = await channel.send(embed=embed, view=FormButton(self))

        self.candidates.save(message.id, name, game_id, phone, trophies)

        return SubmitResult(ok=True)

    async def approve(self, interaction: dc.Interaction):
        """Aprova o formulário."""
        await self._resolve(interaction, approved=True)

    async def decline(self, interaction: dc.Interaction):
        """Recusa o formulário."""
        await self._resolve(interaction, approved=False)

    async def _resolve(self, interaction: dc.Interaction, approved: bool):
        """
        Resolve um formulário como aprovado ou recusado.

        Edita o embed com o status final, desativa os botões e, se aprovado,
        move o candidato para o repositório de membros.

        Parameters
        ----------
        interaction : discord.Interaction
            Interação do discord que originou o envio do formulário.
        approved : bool
            True para aprovar, False para recusar.
        """
        embed = interaction.message.embeds[0]
        label = f"Aprovado por {interaction.user.mention}" if approved else f"Recusado por {interaction.user.mention}!"
        embed.description = embed.description.replace("Aguardando análise...", label)
        embed.color = dc.Color.green() if approved else dc.Color.red()

        if approved:
            candidates = self.candidates.pop(interaction.message.id)
            if candidates:
                self.members.save(*candidates)

        view = interaction.message.components
        from views.form_button import FormButton
        disabled_view = FormButton(self)
        for item in disabled_view.children:
            item.disabled = True

        await interaction.response.edit_message(embed=embed, view=disabled_view)

    def _build_embed(self, interaction: dc.Interaction, name: str, game_id: str, phone: str, reason: str, trophies: int):
        """
        Monta o embed do formulário.
        
        Parameters
        ----------
        interaction: discord.Interaction
            Interação do discord que originou o envio do formulário.
        name : str
            Nome do candidato.
        game_id : str
            ID do jogador.
        phone : str
            Telefone do candidato.
        reason : str
            Motivo para entrar na comunidade.
        trophies : int
            Número de troféus do jogador.

        Returns
        -------
        discord.Embed
            Embed formatado com os dados do candidato para envio.
        """
        trophies_str = f"{trophies:,}".replace(",", ".") if trophies > 0 else "Não sei"
        return dc.Embed(
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
                f"Troféus: {trophies_str}\n"
                f"Telefone: ({phone[:2]}) {phone[2]} {phone[3:7]}-{phone[7:]}\n"
                f"```\n"
                f"**Motivo:**\n"
                f"> {reason}\n"
                f"--------------------------\n"
            )
        ).set_thumbnail(url=interaction.user.display_avatar.url)

    async def _get_channel(self, interaction: dc.Interaction):
        """
        Busca o canal de formulário.
        
        Parameters
        ----------
        interaction : discord.Interaction
            Interação do discord que originou o envio do formulário
        
        Returns
        -------
        discord.TextChannel | None
            Canal de texto ou None, se não encontrar.
        """
        channel = interaction.client.get_channel(FORMS_CHANNEL_ID)
        if channel is None:
            try:
                channel = await interaction.client.fetch_channel(FORMS_CHANNEL_ID)
            except Exception as err:
                print(f"Erro ao buscar canal de logs do formulário: {err}")
        return channel
