# Resumos version 0.3
# Ambas as funções podem ser expandidas para getters caso o Ceffy fique em um abiente controlado (Servidor nosso

from discord import Embed

# Função que retorna um link com os resumos.
def start_get_resumos() -> Embed:
    embed = Embed(colour=0x0049db)
    link = "https://drive.google.com/drive/folders/1G1tu5mtqz0D9vWF43JVp6NiQBrI8Mqnq?usp=sharing"
    msg = f"Clique [aqui]({link}) para acessar o drive de resumos."
    embed.description = msg
    
    # Retornando
    return embed
