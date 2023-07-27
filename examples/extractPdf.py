from pdfminer.high_level import extract_text
from os import listdir

# Função que recebe uma string e formata ela manualmente
def format_text(text) -> str:
    
    # Cedilha
    text = text.replace("¸c", "ç")

    # Acentos agudos
    text = text.replace("´a", "á")
    text = text.replace("´e", "é")
    text = text.replace("´ı", "í")
    text = text.replace("´o", "ó")
    text = text.replace("´u", "ú")

    text = text.replace("´A", "Á")
    text = text.replace("´E", "É")
    text = text.replace("´ı", "Í")
    text = text.replace("´O", "Ó")
    text = text.replace("´U", "Ú")

    
    # Til
    text = text.replace("˜a", "ã")
    text = text.replace("˜o", "õ")

    text = text.replace("˜A", "Ã")
    text = text.replace("˜O", "Õ")

    # Circunflexo
    text = text.replace("ˆe", "ê")
    text = text.replace("ˆo", "ô")

    text = text.replace("ˆE", "Ê")
    text = text.replace("ˆO", "Ô")

    return text

def read_pdf_pdfminer(fileObj) -> None:

    # Extract the text from the PDF file using UTF-8 encoding
    text = extract_text(fileObj)

    formatted_text = format_text(text)

    print(formatted_text)

    f = open("teste.txt", "w", encoding='utf-8')
    f.write(formatted_text)
    f.close()


pdfFileObj = open('ementaExemplo.pdf', 'rb')

read_pdf_pdfminer(pdfFileObj)

pdfFileObj.close()

