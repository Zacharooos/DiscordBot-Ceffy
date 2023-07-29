# Funções responsáveis por extrair texto de um pdf.
# -> Esse código aq ta gambiarra atrás de gambiarra, mas funciona.
# -> Não temos nenhuma outra ideia de como fazer isso aq... Já foi uma merda fazer esse funcionar da forma q ta
# -> Otimização importante para o futuro.

from pdfminer.high_level import extract_text


# "processa" a string para aplicar o backspace
def apply_backspace_effect(input_str):
    result = []
    for char in input_str:
        if char == '\b':
            if result:
                result.pop()
        else:
            result.append(char)
    return ''.join(result)


# "processa" a string para aplica delete (x7f)
def apply_delete_effect(input_str):
    result = []
    i = 0
    while i < len(input_str):
        char = input_str[i]
        if char == '\x7f':
            if i + 1 < len(input_str):
                i += 1
        else:
            result.append(char)
        i += 1
    return ''.join(result)


# Função que recebe uma string e formata ela manualmente
def format_text(text) -> str:
    
    # Cedilha
    text = text.replace("¸c", "ç")
    text = text.replace("C¸", "Ç\x7f")

    # Acentos agudos
    text = text.replace("´a", "á")
    text = text.replace("´e", "é")
    text = text.replace("´ı", "í")
    text = text.replace("´o", "ó")
    text = text.replace("´u", "ú")

    text = text.replace("´A", "\bÁ")
    text = text.replace("´E", "É")
    text = text.replace("´ı", "Í")
    text = text.replace("´O", "\bÓ")
    text = text.replace("´U", "Ú")

    
    # Til
    text = text.replace("˜a", "ã")
    text = text.replace("˜o", "õ")

    text = text.replace("˜A", "Ã")
    text = text.replace("˜O", "Õ")

    # Circunflexo
    text = text.replace("ˆa", "â")
    text = text.replace("ˆe", "ê")
    text = text.replace("ˆo", "ô")

    text = text.replace("ˆA", "Â")
    text = text.replace("ˆE", "Ê")
    text = text.replace("ˆO", "Ô")

    # Aplicando caracteres backslash
    text = apply_backspace_effect(text)
    text = apply_delete_effect(text)

    return text


def read_pdf_pdfminer(fileObj) -> None:

    # Extract the text from the PDF file using UTF-8 encoding
    text = extract_text(fileObj)

    formatted_text = format_text(text)

    return formatted_text


if __name__ == "__main__":

    pdfFileObj = open('examples/ementaExemplo.pdf', 'rb')

    pdf_string = read_pdf_pdfminer(pdfFileObj)

    print(pdf_string)

    f = open("teste.txt", "w", encoding='utf-8')
    f.write(pdf_string)
    f.close()

    pdfFileObj.close()

