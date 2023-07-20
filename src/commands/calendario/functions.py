import pdf2image
import requests
from datetime import datetime
from io import BytesIO
from discord import Embed, File
from typing import Tuple

URL_CALENDARIO = "http://e-computacao.com.br/files/calendario.pdf"

def start() -> Tuple[Embed, File]:
    # pegando pdf do calendario
    file = requests.get(URL_CALENDARIO, allow_redirects=True)
    if(file.status_code != 200):
        raise ConnectionError(f"Não foi possível fazer o download. status_code: {file.status_code}")

    # Transformando em png no buffer e formando discord file attachment
    image_bytes = BytesIO()
    image = pdf2image.convert_from_bytes(pdf_file=file.content, dpi=300)
    image[0].save(image_bytes, 'PNG')
    buffer = BytesIO(image_bytes.getvalue())
    attachment = File(fp=buffer, filename='calendario.png')

    # Montando embed
    embed = Embed(colour=0x0049db, timestamp=datetime.now())
    embed.title = 'Calendário Atual'
    embed.url = URL_CALENDARIO
    embed.set_image(url='attachment://calendario.png')
    embed.description = f'Quer o pdf? Clique [aqui]({URL_CALENDARIO})'

    # Retornando
    return embed, attachment
