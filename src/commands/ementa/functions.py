import requests
import discord
import re
from discord.app_commands import Choice
from json import load
from typing import List, Tuple
from io import BytesIO
from extractPdf import read_pdf_pdfminer


def download_ementa(periodo: int) -> BytesIO:
    '''Faz o download de um pdf de ementa do período especificado'''
    # Pegando URL com base no período
    if(periodo > 10):
        url = "http://e-computacao.com.br/files/ementas/optativas.pdf"
    else:
        url = f"http://e-computacao.com.br/files/ementas/{str(periodo).zfill(2)}.pdf"

    # Fazendo download e inserindo no buffer
    file = requests.get(url, allow_redirects=True)
    if(file.status_code != 200):
        raise ConnectionError(f"Não foi possível fazer o download. status_code: {file.status_code}")
    return BytesIO(file.content)


# ...
def choices_periodos() -> List[Choice]:
    periodos = []
    for i in range(1,10):
        periodos.append(
            Choice(name=f'{i}º Período', value=str(i))
        )
    periodos.append(Choice(name='Optativas', value='11'))
    return periodos

def start_materia(materia: str) -> discord.Embed:
    '''Recebe uma materia e retorna Embed com os dados dela'''
    
    # Verificando o período da matéria e fazendo download
    with open("data/materias.json") as json:
        grade = load(json)
        periodo = grade['materias'][materia]['periodo']

    content = download_ementa(periodo)

    # Pegando texto do pdf da materia
    text = read_pdf_pdfminer(content)

    # Tratando o texto para leitura (do python)
    text = text.replace('\n', ' ').split('DISCIPLINA')
    infos = None
    for i in range(len(text)):
        text[i] = text[i][1:].strip()
        if text[i].startswith(materia.upper()):
            infos = text[i]
            break
    assert infos is not None, f'Erro ao encontrar disciplina "{materia}" na string do pdf'

    # Recuperando informações do texto
    # Bibliografia complementar
    infos, bibliografia_c = infos.split('BIBLIOGRAFIA COMPLEMENTAR')
    bibliografia_c = bibliografia_c.split('•')
    aux = ''
    for item in bibliografia_c:
        item = item.replace('  ', '')
        aux = aux + f'• {item}\n'
    bibliografia_c = aux

    # Bibliografia basica
    infos, bibliografia_b = infos.split('BIBLIOGRAFIA BÁSICA')
    bibliografia_b = bibliografia_b.split('•')
    bibliografia_b.pop(0)
    aux = ''
    for item in bibliografia_b:
        item = item.replace('  ', '')
        aux = aux + f'• {item}\n'
    bibliografia_b = aux

    # Ementa
    infos, ementa = infos.split('EMENTA')
    ementa = re.findall(r'\d+\.\s*(.*?)(?=\s*\d+\.|$)', ementa)
    aux = ''
    for i in range(1, len(ementa)):
        ementa[i-1] = ementa[i].replace('  ', ' ')
        aux = aux + f'{i}. {ementa[i]}\n'
    ementa = aux

    # Pré-requisitos
    infos, pre_requisitos = infos.split('PRÉ-REQUISITOS')
    pre_requisitos = re.findall(r'\d+\.\s*(.*?)(?=\s*\d+\.|$)', pre_requisitos)
    aux = ''
    for item in pre_requisitos:
        aux = aux + f'• {item}\n'
    pre_requisitos = aux

    # Demais informações
    infos, ciclo = infos.split('CRÉDITOS')[0].split('CICLO:')
    infos, tipo = infos.split('TIPO:')
    aux = infos
    try:
        infos, vigencia = infos.split('VIGÊNCIA:')
        infos, codigo = infos.split('CÓDIGO:')
    except:
        infos = aux
        infos, codigo = infos.split('CÓDIGO:')
        infos, vigencia = infos.split('VIGÊNCIA:')

    # Montando Embed
    embed = discord.Embed(colour=0x0049db)
    embed.title = materia
    embed.url = f"http://e-computacao.com.br/files/ementas/{str(periodo).zfill(2)}.pdf"

    descricao = '_ATENÇÃO: Funcionalidade ainda em desenvolvimento. Acesse o PDF para informações mais precisas._\n\n'
    descricao = descricao + '**Confira os detalhes dessa disciplina:**\n\n'
    descricao = descricao + f'**Período:** {periodo}\n'
    descricao = descricao + f'**Código:** {codigo}\n'
    descricao = descricao + f'**Tipo:** {tipo}\n'
    descricao = descricao + f'**Ciclo:** {ciclo}\n'

    # Verificar se a embed ultrapassou o limite de caracteres e adicionar os fields
    if len(descricao) > 1000:
        embed.description = "Descrição muito longa, acesse o pdf."
    else:
        embed.description = descricao    

    if len(pre_requisitos) > 1000:
        embed.add_field(name='Pré-Requisitos:', value="_Texto muito grande, acesse o pdf_", inline=False)
    else:
        embed.add_field(name='Pré-Requisitos:', value=pre_requisitos, inline=False)

    if len(ementa) > 1000:
        embed.add_field(name='Ementa:', value="_Texto muito grande, acesse o pdf_", inline=False)
    else:
        embed.add_field(name='Ementa:', value=ementa, inline=False)

    if len(bibliografia_b) > 1000:
        embed.add_field(name='Bibliografia Básica:', value="_Texto muito grande, acesse o pdf_", inline=False)
    else:
        embed.add_field(name='Bibliografia Básica:', value=bibliografia_b, inline=False)

    embed.set_footer(text='Quer o PDF? Clique no nome da matéria.')

    return embed

def start_periodo(periodo: int) -> Tuple[str, BytesIO]:
    '''Função que recebe um período e retorna o um pdf com o conteúdo.'''

    # Pegando URL com base no período
    if(periodo > 10):
        msg = f"Aqui está o PDF da ementa das matérias optativas 🤓"
    else:
        msg = f"Aqui está o PDF da ementa das matérias do {periodo}º Período!"

    # Fazendo download e inserindo no buffer
    content = download_ementa(periodo)

    # Retornando
    return msg, content
