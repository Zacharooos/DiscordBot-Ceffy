# ARQUIVO DE SETUP DE COMANDOS DO BOT v0.4#
# - Aqui serão importadas as funções "start" de cada comando do bot
# - A função principal setup_commands recebe a tree como parâmetro e popula com os comandos
# - Tentem seguir o padrão de comentário/descrição, declaração, e espaço para proximo comando


# Imports gerais
import discord

# Imports dos comandos
from commands.soma.functions import start as command_soma


def setup_commands(tree) -> bool:
    try:
        '''
        ##COMANDO TESTE##
        Comando apenas para testar se a ceffy está acordada e esperta 🥶🤖
        '''
        @tree.command(name='teste', description='Teste de slash', guild=discord.Object(id=994616556401197179))
        async def self(interaction: discord.Interaction, var: str):
            await interaction.response.send_message(f"Oi. Você mandou '{var}'!")


        '''
        ##COMANDO SOMA##
        Comando que pega dois números e responde uma mensagem com a soma deles
        '''
        @tree.command(name='soma', description='Soma de dois inteiros', guild=discord.Object(id=994616556401197179))
        async def self(interaction: discord.Interaction, a: int, b: int):
            await interaction.response.send_message(command_soma(a,b))


        '''
        #COMANDO TAL#
        ...
        '''
        #@tree.command(...)

        return True

    except Exception as e:
        print('Erro ao incluir comandos!\n', e)
        return False