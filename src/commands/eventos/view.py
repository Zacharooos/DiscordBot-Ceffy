import discord
from commands.eventos.functions import *
from discord.interactions import Interaction


class modal_evento(discord.ui.Modal):
    def __init__(self):
        super().__init__(title='Novo evento', timeout=90)
        # Criando campos
        self.data = discord.ui.TextInput(label='Data (formato dd-mm-aaaa):', placeholder='01-01-2023', max_length=10, style=discord.TextStyle.short)
        self.nome = discord.ui.TextInput(label='Nome', max_length=64)
        self.descricao = discord.ui.TextInput(label='Descrição', style=discord.TextStyle.paragraph, max_length=256, required=False)

        # Adicionando ao modal
        self.add_item(self.data)
        self.add_item(self.nome)
        self.add_item(self.descricao)

    async def on_submit(self, interaction: Interaction):
        await interaction.response.defer()

        # Pegando informações do modal
        data = self.data.value
        nome = self.nome.value
        descricao = self.descricao.value

        # Fazendo tratamento de data

        try:
            aux = datetime.datetime.strptime(data, "%d-%m-%Y")

            if(aux.date() == datetime.datetime.now().date()):
                await interaction.followup.send('Você colocou a data de hj ¬_¬', ephemeral=True)
                return
            if(aux.date() < datetime.datetime.now().date()):
                await interaction.followup.send('A data que vc colocou já passou 😑', ephemeral=True)
                return
        except Exception:
            await interaction.followup.send(f'Não entendi a data que você colocou 😓 (*{data}*)', ephemeral=True)
            raise Exception

        start_cadastro(data, nome, descricao)


        ## TENTAR FAZER SELEÇÃO DE ROLE DEPOIS ##
        # view = discord.ui.View(timeout=30)

        # # Criando classe de RoleSelect para mandar na view
        # async def RoleSelect_callback(it: Interaction):
        #     view.stop()
        #     view.clear_items()
        #     await interaction.followup.send(content='hello', ephemeral=True)

        # roles = discord.ui.RoleSelect()
        # roles.callback = RoleSelect_callback
        # view.add_item(roles)

        # # Mandando mensagem para saber quem será mencionado
        # await interaction.followup.send(content='Quem deve ser notificado?', view=view, ephemeral=True)

        # await view.wait()

        await interaction.followup.send('Cadastrado 😊', ephemeral=True)