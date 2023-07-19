# Provas version 0.1

from discord import Embed

# Função que retorna um link com as provas.
def start_get_provas() -> Embed:
    embed = Embed(colour=0x0049db)
    link = "https://drive.google.com/drive/folders/1ZdiguzhfjE5gcUWJ40XF9qwBbRBIbTru"
    msg = f"Clique [aqui]({link}) para acessar o Drive de Provas"
    embed.description = msg
    
    # Retornando
    return embed

def check_tag(string):
    data = open("data/dataProvasCalendar.txt", "r")

    if len(string) > 5 or len(string) < 3:
        return False
    
    tag = string.upper()

    data_text = data.read()
    data_text = data_text.split()

    if tag in data_text:
        return False
    
check_tag("cras")

