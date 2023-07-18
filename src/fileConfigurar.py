# Arquivo de configuração vs 0.4
# Arquivo para guardar funções que desempenhem papéis de configuração ou ajuste do bot em sí.
import json
import discord
from discord.ext.commands import Bot


# Função de referêncio, em caso de dúvidas, verifique a fileExemplo
def recuperarToken():
    with open("src/config.json") as f:
        token = json.load(f)['token']

    return token

# Iniciar a configuração do cliente.
def iniciarConfig():
    class aclient(discord.Client):
        def __init__(self):
            super().__init__(intents = discord.Intents.default())
            self.synced = False #we use this so the bot doesn't sync commands more than once

        async def on_ready(self):
            await self.wait_until_ready()
            if not self.synced: #check if slash commands have been synced 
                await tree.sync(guild = discord.Object(id=994616556401197179)) #guild specific: leave blank if global (global registration can take 1-24 hours)
                self.synced = True
            print(f"We have logged in as {self.user}.")

    client = aclient()
    tree = discord.app_commands.CommandTree(client)
    return client, tree

# Dá partida do bot depois de terminar as configurações
def terminarConfig(client, token):
    try:
        client.run(token)
    except discord.errors.LoginFailure as e:
        print(f"Ocorreu um erro ao logar na Ceffy:\n{e}")
    return 