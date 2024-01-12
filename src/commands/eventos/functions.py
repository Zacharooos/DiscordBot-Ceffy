import datetime
import discord
import asyncio
from json import load, dump
import discord.ext.tasks

CHANNEL_ID = 1127215221807775795


def start_cadastro(data:str, nome: str, descricao: str):
    # Criando dicionario do novo evento
    novo_evento = {'nome': nome, 'descricao':descricao}
    eventos = ...
    with open("data/eventos.json", 'r') as read:
        eventos = load(read)
    
        try:
            eventos[data].append(novo_evento)
        except KeyError:
            eventos[data] = [novo_evento]

    # Adicionando novo evento no json
    with open("data/eventos.json", 'w') as write:
        dump(eventos, write)


async def verificar_eventos(client: discord.Client):
    while True:
        print(f"Verificando eventos... {datetime.datetime.now()}", flush=True)
        update = None
        with open('data/eventos.json', 'r') as file:
            # Pegando o dict com os eventos
            eventos = dict(load(file))

            # Apagandos os eventos de 30 dias atras
            try:
                deleted = eventos.pop(datetime.datetime.strftime((datetime.datetime.now() - datetime.timedelta(days=30)), "%d-%m-%Y"))
                print(f'Apagando {len(deleted)} eventos...', flush=True)
            except:
                None

            # Verificando eventos para o dia seguinte
            notify = None
            for data in eventos:
                if data == datetime.datetime.strftime((datetime.datetime.now() + datetime.timedelta(days=1)), "%d-%m-%Y"):
                    notify = eventos[data]
                    break
            
            if notify:
                msg = 'Temos 1 evento amanhã:' if len(notify) == 1 else f'Temos {len(notify)} eventos amanhã:'
                embed = discord.Embed(colour=0x0049db)
                embed.title = 'Eventos de amanhã:'
                for evento in notify:
                    embed.add_field(
                    name=evento['nome'],
                    value=(f'*Data: _{data}_*\n' + evento['descricao']),
                    inline=False
                )

                channel = client.get_channel(CHANNEL_ID)
                await channel.send(msg, embed=embed)
            
            # Verificando eventos para a semana (se for domingo)
            notify = None
            if datetime.datetime.now().weekday() == 6:
                notify = {}
                fim_da_semana = datetime.datetime.now().date() + datetime.timedelta(days=7)
                for data in eventos:
                    data_obj = datetime.datetime.strptime(data, "%d-%m-%Y")
                    if data_obj > datetime.datetime.now() and data_obj.date() <= fim_da_semana:
                        notify[data] = eventos[data]

            if notify and len(notify) > 0:
                msg = 'Temos eventos em 1 dia nessa semana:' if len(notify) == 1 else f'Temos eventos em {len(notify)} dias essa semana:'
                embed = discord.Embed(colour=0x0049db)
                embed.title = 'Eventos dessa semana:'
                for data in notify:
                    # TODO: Mostrar dia da semana na notificação
                    for evento in notify[data]:
                        embed.add_field(
                        name=evento['nome'],
                        value=(f'*Data: _{data}_*\n' + evento['descricao']),
                        inline=False
                    )

                channel = client.get_channel(CHANNEL_ID)
                await channel.send(msg, embed=embed)

            # Verificando eventos para o mes (se for dia 1)
            notify = None
            if datetime.datetime.now().day == 1:
                notify = {}
                for data in eventos:
                    data_obj = datetime.datetime.strptime(data, "%d-%m-%Y")
                    if data_obj.month == datetime.datetime.now().month:
                        notify[data] = eventos[data]

            if notify and len(notify) > 0:
                msg = 'Temos eventos em 1 dia nesse mês:' if len(notify) == 1 else f'Temos eventos em {len(notify)} dias esse mês:'
                embed = discord.Embed(colour=0x0049db)
                embed.title = 'Eventos desse mês:'
                for data in notify:
                    # TODO: Mostrar dia da semana na notificação
                    for evento in notify[data]:
                        embed.add_field(
                        name=evento['nome'],
                        value=(f'*Data: _{data}_*\n' + evento['descricao']),
                        inline=False
                    )

                channel = client.get_channel(CHANNEL_ID)
                await channel.send(msg, embed=embed)

            
            update = eventos
        
        # Escrevendo o dict atualizados no json
        with open('data/eventos.json', 'w') as write:
            dump(update, write)
        
        print('-Fim da verificação-', flush=True)

        # Pegando o delta para proxima verificação
        proxima_verificacao = datetime.datetime.now().replace(hour=13, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1)
        delta = proxima_verificacao - datetime.datetime.now()
        segundos = delta.total_seconds()

        await asyncio.sleep(segundos)


def mostrar_eventos(mes):
    # Pegando eventos no json
    eventos = None
    with open("data/eventos.json", 'r') as file:
        eventos = load(file)
        if mes != None:
            aux = {}
            for data in eventos:
                if datetime.datetime.strptime(data, "%d-%m-%Y").month == int(mes.value):
                   aux[f'{data}'] = eventos[data]
            eventos = aux
        else:
            aux = {}
            for data in eventos:
                aux[f'{data}'] = eventos[data]
            eventos = aux
    
    # Monatando a embed
    embed = discord.Embed(colour=0x0049db)
    embed.title = 'Eventos' if mes == None else f'Eventos no mês {mes.value}'
    for data in eventos:
        for evento in eventos[data]:
            embed.add_field(
                name=evento['nome'],
                value=(f'*Data: _{data}_*\n' + evento['descricao']),
                inline=False
            )
    return embed
