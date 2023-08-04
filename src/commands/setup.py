# ARQUIVO DE SETUP DE COMANDOS DO BOT v0.4#
# - Aqui serão importadas as funções de cada comando do bot
# - A função principal setup_commands recebe a tree como parâmetro e popula com os comandos
# - Tentem seguir o padrão de comentário/descrição, declaração, e espaço para proximo comando

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

def setup_commands(tree: discord.app_commands.CommandTree, client: discord.Client) -> bool:
    # Inicializando Services
    logs = Logs(client)

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
                view = ementa.EmentaView(interaction)
                view.log = logs
                await interaction.response.send_message(view=view,
                                                        ephemeral=False)
            except Exception as e:
                msg_error = 'Foi mal, nao consegui pegar os detalhes 😞'
                await interaction.response.send_message(msg_error, ephemeral=True)
                await logs.report_error('detalhes_materia', e)


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
                embed, attachment = calendario.start()
                await interaction.response.send_message(embed=embed, file=attachment, ephemeral=False)
            except Exception as e:
                msg_error = 'Não consegui pegar o calendário 😣'
                await interaction.response.send_message(msg_error, ephemeral=True)
                await logs.report_error('calendario', e)


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
                connection.play(source=discord.FFmpegPCMAudio('data/audios/welcome-to-the-mato.mp3'))
                while(connection.is_playing()):
                    await sleep(2)
                await connection.disconnect()
            except Exception as e:
                await interaction.response.send_message(content='Oii 😊')


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
        print('Erro ao incluir comandos!\n', e)
        return False
