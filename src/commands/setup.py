# ARQUIVO DE SETUP DE COMANDOS DO BOT v1.2#
# - Aqui serão importadas as funções de cada comando do bot
# - A função principal setup_commands recebe a tree como parâmetro e popula com os comandos
# - Tentem seguir o padrão de comentário/descrição, declaração, e espaço para proximo comando
# - Deixem o comando infos como último por favor

# Constantes

ID = 994616556401197179

# Imports gerais
import discord
from logsService import Logs
from asyncio import sleep

# Imports dos comandos
import commands.soma.functions as soma
import commands.provas.functions as provas
import commands.ementa.view as ementa
import commands.resumos.functions as resumos
import commands.calendario.functions as calendario
import commands.info.functions as info
import commands.eventos.view as eventos
import commands.enquetes.functions as enquetes
import commands.chat.functions as aichat

def setup_commands(tree: discord.app_commands.CommandTree, client: discord.Client) -> bool:
    # Inicializando Services
    logs = Logs(client)

    aichat.setup_ai_chat(client)

    try:

        '''
        ##COMANDO SOMA##
        Comando que pega dois números e responde uma mensagem com a soma deles
        '''
        @tree.command(
                    name='soma',
                    description='Soma de dois inteiros',
                    guild=discord.Object(id=ID)
                    )
        async def self(interaction: discord.Interaction, a: int, b: int):
            await interaction.response.send_message(soma.start(a,b))


        '''
        ##COMANDO EMENTA##
        Ceffy baixa o pdf das ementas de um periodo do ste da e-computacao.com.br e envia 
        uma mensagem com o arquivo.
        '''
        @tree.command(
                    name='ementa_por_periodo', 
                    description='PDF da ementa das matérias de um período.', 
                    guild=discord.Object(id=ID)
                    )
        @discord.app_commands.choices(periodo=ementa.choices_periodos())
        async def self(interaction: discord.Interaction, periodo: discord.app_commands.Choice[str]):
            try:
                msg, file = ementa.start_periodo(int(periodo.value))
                filename = f'{periodo.value}periodo.pdf' if int(periodo.value) <= 10 else 'optativas.pdf'
                await interaction.response.send_message(msg, 
                                                        file=discord.File(fp=file, filename=filename),
                                                        ephemeral=False)
            except Exception as e:
                msg_error = 'Foi mal, nao consegui pegar seu PDF 😥'
                await interaction.response.send_message(msg_error, ephemeral=True)
                await logs.report_error('ementa_por_periodo', e)

        
        @tree.command(
                    name='detalhes_materia', 
                    description='Ementa de uma matéria.', 
                    guild=discord.Object(id=ID)
                    )
        async def self(interaction: discord.Interaction):
            try:
                await interaction.response.defer()
                view = ementa.EmentaView(interaction)
                view.log = logs
                await interaction.followup.send(view=view, ephemeral=False)
            except Exception as e:
                await logs.report_error('detalhes_materia', e)
                msg_error = 'Foi mal, nao consegui pegar os detalhes 😞'
                await interaction.response.send_message(msg_error, ephemeral=True)


        '''
        ##COMANDO RESUMOS##
        Ceffy envia um link com acesso ao Drive com os resumos.
        '''
        @tree.command(
                    name='resumos',
                    description='Link do drive com os resumos',
                    guild=discord.Object(id=ID)
                    )
        async def self(interaction: discord.Interaction):
            await interaction.response.send_message(embed=resumos.start_get_resumos())


        '''
        ##COMANDO PROVAS##
        Ceffy envia um link com acesso ao Drive com os resumos.
        '''
        @tree.command(
                    name='provas',
                    description='Link do drive com os provas',
                    guild=discord.Object(id=ID)
                    )
        async def self(interaction: discord.Interaction):
            await interaction.response.send_message(embed=provas.start_get_provas())


        '''
        ##COMANDO CALENDARIO##
        Ceffy envia uma imagem do calendario academico mais atualizado disponível em e-computacao.com.br
        '''
        @tree.command(
                    name='calendario',
                    description='Calendário acadêmico atual',
                    guild=discord.Object(id=ID)
                    )
        async def self(interaction: discord.Interaction):
            try:
                await interaction.response.defer(thinking=True)
                embed, attachment = calendario.start()
                await interaction.followup.send(embed=embed, file=attachment, ephemeral=False)
            except Exception as e:
                await logs.report_error('calendario', e)
                msg_error = 'Não consegui pegar o calendário 😣'
                await interaction.followup.send(msg_error, ephemeral=True)


        '''
        ##COMANDO HELLO_CEFFY\##
        Talvez a ceffy entre no seu canal de voz e diga oi?
        '''
        @tree.command(
                    name='hello_ceffy',
                    description='😊',
                    guild=discord.Object(id=ID)
                    )
        async def self(interaction: discord.Interaction):
            try:
                voice_channel = interaction.user.voice
                if voice_channel is None:
                    await interaction.response.send_message(content='Você não consegue me ouvir 😓')
                    return
                connection = await voice_channel.channel.connect(self_deaf=True)
                await interaction.response.send_message(content='🥳', ephemeral=True)
                discord.opus.load_opus('libopus.so.0')
                if not discord.opus.is_loaded():
                    raise Exception("Opus not loaded")
                connection.play(source=discord.FFmpegPCMAudio('data/audios/welcome-to-the-mato.mp3'))
                while(connection.is_playing()):
                    await sleep(2)
                await connection.disconnect()
            except Exception as e:
                await interaction.response.send_message(content='Oii 😊')
                await logs.report_error('hello_ceffy', e)
                print(e)


        '''
        ##COMANDO CRIAR_EVENTO##
        Ceffy cadastra um evento no sistema
        '''
        @tree.command(
                    name='criar_evento',
                    description='Adiciona um evento que será notificado em sua data',
                    guild=discord.Object(id=ID)
                    )
        async def self(interaction: discord.Interaction):
            try:
                modal = eventos.modal_evento()
                await interaction.response.send_modal(modal)
            except Exception as e:
                await logs.report_error('criar_evento', e)
                await interaction.followup.send('Desculpe, não consegui cadastrar esse evento 😓😓', ephemeral=True)
            

        '''
        ## COMANDO MOSTRAR_EVENTOS##
        Ceffy mostra os eventos que estão no sistema
        '''
        @tree.command(
                    name='mostrar_eventos',
                    description='Mostra os eventos que estão por vir',
                    guild=discord.Object(id=ID)
                    )
        @discord.app_commands.choices(mes=[discord.app_commands.Choice(name=f'{i}', value=f'{i}') for i in range(1,13)])
        async def self(interaction: discord.Interaction, mes: discord.app_commands.Choice[str] = None):
            try:
                await interaction.response.defer(thinking=True)
                await interaction.followup.send(content='Aqui os eventos:', embed=eventos.mostrar_eventos(mes))
            except Exception as e:
                await logs.report_error('mostrar_eventos', e)
                await interaction.followup.send(content='Desculpe, não consegui acessar os eventos.', ephemeral=True)


        '''
        ## COMANDO JSON_EVENTOS##
        Ceffy mostra os eventos que estão no sistema
        '''
        @tree.command(
                    name='json_eventos',
                    description='Retorna o json dos eventos cadastrados',
                    guild=discord.Object(id=ID)
                    )
        async def self(interaction: discord.Interaction):
            try:
                await interaction.response.defer(thinking=True)
                file = eventos.json_eventos()
                filename = 'eventos.json'
                await interaction.followup.send('Aqui os eventos que tenho cadastrados:', 
                                                        file=discord.File(fp=file, filename=filename),
                                                        ephemeral=False)
            except Exception as e:
                msg_error = 'Foi mal, nao consegui mandar o arquivo 😥'
                await interaction.followup.send(msg_error, ephemeral=True)
                await logs.report_error('json_eventos', e)


        '''
        ##COMANDO ENQUETE##
        Ceffy abre uma enquete para votação
        '''
        @tree.command(
                    name='enquete',
                    description='Abrir uma enquete personalizada',
                    guild=discord.Object(id=ID)
                    )
        async def self(interaction: discord.Interaction, titulo: str, opcoes: str, timeout: str = None):
            """
            Parameters
            -----------
            opcoes: str
                Separe as opções com "|". Ex: "Sim|Não|Talvez"
            timeout: str
                Tempo para o fim da enquete. Use 'm', 'h', 'd' para minutos, horas e dias. Ex: "30m", "3h", "2d".
            """
            if 2 <= len(opcoes.split('|')) <= 10:
                await interaction.response.send_message(content='Ok. 😊', delete_after=30, ephemeral=True)
                if timeout:
                    tempo = timeout[:-1]
                    unidade = timeout[-1].lower()
                    if not tempo.isnumeric() or unidade.isnumeric() or unidade not in ['m','h','d']:
                        await interaction.followup.send(content='''O formato do timeout está errado. Use 'm', 'h', 'd' para minutos, horas e dias. Ex: "30m", "3h", "2d".''', 
                                                        ephemeral=True)
                        return
                    await enquetes.start(user=interaction.user, channel=interaction.channel, titulo=titulo, opcoes_str=opcoes, timeout=[int(tempo), unidade])
                else:
                    await enquetes.start(user=interaction.user, channel=interaction.channel, titulo=titulo, opcoes_str=opcoes, timeout=None)
            else:
                await interaction.response.send_message(content='Você precisa me dar no mínimo 2 opções e no máximo 10. Lembre-se de colocar no formato correto.', 
                                                        delete_after=30, ephemeral=True)


        '''
        ##COMANDO INFO##
        Ceffy envia uma mensagem com informações dela
        '''
        @tree.command(
                    name='info',
                    description='Sobre o bot',
                    guild=discord.Object(id=ID)
                    )
        async def self(interaction: discord.Interaction):
            await interaction.response.send_message(embed=info.start(), ephemeral=False)


        '''
        #COMANDO TAL#
        ...
        '''
        #@tree.command(...)

        return True

    except Exception as e:
        print('Erro ao incluir comandos!\n',)
        raise e
