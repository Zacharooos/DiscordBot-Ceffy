import discord
from aiService import AiChat

#TODO: Enriquecer o contexto da ceffy
#TODO: Fazer um historico de chat mais otimizado
#TODO: Fazer exportação e importação de historico JA FIZ EXPORTACAO

ceffy_ai = AiChat()

def setup_ai_chat(client: discord.Client):
    # Criando evento de leitura de mensagens
    @client.event
    async def on_message(message: discord.Message):
        # Verificando canal da mensagem
        if(message.author == client.user or message.channel.id != 1206020968741470228):
            return
        await message.channel.typing()
        
        # Comandos
        if(message.content.startswith("!")):
            # Comando de restart
            if(message.content == "!ceffy restart"):
                try:
                    response = ceffy_ai.get_response(user_input="Ceffy, reinicie o sistema agora!", author_id=-1, to_id=client.user.id)
                except:
                    response = "..."
                await message.channel.send(response + "**(Chat reiniciado)**")
                ceffy_ai.setup_chat()
                return
            
            # Comando de export
            elif(message.content == "!ceffy export"):
                file_bytes = ceffy_ai.export_chat_history()
                await message.channel.send("Aqui está o historico de mensagens", file=discord.File(fp=file_bytes, filename="historico.xlsx"))
                return

            # Comando desconhecido
            else:
                try:
                    prompt = "Ceffy, alguém mandou um comando desconhecido. Fale que você não conhece esse comando!"
                    response = ceffy_ai.get_response(user_input=prompt, author_id=-1, to_id=client.user.id)
                except:
                    response = "Comando não reconhecido"
                await message.channel.send(response)
                return

        
        # Verificando imagem anexada
        image_parts = []
        if(len(message.attachments) > 0):
            image_bytes = await message.attachments[0].read()
            image_type = message.attachments[0].content_type
            image_parts = [
                {
                    "mime_type": image_type,
                    "data": image_bytes
                },
            ]
        
        # Mandando para geração de texto
        response = 'Deu ruim na IA aq cj fez merda nessa porra'
        if(message.reference):
            # Verificando se a mensagem é uma resposta
            previuos = await message.channel.fetch_message(message.reference.message_id)
            to_id = previuos.author.id
            response = ceffy_ai.get_response(user_input=message.content, author_id=message.author.id, to_id=to_id, image=image_parts)
        else:
            # Se não for, ceffy é o destinatario
            response = ceffy_ai.get_response(user_input=message.content, author_id=message.author.id, to_id=client.user.id, image=image_parts)
        
        # Enviando mensagem
        await message.reply(content=response)