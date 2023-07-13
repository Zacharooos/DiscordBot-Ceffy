import requests
from discord.app_commands import Choice
from typing import List, Tuple
from io import BytesIO


def choices_materia() -> List[Choice]:
    materias = [
        Choice(name='abc', value='abc'),
        Choice(name='def', value='def')
    ]
    return materias


def choices_periodos() -> List[Choice]:
    periodos = []
    for i in range(1,10):
        periodos.append(
            Choice(name=f'{i}º Período', value=str(i))
        )
    periodos.append(Choice(name='Optativas', value='11'))
    return periodos


def start_materia(periodo: str, materia: str) -> Tuple[str, bytes]:
    msg = "Aqui está o seu arquivo!\nEspero ter ajudado 🫡"
    file = open('README.txt', 'rb')
    return msg, file

def start_periodo(periodo: int) -> Tuple[str, BytesIO]:
    # Pegando URL com base no período
    if(periodo > 10):
        msg = f"Aqui está o PDF da ementa das matérias optativas 🤓"
        url = "http://e-computacao.com.br/files/ementas/optativas.pdf"
    else:
        msg = f"Aqui está o PDF da ementa das matérias do {periodo}º Período!"
        url = f"http://e-computacao.com.br/files/ementas/{str(periodo).zfill(2)}.pdf"

    # Fazendo download e inserindo no buffer
    file = requests.get(url, allow_redirects=True)
    if(file.status_code != 200):
        raise ConnectionError(f"Não foi possível fazer o download. status_code:{file.status_code}")
    content = BytesIO(file.content)

    # Retornando
    return msg, content
