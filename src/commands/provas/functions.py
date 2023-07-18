# Provas version 0.1

# Função que retorna um link com as provas.
def start_get_provas():
    msg = f"Aqui está o link com acesso ao Drive de Provas: \n-> https://drive.google.com/drive/folders/1ZdiguzhfjE5gcUWJ40XF9qwBbRBIbTru"
    
    # Retornando
    return msg

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

