from nextcord.ext import commands
import nextcord
from nextcord import ButtonStyle
import datetime

serverid = 1087574651150024804

class SearchSkin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="skin",
        description="Procure o ID de skins!",
        guild_ids=[serverid]
    )
    async def skin(self, interaction: nextcord.Interaction, skinid: int):
        if skinid >= 0 and skinid <= 311:
            embed = nextcord.Embed(
                title='Resultado da busca:',
                colour=2895667,
                url='https://assets.open.mp/assets/images/skins',
                description=f'**Skin ID: {skinid}**',
            )

            embed.set_image(url=f'https://assets.open.mp/assets/images/skins/{skinid}.png')
            avatar_url = interaction.user.avatar.url
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            embed.set_footer(text=f"Requisitado por: {interaction.user} | {current_time}", icon_url=avatar_url)

            async def on_previous_click(interaction: nextcord.Interaction):
                nonlocal skinid
                if skinid > 0:
                    skinid -= 1
                    embed.description = f'**Skin ID: {skinid}**'
                    embed.set_image(url=f'https://assets.open.mp/assets/images/skins/{skinid}.png')

                    await interaction.response.edit_message(embed=embed)

            async def on_next_click(interaction: nextcord.Interaction):
                nonlocal skinid
                if skinid < 311:
                    skinid += 1
                    embed.description = f'**Skin ID: {skinid}**'
                    embed.set_image(url=f'https://assets.open.mp/assets/images/skins/{skinid}.png')

                    await interaction.response.edit_message(embed=embed)

            b_previousskin = nextcord.ui.Button(style=ButtonStyle.secondary, label="Anterior")
            b_previousskin.callback = on_previous_click

            b_nextskin = nextcord.ui.Button(style=ButtonStyle.success, label="Próxima")
            b_nextskin.callback = on_next_click

            view = nextcord.ui.View()
            view.add_item(b_previousskin)
            view.add_item(b_nextskin)

            message = await interaction.send(embed=embed, view=view)

            view.message = message

def setup(bot):
    bot.add_cog(SearchSkin(bot))
