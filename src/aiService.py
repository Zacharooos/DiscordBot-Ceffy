import os
import re
import json
import pandas as pd
import google.generativeai as genai
from io import BytesIO
from google.ai.generativelanguage_v1beta.types import Content, Part
from google.generativeai.types.generation_types import StopCandidateException
from google.generativeai.types import HarmCategory, HarmBlockThreshold, BlockedPromptException

from commands.chat.context import *

API_KEY = os.getenv('GOOGLE_API_KEY')

generation_config = {
  "temperature": 1,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}
vision_generation_config = {
  "temperature": 0.6,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

class AiChat():
    '''Classe responsável pela geração de texto por IA, na personalidade de Ceffy.'''
    def __init__(self):
        # Configurando modelo
        genai.configure(api_key=API_KEY)
        self.model = genai.GenerativeModel('gemini-pro', generation_config=generation_config)
        self.vision_model = genai.GenerativeModel('gemini-pro-vision', generation_config=vision_generation_config)
        self.chat = None
        self.filtering_settings = {HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE}
        self.setup_chat()
        print("- IA pronta -")
    
    def setup_chat(self):
        '''Configura um novo chat já com contexto de Ceffy'''
        self.chat = self.model.start_chat(history=chat_history)
        print("- Novo chat de IA configurado! -")

    def export_chat_history(self):
        # Pegando historico
        history_array = list(self.chat.history)
        history_dict = {"input": [], "output": []}

        # Colocando historico no dicionario
        for message in history_array:
            if message.role == "user":
                history_dict["input"].append(message.parts[0].text)
            else:
                history_dict["output"].append(message.parts[0].text)
        
        # Exportando para csv
        history_df = pd.DataFrame.from_dict(history_dict)
        buffer = BytesIO()
        history_df.to_excel(buffer, index=False)
        file = BytesIO(buffer.getvalue())
        buffer.close()

        return file


    def get_response(self, user_input: str, author_id: int, to_id: int, image: list = None) -> str:
        # Pegando autor da mensagem
        try:
            author = AUTHORS[str(author_id)]
        except:
            author = "Unknown"
        try:
            to = AUTHORS[str(to_id)]
        except:
            to = "Unknown"

        # Montando payload
        payload = '{"FROM": <from>, "TO": "<to>", "MESSAGE": "<message>"}'.replace("<message>", user_input).replace("<from>", author).replace("<to>", to)

        # Gerando mensagem com a API
        try:
            if image is not None and len(image) > 0:
                image_description = self.image_input(image=image)
                payload = '{"FROM": <from>, "TO": "<to>", "MESSAGE": "<message>", "IMAGE": <image>}'\
                .replace("<message>", user_input).replace("<from>", author).replace("<to>", to).replace("<image>", image_description)
                response = self.chat.send_message(payload, safety_settings=self.filtering_settings).text
                try:
                    response = json.loads(response.replace("\n", ""), cls=LazyDecoder)
                    response = response['MESSAGE']
                except json.decoder.JSONDecodeError:
                    response = response.split('"MESSAGE": "')
                    response = response[1][:-2]
            else:
                response = self.chat.send_message(payload, safety_settings=self.filtering_settings).text
                # print(response)
                # Tratar o texto de resposta da ia
                try:
                    response = json.loads(response.replace("\n", ""), cls=LazyDecoder)
                    response = response['MESSAGE']
                except json.decoder.JSONDecodeError:
                    response = response.split('"MESSAGE": "')
                    response = response[1][:-2]
        except BlockedPromptException:
            response = "_Filtered_ 🤐"
        except StopCandidateException:
            response = "_EXTREME-FILTERED!_ 🤐"
        except Exception as e:
            print(response)
            response = "Exception: " + str(e) + "\n" + response
        finally:
            return response
        
    def image_input(self, image: list) -> str:
        prompt_parts = [
            VISION_CONTEXT,
            image[0],
        ]
        response = self.vision_model.generate_content(prompt_parts)
        response = response.text
        return response

    def image_input_dev(self, payload: str, image: list) -> str:
        # Função nao utilizada
        self.add_in_history('user', payload)
        history = ''
        history_array = list(self.chat.history)
        history_array.pop(0)
        last_messages = history_array[-5:]
        for message in last_messages:
            history += message.parts[0].text
        chat_context = CONTEXT + history
        prompt_parts = [
            chat_context + payload + "RESPONDA APENAS UMA VEZ",
            image[0],
        ]
        response = self.vision_model.generate_content(prompt_parts)
        print(response.text)
        response = response.text
        self.add_in_history('model', response)
        print("-----HISTORICO ATE AQ-----image")
        print(self.chat.history)
        try:
            response = json.loads(response.replace("\n", ""), cls=LazyDecoder)
            response = response['MESSAGE']
        except json.decoder.JSONDecodeError:
            response = response.split('"MESSAGE": "')
            response = response[1][:-2]
        finally:
            return response
        
    def add_in_history(self, role: str, text: str):
        # Função não utilizada
        new_message = Content()
        new_message.role = role
        part = Part()
        part.text = text
        new_message.parts = [part]
        self.chat.history.append(new_message)

        
class LazyDecoder(json.JSONDecoder):
    def decode(self, s, **kwargs):
        regex_replacements = [
            (re.compile(r'([^\\])\\([^\\])'), r'\1\\\\\2'),
            (re.compile(r',(\s*])'), r'\1'),
        ]
        for regex, replacement in regex_replacements:
            s = regex.sub(replacement, s)
        return super().decode(s, **kwargs)
        

# test = '''{"AUTHOR": "Ceffy","MESSAGE": "O caractere de escape é o caractere de barra invertida (\). Ele é usado para escapar caracteres especiais em uma string, como aspas duplas (\"), aspas simples (\') e barras invertidas (\\). Por exemplo, a string `"Hello, world!"` pode ser representada como `\"Hello, world!\""` usando o caractere de escape."}'''
# '''{"AUTHOR": "Ceffy","MESSAGE": "O caractere de escape é o caractere de barra invertida (\\). Ele é usado para escapar caracteres especiais em uma string, como aspas duplas (\"), aspas simples (') e barras invertidas (\\). Por exemplo, a string `\"Hello, world!\"` pode ser representada como `\"Hello, world!\"` usando o caractere de escape."}'''

# test = AiChat.decode_json(test)
# print(test)
# json.loads(test, cls=LazyDecoder)