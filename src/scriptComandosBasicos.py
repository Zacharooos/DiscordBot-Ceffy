# Arquivo de scripts para Comandos Básicos vs 0.1
# Escreva aqui funções genéricas ou básicas. 
# Pode ser utilizado para fazer testes, simbolize com #TESTE em cima da Func.
 
import discord

#TESTE
def callFalae(client):
    @client.command()
    async def falae(ctx):
        await ctx.reply("Dae mancos")

        
#TESTE SOMA
def callSoma(client):
    @client.command()
    async def soma(ctx, a, b):
        await ctx.reply(f"O resultado é {a+b} pora")