# CeffyBot version 0.3
# Corpo principal da aplicação, funções não devem ser declaradas neste arquivo!

# Notas importantes:
# --- Matheus se você escrever dódigo igual você faz no estágio eu vou te cortar🔪.
# --- O Bot só funciona enquanto o processo gerado pelo main.py existir.
# --- Para conseguir acesso a file config.json, acesse o nosso grupo no Discord.

# Imports para o projeto
import os
import discord
from discord.ext import commands

# Imports de files auxiliares
from fileExemplo import *
from fileConfigurar import *
from scriptComandosBasicos import *

# Chamadas da funções
if __name__ ==  "__main__":
    
    # Função de referêncio, em caso de dúvidas, verifique a fileExemplo
    funcaoExemplo()

    # Função que carrega o Token
    token = recuperarToken()

    # Função que configura o Bot
    client = iniciarConfig()

    # ==================================== #
    # Local para settar os comandos do Bot #
    # ==================================== #

    # Por enquanto, vamos carregar cada resposta individualmente, estou trabalhando para resolve isso.
    callFalae(client)
    callSoma(client)

    # Função que termina a configuração dos comandos e Inicia o Bot
    terminarConfig(client, token)
    