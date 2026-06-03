import discord as dc

class FormButton(dc.ui.View):
    def __init__(self, service):
        super().__init__(timeout=None)
        self.service = service
    
    @dc.ui.button(style=dc.ButtonStyle.green, emoji="✅", custom_id="btn_approve_form")
    async def approve(self, interaction: dc.Interaction, button=dc.ui.Button):
        await self.service.approve(interaction)

    @dc.ui.button(style=dc.ButtonStyle.red, emoji="❌", custom_id="btn_decline_form")
    async def decline(self, interaction: dc.Interaction, button=dc.ui.Button):
        await self.service.decline(interaction)
