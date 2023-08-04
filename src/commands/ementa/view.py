# A chamada das funções do comando aqui é feita na view.
# No setup.py apenas inicializamos a view e ela faz o resto.

from typing import Any
import discord
from discord.interactions import Interaction
from discord.ui.item import Item
from json import load
from commands.ementa.functions import *
from logsService import Logs

class EmentaView(discord.ui.View):
    '''Classe da view responsável pela interação do comando `detalhes_materia`'''

    def __init__(self, interaction: discord.Interaction, log: Logs = None):
        super().__init__(timeout=30)
        self.interaction = interaction
        self.triggered = False
        self.log = log

    # Sobrescrita do callback de timeout
    async def on_timeout(self):
        '''A callback that is called when a view's timeout elapses without being explicitly stopped.'''
        if not self.triggered:
            await self.interaction.edit_original_response(content='Acabou o tempo, amigo 🥱',view=None)
        else:
            await super().on_timeout()

    # Sobrescrita do callback de erro
    async def on_error(self, interaction: Interaction[discord.Client], error: Exception, item: Item[Any]):
        if self.log is not None:
                msg_error = 'Foi mal, nao consegui pegar os detalhes 😞'
                await interaction.response.edit_message(content=msg_error, view=None, delete_after=30)
                await self.log.report_error('detalhes_materia', error)
        else:
            await super().on_error(interaction, error, item)

    
    # Definição do Select Menu e seu callback(quando uma opção é selecionada)
    @discord.ui.select(placeholder='Selecione um período!',
                       options=[discord.SelectOption(label=f'{i}º Período', value=str(i)) for i in range(1,11)])
    async def callback(self, interaction, select):
        self.clear_items()
        self.add_item(select)
        with open('data/materias.json', encoding='utf8') as json:
            grade = load(json)
            for materia in grade['materias']:
                if(grade['materias'][materia]['periodo'] == int(select.values[0])):
                    button = discord.ui.Button(label=materia, style=discord.ButtonStyle.primary)
                    # Função que criará um callback personalizado para cada button
                    def create_callback(btn):
                        async def button_callback(interaction):
                            self.triggered = True
                            await interaction.response.edit_message(content='Aqui estão as informações:',
                                                                    embed=start_materia(btn.label),
                                                                    view=None)
                        return button_callback
                    button.callback = create_callback(button)
                    # Adicionando button na view
                    self.add_item(button)
        # Editando mensagem com a view atualizada
        await interaction.response.edit_message(content=f'Mostrando {select.values[0]}º Período:', view=self)
