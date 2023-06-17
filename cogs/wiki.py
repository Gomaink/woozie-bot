from nextcord.ext import commands
import nextcord
import requests
from bs4 import BeautifulSoup
import datetime
from googletrans import Translator

class SampFunctions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.translator = Translator()

    @nextcord.slash_command(
        name="wiki",
        description="Lista de funções da biblioteca a_samp",
    )
    async def wiki(self, interaction: nextcord.Interaction, function: str = None):
        if function:
            function = function.replace(" ", "")
            url = f"https://team.sa-mp.com/wiki/{function}.html"

            if url:
                response = requests.get(url)
                soup = BeautifulSoup(response.content, 'html.parser')
                description = soup.find('div', class_='description')
                example_usage = soup.find('pre', class_='pawn')
                parameters = soup.find('div', class_='parameters')
                param = soup.find_all('div', class_='param')

                if example_usage:
                    example_usage = example_usage.get_text()
                else:
                    example_usage = "Exemplo de uso não encontrado."

                if description:
                    description = description.get_text()
                    description = self.translator.translate(description, src='en', dest='pt').text
                else:
                    description = "Descrição não encontrada."

                if parameters:
                    parameters = parameters.get_text()
                else:
                    parameters = "Parâmetros não encontrados."

                if param:
                    param = [p.get_text() for p in param]
                    param = '\n'.join(param)
                else:
                    param = "Nenhum parâmetro encontrado."

                embed = nextcord.Embed(
                    title=function,
                    description=f'**Descrição:**\n{description}\n\n**Exemplo de uso:**\n```pawn\n{example_usage}\n```\n**Parâmetros:**\n{parameters}\n\n**Detalhes dos Parâmetros:**\n{param}',
                    color=nextcord.Color.blurple()
                )

                avatar_url = interaction.user.avatar.url
                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                embed.set_footer(text=f"Requisitado por: {interaction.user} | {current_time}", icon_url=avatar_url)
                await interaction.send(embed=embed)

                
            else:
                embed = nextcord.Embed(
                    title='Função não encontrada',
                    description='A função especificada não foi encontrada.',
                    color=nextcord.Color.red()
                )

                avatar_url = interaction.user.avatar.url
                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                embed.set_footer(text=f"Requisitado por: {interaction.user} | {current_time}", icon_url=avatar_url)
                await interaction.send(embed=embed, ephemeral=True)
        else:
            embed = nextcord.Embed(
                title='Função não encontrada',
                description='A função especificada não foi encontrada.',
                color=nextcord.Color.red()
            )

            avatar_url = interaction.user.avatar.url
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            await interaction.send(embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(SampFunctions(bot))
