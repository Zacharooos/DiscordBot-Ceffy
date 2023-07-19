# Classe que servirá para o tratamento de logs.
# - Será chamada para qualquer tipo de notificação, como warings e erros por exemplo
# - Podemos depois fazer algum método para salvar os logs completos em algum arquivo se necessário

# Imports
import discord
import traceback
from datetime import datetime

# Constants
ID_CHANNEL = 1131309217849028720


class Logs:
    def __init__(self, client: discord.Client):
        self.client = client


    def report_error(self, command: str, error: Exception=None):
        '''
        Notifica um erro no canal de erros da Ceffy no discord.

        Parameters
        -----------
        command: :class:`str`
            Nome do comando no qual ocorreu o erro para a notificação
        error: :class:`Exception`
            Exceção que será notificada.
        '''

        channel = self.client.get_channel(ID_CHANNEL)
        date = datetime.today()

        # Pegando traceback
        tb = ''.join(traceback.format_exception(etype=type(error), value=error, tb=error.__traceback__))
        if len(tb) > 512:
            tb = '_Não disponível_'

        # Montando Embed de erro
        embed = discord.Embed(colour=0xff0000)
        embed.title = f"Erro no comando {command}"
        embed.add_field(name='Data da ocorrencia:', value=f'{date}')
        embed.add_field(name='Detalhes:', value=f'{error}', inline=False)
        embed.add_field(name='Traceback:', value=tb)

        return channel.send(embed=embed)