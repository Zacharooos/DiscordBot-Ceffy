# Arquivo de configuração vs 0.3
# Arquivo para guardar funções que desempenhem papéis de configuração ou ajuste do bot em sí.
import json
import discord
from discord.ext.commands import Bot

PREFIX = "!"

# Função de referêncio, em caso de dúvidas, verifique a fileExemplo
def recuperarToken():
    with open("src/config.json") as f:
        token = json.load(f)['token']

    return token

# Iniciar a configuração do cliente.
def iniciarConfig():
    client = Bot(command_prefix = PREFIX, intents = discord.Intents.all())
    return client

# Dá partida do bot depois de terminar as configurações
def terminarConfig(client, token):
    client.run(token)
    return 0