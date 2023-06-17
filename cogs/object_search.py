from nextcord import Interaction, SlashOption, ChannelType
from nextcord.ext import commands
import nextcord
from nextcord import ButtonStyle
import aiohttp
import datetime

serverid = 1087574651150024804

class ObjectSearch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="objeto",
        description="Procure o ID de objeto!",
        guild_ids=[serverid]
    )
    async def objeto(self, interaction: Interaction, objectid: int):
        if objectid >= 0 and objectid <= 19999:
            embed = nextcord.Embed(
                title='Resultado da busca:',
                colour=2895667,
                url='https://dev.prineside.com/gtasa_samp_model_id/category/all/',
                description=f'**Objeto de ID: {objectid}**',
            )

            image_url = f'https://files.prineside.com/gtasa_samp_model_id/blue/{objectid}_b.jpg'

            async with aiohttp.ClientSession() as session:
                async with session.get(image_url) as response:
                    if response.status == 200:
                        content = await response.read()
                        if b"Prineside File Storage" not in content:
                            embed.set_image(url=image_url)
                        else:
                            embed.description = f'Objeto ID {objectid} não foi encontrado.'
                            embed.set_image(url='')

            avatar_url = interaction.user.avatar.url
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            embed.set_footer(text=f"Requisitado por: {interaction.user} | {current_time}", icon_url=avatar_url)

            async def on_previous_click(interaction: nextcord.Interaction):
                nonlocal objectid
                if objectid > 0:
                    objectid -= 1
                    embed.description = f'**Objeto de ID: {objectid}**'
                    image_url = f'https://files.prineside.com/gtasa_samp_model_id/blue/{objectid}_b.jpg'

                    async with aiohttp.ClientSession() as session:
                        async with session.get(image_url) as response:
                            if response.status == 200:
                                content = await response.read()
                                if b"Prineside File Storage" not in content:
                                    embed.set_image(url=image_url)
                                else:
                                    embed.description = f'Objeto ID {objectid} não foi encontrado.'
                                    embed.set_image(url='')

                    await interaction.response.edit_message(embed=embed)

            async def on_next_click(interaction: nextcord.Interaction):
                nonlocal objectid
                if objectid < 19999:
                    objectid += 1
                    embed.description = f'**Objeto de ID: {objectid}**'
                    image_url = f'https://files.prineside.com/gtasa_samp_model_id/blue/{objectid}_b.jpg'

                    async with aiohttp.ClientSession() as session:
                        async with session.get(image_url) as response:
                            if response.status == 200:
                                content = await response.read()
                                if b"Prineside File Storage" not in content:
                                    embed.set_image(url=image_url)
                                else:
                                    embed.description = f'Objeto ID {objectid} não foi encontrado.'
                                    embed.set_image(url='')

                    await interaction.response.edit_message(embed=embed)

            b_previousobject = nextcord.ui.Button(style=ButtonStyle.secondary, label="Anterior")
            b_previousobject.callback = on_previous_click

            b_nextobject = nextcord.ui.Button(style=ButtonStyle.success, label="Próxima")
            b_nextobject.callback = on_next_click

            view = nextcord.ui.View()
            view.add_item(b_previousobject)
            view.add_item(b_nextobject)

            message = await interaction.send(embed=embed, view=view)

            view.message = message

def setup(bot):
    bot.add_cog(ObjectSearch(bot))
