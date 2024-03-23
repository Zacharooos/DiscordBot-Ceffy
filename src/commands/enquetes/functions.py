import discord
from asyncio import sleep

EMOJIS = ['0️⃣','1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣','🔟']
UNIDADES = {"m": "minutos", "h":"horas", "d":"dias"}
TO_SECONDS = {"m": 60, "h":3600, "d":86400}

async def start(user: discord.User, channel, opcoes_str: str, titulo: str, timeout: list):
    # Separando as opções
    opcoes = opcoes_str.split('|')
    
    # Criando embed
    embed = discord.Embed(colour=0x0049db)
    embed.set_author(name=user.display_name, icon_url=user.avatar.url)
    embed.title = f"Enquete!"
    embed.description = "Por favor, vote em uma das opções!"
    if timeout and timeout[0] > 0:
        embed.description += f' Esta enquete se encerrará em {timeout[0]} {UNIDADES[timeout[1]]} ⏳.'
    
    opcoes_str = ''
    for index, opcao in enumerate(opcoes):
        opcoes_str += f'{EMOJIS[index+1]}: _{opcao}_\n'

    embed.add_field(name=f'{titulo}',
                    value=opcoes_str)
    
    # Enviando msg e adicionando reações
    msg = await channel.send(embed=embed)
    for i in range(len(opcoes)):
        await msg.add_reaction(EMOJIS[i+1])

    # Tratando o timeout
    if timeout and timeout[0] > 0:
        # Pegando total de segundos e chamando sleep
        segundos = int(timeout[0]) * TO_SECONDS[timeout[1]]
        await sleep(segundos)

        # Verificando resultados
        msg = await channel.fetch_message(msg.id)
        reactions = msg.reactions
        resultados = {}
        for reaction in reactions:
            resultados[str(reaction.emoji)] = [user async for user in reaction.users()]
        
        await msg.clear_reactions()

        # Montando embed com resultados
        embed = discord.Embed(colour=0x0049db)
        embed.set_author(name=user.display_name, icon_url=user.avatar.url)
        embed.title = f"Resultados da enquete!"
        embed.description = f'O tempo acabou! Veja o resultado dos votos:\n"**{titulo}**"'

        for emoji in resultados:
            print(emoji)
            opcao = opcoes[EMOJIS.index(emoji)-1]
            votos = len(resultados[emoji]) - 1
            users_str = ''
            for user in resultados[emoji]:
                if user.id != 1137377861653778542 and user.id != 1072165474521071716:
                    users_str += f"<@{user.id}> \n"
            
            embed.add_field(name=f"{emoji}: {opcao} ({votos} votos)", value=users_str, inline=False)
        
        # Editando mensagem original
        await msg.edit(embed=embed)
