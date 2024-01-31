import discord

VERSION = '1.2'

LINK_GITHUB = 'https://github.com/Zacharooos/DiscordBot-Ceffy'

DESCRICAO = f'''\
Oi. Sou a **Ceffy**, bot feito para facilitar o acesso à informações do curso de Engenharia da Computação (CEFET-RJ). \
Possuo alguns comandos que podem ajudar com assuntos relacionados à faculdade. \
No geral, meu objetivo é ajudar com essas coisas usando a praticidade do discord.
Digite `/` para começar a explorar os comandos.

Minhas funcionalidades ainda estão em desenvolvimento e mais coisas serão adicionadas.

Caso tenha interesse no meu código fonte, pode acessar o [repositório no GitHub]({LINK_GITHUB}).

Se quiser mais informações, tirar dúvidas, reclamar, fazer um pix ou trocar uma ideia, aqui estão os meus devs:
'''

def start():
    embed = discord.Embed(colour=0x0049db)

    embed.title = 'Sobre o bot'
    embed.set_author(
        name='Ceffy Discord Bot',
        url=LINK_GITHUB,
        icon_url='https://media.discordapp.net/attachments/866760339681050655/868248456525930576/unknown.png?width=563&height=662'
    )

    embed.set_thumbnail(url='https://scontent.fsdu13-1.fna.fbcdn.net/v/t39.30808-6/302441973_582779256881936_1409122440030307371_n.jpg?_nc_cat=111&ccb=1-7&_nc_sid=09cbfe&_nc_eui2=AeGmo63T2zpGzywXc-H7IWGNHhFKKGnSM9UeEUooadIz1RCK4ZC-S8ItHQTg5vZuTi7GLI-bgD9C_kzJcdu37SRz&_nc_ohc=d-RGdv73pfoAX8MHibU&_nc_ht=scontent.fsdu13-1.fna&oh=00_AfDFThI6apn1fALhCCnkogh52donbhz4IqR-V6isEWf5VA&oe=64D08142')

    embed.description = DESCRICAO

    # Informações dos Devs
    embed.add_field(
        name='Gabriel Cesar "Zacharos"',
        value=
        '''Discord: @zacharos.oficial\n''' +
        '''GitHub: [Zacharooos](https://github.com/Zacharooos)''',
        inline=True
    )
    embed.add_field(
        name='Carlos Lagreca',
        value=
        '''Discord: @cjplayer\n''' +
        '''GitHub: [CarlosLagreca](https://github.com/CarlosLagreca)''',
        inline=True
    )

    embed.set_footer(text=f'Ceffy Discord Bot v{VERSION}')

    return embed
