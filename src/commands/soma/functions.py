'''
## DECLARAÇÃO DE FUNÇÕES DO COMANDO ##
Dentro da pasta "soma", serão colocados todos os arquivos .py do comando "soma".
O jeito que um arquivo conversa com outro depende de comando pra comando.
Mas o functions.py deverá existir com a função start, que retornará a resposta da Ceffy.
A função start será importada em commands/setup.py para configurar o respectivo comando, nesse caso, "soma"
'''

def start(a:int, b:int) -> str:
    # CORPO DA FUNCAO #
    response = f"Não sabe fazer conta?\nO resultado é: {a+b}"
    return response